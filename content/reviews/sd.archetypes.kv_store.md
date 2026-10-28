# Review: sd.archetypes.kv_store

**Verdict: PASS (clean, publishable).** Independent content review, 2026-10-27.

## Technical accuracy & currency
- Build-up ladder correct: single dict (RAM) → consistent-hashing ring + virtual nodes (sharding, few keys move on add/remove, vs hash()%n) → N replicas (replication factor, typically N=3, tolerate N-1 loss) → quorum R/W. Each step removes one weakness and exposes the next. Dynamo-style leaderless framing current (2026).
- Conflict resolution: LWW (simple, can lose a write) vs vector clock (keeps both concurrent writes for app merge); hinted handoff + read repair + Merkle anti-entropy; LSM-tree disk engine. All correct.

## Special checks (all pass)
- dict → consistent-hashing ring → N replicas → quorum: present and correct (b01–b05).
- **W+R>N correct**: stated correctly and repeatedly (b05, b06, b07, S251, S252) with the pigeonhole/intersection justification — read set and write set overlap in ≥1 node holding the latest write.
- R/W tuning VERIFIED:
  - Balanced R=W=⌈(N+1)/2⌉: for N=3, ⌈4/2⌉=2 → R=W=2; b06 fill answer "2" correct, explanation R+W=4>3 correct.
  - Read-heavy = R=1, W=N — NOT inverted. b07 correctly gives read-heavy → R=1, W=3 (reads cheap, writes to all), and write-heavy → W=1, R=3. Directions are correct, not swapped.
  - Availability-leaning (cart) → W=1, R=1 (W+R=2≤N), eventual consistency, resolve via vector clock/read repair (b08, S252). Consistency-leaning → R+W>N. Correct.
- Vector clock / LWW conflict: present and correct (b10, S252).

## Quiz / check items
- b04, b08 (MCQ), b06 (fill): answers/explanations correct. b08 cart scenario correctly selects W=1,R=1; explanation that W=3 means one dead node blocks writes is right.
- S250 (diff1 N/W/R recall), S251 (diff2 read-after-write quorum choice + justification), S252 (diff3 interview matching mastery_bar_vi: build-up + why R+W>N + choose R,W for consistency-leaning vs availability-leaning + cost): correct, level-appropriate, rubrics sensible.

## Reuse of taught concepts
- Reuses consistent hashing (sd.data.consistent_hashing), replication (sd.data.replication), gossip/quorum (sd.distributed.gossip_quorum), conflict resolution (sd.distributed.conflict_resolution). Applies, not re-teaches.

## Language
- Vietnamese clear; English terms parenthesized throughout. (Typo "chí mạng" for "chí mạng/chí tử" sense in b01 — harmless.)

No must-fix items.
