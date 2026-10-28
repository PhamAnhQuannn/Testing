# Review: sd.archetypes.chat_presence

**Verdict: APPROVE** (no must-fix). Reviewer: independent content pass, 2026-10-27.

## Technical accuracy & currency
- **WebSocket gateways + pub/sub fanout verified**: stateful connection gateways, Redis routing/session registry (user -> gateway/connections), gateways bridged by a pub/sub backbone (Redis Pub/Sub, or Kafka when durability/replay needed); publish to recipient's channel, only the holding gateway delivers. Correct and current.
- **Per-conversation ordering verified**: per-conversation monotonic sequence number for total order (not clock timestamps, due to clock skew); used for ordering, gap detection, and resync. Correct. Receipts sent/delivered/read correct.
- Storage: durable message store, NoSQL sharded by conversation_id — correct. Offline -> message already stored -> push (APNs/FCM); on reconnect client sends its seq, server syncs seq > X. Correct.
- **Presence heartbeat+TTL verified**: refresh `online:U` key with short TTL; missed heartbeat -> key expires -> offline (no cooperation from a crashed client). Correct, incl. presence latency ~TTL caveat. Thundering-herd on large friend lists + mitigation (push only to open chats / client pulls / batch + throttle) correct.
- **write vs read fanout verified**: 1:1 + small groups -> write-fanout (fast reads); very large / sparse-read groups -> read-fanout (one copy, fan out on read); hybrid in practice. Correct.

## Checks
- Quiz b03 (b, G1 can't deliver to Bob on G2), b06 fill (sequence number), b09 (b, TTL vs explicit offline), b10 (b, read-fanout for large groups) — all answers + explanations correct.
- S181 diff1 recall (gateway stateful + routing registry): correct; rubric sensible.
- S182 diff2 score-2 scenario (A on G1 -> B on G2): answer correct (routing + backbone, durable + seq, offline push); rubric sensible.
- S183 diff3 interview: matches mastery_bar level 3 (cross-gateway delivery, storage, sequencing, online/offline, offline resync). Rubric aligns. Good.

## Pedagogy / language
- Reuses prerequisites (realtime_protocols, queues_pubsub, sql_vs_nosql) by applying, not re-teaching.
- Vietnamese clear; English terms parenthesized consistently.

No corrections required.
