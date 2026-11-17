"""Spec §6 — demo surface (optional). Run from the repo root: streamlit run prototype/app.py"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import streamlit as st  # noqa: E402

import evals  # noqa: E402

st.set_page_config(page_title="LabelFlow refund agent — prototype v0", layout="wide")
page = st.sidebar.radio("Prototype v0", ["Queue", "Eval — eval_set_v0.csv"])
st.sidebar.caption("Prototype — no money moves.")

with open(evals.EVAL_SET, newline="", encoding="utf-8") as f:
    cases = [c for c in csv.DictReader(f) if c.get("case_id")]

if page == "Queue":
    st.title("Refund queue — prototype v0")
    labels = [f"{c['case_id']} · €{c['amount_eur'] or '?'} · {c['input_text'][:50]}" for c in cases]
    left, right = st.columns([1, 2])
    with left:
        choice = st.radio("Pick a case", labels, label_visibility="collapsed")
    case = cases[labels.index(choice)]
    with right:
        r = evals.run_one(case)
        st.subheader(f"{case['case_id']} · {case['input_text']}")
        st.markdown(f"**Decision:** `{r['action']}` · trust level **{r['trust_level']}**")
        if r["clause_id"]:
            st.markdown(f"**Clause applied:** {r['clause_id']}")
            st.caption(r["clause_text"])
        else:
            st.warning(f"Goes to a person: {r['reason']}")
        st.markdown(f"**Tracking evidence:** {r['evidence']}")
        st.markdown(f"**Amount:** €{r['amount_eur']}" if r["amount_eur"] else "**Amount:** missing")
        st.caption(f"Policy check: {r['policy']} · {r['model_version']} · policy {r['policy_version']}")
        b1, b2 = st.columns(2)
        can_execute = r["action"] == "refund" and r["trust_level"] == "L4"
        if b1.button("Execute", type="primary", disabled=not can_execute):
            st.toast("Prototype — nothing was posted.")
        if b2.button("Escalate to a person"):
            st.toast("Escalated with the receipt attached.")
        if not can_execute:
            st.caption("Execute is disabled: only an L4 refund under €20 with tracking evidence can settle alone.")
else:
    st.title("Eval — evals/eval_set_v0.csv")
    rows = evals.run()
    cols = ("case_id", "split", "expected_action", "action", "expected_clause", "clause_id", "ok")
    st.dataframe([{k: r[k] for k in cols} for r in rows], hide_index=True)