# Review: ml.system_design.ml_inference_platform

**Verdict: PASS — no must-fix. Technically accurate, currency OK for 2026, capacity math verified, ready to publish.**

Reviewer: independent content review (AI-engineer concept track). Date: 2026-10-27.

## Technical accuracy & currency
- Sync vs async+queue+job_id+metadata DB; model registry + versioning (artifact store + cache near GPU, promote/rollback via production pointer, canary/A-B/shadow). Matches checklist.
- Scheduler + continuous/in-flight batching (vLLM/TGI) + KV cache + streaming + cancel for LLM; dynamic batching with ms cap for others; backpressure (429) + tier priority (no unbounded queue). Correct and current.
- Autoscale on queue depth / GPU utilization / pending tokens, NOT CPU (correct rationale: GPU saturated while CPU idle). Cold start = weight load → warm pool / model caching; scale-to-zero only for latency-tolerant models. Correct.
- Multi-tenancy: isolation + quota + fairness, per-tier SLO (p99, availability), routing. Observability per model/tenant + reliability (health check, bounded retry, fallback, fleet-wide backoff + jitter). Correct.

## Capacity example (recomputed — all correct)
- 20 req/s × 500 tok = **10,000 tok/s**.
- 10,000 ÷ 200 tok/s/GPU = **50 GPU** at 100% util.
- 50 ÷ 0.7 ≈ 71.4 → **~72 GPU** at 70% target (+ failure headroom).
- 72 × $2/hr = **$144/hr**. Peak 20×3600 = 72,000 req/hr → 144/72,000 = **$0.002/req**.
- "~3× cost/req at ~30% avg load" checks out: 0.3×72,000 = 21,600 req/hr → 144/21,600 ≈ $0.0067 ≈ 3.3× of $0.002.
- Fill b10 (10,000 ÷ 200 = 50) correct.

## Quizzes
- b03 (shadow traffic, ans a), b06 (cold start, ans a), b09 fill (50), b11 (backpressure batch tier + autoscale, ans a): all correct; distractors sound (canary still affects users; FIFO under overload is wrong).

## Mastery items
- S367 diff1 recall (3 rollout methods, safest, rollback mechanism): right level.
- S368 diff2 (overload tier contention + cold start + why not CPU): right level, correct.
- S369 diff3 interview (full platform + numeric capacity/cost + cost levers): matches mastery_bar_vi (batching, queue, autoscaling, versioning, SLO, capacity + cost by numbers). Rubric aligns and re-states the correct numbers.

## Prior-concept reuse & language
- Capstone reusing batching_scheduling, cost_latency_design, deployment_patterns, sd_eng_minimum without re-teaching. Vietnamese clear; English terms parenthesized (continuous batching, KV cache, shadow traffic, cold start, warm pool, backpressure, SLO, jitter).
