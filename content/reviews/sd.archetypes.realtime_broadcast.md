# Review: sd.archetypes.realtime_broadcast

**Verdict: PASS (clean, publishable).** Independent content review, 2026-10-27.

## Technical accuracy & currency
- Archetype framed correctly: one source → millions of read-only viewers on one shared stream; contrasted with many-to-many chat. Core problem = fan-out, not routing.
- Multi-tier fan-out correct: origin/ingest → pub/sub bus per topic → many edge/broadcast servers (each holding tens of thousands of connections, subscribing to the topic, re-fanning to its clients). "CDN for live messages" analogy and "no single machine holds a million connections" are right (connection memory + fd + bandwidth limits).
- Conflation/batching correct: coalesce updates in a ~100–500 ms window, send latest state (score) or batched comments; per-client throttling for slow clients. Sound.
- Snapshot + delta reconnect correct: snapshot of current state with a sequence number K, then contiguous deltas K+1, K+2…; gap detection via sequence jump → request missing or reload snapshot. On reconnect, client sends last seq, server sends deltas or a fresh snapshot if too far behind.
- SSE vs WebSocket correct and current (2026): one-directional → SSE (HTTP, auto-reconnect, Last-Event-ID matches snapshot+delta); WebSocket only when two-way low-latency needed. Hot-topic skew → spread one topic's viewers across many edge servers.

## Special checks (all pass)
- Multi-tier fan-out to millions: present and correct (b02–b04, S256, S258).
- Batching/conflation: present and correct (b05, b06, S257, S258).
- Reconnect via snapshot+delta: present and correct (b07, b08, S258).

## Quiz / check items
- b04, b06, b10 (MCQ), b08 (fill): answers/explanations correct; distractors genuinely wrong (SSE "faster/better binary", send full history, 20×/s to 5M, etc.).
- S256 (diff1 why fan-out tiers), S257 (diff2 score-board conflation + per-client throttling scenario), S258 (diff3 interview matching mastery_bar_vi: multi-tier fan-out + batching + snapshot/delta reconnect, plus SSE/WS and hot-topic skew): correct, level-appropriate, rubrics sensible.

## Reuse of taught concepts
- Reuses realtime protocols/WebSocket/SSE (sd.networking.realtime_protocols) and queues/pub-sub (sd.async.queues_pubsub). Applies, not re-teaches.

## Language
- Vietnamese clear; English terms parenthesized throughout (fan-out tiers, edge servers, pub/sub, conflation/batching, per-client throttling, snapshot, delta, sequence number, SSE, WebSocket, hot topic skew).

No must-fix items.
