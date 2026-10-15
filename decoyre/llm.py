"""LLM backends behind one small interface.

chat(messages, tools=None, json_mode=False) -> dict(content, tool_calls, prompt_tokens, completion_tokens)
embed(texts) -> list[list[float]]

Neutral message format used by the agents:
  {"role": "system"|"user", "content": str}
  {"role": "assistant", "content": str, "tool_calls": [{"id", "name", "args"}]}
  {"role": "tool", "tool_call_id": str, "name": str, "content": str}
"""
import hashlib
import json
import math
import os
import re
import time
import urllib.request

from .textutil import tokenize

THINK = re.compile(r"<think>.*?</think>", re.S)


def _post(url, payload, headers=None, timeout=600, retries=2):
    data = json.dumps(payload).encode()
    h = {"Content-Type": "application/json", **(headers or {})}
    last = None
    for i in range(retries + 1):
        try:
            req = urllib.request.Request(url, data=data, headers=h)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read())
        except Exception as e:  # network hiccup / rate limit
            last = e
            time.sleep(2 * (i + 1))
    raise RuntimeError(f"LLM request failed: {last}")


class OllamaLLM:
    def __init__(self, model="qwen3:8b", embed_model="nomic-embed-text",
                 host=None, num_ctx=8192, think="auto"):
        self.model, self.embed_model = model, embed_model
        self.host = host or os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        if think == "auto":  # only thinking-capable families get think=False; others omit the field
            think = False if model.startswith(("qwen3", "deepseek-r1", "gpt-oss", "magistral")) else None
        self.num_ctx, self.think = num_ctx, think
        self.name = f"ollama:{model}"

    def _convert(self, messages):
        out = []
        for m in messages:
            if m["role"] == "assistant":
                mm = {"role": "assistant", "content": m.get("content", "")}
                if m.get("tool_calls"):
                    mm["tool_calls"] = [{"function": {"name": t["name"], "arguments": t["args"]}} for t in m["tool_calls"]]
                out.append(mm)
            elif m["role"] == "tool":
                out.append({"role": "tool", "content": m["content"], "tool_name": m["name"]})
            else:
                out.append({"role": m["role"], "content": m["content"]})
        return out

    def chat(self, messages, tools=None, json_mode=False, temperature=0.0):
        payload = {"model": self.model, "messages": self._convert(messages), "stream": False,
                   "options": {"temperature": temperature, "num_ctx": self.num_ctx, "seed": 42}}
        if self.think is not None:
            payload["think"] = self.think
        if tools:
            payload["tools"] = tools
        if json_mode:
            payload["format"] = "json"
        r = _post(f"{self.host}/api/chat", payload)
        msg = r.get("message", {})
        calls = []
        for i, tc in enumerate(msg.get("tool_calls") or []):
            fn = tc.get("function", {})
            args = fn.get("arguments", {})
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    args = {}
            calls.append({"id": f"call_{i}", "name": fn.get("name", ""), "args": args or {}})
        return {"content": THINK.sub("", msg.get("content", "") or "").strip(), "tool_calls": calls,
                "prompt_tokens": r.get("prompt_eval_count", 0) or 0,
                "completion_tokens": r.get("eval_count", 0) or 0}

    def embed(self, texts):
        out = []
        for i in range(0, len(texts), 32):
            r = _post(f"{self.host}/api/embed", {"model": self.embed_model, "input": texts[i:i + 32]})
            out += r["embeddings"]
        return out


