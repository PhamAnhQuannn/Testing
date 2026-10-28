# Review: ml.llm.decoding_sampling

**Verdict: OK** (clean — no must-fix)

Independent content review (AI-engineer / LLM concept track, currency target 2026).

## Technical accuracy
- logit → softmax → probability, decoding = selection rule over that table, model fixed. Correct.
- greedy (argmax, stable, repetitive) vs sampling (draw by probability, diverse). Correct.
- temperature = softmax(logit / T); T<1 sharpens (dividing by <1 widens logit gaps), T>1 flattens, T=1 unchanged; "adds no information, only reshapes". Correct.
- top-k = keep k highest; top-p (nucleus) = smallest set with cumulative prob ≥ p, self-adjusting, generally preferred over top-k; applied after temperature then re-normalized. Correct.
- b06 worked example: A=.50,B=.20,C=.15 with p=0.8 → {A,B,C} (0.70<0.8, 0.85≥0.8). Arithmetic and reasoning correct.
- task-based parameter choice (extraction/code/tool → low temp or greedy; creative → higher temp + top-p ~0.9; tune one knob at a time). Correct.
- temperature 0 ≈ deterministic but not bit-for-bit: floating-point non-associativity + non-deterministic batching / GPU reduction order shift logits at the last digits, flipping argmax when two tokens are near-tied. This is the current (2025–2026 batch-invariance) explanation and is correct.

## Quiz / mastery correctness
- b04 (→ a), b06 (→ b), b08 (→ a) — all answers/explanations correct.
- S016 (L1), S017 (L2 score-2: JSON extraction determinism), S018 (L3 interview) — correct; rubrics sensible and leveled. S018 covers two of the mastery_bar's three clauses (param selection + temp-0 non-determinism).

## Coverage discipline
- Mastery items test only taught ideas. Good.

## Language
- Vietnamese clear; English terms in parentheses.

## Nice-to-have
- mastery_bar_vi includes "cài temperature/top-k/top-p bằng NumPy" (implement in NumPy), but this is a concept-track lesson with no code problems, so L3 item S018 tests the two conceptual clauses only. Consistent with the lesson scope (does not teach NumPy coding); mismatch is with the mastery_bar wording, not the item. No action required for concept track.
