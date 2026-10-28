# Review: sd.data.sql_vs_nosql (independent reviewer pass)

**Verdict: OK** (no must-fix; clean)

11 blocks; graded: b03 (mcq), b05 (fill), b08 (mcq), b09 (mcq). mastery_check l1 [S043], l2 [S044], l3 [S045].
mastery_bar_vi: "chọn đúng loại kho cho từng dữ liệu bằng checklist 5 câu và nêu giới hạn quy mô" — S045 covers it.

## Technical accuracy (verified, 2026-current)
- SQL strengths (join, ACID, secondary index, normalization) stated correctly; ACID expanded correctly.
- Four NoSQL families mapped correctly: key-value (Redis/DynamoDB), document (MongoDB), wide-column (Cassandra), graph (Neo4j), each with correct good/bad fit.
- Scale-limit framing correct: RDBMS write ceiling = all writes to one primary; read replicas scale reads only; wide-column ~linear write scaling; graph hard to shard. All accurate.
- Interview callout (JSONB+GIN, partial index, `SELECT ... FOR UPDATE SKIP LOCKED` as a job queue, polyglot persistence, "start with an RDBMS") is current and correct. Postgres/MySQL named as most popular RDBMS 2026 — reasonable.

## Quiz / mastery correctness
- b03 [b] key-value for session-by-id: correct; (a)/(c) correctly refuted.
- b05 fill ACID: correct; accept list covers upper/lower case.
- b08 [b] wide-column for billions-of-messages-by-conversation: correct; consistent with sharding lesson's chat example.
- b09 [b] RDBMS balance → writes to one primary, sharding loses cross-shard join/txn: correct; (a)/(c) refuted correctly.
- S043 (L1 recall): 4 families + 2 SQL strengths; rubric sensible.
- S044 (L2 gate): shopping-cart via 5-Q checklist, pick store, name a scale limit (hot key / RAM). Genuine scenario gate.
- S045 (L3 interview): 4-datum social-network backend, store per datum + scale limit each + polyglot justification. Matches mastery_bar. Answers correct (a SQL, b wide-column, c graph, d key-value).

## Coverage discipline
Mastery items test only taught ideas (5-Q checklist, 4 families, scale limits, polyglot). No leakage.

## Language
Vietnamese clear; English terms parenthesised (ACID, BASE, key-value, document, wide-column, partition key, eventual consistency, polyglot persistence). Good.

## Findings
None blocking. Accurate and interview-correct.
