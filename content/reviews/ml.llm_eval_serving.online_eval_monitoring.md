# Review: ml.llm_eval_serving.online_eval_monitoring

**Reviewer:** independent content reviewer (AI-engineer track)
**Date:** 2026-10-27
**Verdict: PASS — no must-fix.** Accurate, current (2026); all quizzes and mastery items correct.

## Technical accuracy & currency
- Core premise correct: online has no per-request ground truth → trace everything, infer from signals, close the loop.
- Explicit (👍/👎, rating — sparse, sampling-biased) vs implicit signals (regeneration/retry, edit/accept, thread abandonment, conversation length, task completion) — correct and well distinguished.
- Operational metrics (latency, token/cost, error rate) + online LLM-as-judge sampling (1-5%, prioritize bad-signal turns, calibrate vs human) — correct.
- Tracing / OpenTelemetry GenAI conventions — current and correct.
- Feedback loop (log → sample & label → push hard cases into eval set → re-test) — matches SPECIAL check.
- Regression detection: baseline + alert, A/B test, drift (input-distribution shift vs silent provider update), pinned eval to disambiguate — all correct. Pinned-eval logic consistent across b07/b08/b09 and S315.

## Quizzes
- b04 [a] implicit signals + judge sampling — correct; forced feedback / offline-only correctly rejected.
- b06 fill "eval set" — correct (closing the loop), good accept list.
- b09 [a] verify against baseline/segment/significance/pinned eval — correct; blind model swap / prompt platitude rejected.
- b10 [a] A/B test for online validation — correct; week-over-week confounds drift (rightly rejected).

## Mastery items
- S313 (diff1): list signals + explicit vs implicit — right level, rubric sensible.
- S314 (diff2 scenario): sparse 👍/👎 → add implicit + judge, feedback loop, one operational metric — all lesson-taught; rubric sensible.
- S315 (diff3 interview): feedback loop + signal tiers + verify-by-numbers + pinned eval to separate model-change vs input-drift — matches `mastery_bar_vi`. Only tests taught ideas.

## Language
Vietnamese clear; English terms parenthesized (implicit/explicit, regeneration, task completion, drift, pinned eval, A/B test).
