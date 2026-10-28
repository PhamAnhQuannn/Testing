# Review: ml.llm.context_engineering

**Verdict: OK** (clean — no must-fix)

Independent content review (AI-engineer / LLM concept track, currency target 2026).

## Technical accuracy
- context window contents (system prompt + history + retrieved docs + tool defs/results) correct.
- API is stateless; app must resend history each request — correct, and the "forgot the name at turn 20" quiz illustrates it well.
- token cost formula `input×price_in + output×price_out`; output priced higher than input; ~1 token ≈ 0.75 EN words; in long chats the input (growing history) dominates. Correct.
- long-conversation strategies: truncation/sliding window, summarization/compaction, external memory; on context-length-exceeded → catch, trim/summarize, retry. Correct.
- RAG vs long-context tradeoffs correct (long-context simple but pays per turn + lost-in-the-middle; RAG cheaper/scalable but needs embedding+vector infra and depends on retrieval quality).
- prompt caching: exact-prefix match, stable prefix first / variable (user question) last, cache-read discount, TTL, first write slightly costlier. Correct and current; "put question first → cache misses entirely" is right.
- lost-in-the-middle / context rot correct; "less but on-target" guidance sound.

## Quiz / mastery correctness
- b03 (→ b), b05 (→ c, compaction+memory), b08 (→ b, stable prefix first) — all answers/explanations correct.
- S019 (L1), S020 (L2 score-2: context-length-exceeded, keep early decisions), S021 (L3 interview: full context strategy + token-cost estimate) — correct; L3 matches mastery_bar exactly; cost figures (RAG 3×500=1.5k vs long-context 50k/turn) consistent with the lesson.

## Coverage discipline
- Mastery items test only taught ideas. Good.

## Language
- Vietnamese clear; English terms in parentheses.

## Nice-to-have
- None material.
