# Review: ml.rag_agents.agent_reliability

**Verdict: PASS (clean, publishable).** Independent content review, 2026-10-27.

## Technical accuracy & currency
- **Compounding-error math verified:** independent per-step reliability multiplies; 0.95^10 ≈ 0.599 ≈ 0.60, i.e. ~40% of runs fail somewhere. Correct in b01, b03, S304, and summary.
- Four failure modes (wrong tool, bad arguments, non-termination, cost/latency blowup) accurate.
- Reliability techniques: step/budget limits + timeout, input/output validation, bounded retry + fallback, useful error messages, step tracing — all correct.
- Human-in-the-loop for risky/irreversible actions; guardrails as hard rules outside the model — correct.
- **Prompt injection** via tool output / retrieved docs correctly framed: treat tool output + retrieved text as untrusted data, not commands; danger amplified because agents have action tools; defense = least privilege + separation + human approval, not a prompt instruction. Accurate and current.
- Least privilege, sandbox, destructive-action confirmation (defense in depth) correct.
- Trajectory eval: score trajectory (tool-selection accuracy) + outcome (task success rate) + cost/steps via a repeatable harness. Correct.

## Quiz / fill items
- b03 (a — includes the 0.95^10 ≈ 0.60 math), b05 (a), b09 (a), b11 (trajectory): all `answer` + `explain_md` correct. b03 distractors correctly reject additive probability.

## Mastery items
- S304 diff1 recall: four failure modes + compounding errors (with the 0.95^10 figure). Right level.
- S305 diff2: email-reading agent with send-mail + refund tools — loop control, human approval, injection, plus one more measure. Matches lesson.
- S306 diff3 interview: matches `mastery_bar_vi` (design trajectory-eval harness + safety guardrails incl. step limits, permissions, human confirmation). Rubric requires trajectory scoring + all three mandatory constraints. Right level.
- Mastery items stay within lesson scope.

## Vietnamese + terms
Clear; terms parenthesized (compounding errors, failure modes, human-in-the-loop, guardrails, prompt injection, least privilege, sandbox, trajectory, tool-selection accuracy, task success rate).

No must-fix items.
