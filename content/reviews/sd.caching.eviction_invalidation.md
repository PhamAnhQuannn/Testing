# Review: sd.caching.eviction_invalidation (independent reviewer pass)

**Verdict: OK** (no must-fix; clean)

10 blocks; graded: b03 (mcq), b05 (fill), b09 (mcq). mastery_check l1 [S076], l2 [S077], l3 [S078].
mastery_bar_vi: "cài LRU với hashmap và danh sách liên kết đôi, giải thích race giữa ghi DB và xóa cache bằng timeline và cách giảm" — S078 covers all.

## Technical accuracy (verified)
- Eviction (capacity: which item to drop) vs invalidation (correctness: avoid serving stale) distinction correct.
- Policies correct: LRU (temporal locality, good default), LFU (frequency, stale-hot aging caveat noted), FIFO, random, TTL (max-staleness; both time-eviction and invalidation tool). Accurate.
- **LRU O(1) mechanism correct**: hash map (key→node, O(1) lookup) + doubly linked list (MRU head / LRU tail; node knows prev+next → unlink-from-middle and move-to-head in O(1)). get/put flows and evict-from-tail correct; "need both or lose O(1)" correct.
- Invalidation: TTL (simple, stale until expiry), explicit delete-on-write (fresh, race-prone), versioned keys (old key ignored, GC'd by eviction). Correct.
- **DB-write / cache-delete race timeline correct** (classic stale-reload): T1 A miss, T2 A reads DB V0 (stalls), T3 B writes DB V1, T4 B deletes key (empty → no-op), T5 A writes V0 → cache stuck on V0 until TTL. Root cause (A read V0 before B's write but wrote cache after B's delete) correct.
- Mitigations correct: delete-after-commit, delayed double delete (delete now + scheduled second delete after ~hundreds ms), short TTL (safety net, doesn't prevent), write-through. Accurate.

## Quiz / mastery correctness
- b03 [b] LRU for strong temporal locality: correct; (a) FIFO, (c) random refuted correctly.
- b05 fill: hash map + doubly linked list: correct; accept lists cover EN/VI variants.
- b09 [b] delete-before-commit worse (gap lets a read reload old DB value): correct; (a) causality wrong, (c) key-permanently-lost wrong refuted correctly.
- S076 (L1 recall): name ≥4/5 policies + eviction vs invalidation. Sensible.
- S077 (L2 gate): profile cache invalidation strategy + trade-off, why TTL alone serves stale, LRU choice. Good score-2 scenario; answer correct.
- S078 (L3 interview): (A) LRU O(1) both structures + why both needed, (B) race timeline + root cause, (C) ≥2 mitigations + trade-offs. Matches mastery_bar; all correct.

## Coverage discipline
Mastery items test only taught ideas (policies, LRU internals, race+mitigations). No leakage.

## Language
Vietnamese clear; English terms parenthesised (eviction, invalidation, LRU/LFU/FIFO/TTL, temporal locality, hash map, doubly linked list, delete-after-commit, delayed double delete, write-through, versioned keys). Good.

## Findings
None blocking. Accurate and interview-correct.
