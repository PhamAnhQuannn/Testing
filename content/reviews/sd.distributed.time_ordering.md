# Review: sd.distributed.time_ordering (independent reviewer pass)

**Verdict: OK** (no must-fix; clean)

10 blocks; graded: b03 (mcq), b05 (fill), b07 (mcq). mastery_check l1 [S142], l2 [S143], l3 [S144].
mastery_bar_vi: "giải thích vì sao không dựa vào đồng hồ thật và chọn logical clock hoặc số thứ tự cho thứ tự sự kiện." — S144 covers all.

## Technical accuracy (verified)
- Why wall clocks fail: clock skew, NTP step/jump (forward and backward), clocks running backward → LWW-by-timestamp can let an old record overwrite a new one silently. Correct.
- Monotonic sequence number from a single source (Kafka partition offset, DB auto-increment) as simplest ordering; limitation = single source is bottleneck/SPOF, needs all events through one place. Correct.
- **Lamport receive rule verified correct: local = max(local, received) + 1.** Worked example in b04 (local 1, received 3 → max(1,3)+1 = 4) correct. Lamport gives a total order consistent with causality, but a<b does NOT prove causality (independent/concurrent events can differ). Correct. (Minor: strict total order needs a node-id tie-break on equal timestamps, unmentioned — acceptable simplification, not a must-fix; the load-bearing claims are right.)
- Vector clocks: per-node counter vector; dominates at every index (and strictly greater somewhere) → descendant/comparable; each side greater at some index → concurrent/conflict. Vector clocks DETECT concurrency, which Lamport cannot. Correct.
- TrueTime/Spanner: bounded uncertainty interval + commit-wait; use physical time safely only by knowing max error and waiting it out. Correct and current.

## Quiz / mastery correctness
- b03 [b] skew/jump/backward → new record with smaller timestamp silently overwritten: correct; (a) off-point, (c) NTP does not make clocks exactly equal — refuted correctly.
- b05 fill (**the Lamport-rule quiz**): B counter 5, receives 9 → max(5,9)+1 = **10**. Verified correct; accept "10". Explanation restates rule correctly.
- b07 [b] (A=2,B=0) vs (A=1,B=1) → concurrent/conflict: correct; (a) sum-comparison and (c) nonzero-count are explicitly wrong ways to compare — refuted correctly.
- S142 (L1): why not wall-clock + one LWW consequence. Sensible.
- S143 (L2 scenario): chat ordering without device clocks — sequence number + condition, Lamport clock + the receive rule `local = max(local, received)+1`. Correct; rubric penalizes forgetting max or +1.
- S144 (L3 interview): why not physical clock; pick tool for each need (sequence / Lamport / vector); the one thing Lamport cannot do that vector can. Matches mastery_bar; correct.

## Coverage discipline
Mastery items test only taught ideas. No leakage.

## Language
Vietnamese clear; English terms parenthesised (wall-clock time, clock skew, NTP, last-write-wins, monotonic sequence number, offset, Lamport clock, counter, causality, vector clock, comparable/concurrent, TrueTime, commit-wait, bounded uncertainty). Good.

## Findings
None blocking. Lamport receive rule and the b05 quiz answer (10) both verified correct.
