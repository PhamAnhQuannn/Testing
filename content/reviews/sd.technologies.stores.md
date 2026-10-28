# Review: sd.technologies.stores

**Verdict: PASS (clean, ready to publish).** Independent content review, 2026-10-27.

## Technical accuracy & currency
- PostgreSQL framed correctly as the relational default: ACID, joins, secondary indexes; core limit = single-primary write ceiling, read replicas offload reads only, sharding needed to split *write* load and it breaks cross-shard joins/transactions. Correct and current.
- DynamoDB/Cassandra (wide-column/KV): partition-key design, very high write throughput, tunable consistency, no joins / limited ad-hoc query. Correct.
- S3/object storage: cheap+durable blob store, not a database, immutable objects (overwrite whole object), presigned URL/CDN, standard pattern = metadata in Postgres + bytes in S3. Correct.
- Polyglot persistence and "default to Postgres, change only for a requirement reason" framing is sound.

## Quizzes
- b04 (order service → Postgres + single-primary write ceiling limit): answer `b` correct; distractors fair.
- b06 (why not wide-column for ad-hoc aggregate reporting): answer `a` correct; explain correctly steers to OLAP/ClickHouse or a Postgres replica.
- b07 fill (partition key): accept list covers EN/VI variants.

## Mastery items
- S151 diff1 recall (name 3 stores + what each is best at) — appropriate level; answer/rubric correct.
- S152 diff2 scenario (chat history → wide-column, limit, then OLAP for reporting) — score-2 scenario, rubric sensible.
- S153 diff3 interview (e-commerce: 3 entities each → store + 1-2 reqs + 1 limit + general principle) — matches mastery_bar_vi exactly.
- Items test only ideas the lesson teaches (ClickHouse/OLAP is introduced in b06). Vietnamese clear; English terms parenthesized.

No must-fix items.
