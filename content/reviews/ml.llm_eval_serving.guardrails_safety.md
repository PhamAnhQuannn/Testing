# Review: ml.llm_eval_serving.guardrails_safety

**Reviewer:** independent content reviewer (AI-engineer track)
**Date:** 2026-10-27
**Verdict: PASS — no must-fix.** Accurate, current (2026); lethal-trifecta (3 legs) verified correct; all quizzes and mastery items correct.

## Technical accuracy & currency
- Threats correct: prompt injection direct (user types "ignore instructions") vs indirect (hidden in retrieved docs/email/web/tool output) — indirect rightly flagged as more dangerous; jailbreak; sensitive-data leakage/exfiltration; harmful output; tool misuse.
- Foundational principle "all non-authored text (user input, retrieved content, tool output) is untrusted DATA, not instructions" — correct and stated clearly; matches SPECIAL check (treat tool output as untrusted).
- Defense in depth correct: input filtering, output moderation + PII redaction, separate guardrail model/validator, structured/constrained output, least privilege + allowlist + human approval, sandbox + rate limit; no silver bullet; refusal vs over-refusal; red teaming. Matches SPECIAL check (layered defense).
- **Lethal trifecta = private data + untrusted content + external communication (exactly 3 legs)** — correct; attributed to Simon Willison (correct); "remove any one leg breaks the chain" correct. b09 fill reinforces the number 3. Matches SPECIAL check precisely.

## Quizzes
- b03 [a] indirect injection (hidden command in forwarded email) — correct; jailbreak / "mailbox is trusted" rightly rejected.
- b06 [a] defense-in-depth rationale — correct; "faster/cheaper" and "one system-prompt line suffices" rejected.
- b09 fill "ba/3" — correct, good accept list.
- b10 [a] remove a leg (architectural) — correct; prompt platitude / "stronger model is immune" rejected.

## Mastery items
- S319 (diff1): direct vs indirect injection + why indirect worse — right level, rubric sensible.
- S320 (diff2 scenario): support bot with refund tool → ≥3 distinct layers each mapped to a threat, must include refund-tool protection — lesson-taught; rubric sensible.
- S321 (diff3 interview): threats + layered defense + lethal trifecta (correct 3 legs) + remove-a-leg as strongest architectural fix — matches `mastery_bar_vi`. Only tests taught ideas.

## Language
Vietnamese clear; English terms parenthesized (prompt injection direct/indirect, jailbreak, exfiltration, defense in depth, least privilege, lethal trifecta).
