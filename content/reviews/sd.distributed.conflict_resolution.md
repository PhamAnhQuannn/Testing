# Review: sd.distributed.conflict_resolution (independent reviewer pass)

**Verdict: OK** (no must-fix; clean)

11 blocks; graded: b03 (mcq), b05 (mcq), b08 (fill), b10 (mcq). mastery_check l1 [S145], l2 [S146], l3 [S147].
mastery_bar_vi: "so sánh LWW, OT và CRDT bằng ví dụ 'ab' và G-counter, dùng vector clock để nhận ra xung đột và nêu chi phí của tombstone." — S147 covers all.

## Technical accuracy (verified numbers)
- Concurrent writes on multiple replicas (offline / multi-master) cause conflicts; three merge approaches: LWW, OT, CRDT. Correct.
- LWW: timestamp per write, later wins, loser silently dropped → drops data + depends on machine clocks; fine for single values, bad for data needing merge (cart, shared doc). Correct — LWW drops data correctly characterised.
- Vector clock detection: {A:2,B:1} vs {A:1,B:1} → first ≥ at all indices → descendant (just replace); {A:2,B:0} vs {A:1,B:1} → each side greater somewhere → concurrent/conflict. Correct. Detect vs resolve distinction explicit.
- OT: send operations, server transforms against already-applied ops. 'ab' example: An insert 'X'@0, Bình insert 'Y'@2; apply An first → 'Xab', then shift Bình's op from index 2 → 3 → 'XabY' everywhere. Correct; needs central server, preserves intent, complex (all transform pairs).
- **G-counter merge = element-wise max then sum — worked number verified.** {A:3,B:0} ⊔ {A:2,B:4} → max per node {A:3,B:4} → sum = 3+4 = **7**. Correct; idempotent (max), does not double-count on duplicate delivery; explicitly warns against summing 3+0+2+4. CRDT commutative/associative/idempotent → strong eventual consistency; cost = metadata bloat. Correct.
- Tombstone: delete leaves a marker so a stale replica does not resurrect the element on merge; cost = tombstones accumulate, need periodic GC. Correct.

## Quiz / mastery correctness
- b03 [b] cart LWW → only later item kept, other dropped: correct; (a) LWW is not union, (c) LWW does not void both — refuted correctly.
- b05 [b] (A:2,B:0) vs (A:1,B:1) concurrent: correct; (a) dominating vector = newer, (c) equal = same version — refuted correctly.
- b08 fill: G-counter merge → **7**. Verified (max 3/4 then sum); accept "7"/"bảy". Explanation correct and warns against vertical-sum error.
- b10 [a] tombstone prevents resurrection, cost = accumulation needing GC: correct; (b) index/speed and (c) compression are wrong characterisations — refuted correctly.
- S145 (L1): LWW merge mechanism + main drawback. Sensible.
- S146 (L2 scenario): {A:3,B:0}/{A:2,B:4} — LWW undercounts, G-counter merge = 7, idempotent-max no double count. Correct, good score-2 item.
- S147 (L3 interview): 'ab'/OT (2→3→'XabY'), G-counter=7, vector clock descendant vs concurrent, tombstone cost, selection. Matches mastery_bar; correct.

## Coverage discipline
Mastery items test only taught ideas. No leakage.

## Language
Vietnamese clear; English terms parenthesised (replica, concurrent, multi-master, merge, LWW/last-write-wins, OT/operational transformation, intent, CRDT, G-counter/grow-only, commutative/associative/idempotent, strong eventual consistency, vector clock, comparable/concurrent, siblings, tombstone, garbage collection). Good.

## Findings
None blocking. G-counter worked value (7) and OT 'ab'→'XabY' both verified correct.
