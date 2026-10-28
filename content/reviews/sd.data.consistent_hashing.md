# Review: sd.data.consistent_hashing (independent reviewer pass)

**Verdict: OK** (no must-fix; clean) — SPECIAL number check PASSED.

11 blocks; graded: b04 (mcq), b06 (fill), b08 (mcq). mastery_check l1 [S055], l2 [S056], l3 [S057].
mastery_bar_vi: "vẽ vòng, tìm máy của một khóa, nói thêm/bớt một máy dời bao nhiêu khóa, vì sao cần virtual node" — S057 covers all.

## SPECIAL number check (verified correct)
- Key-movement claim is correct: adding the Nth node moves ~**K/N ≈ 1/N** of keys (NOT ~all). Stated in b05, b06 fill, b10, summary, S055, S056, S057. The new node occupies ~1/N of the ring so pulls ~K/N keys from its one clockwise successor; removing a node frees ~1/N (its own share). Correct.
- Contrast number correct: `hash(key) % N` reshuffles nearly 100%; **4→5 nodes ≈ 80%** (b01, b11, S056). n/(n+1) = 4/5 = 80%. Correct.
- b06 fill answer `1/N` with regex `^\(?\s*1\s*/\s*[nN]\s*\)?$` — correct and matches the explanation.
- Virtual-node rationale correct: one point/node gives uneven arcs (A owns (300,90]≈150°, C owns (200,300]≈100° — arithmetic correct) and dumps all of a leaving node's load onto one successor; vnodes (100–200 points/node) average arc length (even load), spread rebalance across many nodes, and allow weighted nodes. Correct. Correctly distinguishes vnodes from replication (b08 c refuted).

## Ring-geometry correctness (A=90, B=200, C=300)
- b03 arcs: A (300,90], B (90,200], C (200,300] — correct (clockwise, wrap at 360).
- b04 [b] key 210 → clockwise → C(300) first (not "nearest"): correct; (a) nearest-distance, (c) smallest-position refuted correctly.
- b05 add D=270 → D takes (200,270] from C only; A,B and C's (270,300] unchanged. Remove C → keys go to next clockwise = A. Correct.
- S057: 250→C; add D 270 moves (200,270] C→D (incl. 250), A/B unchanged; remove C → C's keys to A; ~K/N per add/remove; vnode rationale. All correct.

## Quiz / mastery correctness
- b08 [b] vnode = even load + smooth rebalance + weighting: correct; (a) fewer machines, (c) replication refuted correctly.
- S055 (L1 recall): clockwise-first assignment + ~1/N moved. Sensible.
- S056 (L2 gate): 4→5 cache nodes — `% N` ~80% → cache-miss stampede → DB; consistent hashing ~1/5≈20%; "position independent of N". Good gate; numbers correct.
- S057 (L3 interview): full ring walkthrough + add/remove + ~K/N + vnode. Matches mastery_bar.

## Coverage / cross-lesson consistency
Mastery items test only taught ideas. Consistent with sd.data.sharding (prereq): both state `hash % n` reshuffles ~all, consistent hashing moves a small fraction. No contradiction. rendezvous/HRW and Dynamo N-successor replication correctly noted as adjacent concepts.

## Language
Vietnamese clear; English terms parenthesised (consistent hashing, hash ring, clockwise, virtual node/vnode, weighted nodes, preference list, rendezvous hashing). Good.

## Findings
None blocking. Numbers (K/N ≈ 1/N, 4→5 ≈ 80%) and vnode rationale all correct.
