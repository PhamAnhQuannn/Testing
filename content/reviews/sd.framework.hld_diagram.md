# Review: sd.framework.hld_diagram (independent reviewer pass)

**Verdict: OK** (no must-fix)

12 blocks; graded: b04 (mcq), b07 (mcq), b08 (fill), b10 (mcq). mastery_check l1[S037] l2[S038] l3[S039].
mastery_bar_vi: "vẽ sơ đồ sạch, kể đường đọc và đường ghi, nói được lý do của từng hộp" — S039 matches.

## Technical accuracy
- Standard box set in request order: client → DNS/CDN → LB → stateless service tier → cache → DB/read replica → queue+worker → blob store. Correct and current.
- Write path: client → LB → service → **primary** (async work to queue; large files to blob store, DB keeps path). Correct.
- Read path: client → (CDN static) → LB → service → cache → (miss) read replica, then populate cache (cache-aside). Correct.
- "Start simple (client→service→DB), add a box only when a requirement demands it" — correct design discipline, explicitly chained to sd.fundamentals.scalability's 5-step roadmap.

## Quiz / mastery correctness
- b04 [b] start simple then grow — correct; (a) draw-everything and (c) shard-first correctly refuted.
- b07 [a] miss → read replica + write-back to cache — correct; (b) "miss=error" and (c) "LB reads" refuted.
- b08 fill: load balancer / primary / blob store — correct.
- b10 [b] queue = push slow work async — correct; (a) "everyone has one" and (c) "replaces DB" refuted.
- S037 (L1): box order + CDN/blob roles; rubric accepts core spine. Good.
- S038 (L2 gate): post-with-image — write path to primary + blob, read path with hit/miss, one box to drop when small. Correct.
- S039 (L3): URL shortener — clean diagram, both paths with hit/miss, per-box justification, drop boxes at low load. Matches bar.

## Consistency
Step 5 of the pipeline; explicitly builds on scalability (stateless, LB, replica, write-to-primary bottleneck). Write-to-primary framing handed forward to deep_dive_tradeoffs (bottleneck). Box vocabulary reused consistently.

## Language
Vietnamese clear; English terms parenthesized (HLD, stateless, load balancer, read replica, primary, queue/worker, blob/object store, CDN, cache miss/hit). Good.
