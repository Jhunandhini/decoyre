import re

STOP = set("""a an the of to in on for and or is are was were be by with at from as it this that
which what how do does did we our i you your me my can should could would will there their its
into about any all get use used using current currently now today give tell list every complete full""".split())


def parse_frontmatter(text):
    meta, body = {}, text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            for line in parts[1].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
            body = parts[2].strip()
    return meta, body


_TOK = re.compile(r"[a-z0-9_]+(?:-[0-9]+)?")


def tokenize(text, keep_stop=False):
    toks = []
    for t in _TOK.findall(text.lower()):
        if not keep_stop and t in STOP:
            continue
        toks.append(t)
        if "_" in t:                       # snake_case: also index the parts
            toks += [p for p in t.split("_") if p and p not in STOP]
    return toks


def chunk_text(text, size=600, overlap=60):
    """Line-aware fixed-size chunking (typical RAG splitter behaviour)."""
    lines, chunks, cur = text.splitlines(keepends=True), [], ""
    for ln in lines:
        if len(cur) + len(ln) > size and cur.strip():
            chunks.append(cur)
            cur = cur[-overlap:] if overlap else ""
        cur += ln
    if cur.strip():
        chunks.append(cur)
    return chunks


def identifiers(text):
    """Distinctive tokens worth grounding-checking: snake_case, IDs, numbers."""
    out = set(re.findall(r"\b[a-z]+(?:_[a-z0-9]+)+\b", text.lower()))
    out |= set(re.findall(r"\b[A-Z]{2,5}-\d{3,5}\b", text))
    return out


ABSTAIN_PAT = re.compile(
    r"(i don'?t know|i do not know|not (?:documented|found|available|defined|specified|mentioned|covered)|"
    r"no (?:information|documentation|policy|record|mention)|does not (?:exist|contain|mention)|"
    r"there is no|couldn'?t find|could not find|cannot find|unable to find)", re.I)


def is_abstention(answer):
    head = answer.strip()[:220]
    return bool(ABSTAIN_PAT.search(head))


CITE_PAT = re.compile(r"\[([\w\-./]+?(?:\.md)?)\]")


def citations(answer):
    return [c for c in CITE_PAT.findall(answer) if "/" in c or c.endswith(".md")]
