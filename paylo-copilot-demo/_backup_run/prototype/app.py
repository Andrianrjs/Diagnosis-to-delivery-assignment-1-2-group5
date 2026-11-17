"""Streamlit demo surface: inbox, ticket view, draft panel, eval page. Run: streamlit run prototype/app.py"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import streamlit as st, pandas as pd
import router, route_rule, retrieve, draft as drafter, policy

st.set_page_config(page_title="Support copilot — prototype v0", layout="wide")
page = st.sidebar.radio("Prototype v0", ["Inbox", "Eval — tickets_v0.csv"])
st.sidebar.caption("Streamlit = demo surface. One file, one session, no auth, no logs.")

if page == "Inbox":
    st.title("Support copilot — prototype v0")
    tickets = pd.read_csv("evals/tickets_v0.csv")          # demo rows: replace with your own demo tickets, NOT the eval rows
    c1, c2 = st.columns([1.1, 2])
    with c1:
        st.subheader("Open tickets")
        choice = st.radio("Pick a ticket", tickets["id"] + " · " + tickets["text"].str.slice(0, 60), label_visibility="collapsed")
    with c2:
        row = tickets.iloc[int(choice.split(" · ")[0][1:]) - 1]
        cat, conf = router.predict(row["text"])
        decision = route_rule.decide(cat, conf, row["text"])
        st.subheader(row["id"] + " · " + row["text"])
        st.caption(f"routed as {cat} ({conf:.2f}) → {decision}")
        if decision == "draft":
            passages = retrieve.top_k(row["text"])
            text = drafter.draft(row["text"], passages)
            status, reason = policy.check(text)
            st.markdown("**Suggested reply — review before sending**")
            st.write(text)
            st.caption("Sources: " + " · ".join(f"{p['article']} · {p['section']}" for p in passages))
            st.caption(f"Policy check: {status} {reason} · Trust level L2 · not sent until you approve")
            b1, b2, b3 = st.columns(3)
            b1.button("✅ Approve & send", type="primary"); b2.button("✏️ Edit draft"); b3.button("↗ Escalate to human")
        else:
            st.warning("Human only — no draft. Escalated with the context.")
else:
    st.title("Eval — evals/tickets_v0.csv")
    import evals
    out = evals.run()
    st.dataframe(out, use_container_width=True, hide_index=True)
