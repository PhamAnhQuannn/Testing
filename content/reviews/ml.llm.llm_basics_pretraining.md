# Review: ml.llm.llm_basics_pretraining

**Verdict: OK** (clean — no must-fix)

Independent content review (AI-engineer / LLM concept track, currency target 2026).

## Technical accuracy
- Training order stated correctly and repeatedly: pretraining → SFT → preference tuning (RLHF/DPO). Correct.
- "pretraining gives knowledge, post-training gives behaviour" framing is accurate and interview-grade.
- base vs instruct vs reasoning distinctions correct; reasoning model described as "RL with reward for correct answers" (RLVR) — current and correct for 2026.
- Next-token prediction / token / causal LM framing correct.
- context window = max tokens per call including **both** prompt and generated output; overflow → error/truncation. Correct.
- knowledge cutoff cleanly separated from context window; "widening context does not refresh knowledge, you must put new info in the prompt (RAG)". Correct.
- 2026 currency fine (mentions ~million-token context models; DPO "now very common").

## Quiz / mastery correctness
- b03 (→ b), b07 (→ b), b10 (→ a), b05 fill (order) — all answers and explanations correct.
- S010 (L1 recall), S011 (L2 score-2 scenario: base model for chatbot), S012 (L3 interview) — all `answer_md` correct, rubrics sensible and leveled; L3 matches mastery_bar (order + base/instruct/reasoning + context-window limit).

## Coverage discipline
- Mastery items test only what the lesson teaches. Lesson omits Chinchilla/scaling-laws (a `key_concepts` entry) but no mastery item relies on it — fine.

## Language
- Vietnamese clear; English terms kept in parentheses throughout.

## Nice-to-have
- None material.
