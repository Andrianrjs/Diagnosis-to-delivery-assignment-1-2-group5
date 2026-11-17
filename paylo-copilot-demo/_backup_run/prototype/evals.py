"""Spec §7. Never tune while looking at these rows."""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
import pandas as pd
from collections import Counter
import router, route_rule, retrieve, draft as drafter, policy

CRITERION = 0.45


def run_one(text):
    cat, conf = router.predict(text)
    decision = route_rule.decide(cat, conf, text)
    passages = retrieve.top_k(text) if decision == "draft" else []
    text_out = drafter.draft(text, passages) if decision == "draft" else "NO_DRAFT"
    if decision == "draft" and text_out == "NO_DRAFT":
        decision = "escalate"
    status, reason = policy.check(text_out)
    return dict(category=cat, confidence=round(conf, 2), decision=decision, draft=text_out,
                citations=[{"article": p["article"], "section": p["section"], "score": round(p["score"], 2)} for p in passages],
                policy=status, reason=reason)


def run(path="evals/tickets_v0.csv"):
    df = pd.read_csv(path)
    rows = []
    for _, r in df.iterrows():
        o = run_one(r["text"])
        cited = {(c["article"], c["section"]) for c in o["citations"]}
        cited_in_text = re.findall(r"\[(KB-\d+) · ([^\]]+)\]", o["draft"])
        hit3 = (r["expected_article"] in {c["article"] for c in o["citations"]}) if o["decision"] == "draft" and isinstance(r["expected_article"], str) else None
        sendable = (o["decision"] == "draft" and o["policy"] == "pass" and (r["expected_article"], r["expected_section"]) in {(a, s.strip()) for a, s in cited_in_text})
        rows.append({"id": r["id"], "expected": r["expected_category"], "routed": o["category"], "conf": o["confidence"], "decision": o["decision"],
                     "expected_outcome": r["expected_outcome"], "hit@3": hit3, "policy": o["policy"], "sendable": sendable,
                     "expected_section": r["expected_section"], "cited": "; ".join(f"{a} · {s}" for a, s in cited_in_text) or "—"})
    out = pd.DataFrame(rows)
    hdi = out[out["expected"] == "how_do_i"]
    n_send, n_hdi = int(hdi["sendable"].sum()), len(hdi)
    print(out[["id", "expected", "routed", "conf", "decision", "hit@3", "policy", "sendable", "expected_section", "cited"]].to_string(index=False))
    print(f"\nrouting accuracy      {(out['expected'] == out['routed']).mean():.2f}")
    print(f"retrieval hit@3       {out['hit@3'].dropna().mean():.2f}")
    print(f"sendable as is        {n_send}/{n_hdi} how-do-I tickets = {n_send / n_hdi:.0%}   (criterion {CRITERION:.0%})")
    print(f"drafts on human-only  {int(((out['expected_outcome'] == 'escalate') & (out['decision'] == 'draft')).sum())}   (must be 0)")
    print(f"policy blocks         {int((out['policy'] == 'block').sum())}")
    misses = hdi[~hdi["sendable"]]
    print("\nmisses by cause:")
    for sec, n in Counter(misses["expected_section"]).most_common():
        ids = ", ".join(misses[misses["expected_section"] == sec]["id"])
        print(f"  {n} × expected section '{sec}'  ({ids})")
    verdict = "PASS" if n_send / n_hdi >= CRITERION else "FAIL — do not fix the prompt; propose the change to spec.md"
    print(f"\nverdict: {verdict}")
    return out


if __name__ == "__main__":
    run()
