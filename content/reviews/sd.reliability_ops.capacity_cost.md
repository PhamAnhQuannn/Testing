# Review: sd.reliability_ops.capacity_cost

**Verdict: PASS (clean, ready to publish).** Independent content review, 2026-10-27.

## Technical accuracy & currency
- Size-by-peak (not average), headroom (target ~60-70% per node at peak for failover absorption / spike buffer / stable p99), and N+1/N+2 redundancy — all correct and well separated (headroom = load, N+k = spare machine count).
- Autoscaling signals correct and mapped to the real bottleneck: CPU% (compute, lags on I/O), QPS/RPS (web/API), queue depth / consumer lag (background workers — best signal), p99 latency (user-facing). Reactive vs scheduled/predictive, and cold-start/warm-up justifying headroom + pre-warm — correct.
- Three+ concrete cost levers given: tiered/lifecycle storage, compression, CDN/cache to cut egress, reserved/spot, retention/TTL. Valid.

## Machine-count arithmetic — RE-CHECKED, all correct
- Lesson b03: 1,000 × 0.70 = 700; 30,000 ÷ 700 = 42.86 → round **up 43**; N+1 → **44**. Alt path 30,000÷1,000÷0.70 = 42.86 → 43 → 44. Correct.
- b04 quiz: 500 × 0.80 = 400; 20,000 ÷ 400 = **50** (exact); N+1 → **51**. Answer `b` correct; `a` (no headroom/redundancy) and `c` (forgot +1) correctly rejected.
- S167: 500 × 0.60 = 300; 20,000 ÷ 300 = 66.67 → **67**; N+1 → **68**. Correct.
- S168: 1,000 × 0.70 = 700; 50,000 ÷ 700 = 71.43 → **72**; N+2 → **74**. Correct.
- b09 fill (CDN / egress) correct.

## Mastery items
- S166 diff1 recall (peak vs average + what headroom is / why ~60-70%) — right level.
- S167 diff2 scenario (compute 68 machines + autoscaling signal + why act ahead of load) — score-2, rubric sensible (demands round-up and +1).
- S168 diff3 interview (compute 74 machines + signal at bottleneck + 3 concrete cost cuts) — matches mastery_bar_vi (machine count with headroom + autoscaling signal + 3 cost levers).
- Items test only taught ideas; Vietnamese clear, English parenthesized.

No must-fix items.
