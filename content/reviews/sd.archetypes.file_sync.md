# Review: sd.archetypes.file_sync

**Verdict: PASS** (independent content review, 2026). No must-fix.

## Technical accuracy
- Goal (transfer only what changed) and chunking framed well; resumable upload per chunk correct.
- **Content-defined chunking**: fixed-size chunking shifts all boundaries when a byte is inserted (almost every later chunk becomes "new"); content-defined chunking anchors boundaries to content (rolling hash hitting a marker) so insert/delete only affects chunks around the edit. Correct — the core CDC-vs-fixed insight (rsync/restic-style).
- **Content-hash dedup**: per-chunk hash (SHA-256) = fingerprint; same content → same hash; store each hash once (content-addressed). Correct.
- **Delta sync**: re-chunk, hash, diff against old hash list, upload only new hashes, send ordered hash list for the new version; one-line edit in a 100 MB file ≈ one chunk uploaded. Correct.
- Architecture split: object storage (large immutable content-addressed chunks) vs metadata service on a DB (file/version → ordered hash list, owner, permissions); versioning = a few metadata rows, no file copy. Plus notification/sync channel (WebSocket/long-poll, polling fallback) that only signals "folder changed." Correct metadata-points-to-blob pattern.
- **Conflict**: two offline edits from the same base → neither supersedes the other; overwrite loses data silently; keep both (primary + conflicted copy with a distinct name). Correct, standard Dropbox-style behavior.

## Quizzes / mastery
- b04 CDC reason = b correct (a "smaller chunks" / c "no hashing needed" false); b07 metadata/object-storage split = b correct (a overstated, c anti-dedup); b10 conflict = b correct (a overwrite loses data, c global lock breaks offline).
- S217 (diff1): content hash purpose + one benefit — recall, right level.
- S218 (diff2): one-line edit in 100 MB → chunking + CDC reason + hash-diff + ~one chunk. Right level.
- S219 (diff3 interview): 5-part Dropbox design (chunk/dedup/delta/metadata-split+channel/conflict). Matches mastery_bar. Rubrics sensible.

## Reuse (no re-teach)
Builds on object_blob_storage and realtime_protocols by name. Good.

## Language
Clear Vietnamese; English terms parenthesized (chunk, content-defined chunking, rolling hash, content hash, dedup, delta sync, object storage, conflicted copy). No issues.

## Optional nit (not blocking)
Real Dropbox uses fixed 4 MB blocks; content-defined chunking is the better pedagogical/interview answer (rsync/restic/borg use it). The lesson teaches the concept, not a product, so this is fine.
