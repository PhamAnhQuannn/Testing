# Review: ml.llm.hallucination_reasoning

**Verdict: OK** (clean — no must-fix)

Independent content review (AI-engineer / LLM concept track, currency target 2026).

## Technical accuracy
- Hallucination cause correct: LLM trained to predict the next plausible token, no built-in truth check; compounded by missing/stale knowledge (knowledge cutoff) and pressure to answer + sampling. Matches the special-check requirement exactly (b01, b02).
- Mitigations correct and complete: grounding/RAG, citations, abstention ("Không đủ thông tin"), low temperature for factual tasks, verification (self-consistency / separate check), constrained output — and the AI-engineer point that each must be *measured* (groundedness / timely-abstention on an eval set). (b05, b06)
- Reasoning models correct: long chain-of-thought, test-time compute, thinking tokens billed as output; explicitly NOT a hallucination cure (b03, b08, b09). CoT faithfulness caveat is accurate and current.
- "Use code/tool, not an LLM, for deterministic tasks (23×47, fixed rule, table lookup)" is a correct and valuable framing (b09, b10).

## Quiz / mastery correctness
- b04 (→ a), b07 (→ a, grounding + abstention + citations + eval), b10 (→ a, multi-step logic puzzle), b11 fill (abstention) — all answers/explanations correct. Distractors correctly reject "model lies on purpose", "raise temperature", and "reasoning model cures hallucination".
- S274 (L1 recall), S275 (L2 score-2 scenario: grounding + stability + measurement), S276 (L3 interview) — answers correct, rubrics sensible, levels right. S276 maps exactly to `mastery_bar_vi` (causes + measurable mitigations + when to use code vs LLM).

## Coverage discipline
- Mastery items test only taught ideas. Good.

## Language
- Vietnamese clear; English terms parenthesized (hallucination, grounding, abstention, test-time compute, faithfulness).

## Nice-to-have
- None material.
