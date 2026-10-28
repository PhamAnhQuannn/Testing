# Review: sd.archetypes.collab_editing

**Verdict: PASS (clean, publishable).** Independent content review, 2026-10-27.

## Technical accuracy & currency
- LWW-on-whole-document loses writes; modelling edits as position-based insert/delete operations is correct.
- Concurrency problem framed correctly: positions are computed against the sender's seen version, so applying raw in different orders diverges.
- OT vs CRDT contrast is accurate and current (2026): OT = numeric positions + transform, usually needs a central server to fix a canonical order; CRDT = immutable ordered per-char IDs, order-independent merge, no central transform, higher memory (per-char metadata, tombstone cleanup). "Both converge" stated correctly. Product mapping (Docs → OT; Figma/local-first → CRDT) reasonable.
- Per-document server correct: one owner per document, serialize ops, assign increasing sequence number, broadcast over WebSocket, shard by document_id to scale.

## Special checks (all pass)
- Concurrent ops must be transformed + worked example converges: VERIFIED. Doc `ab`, An inserts `X`@1, Bình inserts `Y`@1. Raw apply diverges (`aYXb` vs `aXYb`); OT fixes An first → `aXb`, transforms Bình's position 1→2 (An's insert at position 1 is at-or-before Bình's) → `aXYb`; all machines converge to `aXYb`. The tie-break (equal positions) is standard and sound.
- OT vs CRDT: present and correct (b05, b06, S246).
- Per-document server assigns sequence: present and correct (b07, b08).

## Quiz / check items
- b04, b06, b11 (MCQ), b08 (fill): answers and explanations correct; CRDT "costs less memory" distractor correctly marked wrong.
- S244 (diff1), S245 (diff2 scenario with the `aXYb` worked example), S246 (diff3 interview matching mastery_bar_vi: example-driven why-transform + OT/CRDT + per-document server): correct, level-appropriate, rubrics sensible.

## Reuse of taught concepts
- Reuses realtime protocols/WebSocket/sequence/reconnect (sd.networking.realtime_protocols) and conflict resolution OT/CRDT (sd.distributed.conflict_resolution); explicitly applies, not re-teaches.

## Language
- Vietnamese clear; English terms parenthesized throughout.

## Minor (non-blocking, not must-fix)
- b03 intermediate shorthand writes "`aX` rồi chèn `Y` tại 1" (drops the trailing `b`); the stated result `aYXb` is correct, so this is cosmetic only.

No must-fix items.
