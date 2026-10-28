# Review: sd.archetypes.coordination_primitives (Snowflake)

**Verdict: APPROVE** (no must-fix). Reviewer: independent content pass, 2026-10-27.

## Bit-layout math (verified)
- 1 (sign) + 41 (timestamp ms) + 10 (machine) + 12 (sequence) = **64 bits** ✓ (lesson b03, summary, S193 all consistent).
- 2^12 = **4096** ids/ms/node ✓ (and ~4,096,000 ids/s/node ✓: 4096 × 1000).
- 2^10 = **1024** machines ✓.
- 2^41 ms ≈ **69 years** ✓ (2^41 ms = 2.199e12 ms ≈ 69.7 yr).
All numbers correct in lesson (b03, b04, b10, b11), checks (S193–S195). No discrepancies.

## Technical accuracy & currency
- k-sortable rationale correct: time in high bits -> index-friendly (sequential B-tree inserts) vs random UUIDv4. Explanation of "approximate" ordering across nodes within a ms is accurate.
- Clock-rollback handling correct: track max timestamp emitted; if wall clock < max, refuse or wait. Correctly notes sequence cannot rescue a rolled-back ms (same machine_id + reused sequence -> collision).
- Sequence overflow: busy-wait to next ms, reset to 0 — correct.
- Machine-id assignment via ZooKeeper/etcd at startup, single coordination point — correct and current.
- Comparison vs UUIDv4 (128-bit random, index-unfriendly), UUIDv7 (128-bit, timestamp-prefixed, k-sortable — current per RFC 9562), DB auto-increment (bottleneck/SPOF), ticket/range server (block allocation, gaps on crash): all accurate and 2026-current.

## Checks
- b04 fill (4096 / 1024), b07 (b), b09 (c) — answers + explanations correct.
- S193 diff1 recall (four fields, order, widths): correct, rubric sensible.
- S194 diff2 score-2 (clock rollback + why sequence fails): correct, rubric sensible.
- S195 diff3 interview (100k/s on 50 machines, PK use, full justification): matches mastery_bar (assemble Snowflake, per-bit capacity, clock rollback + machine-id assignment). Capacity sanity (50 machines >> needed, 4096/ms headroom) correct. Rubric aligns.

## Pedagogy / language
- Builds on sd.distributed.time_ordering without re-teaching.
- Vietnamese clear; English terms parenthesized.

No corrections required.
