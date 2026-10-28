# Review: ml.llm_eval_serving.llm_as_judge

**Reviewer:** independent content reviewer (AI-engineer track)
**Date:** 2026-10-27
**Verdict: PASS — no must-fix.** Accurate, current (2026); kappa arithmetic verified; all quizzes and mastery items correct.

## Technical accuracy & currency
- LLM-as-judge rationale (scalable/cheap vs human eval, but biased → must validate) correct.
- Pointwise (absolute, unstable) vs pairwise (relative, more reliable); reference-based vs reference-free — correct.
- Good-judge design: clear rubric with per-level descriptions, few-shot, CoT-then-verdict (reason before score, G-Eval), constrained output (JSON), temperature 0 — all correct and current.
- **Kappa (chance-corrected agreement):** formula kappa = (p_o − p_e)/(1 − p_e) correct; worked example (0.8 − 0.5)/(1 − 0.5) = **0.6** verified; interpretation ranges (≈ Landis–Koch) reasonable; rightly preferred over raw %. Matches SPECIAL check. (concepts_vi example in subtopics.json also checks: 16/20=0.8 observed, p_e=0.5, kappa=0.6.)
- **≥3 biases + mitigations:** position (swap order, score both ways / win-both), verbosity/length (rubric states length ≠ criterion, control length), self-preference (use different model family, multi-judge); plus leniency, format — matches SPECIAL check.
- Human eval still needed for final sign-off, safety, periodic calibration — correct.

## Quizzes
- b03 [a] pairwise > pointwise because relative comparison more stable — correct; "pairwise always cheaper" and "never biased" correctly refuted.
- b06 [a] temp0 + rubric + CoT-then-verdict + constrained output — correct.
- b08 fill "Cohen's kappa" — correct, broad accept list.
- b10 [a] position bias + swap/aggregate — correct; distractors mislabel bias type (rightly wrong).

## Mastery items
- S316 (diff1): pointwise vs pairwise + why pairwise more reliable — right level.
- S317 (diff2 scenario): unstable scores → temp0/rubric/CoT/constrained; 88% agreement insufficient → kappa — both halves lesson-taught; rubric sensible.
- S318 (diff3 interview): rubric design + kappa (with why-not-raw-%) + ≥3 biases/mitigations + when human eval — matches `mastery_bar_vi` exactly. Only tests taught ideas.

## Language
Vietnamese clear; English terms parenthesized (pointwise, pairwise, rubric, CoT-then-verdict, Cohen's kappa, position/verbosity/self-preference bias).
