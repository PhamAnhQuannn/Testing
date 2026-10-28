# Review: sd.networking.service_discovery_mesh

**Verdict: OK** (clean — no must-fix)

Independent content review (System Design concept track, Vietnamese, currency target 2026).

## Technical accuracy
- Problem framing: dynamic infra (autoscaling, containers rescheduled, instances die/respawn with new IPs) makes hardcoded addresses stale → need discovery. Correct.
- Service registry: instance self-registers, sends heartbeat, TTL expiry → deregister; registry holds only healthy instances. Consul/etcd (Eureka/ZooKeeper legacy), Kubernetes built-in Service DNS (`*.svc.cluster.local`). Correct. DNS-TTL client-cache pitfall (stale address until cache expiry) correctly noted.
- Client-side discovery: client queries registry and self load-balances, calls instance directly → fewer hops, but discovery/LB logic lives in client (per-language library, hard for polyglot); gRPC client-side LB as the example. Correct.
- Server-side discovery: client calls one fixed address (LB/gateway/DNS), that component queries registry and forwards → simple client (polyglot-friendly) but adds a hop and the LB itself must scale/be HA; Kubernetes Service is server-side. Correct.
- Service mesh: sidecar proxy (Envoy) beside each service; path `[A] → [sidecar A] ══ net ══ [sidecar B] → [B]`. Correct sidecar placement. Sidecars = data plane, control plane pushes config. mTLS correctly defined as two-way cert (encrypt + mutual identity). retries/timeout/circuit-breaking/traffic-splitting/observability correct.
- Mesh latency: each call crosses two proxy hops (out of caller sidecar, into callee sidecar), adds ms, compounds over long call chains — the special-check item, correct.
- When mesh is worth it: overkill at ~5 services/one language (shared library suffices); worth it at tens–hundreds of services + polyglot. Sound.

## Quiz / mastery correctness
- b03 (→ b, addresses change in dynamic fleet), b05 (→ a, client/server-side tradeoff), b07 fill (sidecar / mTLS), b10 (→ b, mesh overkill at 5 services, adds latency) — all correct. b10 explanation correctly rebuts "mesh makes calls faster".
- S094 (L1 recall), S095 (L2 score-2: client vs server-side + polyglot), S096 (L3 interview: compare + draw sidecar + when worth it + where latency). Levels correct; rubrics sensible, matching mastery_bar_vi.

## Coverage discipline
- Mastery items test only taught ideas. Good.

## Language
- Vietnamese clear; English terms parenthesized consistently.
