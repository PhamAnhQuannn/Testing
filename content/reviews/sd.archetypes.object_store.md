# Review: sd.archetypes.object_store

**Verdict: PASS (clean, publishable).** Independent content review, 2026-10-27.

## Technical accuracy & currency
- Metadata service vs data nodes split correct: metadata = small but critical ledger (object key → chunk list, size, checksum, version; on a consensus-backed store), data nodes = raw bytes in large immutable chunks (scale by adding machines). Rationale for the split is right.
- GFS/HDFS 64 MB immutable chunks correct and current.
- Write path order correct: ask metadata → chunk → write + replicate (or erasure) to data nodes across failure domains → wait for enough durable copies → commit metadata via consensus; object exists only after metadata commit. Read path (metadata directs, bytes flow direct) correct.
- Durability mechanics correct: re-replication/repair, scrubbing for bit rot, immutability + versioning, delete-then-GC. 11-nines framing reasonable.

## Special checks (all numbers verified correct)
- 3-replica = **3x** capacity, tolerate **2** lost copies (1 survives): correct (b07, b08, S254, S255).
- Erasure coding **10+4 = 1.4x** (14/10) capacity, tolerate **4** lost fragments: correct (b07, b08, S254, S255).
- General formula k+m: (k+m)/k capacity, tolerate m; example 6+3 = 1.5x tolerate 3: correct.
- b08 fill answers: 3 GB / 2 / 1.4 GB / 4 — all correct.

## Quiz / check items
- b03, b06 (MCQ), b08 (fill): answers/explanations correct; distractors genuinely wrong.
- S253 (diff1 metadata/data split recall), S254 (diff2 replication-vs-erasure number scenario, correctly picks erasure for cold data with the CPU/network tradeoff), S255 (diff3 interview matching mastery_bar_vi: write path through metadata + data nodes, and replication-vs-erasure by the numbers): correct, level-appropriate, rubrics sensible.

## Reuse of taught concepts
- Builds on blob storage usage (sd.data.object_blob_storage) and consensus (referenced). Applies (designs internals), not re-teaches.

## Language
- Vietnamese clear; English terms parenthesized throughout (metadata service, data nodes, chunk, replication, erasure coding, parity, failure domain, scrubbing, garbage collection).

No must-fix items.
