# Review: sd.networking.load_balancing

**Verdict: OK** (clean — no must-fix)

Independent content review (System Design concept track, Vietnamese, currency target 2026).

## Technical accuracy
- L4 (transport, TCP/UDP, no content inspection, fast, "blind") vs L7 (application, reads URL/header/cookie, path routing, TLS termination, higher CPU). Characterization correct, tradeoff stated correctly.
- Algorithms: round robin / weighted (even, homogeneous servers), least connections (uneven request duration or long-lived connections), IP hash / consistent hash (affinity, cache locality, sticky). All correct; consistent hash correctly noted to limit reshuffle on membership change.
- Long-lived connections → least connections, NOT round robin: correct and well-justified (true load = open-connection count; RR counts only "turns dealt", so machines bloat over time). This is the key special check — sound.
- Sticky session: correctly flagged as causing skew + session loss on node death; cleaner fix = externalize session to shared store (stateless). Correct.
- Health checks: active (periodic `/health` probe, early detection, probe traffic cost) vs passive (observe real traffic errors, no probe cost but reactive); combine both. Correct.
- LB-as-SPOF mitigations: active–passive with floating IP/VIP via VRRP + failover; active–active via anycast/ECMP or DNS (multi-IP, drop dead IP); GSLB for multi-region. All correct.

## Quiz / mastery correctness
- b03 (→ b, L7 for path routing + TLS termination), b05 (→ b, least connections for long-lived WS), b07 fill (active / passive) — all answers and explanations correct.
- S088 (L1 recall: L4 vs L7), S089 (L2 score-2 scenario: WS algorithm + sticky + health check), S090 (L3 interview: L4/L7 compare + algorithm choice + SPOF). Levels correct; rubrics sensible and leveled.
- S090 maps to mastery_bar_vi (compare L4/L7, algorithm for normal API vs long-lived, avoid LB-SPOF). Sticky-session clause of the bar is covered inside the S090 answer and S089. Acceptable.

## Coverage discipline
- Mastery items test only ideas the lesson teaches. Good. (Power-of-two-choices in key_concepts is not tested — fine.)

## Language
- Vietnamese clear; English terms parenthesized consistently.
