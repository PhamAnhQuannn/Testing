# Review: ml.system_design.llm_product_design

**Verdict: PASS — no must-fix. Technically accurate, currency OK for 2026, ready to publish.**

Reviewer: independent content review (AI-engineer concept track). Date: 2026-10-27.

## Technical accuracy & currency
- Pipeline order requirements → adaptation choice (prompt/RAG/fine-tune, API/self-host) → eval → safety → serving. Matches checklist.
- Safety includes lethal trifecta stated correctly: (1) untrusted content, (2) access to private data/secrets, (3) exfiltration channel; defense = break at least one leg. Correct and current.
- Streaming via SSE (one-way, reconnect), WebSocket when bidirectional; TTFT metric. Correct — streaming improves perceived latency, not completion time (explicitly, correctly stated).
- Core tradeoff latency ↔ GPU/cost ↔ quality with model routing. Matches checklist.

## Worked numbers (recomputed)
- Cost: $5/1M input + $15/1M output; 2k in + 500 out = 2000/1e6×5 + 500/1e6×15 = $0.010 + $0.0075 = **$0.0175 ≈ $0.018**. Correct.
- GPU: need 10,000 tok/s, 2,000 tok/s/GPU → **5 GPU**. Correct. Fill b11 (throughput per GPU) correct.

## Quizzes
- b04 (RAG for weekly-changing policy, ans a), b08 (lethal trifecta, break a leg, ans a), b11 fill (throughput per GPU): all correct; distractors sound (weekly fine-tune wasteful; prompt-only injection defense insufficient).

## Mastery items
- S364 diff1 recall (step order + streaming/SSE role): right level.
- S365 diff2 (support chatbot: RAG+API, grounding, one guardrail): right level, correct.
- S366 diff3 interview (coding assistant end-to-end with numbers + latency↔GPU↔quality tradeoff + rollout): matches mastery_bar_vi. Rubric aligns.

## Prior-concept reuse & language
- Capstone reusing prompt engineering, RAG/agent, eval/serving, guardrails, cost/latency without re-teaching. Vietnamese clear; English terms parenthesized (RAG, fine-tune, SSE, TTFT, lethal trifecta, canary/A-B, model routing).
