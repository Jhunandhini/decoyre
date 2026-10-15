import hashlib
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

from .textutil import chunk_text, parse_frontmatter, tokenize


def load_docs(raw_dir):
    docs = []
    root = Path(raw_dir)
    for p in sorted(root.rglob("*.md")):
        text = p.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        rel = p.relative_to(root).as_posix()
        meta["kind"] = rel.split("/")[0]
        docs.append({"path": rel, "meta": meta, "body": body, "text": text})
    return docs


class BM25:
    def __init__(self, texts, k1=1.5, b=0.75):
        self.toks = [tokenize(t) for t in texts]
        self.k1, self.b = k1, b
        self.avg = sum(map(len, self.toks)) / max(1, len(self.toks))
        df = Counter(t for d in self.toks for t in set(d))
        n = len(self.toks)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}
        self.tf = [Counter(d) for d in self.toks]

    def scores(self, query):
        q = tokenize(query)
        out = []
        for tf, d in zip(self.tf, self.toks):
            s = 0.0
            for t in q:
                if t in tf:
                    f = tf[t]
                    s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * len(d) / self.avg))
            out.append(s)
        return np.array(out)


class EmbedCache:
    def __init__(self, llm, cache_file):
        self.llm, self.file = llm, Path(cache_file)
        self.store = json.loads(self.file.read_text()) if self.file.exists() else {}

    def embed(self, texts):
        keys = [hashlib.md5(t.encode()).hexdigest() for t in texts]
        missing = [(k, t) for k, t in zip(keys, texts) if k not in self.store]
        if missing:
            vecs = self.llm.embed([t for _, t in missing])
            for (k, _), v in zip(missing, vecs):
                self.store[k] = v
            self.file.parent.mkdir(parents=True, exist_ok=True)
            self.file.write_text(json.dumps(self.store))
        m = np.array([self.store[k] for k in keys], dtype=np.float32)
        return m / (np.linalg.norm(m, axis=1, keepdims=True) + 1e-9)


class CorpusIndex:
    """Fixed-size chunks over the raw corpus. Used by RAG baselines and by search_docs."""

    def __init__(self, docs, llm, cache_dir, size=600, overlap=60):
        self.chunks = []
        for d in docs:
            for i, c in enumerate(chunk_text(d["body"], size, overlap)):
                self.chunks.append({"id": f"{d['path']}#{i}", "source": d["path"], "text": c.strip()})
        texts = [c["text"] for c in self.chunks]
        self.bm25 = BM25(texts)
        tag = getattr(llm, "embed_model", None) or llm.name
        self.cache = EmbedCache(llm, Path(cache_dir) / f"emb_{str(tag).replace(':', '_').replace('/', '_')}.json")
        self.mat = self.cache.embed(texts)

    def dense(self, query, k=5):
        q = self.cache.embed([query])[0]
        sims = self.mat @ q
        idx = np.argsort(-sims)[:k]
        return [dict(self.chunks[i], score=float(sims[i])) for i in idx]

    def hybrid(self, query, k=5, rrf_k=60, pool=30):
        q = self.cache.embed([query])[0]
        dense_rank = np.argsort(-(self.mat @ q))[:pool]
        bm_rank = np.argsort(-self.bm25.scores(query))[:pool]
        fused = Counter()
        for r, i in enumerate(dense_rank):
            fused[int(i)] += 1 / (rrf_k + r + 1)
        for r, i in enumerate(bm_rank):
            fused[int(i)] += 1 / (rrf_k + r + 1)
        return [dict(self.chunks[i], score=s) for i, s in fused.most_common(k)]
