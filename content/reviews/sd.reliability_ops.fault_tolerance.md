# Review: sd.reliability_ops.fault_tolerance

**Verdict: PASS (clean, ready to publish).** Independent content review, 2026-10-27.

## Technical accuracy & currency
- Six mechanisms correct: timeout (+ deadline propagation), retry (exponential backoff + jitter, idempotent-only), circuit breaker, bulkhead, graceful degradation/fallback, load shedding (+ queue-based load leveling). Cascading-failure framing (thread-pool exhaustion) is accurate.
- Circuit breaker states correct: **Closed** (pass + count errors) → **Open** (threshold exceeded, fail fast / fallback, stop calling) → **Half-open** (probe a few requests, back to Closed if healthy else Open). Correct.
- Bulkhead (per-dependency resource pools) and backoff+jitter (de-synchronize clients) correct.

## Retry-storm arithmetic — RE-CHECKED, correct
- 3 tiers × max 3 retries: amplification 3 × 3 × 3 = **27×**; 1,000 req/s → **27,000 req/s**. Correct.
- Retry budget ~10% → ×1.1 per tier; 1.1 × 1.1 × 1.1 ≈ **1.33×** → ~**1,330 req/s** vs 27,000. Correct (1.1^3 = 1.331).
- b09 quiz answer `a` encodes exactly these numbers; distractor `b` (9× = 2 tiers, budget=0) and `c` (3×, only deepest tier) correctly rejected.

## Quizzes
- b04 (why jitter): answer `a` correct (de-sync spike); correctly notes backoff slows, jitter ≠ timeout replacement.
- b06 (circuit breaker + half-open): answer `a` correct.

## Mastery items
- S160 diff1 recall (name ≥4 of 6 + 3 breaker states) — right level.
- S161 diff2 scenario (payment→recommendation slow 30s: timeout+bulkhead / circuit breaker / fallback) — score-2, rubric sensible.
- S162 diff3 interview (3-tier aggregator: place mechanisms + retry storm 27× by the numbers + retry budget 1.33×) — matches mastery_bar_vi (mechanisms + retry storm by numbers + budget).
- Items test only taught ideas; Vietnamese clear, English parenthesized.

No must-fix items.
