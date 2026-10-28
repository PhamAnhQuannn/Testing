# Review: sd.networking.realtime_protocols

**Verdict: OK** (clean — no must-fix)

Independent content review (System Design concept track, Vietnamese, currency target 2026).

## Technical accuracy
- HTTP is request–response (server cannot natively push). Correct framing.
- Short polling (simple, wasteful, latency = poll interval; 1M @ 5s ≈ 200k rps — arithmetic correct) vs long polling (server holds request open until new data; near-instant but one round-trip per message). Correct.
- SSE: single held HTTP connection, server pushes **one-way** (server→client), proxy/firewall friendly, browser auto-reconnect with `Last-Event-ID` for gap backfill; client→server still needs a separate HTTP request. Correct — the special-check SSE characterization is right.
- WebSocket: HTTP upgrade handshake → **full-duplex** long-lived channel, low latency, own protocol (more infra effort), needs heartbeat + reconnect logic. Correct.
- gRPC streaming: HTTP/2, typed (protobuf), server/client/bidirectional; for service-to-service, not browser. Correct (b07 option c correctly rejects direct browser→model gRPC bidi). WebRTC P2P correctly scoped out.
- Protocol picks: feed/notifications → SSE (or long polling for legacy), chat → WebSocket, live score → SSE (WebSocket if client-send later needed), chatbot LLM token stream → SSE with prompt via separate HTTP request. All sound; LLM-token-streaming = SSE one-way is the special-check item, correct.
- Scaling to millions: stateful connection-gateway tier + connection map, pub/sub (Redis/Kafka) fan-out across gateways, sticky routing via L4 LB with least-connections (not RR, because long-lived), heartbeat + reconnect-with-backoff + last-event-id, backpressure when client slower than server, per-node connection cap (fd/port/RAM), APNs/FCM when app closed. Sound. ~100k conns/machine → 1M ≈ 10 machines: reasonable interview rule-of-thumb, arithmetic correct.

## Quiz / mastery correctness
- b05 (→ a, SSE one-way vs WS full-duplex), b07 (→ b, SSE for LLM token stream), b09 (→ b, pub/sub fan-out between gateways) — all answers and explanations correct.
- S097 (L1 recall: 4 methods one/two-way), S098 (L2 score-2: chatbot → SSE, why not WS, prompt via HTTP), S099 (L3 interview: 4 protocol picks + scale to millions). Levels correct; rubrics sensible and leveled, matching mastery_bar_vi.

## Coverage discipline
- Mastery items test only taught ideas. Good.

## Language
- Vietnamese clear; English terms parenthesized consistently.
