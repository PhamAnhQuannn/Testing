# Review: ml.llm.adaptation_decision

**Verdict: OK** (clean — no must-fix)

Independent content review (AI-engineer / LLM concept track, currency target 2026).

## Technical accuracy
- Failure-mode-first framing correct: diagnose the error type (missing knowledge / wrong behavior / wrong format) before picking a technique (b01).
- **Decision mantra correct and matches special-check**: "new knowledge → RAG; new behavior → fine-tune; try prompt first" (b02 ladder, b08 interview callout, b09 fill). Cost-escalating ladder prompt → RAG → fine-tune → combine, each measured on an eval set. Accurate.
- RAG vs fine-tune reasoning correct: fine-tune doesn't reliably inject fresh facts, is costly, goes stale, still can hallucinate; RAG updates by re-indexing and supports citations (b04). Fine-tune conditions (good labeled data + prompt already tried) correct (b05).
- **API vs self-host axis correct and matches special-check**: presented as an orthogonal axis. Hosted API = fast start, no ops, per-token, data leaves boundary, vendor lock-in; self-host open model = control + data stays in-house (privacy), fixed GPU cost (cheaper at steady high volume), full ops burden. Correct (b07, b10).
- Advanced points (routing/cascade, distillation, reducing vendor lock-in via abstraction + portable evals) correct (b11).

## Quiz / mastery correctness
- b03 (→ a, new policy = knowledge → RAG), b06 (→ a, wrong tone + 800 labeled pairs = behavior → fine-tune), b09 fill (RAG / prompt), b10 (→ a, sensitive data can't leave → self-host) — all correct. Distractors correctly reject "always fine-tune", "RAG mandatory before fine-tune", "API always cheaper/safer", "must retrain from scratch".
- S286 (L1 mantra), S287 (L2 score-2: two simultaneous problems, diagnose + map + why not fine-tune both), S288 (L3 interview: both axes + cost/latency/privacy trade-offs) — correct, rubrics sensible, levels right. S288 maps exactly to `mastery_bar_vi`.

## Coverage discipline
- Mastery items test only taught ideas. Good.

## Language
- Vietnamese clear; English terms parenthesized (RAG, fine-tune, hosted API, self-host, routing/cascade, distillation, vendor lock-in, compliance).

## Nice-to-have
- None material.
