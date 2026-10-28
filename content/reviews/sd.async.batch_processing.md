# Review: sd.async.batch_processing

**Verdict: PASS (clean).** Independent content review, 2026-10-27.

## Technical accuracy & currency (2026)
- Batch vs stream correct: bounded data, one pass, usually scheduled, minutes-to-hours latency; batch sufficient and cheaper when no real-time need (daily report, recompute, model retraining). Accurate.
- MapReduce via word count correct:
  - Map: each machine reads its own shard, emits (key, value); `a b a` → (a,1)(b,1)(a,1); fully parallel/local. Correct.
  - Shuffle: gather all pairs with same key to one reduce machine (a → [1,1], b → [1]); moves data over network → most expensive phase. Correct.
  - Reduce: merge per key; word count = sum; a=2, b=1. Correct.
- Data skew correct: hot key (stop word "the", celebrity id, null key) → one reducer becomes straggler; whole job waits. Fixes: combiner/pre-aggregation (send "the→1000000" once), salting hot key (the_0..the_9) across reducers + two-stage aggregation. Correct and complete.
- Re-runnable/idempotent job correct: write to new output dir + atomic swap on full completion (failed run leaves temp garbage, doesn't touch live output); overwrite by date/partition not append; deterministic output so re-run replaces, not accumulates → no double-count. Accurate.
- Spark framing accurate (in-memory, lazy/lazy evaluation); correctly framed as an implementation of the model, not the point.

## SPECIAL checks
- map/shuffle/reduce via word count correct: verified above.
- data skew + fixes (combiner/salting/two-stage): correct.
- re-runnable/idempotent job: correct (atomic swap + deterministic output + overwrite not append).

## Quizzes
- b04 (most expensive phase): answer `b` (shuffle, network) correct; (a) each machine reads only its shard, (c) sum is cheap — accurate.
- b06 (celebrity hot key fix): answer `a` (salt + two-stage) correct; (b) more RAM still one straggler, (c) dropping shuffle breaks the computation — accurate.
- b08 fill (idempotent / atomic swap): both correct, accept lists generous and reasonable.

## Mastery items vs bar
Bar: "giải thích map, shuffle, reduce bằng ví dụ đếm từ, nêu cách xử lý data skew và làm job chạy lại được."
- S127 (diff1 recall): three phases in order + word count. Correct.
- S128 (diff2 score-2 scenario): one reducer hot → name data skew + two fixes. Correct; rubric rejects "just add RAM/machines".
- S129 (diff3 interview): full 1 TB word count (map/shuffle/reduce + expensive phase, data skew, re-runnable). Matches bar exactly.
- All items test taught ideas. 

## Language
Vietnamese clear; English terms parenthesized (batch, MapReduce, map/shuffle/reduce, word count, data skew, hot key, straggler, combiner, pre-aggregation, salting, two-stage aggregation, atomic swap, deterministic, idempotent).

No must-fix issues.