class OpenAICompatLLM:
    """Any OpenAI-compatible server: Groq, OpenRouter, Together, vLLM, LM Studio, OpenAI."""

    def __init__(self, model, base_url=None, api_key=None, embed_model=None):
        self.model = model
        self.base = (base_url or os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")).rstrip("/")
        self.key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.embed_model = embed_model
        self.name = f"openai:{model}"

    def _convert(self, messages):
        out = []
        for m in messages:
            if m["role"] == "assistant":
                mm = {"role": "assistant", "content": m.get("content") or ""}
                if m.get("tool_calls"):
                    mm["tool_calls"] = [{"id": t["id"], "type": "function",
                                         "function": {"name": t["name"], "arguments": json.dumps(t["args"])}}
                                        for t in m["tool_calls"]]
                out.append(mm)
            elif m["role"] == "tool":
                out.append({"role": "tool", "tool_call_id": m["tool_call_id"], "content": m["content"]})
            else:
                out.append({"role": m["role"], "content": m["content"]})
        return out

    def chat(self, messages, tools=None, json_mode=False, temperature=0.0):
        payload = {"model": self.model, "messages": self._convert(messages), "temperature": temperature}
        if tools:
            payload["tools"] = tools
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        r = _post(f"{self.base}/chat/completions", payload, {"Authorization": f"Bearer {self.key}"})
        msg = r["choices"][0]["message"]
        calls = []
        for tc in msg.get("tool_calls") or []:
            try:
                args = json.loads(tc["function"].get("arguments") or "{}")
            except json.JSONDecodeError:
                args = {}
            calls.append({"id": tc.get("id", "call"), "name": tc["function"]["name"], "args": args})
        u = r.get("usage", {})
        return {"content": THINK.sub("", msg.get("content") or "").strip(), "tool_calls": calls,
                "prompt_tokens": u.get("prompt_tokens", 0), "completion_tokens": u.get("completion_tokens", 0)}

    def embed(self, texts):
        if not self.embed_model:
            return HashEmbedder().embed(texts)
        r = _post(f"{self.base}/embeddings", {"model": self.embed_model, "input": texts},
                  {"Authorization": f"Bearer {self.key}"})
        return [d["embedding"] for d in r["data"]]


class HashEmbedder:
    """Deterministic offline embedding (hashed sublinear TF). Used by the mock and as a fallback."""

    def __init__(self, dim=1024):
        self.dim = dim

    def embed(self, texts):
        out = []
        for t in texts:
            v = [0.0] * self.dim
            for tok in tokenize(t):
                h = int(hashlib.md5(tok.encode()).hexdigest(), 16)
                v[h % self.dim] += 1.0
            v = [math.log1p(x) for x in v]
            n = math.sqrt(sum(x * x for x in v)) or 1.0
            out.append([x / n for x in v])
        return out


class MockLLM:
    """Offline stand-in so the whole pipeline can be tested without a model.

    It is a crude extractive reader: it calls the most plausible tool once or twice,
    then answers with the context lines that overlap most with the question.
    Numbers produced with it are NOT results; use a real model for the paper.
    """
    name = "mock"

    def __init__(self):
        self._emb = HashEmbedder()

    def embed(self, texts):
        return self._emb.embed(texts)

    @staticmethod
    def _question(messages):
        for m in reversed(messages):
            if m["role"] == "user":
                mt = re.search(r"QUESTION:\s*(.+)", m["content"])
                return mt.group(1).strip() if mt else m["content"].strip().splitlines()[-1]
        return ""

    @staticmethod
    def _extract(question, context):
        q = set(tokenize(question))
        best, src = [], None
        for line in context.splitlines():
            hdr = re.match(r"^\[([\w\-./]+\.md)", line.strip())
            if hdr:
                src = hdr.group(1)
                continue
            if line.startswith(("QUESTION:", "ROUTER HINT", "BUNDLE INDEX", "- [")):
                continue
            s = len(q & set(tokenize(line)))
            if s >= 2 and len(line.strip()) > 10:
                best.append((s, line.strip(), src))
        if not best:
            return "I don't know: the sources do not contain this."
        best.sort(key=lambda x: -x[0])
        return " ".join(f"{l} [{s}]" if s else l for _, l, s in best[:3])

    def chat(self, messages, tools=None, json_mode=False, temperature=0.0):
        ptoks = sum(len(m.get("content") or "") for m in messages) // 4
        if json_mode:
            return {"content": "{}", "tool_calls": [], "prompt_tokens": ptoks, "completion_tokens": 2}
        q = self._question(messages)
        last_user = max(i for i, m in enumerate(messages) if m["role"] == "user")
        results = [m for m in messages[last_user:] if m["role"] == "tool"]
        names = [t["function"]["name"] for t in (tools or [])]
        call = None
        if tools and len(results) < 2:
            ctx = " ".join(m["content"] for m in messages if m["role"] in ("system", "user"))
            ids = re.findall(r"\[([\w\-/]+)\]", ctx)
            qt = set(tokenize(q))
            scored = sorted(((len(qt & set(tokenize(i.replace("/", " ").replace("-", " ")))), i) for i in ids), reverse=True)
            tried = {json.dumps(m.get("name")) for m in results}
            if "read_concept" in names and scored and scored[0][0] > 0 and not results:
                call = {"id": "m1", "name": "read_concept", "args": {"concept_id": scored[0][1]}}
            elif "search_docs" in names and '"search_docs"' not in tried:
                call = {"id": "m2", "name": "search_docs", "args": {"query": q}}
        if call:
            return {"content": "", "tool_calls": [call], "prompt_tokens": ptoks, "completion_tokens": 10}
        context = "\n".join(m["content"] for m in messages[last_user:] if m["role"] in ("tool", "user"))
        ans = self._extract(q, context)
        return {"content": ans, "tool_calls": [], "prompt_tokens": ptoks, "completion_tokens": len(ans) // 4}


def make_llm(backend="ollama", model=None, **kw):
    if backend == "ollama":
        return OllamaLLM(model=model or "qwen3:8b", **kw)
    if backend == "openai":
        return OpenAICompatLLM(model=model or "gpt-4o-mini", **kw)
    if backend == "mock":
        return MockLLM()
    raise ValueError(backend)
