# Review: ml.system_design.rag_assistant

**Verdict: PASS — no must-fix. Technically accurate, currency OK for 2026, ready to publish.**

Reviewer: independent content review (AI-engineer concept track). Date: 2026-10-27.

## Technical accuracy & currency
- Two-stream split: background/async ingest vs online query (seconds). Correct and the right first point.
- Ingest: connector, incremental sync, parse→chunk→embed→index (upsert), update/delete handling (delete vectors by doc_id), dedup by content hash, queue+workers. Correct; freshness ↔ cost tradeoff stated.
- ACL/permission filter AT retrieval time (ACL in chunk metadata, filter by identity/group), not left to the LLM; multi-tenant via per-tenant index vs forced tenant_id filter with tradeoff. Matches checklist exactly.
- Citations + grounding + "I don't know" fallback + guardrails (verify citations real, audit log). Correct; grounding ↔ coverage tradeoff noted.
- Eval split: retrieval (recall@k/hit rate/MRR on golden) vs generation (groundedness/correctness on golden Q&A, human or LLM-judge). Matches checklist.
- Cost: embedding tokens, LLM tokens/query, vector store size — worked estimate 100,000 chunks × 768 dim × 4 bytes ≈ 0.3 GB is arithmetically correct (307.2 MB). Freshness SLA per doc type; cache key must include ACL scope (correct leak warning).

## Quizzes
- b03 (delete vectors by doc_id, ans a), b05 (filter at retrieval, ans a), b07 fill (groundedness/faithfulness), b09 (separate retrieval vs generation eval, ans a): all correct; distractors sound (vector store does not auto-sync; prompt-only ACL leaks).

## Mastery items
- S361 diff1 recall (name the two streams): right level.
- S362 diff2 (multi-tenant + ACL + delete-on-source-delete, why filter > LLM): right level, correct.
- S363 diff3 interview (full production RAG assistant, tradeoff per choice): matches mastery_bar_vi (ingest, ACL, citations, eval, cost, explicit tradeoffs). Rubric aligns (5 pillars + tradeoffs).

## Prior-concept reuse & language
- Explicitly a capstone reusing rag_pipeline, chunking, hybrid_rerank, eval_sets_metrics without re-teaching. Vietnamese clear; English terms parenthesized (ACL, tenant, incremental sync, upsert, groundedness/faithfulness, recall@k).
