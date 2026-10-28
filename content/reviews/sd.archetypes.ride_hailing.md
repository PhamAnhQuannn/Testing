# Review: sd.archetypes.ride_hailing

**Verdict: APPROVE** (no must-fix). Reviewer: independent content pass, 2026-10-27.

## Technical accuracy & currency
- Write-load number verified: 100,000 drivers pinging every 4s = **25,000 writes/s** ✓ (consistent in b02, b04, S202, S203, S204).
- High-write location updates kept hot in-memory/Redis (last-write-wins, no per-ping RDBMS write), batch/sample to cold store for history — correct, matches special-check.
- Geo-index: geohash / quadtree / S2 cell decomposition, each cell holds drivers; nearest query = customer's cell + neighbor cells, then filter by true distance — correct. Cell-size tradeoff (big = crowded/over-fetch, small = must union more neighbors) accurate. Correctly notes index lives in RAM because positions change constantly.
- Matching/dispatch: cell query -> rank by distance/ETA -> offer with timeout (~15s) -> next driver; dispatch over queue/pub-sub — correct.
- Double-assign avoidance: atomic claim/lock with TTL = offer timeout, auto-releases if driver doesn't accept or holder dies — correct, matches special-check and reuses distributed_locks properly.
- Real-time tracking via WebSocket (not polling) — correct. Trip state machine requested->matched->enroute->ongoing->completed with reliable transitions — correct.
- Exactly-once charging at trip end via idempotency key — correct, tied back to payments.
- Extensions: surge pricing per-cell (demand/supply), geo-sharding per city — both sound.

## Checks
- b04 (b), b07 (b, boundary-cell neighbor scan), b09 fill (lock/claim; idempotency key) — answers + explanations correct; fill accepts VN + EN synonyms.
- S202 diff1 recall (why RAM + what geo-index does): correct, rubric sensible.
- S203 diff2 score-2 (double-assign fix + TTL + exactly-once charge link): correct, rubric sensible.
- S204 diff3 interview: six-part full design + one extension, matching mastery_bar (matching, in-RAM cells, avoid double-assign, trip state machine). Rubric aligns.

## Pedagogy / language
- Reuses sd.data.geo_indexing, sd.networking.realtime_protocols, sd.distributed.distributed_locks, sd.async.queues_pubsub by reference, not re-teaching.
- Vietnamese clear; English terms parenthesized.

No corrections required.
