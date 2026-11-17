"""Retrieval over the KB articles (provided). Chunks by heading, cosine top-k."""
import glob, os, re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_CHUNKS, _VEC, _MAT = [], None, None


def _load(kb_dir="kb"):
    global _CHUNKS, _VEC, _MAT
    _CHUNKS = []
    for path in sorted(glob.glob(os.path.join(kb_dir, "*.md"))):
        art = os.path.basename(path).replace(".md", "")
        text = open(path, encoding="utf-8").read()
        for sec in re.split(r"\n## ", text)[1:]:
            title, _, body = sec.partition("\n")
            _CHUNKS.append({"article": art, "section": title.strip(), "text": body.strip()})
    _VEC = TfidfVectorizer(ngram_range=(1, 2)).fit([c["section"] + " " + c["text"] for c in _CHUNKS])
    _MAT = _VEC.transform([c["section"] + " " + c["text"] for c in _CHUNKS])


def top_k(query, k=3, min_score=0.05):
    if _VEC is None:
        _load()
    sims = cosine_similarity(_VEC.transform([query]), _MAT)[0]
    order = sims.argsort()[::-1][:k]
    return [dict(_CHUNKS[i], score=float(sims[i])) for i in order if sims[i] >= min_score]
