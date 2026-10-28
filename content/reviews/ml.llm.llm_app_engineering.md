# Review: ml.llm.llm_app_engineering

**Verdict: OK** (clean — no must-fix)

Independent content review (AI-engineer / LLM concept track, currency target 2026).

## Technical accuracy
- LLM call = web API: messages (system/user/assistant) + params (model, temperature, max_tokens) + `usage` (input/output tokens). Correct (b01).
- Streaming via SSE and TTFT correct: streaming lowers TTFT and improves *perceived* latency but does NOT shorten total time or reduce cost — total latency scales with output tokens. Accurately stated (b02, b04, b11 fill). Matches special-check requirement.
- Per-token cost correct: `cost = in×price_in + out×price_out`, output priced higher, reasoning tokens billed as output. Worked example verified: 1000 req × (500 in + 300 out), $1/M in + $5/M out → $0.50 + $1.50 = $2/day ≈ $60/mo. Arithmetic correct (b05).
- Cost levers correct: prompt caching, context trimming, max_tokens, model routing (small model for easy tasks), response/semantic cache with the semantic-cache risk noted (b06).
- Reliability correct: timeout; retry with exponential backoff + jitter on 429/5xx; do NOT retry 400/401; cap retries; fallback; graceful degradation; respect Retry-After and RPM/TPM; batch / bounded concurrency for bulk jobs (b08, b09, b10). Matches special-check requirement.
- Observability (log tokens/cost/latency/errors/retries + trace) correct (b12).

## Quiz / mastery correctness
- b04 (→ a), b07 (→ a, small model + low max_tokens + prompt caching), b10 (→ a, retry 429/5xx with backoff+jitter, not 400/401), b11 fill (TTFT) — all correct. Distractors correctly reject "temperature shortens output", "retry everything forever", "switch to the biggest model".
- S277 (L1), S278 (L2 score-2: cost reduction + error handling + hide raw error), S279 (L3 interview: five facets, chat vs bulk) — correct, rubrics sensible, levels right. S279 covers the full `mastery_bar_vi` (streaming, retry+backoff, caching, 429/timeout, token cost).

## Coverage discipline
- Mastery items test only taught ideas. Good.

## Language
- Vietnamese clear; English terms parenthesized (SSE, TTFT, backoff, jitter, quota, Batch API).

## Nice-to-have
- None material.
