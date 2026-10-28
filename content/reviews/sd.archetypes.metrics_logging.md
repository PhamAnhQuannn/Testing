# Review: sd.archetypes.metrics_logging

**Verdict: PASS** (independent content review, 2026). No must-fix.

## Technical accuracy
- Three observability pillars correct: metrics (cheap time-series numbers → dashboards/alerts, "is something wrong?"), logs (searchable text events, expensive/indexed, "what happened?"), traces (one request across services, "which hop is slow?"). Accurate.
- Collection path: per-server agent (push or pull) → buffer pipeline (Kafka) to absorb spikes + decouple producers from stores → split: metrics → time-series DB, logs → indexed/search store. Correct reuse of data_pipeline + kafka_log.
- **Cardinality**: each label combination = one series the TSDB indexes in RAM; a high-cardinality label (user_id, request_id) explodes series count → RAM exhaustion/slowdown; rule = only low-cardinality labels, per-user data belongs in logs/analytics. Correct (same "too-high-selectivity key" idea as analytics_storage).
- Rollup/downsampling + tiered retention (hot/warm/cold → delete) correctly paired and explained.
- Alerting: symptom-based + SLO burn-rate, dedup, one action per alert, avoid alert fatigue. Correct, current best practice.

## Quizzes / mastery
- b03 dashboard source = b (metrics) correct; b05 user_id label = b correct (a "TSDB can't store strings" false, c "max 2 labels" false — good distractors); b07 fill downsampling/rollup + tầng(tiered) correct; b09 3am page = b correct.
- S205 (diff1): name 3 pillars — recall, right level.
- S206 (diff2): explain cardinality blow-up + fix + a retention technique. Right level.
- S207 (diff3 interview): 5000 servers, 100 metrics/10s, 30-day retention. Sizing **50,000 points/sec** correct (5000×100/10). Collection + cardinality + rollup/tiered + alerting. Matches mastery_bar. Rubrics sensible.

## Reuse (no re-teach)
References data_pipeline, kafka_log, analytics_storage by name without re-teaching. Good.

## Language
Clear Vietnamese; English terms parenthesized (observability, cardinality, downsampling, tiered retention, SLO burn, alert fatigue, dedup). No issues.
