# Review: ml.rag_agents.rag_pipeline

**Verdict: OK** (clean — no must-fix)

Independent content review (AI-engineer / RAG concept track, currency target 2026).

## Technical accuracy
- RAG definition correct: retrieve relevant chunks, put them in the prompt, answer grounded on them; reduces hallucination, adds new/private knowledge, enables citations — without retraining (b01).
- **Two-phase architecture correct and matches special-check**:
  - Index (offline): documents → chunk → embed each chunk → store in vector DB. Correct, with the right rationale (can't embed a whole book; want the relevant passage) (b03).
  - Query (online): embed question with the *same* embedding model → retrieve top-k → augment (build prompt + grounding + citation) → generate. The retrieve → augment → generate verbs are correct (b04).
- Prompt construction / grounding correct: "answer only from the passages, say 'không đủ thông tin' otherwise, cite passage numbers, wrap passages in delimiters" — correctly inherited from grounding (b06).
- **Debug by isolating retrieval vs generation correct and matches special-check**: retrieval failure = correct chunk not in top-k (fix chunking/embedding/k/hybrid/rerank); generation failure = correct chunk present but model ignores/misreads/hallucinates (fix prompt/citation/noise/model). The decisive tip — *inspect the actually-retrieved chunks first* — is exactly right (b07, b08).

## Quiz / mastery correctness
- b05 (→ a, RAG vs fine-tune for weekly-updated + cited docs; correctly notes RAG *reduces* not *eliminates* hallucination), b09 (→ a, retrieved top-5 all off-topic → retrieval failure), b10 fill (generation) — all correct. Distractors correctly reject "RAG eliminates hallucination entirely", "fine-tune needs a vector DB", and the temperature red herring.
- S289 (L1: definition + two phases), S290 (L2 score-2: correct chunk present → generation failure, plus the inverted case), S291 (L3 interview: draw end-to-end architecture + diagnosis procedure) — correct, rubrics sensible, levels right. S291 maps exactly to `mastery_bar_vi` (build end-to-end, justify design, diagnose to the right layer).

## Coverage discipline
- Mastery items test taught ideas. "lost-in-the-middle" appears only as a parenthetical example of "noise/extra chunks" in S290/S291 answers; the lesson teaches the concept ("giảm nhiễu / bớt đoạn thừa") though not that exact English term. Not required by any rubric — acceptable, not a must-fix.

## Language
- Vietnamese clear; English terms parenthesized (RAG, chunk, embed, vector DB, top-k, retrieve/augment/generate, grounding, citation, hybrid search, rerank, retrieval/generation failure).

## Nice-to-have
- Optional: parenthesize "lost-in-the-middle" where first used in the mastery answers, or drop the term, for consistency with the lesson's wording.
