# Review: sd.distributed.consensus (independent reviewer pass)

**Verdict: OK** (no must-fix; clean)

11 blocks; graded: b03 (mcq), b06 (mcq), b07 (fill), b10 (mcq). mastery_check l1 [S133], l2 [S134], l3 [S135].
mastery_bar_vi: "giải thích Raft ở mức term, bầu cử, log replication và quorum, và biết khi nào cần etcd hoặc ZooKeeper." — S135 covers all.

## Technical accuracy (verified numbers)
- Majority quorum = ⌊n/2⌋+1: 5→3, 7→4. Correct.
- Two majorities always overlap in ≥1 node → single truth, anti-split-brain. Correct.
- Fault tolerance 2f+1: 3 nodes tolerate 1, 5 nodes tolerate 2; odd clusters preferred, 4 does not beat 3. Verified: 4 nodes majority = 3, tolerate 1. Correct.
- Raft: terms (monotonically numbered election epochs, ≤1 leader per term, higher term beats lower, stale leader rejected); election (follower election timeout → term++ → candidate → request votes → majority wins; one vote per term so no two leaders per term); log replication (all changes via leader, append → replicate → commit when majority acks → apply/reply). Correct.
- Commit-survives-future-elections argument (overlap guarantees a future leader sees any committed entry) correct.
- Paxos stated as equivalent power to Raft but harder to understand/implement; Raft designed for understandability. Correct.
- etcd/ZooKeeper use cases (config/metadata, leader election, service discovery, distributed lock/fencing; ephemeral nodes, watch) and limit (few KB, quorum write latency, does not scale write throughput, not a primary datastore). Correct.

## Quiz / mastery correctness
- b03 [b] 5 nodes need 3, tolerate 2 (2f+1, f=2): correct; a/c refuted correctly.
- b06 [b] commit when majority acks: correct; (a) no majority = possible loss, (c) all = loses fault tolerance — both refuted correctly.
- b07 fill: 7 nodes → majority 4, tolerate 3. Verified ⌊7/2⌋+1=4, 7−4=3 (2f+1, f=3). Correct; accept lists cover numerals/words.
- b10 [b] etcd/ZooKeeper for small consistent data: correct; (a) primary DB, (c) high-throughput cache refuted correctly.
- S133 (L1): consensus definition + quorum formula. Sensible.
- S134 (L2 scenario): odd vs even, 5 tolerate 2, why overlap prevents two leaders. Correct, good score-2 item.
- S135 (L3 interview): term + election + log replication/commit + quorum overlap + etcd/ZooKeeper + limit, Paxos one-liner. Matches mastery_bar; correct.

## Coverage discipline
Mastery items test only taught ideas. No leakage.

## Language
Vietnamese clear; English terms parenthesised (consensus, leader election, replicated log, majority quorum, term, candidate, request votes, commit/ack, Raft, Paxos, etcd/ZooKeeper, ephemeral node, watch, service discovery, distributed lock). Good.

## Findings
None blocking. All quorum/fault-tolerance numbers verified correct.
