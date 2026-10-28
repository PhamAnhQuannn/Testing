# Review: sd.archetypes.ads_platform

**Verdict: PASS** (independent content review, 2026). No must-fix. A few optional nits below.

## Technical accuracy
- eCPM = bid × pCTR used consistently for ranking. Worked winner correct: X 2.0×0.05 = **0.1** beats Y 5.0×0.015 = **0.075**; X wins despite lower bid. All arithmetic verified.
- Budget pacing: 240 $/day ≈ 10 $/h correct; "100 $ in 3h = >33 $/h" correct (33.3). Sliced-quota per server framed as distributed token-bucket — accurate reuse of rate_limiter.
- Frequency cap: per-user sliding-window counter; Redis sorted-set ZADD / ZREMRANGEBYSCORE / ZCARD mechanics correct; runs inside latency budget.
- Overspend: spend arrives via delayed (eventually-consistent) stream counter → slight overspend inevitable; hard cap would break ~100 ms latency budget + throughput; reconciliation compensates. Consistency↔latency trade-off correctly stated.

## Quizzes / mastery
- b04 A=0.09/B=0.08/C=0.06 → A. Correct. b06 pacing=a correct. b10 overspend=a correct. b08 fill "frequency cap" correct.
- S211 (diff1 recall): eCPM formula + highest wins — right level.
- S212 (diff2): P=0.1, Q=0.075, P wins + one pacing reason. Math correct, right level.
- S213 (diff3 interview): flow + A=0.08/B=0.10/C=0.09 → B + overspend location. Math correct; matches mastery_bar (flow + budget/freq cap + compute winner + overspend). Rubrics sensible.

## Reuse (no re-teach)
Explicitly builds on stream_processing, rate_limiter, distributed_cache; names them without re-teaching. Good.

## Language
Vietnamese clear; English terms parenthesized (eCPM, pCTR, budget pacing, frequency cap, second-price, reconciliation).

## Optional nits (not blocking)
- b03: strictly "eCPM" is per-mille, i.e. bid×pCTR×**1000**; lesson calls bid×pCTR the eCPM but then correctly notes ×1000 for "per mille", so it is internally consistent and ranking-equivalent. Brief endorses bid×pCTR. Fine.
- Second-price auction is framed as "ý tưởng" (the concept). For 2026 currency, most real display exchanges moved to first-price (~2019, header-bidding). Acceptable as a teaching concept; could add one line noting the first-price shift.
- b08 prompt hint says "3 chữ tiếng Anh" but "frequency cap" is 2 words. Harmless; hint could read "2 chữ".
