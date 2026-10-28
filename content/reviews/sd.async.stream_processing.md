# Review: sd.async.stream_processing

**Verdict: PASS (clean).** Independent content review, 2026-10-27.

## Technical accuracy & currency (2026)
- Stream (continuous, low-latency) vs batch (bounded, high-throughput) distinction correct; when batch suffices (no low-latency need, or large historical recompute/backfill) stated correctly.
- event time vs processing time correct, with the 10:00:59 / 10:01:03 example; counting by event time is right. Late event defined correctly.
- Windowing correct: tumbling (fixed, non-overlapping), sliding (fixed length, small step, event in multiple windows), session (gap-based, variable length).
- Watermark correct: "all events with event time < T assumed arrived"; = max-seen-event-time − allowed lateness; closes window when it passes window end; large margin = more accurate but later, small = faster but misses stragglers; late-after-watermark dropped or to side output. Accurate.
- Checkpoint correct: consistent snapshot of state + Kafka offset; restore reloads state and replays from offset; replay → idempotent sink (upsert by [window, id]) → exactly-once at sink. Correct.
- Tooling (Flink / Spark Structured Streaming micro-batch / Kafka Streams) described accurately and currently; correctly framed as secondary to concepts.

## SPECIAL checks
- windowing, event vs processing time, watermark for late events, checkpoint recovery, idempotent sink, when batch suffices: all present and correct.

## Quizzes
- b04 (top-10 over last 1h updated each min): answer `b` (sliding 1h/1min) correct; tumbling/session rebuttals accurate.
- b06 (watermark purpose): answer `b` correct; (a) not processing-time sort, (c) that's checkpoint — accurate.
- b08 fill (checkpoint / idempotent): both correct, accept lists reasonable.

## Mastery items vs bar
Bar: "thiết kế pipeline đếm theo window, xử lý sự kiện muộn bằng watermark, khôi phục bằng checkpoint, ghi idempotent và biết khi nào chỉ cần batch."
- S118 (diff1 recall): stream vs batch + event/processing time + 3 windows. Correct.
- S119 (diff2 score-2 scenario): tumbling 1-min by event time, 10:00 via watermark, idempotent for replay. Correct; rubric sensible.
- S120 (diff3 interview): full 6-part pipeline (Kafka+event time, window, watermark+trade-off, checkpoint, idempotent sink, when-batch). Matches bar exactly.
- Side output (S120) is taught in b05; all items test taught ideas. 

## Language
Vietnamese clear; English terms parenthesized (low latency, bounded, event/processing time, late event, tumbling/sliding/session window, watermark, checkpoint, idempotent, side output, sink).

No must-fix issues.
