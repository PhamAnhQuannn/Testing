# Review: sd.distributed.gossip_quorum (independent reviewer pass)

**Verdict: OK** (no must-fix; clean)

10 blocks; graded: b03 (mcq), b05 (fill), b07 (mcq). mastery_check l1 [S148], l2 [S149], l3 [S150].
mastery_bar_vi: "giải thích đường đọc ghi kiểu Dynamo, chọn N, R, W cho yêu cầu cho trước, nêu vai trò của read repair, hinted handoff và cách gossip phát hiện lỗi." — S150 covers all.

## Technical accuracy (verified numbers)
- Leaderless/Dynamo (Cassandra): no leader; client or coordinator sends writes to replicas and reads from replicas. Consistent hashing picks N successor nodes per key; replication to N. Correct.
- N/W/R defined correctly (N replicas, W write-acks, R read-responses).
- **W + R > N verified as the read-your-writes overlap rule.** States write-set and read-set intersect in ≥1 node holding the newest write. Correctly insists on strict greater-than, not ≥. Version compare via vector clock referenced. Correct.
- **Numeric example verified: N=3, W=2, R=2 → 4 > 3 OK.** Also tunable cases: W large = durable/slow; W=1 = fast/weak; read-heavy R=1,W=N; balanced R=W=⌈(N+1)/2⌉ (N=3 → 2). Verified ⌈4/2⌉=2. Correct.
- read repair (coordinator pushes newest back to a stale replica on the read path) and hinted handoff (another node takes the write with a hint while a replica is temporarily down, replays on recovery) correct. Sloppy quorum correctly noted to weaken the W+R>N guarantee temporarily; anti-entropy via Merkle trees mentioned as deep-dive. Correct.
- Gossip: each node periodically contacts a few random peers exchanging cluster state; spread ~doubles per round (1000 nodes ≈ 10 rounds — verified log2(1000)≈10); no central registry → scales, no SPOF; missing heartbeat → suspected-dead, spreads via gossip; cluster converges on membership for the hash ring. Correct.

## Quiz / mastery correctness
- b03 [b] N=3, W=2, R=2 (4>3) guarantees overlap: correct; (a) 1+1=2<3 may read stale, (c) 1+2=3 NOT >3 (must be strictly greater) — both refuted correctly, including the strict-inequality trap.
- b05 fill (**the numeric W+R>N quiz**): N=5, W=3, smallest R → 3+R>5 → R>2 → **R=3**. Verified correct; accept "3"/"R=3". Explanation notes R=2 gives 5, not >5.
- b07 [b] hinted handoff: correct; (a) read repair only on read path, (c) raising N irrelevant — refuted correctly.
- S148 (L1): define N/W/R + write W+R>N + why. Rubric correctly rejects W+R≥N. Sensible.
- S149 (L2 scenario): N=3 — cart (W small, always-writable) vs config (W+R>N for fresh reads). Correct; (a) W=1 then R=3 (1+3>3) or accept staleness; (b) W=3,R=1 or W=2,R=2. Numbers sound.
- S150 (L3 interview): write/read path + coordinator/ring, read-heavy fresh → N=3,R=1,W=3 (4>3), read repair + hinted handoff + gossip membership/failure detection. Matches mastery_bar; correct.

## Coverage discipline
Mastery items test only taught ideas. No leakage.

## Language
Vietnamese clear; English terms parenthesised (leaderless, Dynamo, coordinator, consistent hashing, replication, quorum, N/W/R, tunable consistency, read-your-writes, read repair, hinted handoff, hint/replay, sloppy quorum, anti-entropy, Merkle tree, gossip, membership, failure detection, heartbeat). Good.

## Findings
None blocking. W+R>N rule, N=3/W=2/R=2 example, and b05 (R=3) all verified correct.
