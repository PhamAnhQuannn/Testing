# Review: sd.archetypes.rate_limiter

**Verdict: APPROVE** (no must-fix). Reviewer: independent content pass, 2026-10-27.

## Technical accuracy & currency
- Algorithm coverage correct and current: token bucket (allows burst up to capacity, refill rate R), leaky bucket (queues, smooths to fixed output rate), fixed window (simple, boundary-burst leak up to 2x), sliding window log (accurate, memory-heavy), sliding window counter (approximate, light). Tradeoff accuracy-vs-cost stated correctly.
- **Distributed counter verified**: multiple stateless servers counting locally multiplies the limit (~100x); shared counter on Redis via INCR + EXPIRE, or whole token-bucket logic in an atomic Lua script. Correct.
- **Atomicity/race verified**: read-check-increment must be atomic, else two concurrent requests both pass -> race condition. INCR and Lua give atomicity. Correct.
- 429 Too Many Requests + Retry-After + rate-limit headers: correct. Multi-level/per-tenant limits correct.
- fail-open (fair-use, don't let the guard kill the service) vs fail-closed (abuse/DDoS, expensive resources): correct nuance.

## Checks
- Quiz b03 (b, token bucket for burst), b05 (a, fixed-window boundary burst), b07 fill (atomic / race), b10 (b, shared atomic counter) — all answers + explanations correct. Distractor rebuttals accurate (b05 c correctly notes Redis does support atomic ops).
- S172 diff1 recall (token vs leaky): correct; rubric sensible (both halves, burst vs smooth).
- S173 diff2 score-2 scenario (fixed-window ~200 in seconds): answer correct (boundary burst + sliding alternatives with tradeoff); rubric sensible.
- S174 diff3 interview: matches mastery_bar level 3 (multi-server limiter, why atomic, fail-open vs fail-closed). Rubric aligns. Good.

## Pedagogy / language
- Reuses prerequisite (caching.patterns / shared cache, stateless service) by applying, not re-teaching.
- Vietnamese clear; English terms parenthesized consistently.

No corrections required.
