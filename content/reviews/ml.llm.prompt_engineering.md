# Review: ml.llm.prompt_engineering

**Verdict: OK** (clean — no must-fix)

Independent content review (AI-engineer / LLM concept track, currency target 2026).

## Technical accuracy
- system / user / assistant roles + instruction hierarchy (system outranks user) correct and current.
- zero-shot vs few-shot (2-5 in-context examples, no weight change) correct.
- CoT correct; the 2026 note that reasoning models already reason internally and usually don't need manual CoT is accurate.
- grounding to reduce hallucination (answer only from supplied context, allow "don't know", cite) correct; framed as the basis of RAG.
- prompt injection: direct (user types malicious instruction) vs indirect (instruction hidden in docs/websites the app ingests) — correct, and indirect is correctly called the more dangerous one. Defenses are realistic and honest ("none absolute, layer them"): treat external text as data + delimiters, privilege separation / least privilege, output validation. No over-promising on delimiters.
- systematic improvement via a fixed eval set with gold labels, baseline, change-one-thing, regression test, versioning — correct and interview-grade.

## Quiz / mastery correctness
- b03 (→ a), b06 (→ a), b08 (→ a), b10 fill (eval set) — all answers/explanations correct; distractors correctly refute "few-shot = fine-tune" and "few-shot cheaper".
- S013 (L1), S014 (L2 score-2: fix a Q&A prompt), S015 (L3 interview: systematic improvement + injection) — correct; L3 matches mastery_bar exactly (prove improvement via eval set + prevent prompt injection).

## Coverage discipline
- Mastery items test only taught ideas. Good.

## Language
- Vietnamese clear; English terms in parentheses.

## Nice-to-have
- None material.
