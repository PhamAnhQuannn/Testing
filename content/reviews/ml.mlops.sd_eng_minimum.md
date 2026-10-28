# Review: ml.mlops.sd_eng_minimum

**Verdict: PASS — no must-fix. Technically accurate, QPS arithmetic verified, ready to publish.**

Reviewer: independent content review (AI-engineer concept track). Date: 2026-10-27.

## Technical accuracy & currency
- Plain-language glossary as intended: QPS (load), p50/p95/p99 (tail), SLO vs SLA, queue+worker (producer/consumer, smooth spikes, background job id + polling/webhook), Docker/container (Dockerfile/image/container distinction), CI/CD. All definitions correct and current.
- SLO vs SLA distinction correct (internal measurable objective vs external contractual commitment, SLA looser for safety margin).
- Availability note: 99.9%/month ≈ ~43 min downtime — correct (0.001 × 43,200 min = 43.2).
- p95 example: 20 sorted values, nearest-rank p95 = 19th value = 800 ms, average ~203 ms pulled up by tail — arithmetically sound.

## QPS-from-daily arithmetic (recomputed — all correct, ÷86,400 + peak factor)
- b02: 1,000,000 ÷ 86,400 ≈ **11.6/s**; ×5 peak ≈ **58/s**. Correct.
- b03: 4,320,000 ÷ 86,400 = **50/s**. Correct (distractor c = ÷1,440 min = req/min, correctly flagged).
- Fill b10: 86,400 (24×3600). Correct.
- S374: 2,000,000 ÷ 86,400 ≈ **23/s**; ×4 ≈ **92/s**. Correct.
- S375: 8,640,000 ÷ 86,400 = **100/s**; ×3 = **300/s**. Correct.

## Quizzes
- b03 (50/s, ans a), b05 (p95 meaning, ans a), b10 fill (86,400), b11 (SLO vs SLA, ans a): all correct; distractors sound (per-ms/per-minute confusion, average vs percentile).

## Mastery items
- S373 diff1 recall (QPS + p95 in plain words): right level.
- S374 diff2 (estimate avg+peak QPS for 2M/day ×4 + write an SLO, SLO vs SLA): right level, correct.
- S375 diff3 interview (explain all six terms + estimate QPS for 8.64M/day ×3): matches mastery_bar_vi ("giải thích bằng lời thường QPS, p95, SLO, queue, Docker, CI/CD và làm được phép ước lượng QPS từ số lượt dùng mỗi ngày"). Rubric aligns.

## Prior-concept reuse & language
- Positioned as prerequisite glossary for later MLOps/system-design topics; does not over-teach. Vietnamese clear; English terms parenthesized (QPS, latency percentile, SLO/SLA, queue/producer/consumer, Dockerfile/image/container, CI/CD).
