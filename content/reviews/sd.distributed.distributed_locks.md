# Review: sd.distributed.distributed_locks (independent reviewer pass)

**Verdict: OK** (no must-fix; clean)

11 blocks; graded: b05 (mcq), b07 (mcq), b09 (fill). mastery_check l1 [S136], l2 [S137], l3 [S138].
mastery_bar_vi: "thiết kế lock service với lease và fencing token, và nêu khi nào nên thay khóa bằng compare-and-set." — S138 covers all.

## Technical accuracy (verified)
- Why hard: not acquisition but holder hanging/dying mid-hold; a never-released lock blocks the system (liveness). Correct.
- Lease = TTL lock, auto-releases on expiry so a dead node does not hold forever; live holder must renew. Redis `SET lock id NX PX 30000` (NX = only if absent, PX = expire 30000ms) correct; release only if value == own id. Correct.
- GC-pause-overwrite case correct: A holds lease, GC-pauses past TTL, lease expires, B acquires and writes, A wakes unaware and overwrites. TTL alone cannot save it (A doesn't know it overran). Correct.
- Fencing token: monotonic number issued per grant (33, then 34), attached to each write; **protected resource rejects any write whose token < max token seen**. Stops the stale actor; safety does not depend on A noticing it lost the lock. Correct and precisely stated.
- Lock-store strength: single Redis = SPOF; consensus-based (ZooKeeper/etcd, ephemeral nodes, majority write) safer. Redlock critique correct — its safety assumes well-behaved clocks and no long pauses (exactly what the failure model says not to trust); regardless of store, fencing token at the resource is the real safety net. Correct.
- CAS / optimistic concurrency for single-key update correct: conditional write "value unchanged since read" (version check, e.g. id=7 AND version=5), loser retries; no lease/renew/fencing needed when the op fits one key/record. Correct; applicability condition (single key/record, atomic conditional write; not multi-resource/multi-step) stated.

## Quiz / mastery correctness
- b05 [b] hung node writes unaware + resource rejects lower token: correct; (a) long TTL only lowers probability, (c) clocks not assumable — both refuted correctly.
- b07 [b] Redlock assumes good clocks; consensus store safer + still use fencing: correct; (a) single Redis worse, (c) TTL doesn't fix overrun — refuted correctly.
- b09 fill: "CAS": correct; accept list covers CAS/compare-and-set variants.
- S136 (L1): lease vs plain lock + which risk it solves. Sensible.
- S137 (L2 scenario): 30s lease + 40s GC pause → why TTL insufficient, fencing token mechanism, who checks (target store). Correct, good score-2 item.
- S138 (L3 interview): acquire/renew/release API, fencing issued-at-acquire + enforced-at-resource, consensus-backed state + Redlock critique, single-key→CAS with applicability. Matches mastery_bar; correct.

## Coverage discipline
Mastery items test only taught ideas. No leakage.

## Language
Vietnamese clear; English terms parenthesised (distributed lock, lease, TTL, renew, GC pause, fencing token, monotonic, resource, ephemeral node, consensus, Redlock, compare-and-set/CAS, optimistic concurrency, liveness/safety). Good.

## Findings
None blocking. Accurate and interview-correct.
