# Review: sd.archetypes.delivery_maps

**Verdict: PASS (clean, publishable).** Independent content review, 2026.

## Technical accuracy & currency
- Order lifecycle correct as a state machine: placed → assigned → picked_up → en_route → delivered; each transition a durably-persisted, idempotent event; only legal transitions allowed. Rationale (legal-transition guard, safe retry/cancel on a stuck step, durable events for notification + reconciliation) accurate.
- Assignment tradeoff correct: nearest-available/single-order (simple, fast per customer, but courier/cost-heavy, many empty miles) vs batching (2-3 orders on one route → cheaper/fewer couriers, but some customers slower + combinatorial route/stop-ordering problem). Delivery-specific prep-time nuance (dispatch to arrive just as food is ready; parallel assign while kitchen cooks) correctly distinguishes from ride-hailing.
- Live tracking correct and matches the spec: live location kept **in-memory (Redis)** because it's high-write and only the latest value matters, then **pushed over WebSocket/SSE** to the specific customer's open connection (no polling). Key architectural split — live state (location, in-memory, pushed) vs durable state (order status, few transitions, DB) — stated clearly.
- ETA additive model (prep + courier-to-restaurant + restaurant-to-customer via routing/traffic) correct and marked dynamic; interview depth appropriate.
- Reuses ride_hailing / geo-index / realtime protocols by reference — no re-teach.

## Quizzes
- b03 (why state machine vs overwritten status column) ans=a ✓; (b) false-by-nature, (c) off-topic geo correctly rejected.
- b05 (nearest vs batching core tradeoff) ans=a ✓; (b) "batching always better" and (c) "differ by protocol" correctly rejected.
- b07 fill (in-memory / push / WebSocket) accept-lists sensible ✓.

## Mastery items
- S271 diff1 recall (5 states in order): correct, right level.
- S272 diff2 score-2 (switch to batching at peak): 3-part answer correct (savings / tradeoff / prep-time); rubric sensible. Right level.
- S273 diff3 interview: order flow/state machine / nearest-vs-batching with when-to-pick + prep-time / live push with live-vs-durable split and explicit reuse of geo-index/ride_hailing/realtime — matches `mastery_bar_vi`. Rubric sensible.

## Language
Vietnamese clear; English terms parenthesized (state machine, nearest-available, batching, prep time, in-memory, push, WebSocket/SSE, ETA).

No must-fix items.
