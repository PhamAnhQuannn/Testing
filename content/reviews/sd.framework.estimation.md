# Review: sd.framework.estimation (independent reviewer pass)

**Verdict: OK with 1 must-fix (coverage leak in S033 rubric)** — all arithmetic verified correct.

11 blocks; graded: b03 (fill), b05 (mcq), b09 (mcq). mastery_check l1[S031] l2[S032] l3[S033].
mastery_bar_vi: "trong 3 phút tính QPS, dung lượng, băng thông, làm tròn, nói quyết định (cache/shard/CDN)" — S033 matches.

## Arithmetic — every claim re-checked (all correct)
Constants: day ≈ 86,400 ≈ 10^5 s (stated error ~15% is accurate: 10^5/86400 = 1.157); KB/MB/GB/TB/PB = 10^3/10^6/10^9/10^12/10^15. All good.
- b02: 10^7 writes/day ÷ 10^5 = **100 w/s**, peak x3 = 300; reads 100x = 10^9/day ÷ 10^5 = **10,000 r/s**, peak 30,000. ✓
- b03 fill: 2×10^7 ÷ 10^5 = **200 w/s** (peak x3 = 600). ✓
- b04/b05 storage: 10^7 × 500 B = 5×10^9 B = **5 GB/day**; ×365 = 1,825 GB ≈ **1.8 TB/yr**; ×3 = **5.4 TB**. ✓ (365≈400 → ~2 TB also fine)
- b06 bandwidth: 30,000 × 500 B = 1.5×10^7 B/s = **15 MB/s** = **120 Mb/s** (×8). 2 MB image → GB/s. ✓
- S031: 86,400 ≈ 10^5; QPS avg = ops/day ÷ 10^5; peak = avg × (2-5). ✓
- S032: 2×10^7 × 40 = 8×10^8; ÷10^5 = **8,000 w/s**; ×4 = **32,000 w/s**; "large for single DB" correct. ✓
- S033: writes 5×10^7 ÷ 10^5 = **500 w/s** (peak 1,500); reads 10x → avg **5,000**, peak **15,000 r/s**. Storage 5×10^7 × 2 MB = 10^8 MB = **100 TB/day**; ×1,825 days = 182,500 TB = **~180 PB** (x1), **~540 PB** (x3; exact 547.5, rounded down — within one-sig-fig tolerance). Bandwidth 15,000 × 2 MB = 30,000 MB/s = **30 GB/s**. ✓ All units correct (KB/MB/GB/TB/PB, seconds/day).

## Quiz / mastery correctness
- b03=200 ✓; b05 [a] 1.8 TB (b forgets ×days, c confuses TB/PB — both correctly refuted) ✓; b09 [a] cache yes / shard no at ~1.8 TB ✓.
- S031 (L1), S032 (L2 gate), S033 (L3) answers all correct; rubrics sensible and quantitative.

## Coverage discipline — MUST-FIX
S033 rubric requires "**object storage** + sharding (hàng trăm PB) và CDN" to reach mark-3, but **object storage / blob store is NOT taught in this estimation lesson** — b08's decision framework teaches only cache / shard / CDN. (Blob/object store is introduced later in sd.framework.hld_diagram, which comes *after* estimation in the pipeline.) Requiring an untaught concept to pass the L3 gate violates coverage discipline. Fix below.

## Consistency
Numbers reuse requirements' DAU/read-heavy inputs; cache/shard/CDN decisions feed hld_diagram and deep_dive. 10^5-second and x2-5 peak conventions consistent across all items.

## Language
Vietnamese clear; English terms parenthesized (back-of-envelope, QPS, DAU, egress, CDN). Good.

## Findings
- **must-fix:** S033 — make "object storage" a bonus, not a mark-3 requirement (keep sharding + CDN + cache, which the lesson teaches), OR the lesson b08 should add one line that huge binary payloads go to blob/object store.
