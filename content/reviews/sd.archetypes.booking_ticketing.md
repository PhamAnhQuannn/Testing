# Review: sd.archetypes.booking_ticketing

**Verdict: APPROVE (clean).** Independent content review, 2026.

- Technical accuracy: core invariant no-double-booking correctly framed as inventory contention; seat lifecycle free → held → sold; hold with TTL + auto-release; idempotent confirm with idempotency key — all correct.
- Special check: the three locking approaches are all present and correct on the An/Bình same-seat A1 example — pessimistic `SELECT ... FOR UPDATE` (blocks/waits, throughput cost, deadlock risk), optimistic/compare-and-set (`UPDATE ... WHERE trang_thai='trong'` or version column; one row affected wins, loser retries), DB unique constraint on `(su_kien, ghe)` (second INSERT rejected, DB as final arbiter). Combining fast path + unique-constraint safety net, DB as source of truth even with Redis hold — all correct.
- Virtual waiting room: correctly motivated (CAS stays correct but doesn't prevent overload), gate-level queue releasing small batches, + search-vs-booking path split.
- Quizzes: b06 (CAS atomic, distinguishes from pessimistic FOR UPDATE in distractor), b07 fill (unique constraint), b10 (waiting room for overload, rejects sticky-session/longer-TTL traps) — every `answer` + `explain_md` correct.
- Mastery: S229 diff1 recall, S230 diff2 scenario (two approaches + why combine), S231 diff3 interview covering all three locks via An/Bình + waiting room, matching Mức-3 bar. S231 even handles the "payment completes just as hold expires" edge. Levels/rubrics sensible.
- Reuse: leans on transactions, TTL/Redis, cache, queue from earlier.
- Language: Vietnamese clear; English terms parenthesized.
