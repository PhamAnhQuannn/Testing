# Review: sd.networking.reverse_proxy_gateway

**Verdict: OK** (clean — no must-fix)

Independent content review (System Design concept track, Vietnamese, currency target 2026).

## Technical accuracy
- Forward proxy (in front of client) vs reverse proxy (in front of server, hides backend). Correct.
- Reverse proxy duties: terminate client connection + TLS termination, serve static/cache, hide/protect backend, connection pooling, compression. Correct (nginx, Envoy, HAProxy).
- API gateway = reverse proxy specialized for API + application-layer policy: authN/authZ, rate limiting, routing/aggregation, versioning, observability. Correct.
- Edge placement rationale: auth/rate-limit/routing are cross-cutting concerns → do once at edge (consistency, no duplication across services, early rejection before backend cost). Correct. "Do not put business logic in gateway" correctly stated.
- Fat gateway risk: bottleneck / SPOF / deployment chokepoint — all three correct and well explained (gateway on every request path).
- Scaling: keep stateless → horizontal (multiple instances behind an LB) + keep logic thin. Correct.
- LB vs gateway distinction correct: LB distributes/health-checks (content-blind); gateway adds app-layer policy (content-aware); real-world stacking LB → stateless gateway instances. Correct.

## Quiz / mastery correctness
- b03 (→ b, gateway = RP + API policy), b05 (→ b, auth/rate-limit at edge gateway), b07 (→ a, fat gateway danger + stateless/thin/scale-out) — all correct.
- S091 (L1 recall: RP vs gateway), S092 (L2 score-2: where to put auth/rate-limit for 20 services + no business logic), S093 (L3 interview: placement + why + fat-gateway risk + scale + LB-vs-gateway). Levels correct; rubrics sensible and leveled, matching mastery_bar_vi.

## Coverage discipline
- Mastery items test only taught ideas (BFF pattern / ingress controller in key_concepts untested — fine). Good.

## Language
- Vietnamese clear; English terms parenthesized consistently.
