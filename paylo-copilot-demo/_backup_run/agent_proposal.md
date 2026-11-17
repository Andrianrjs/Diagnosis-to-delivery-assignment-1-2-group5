# What the agent should say after the eval (and what to say if it doesn't)

**Result:** 8/20 how-do-I tickets sendable as is = 40 % — criterion 45 % → FAIL. Drafts on human-only: 0. Policy blocks: 0.

**Misses, by cause**
1. 9 × expected section "Release notes 4.12" — the knowledge base has no such section. Nine tickets are about what changed in the update (button moved, new CSV column order, Payslips renamed, scheduled export paused). The drafter cites the old "Export a run as CSV" section, which now describes a button that no longer exists. → **Not a prompt problem: a KB gap.**
2. 2 × "Add an admin user" (E17 French ticket at confidence 0.57; E19 "invitation link expired" at 0.68) — escalated by the 0.70 threshold. → A threshold/coverage question, not a drafting one.
3. 1 × "Payslips as PDF" (E02) — escalated at confidence 0.68, just under the threshold. → Same cause as 2: the 0.70 threshold is a cost decision, revisit it with the cost matrix.

**Proposed changes to spec.md (not to the prompt)**
- §10 / kb: add a "Release notes 4.12" section to KB-214 (what moved, the Legacy CSV option, Documents menu, scheduled export paused). Expected effect: most of cause 1.
- §4: French tickets — either translate the query before retrieval, or route `language != en` to escalate explicitly, so the miss is a decision and not an accident.
- §2.3: retrieval chunk = heading + first sentence, and add a synonyms line per article ("payslip = bulletin de paie = Documents").
- §7: keep the eval-set frozen; re-run after each change; the number must come from the same 25 rows.

**After the first change alone** (after_fix/kb): 13/20 = 65 % → PASS. Four "release notes" tickets still miss (retrieval ranks the old section first for E03/E12/E13/E14): that is the next line of spec v2, not a prompt tweak.

**If the live agent proposes something else:** read it aloud, then say: "Whatever it proposes, look at the shape: it is a change to the spec or the data, not to the prompt. That is the loop."
**If the live number differs from 40 %:** say so — "your number will differ too; what matters is the misses by cause." The backup output is in eval_output_before_fix.txt.
