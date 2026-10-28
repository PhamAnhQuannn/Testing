# Review: sd.framework.api_data_model (independent reviewer pass)

**Verdict: OK** (no must-fix; 1 nice-to-have)

11 blocks; graded: b05 (mcq), b07 (mcq), b09 (fill). mastery_check l1[S034] l2[S035] l3[S036].
mastery_bar_vi: "từ yêu cầu phác API và bảng đúng access pattern, chỉ rõ PK, partition key, index chính trong ~8 phút" — S036 matches.

## Technical accuracy
- API: resource/verb/key-params, cursor+limit pagination, Idempotency-Key on writes, identity from token not body — all correct and current (2026).
- "Query the way you read" / access-pattern-driven schema; `(user_id, created_at)` index for feed — correct.
- PK vs partition/shard key vs index distinction (b06/b07) correct; hot-partition caveat right.
- Relational-by-default, NoSQL for scale-by-known-key with weaker joins/txn — correct, current, appropriately hedged for HLD.

## Quiz / mastery correctness
- b05 [b] access-pattern → cols+index — correct; (a) table-first and (c) JSON-blob feed correctly refuted.
- b07 [a] partition=which shard vs primary=unique row — correct; (b)/(c) refuted precisely.
- b09 fill: pagination / idempotency key — correct.
- S034 (L1): endpoint parts + access-pattern meaning; rubric sensible.
- S035 (L2 gate): e-commerce order history — GET /orders paginated + token identity, PK=id, index (user_id, created_at) tied to access pattern. Correct.
- S036 (L3): URL shortener API+model, PK/partition=code, secondary index, relational-vs-NoSQL with reason. Matches bar. All keys correctly justified.

## Consistency
Follows requirements (steps 3+4). URL-shortener example coheres with the same example in requirements S030, estimation, hld_diagram S039, deep_dive S042. Idempotency-Key terminology matches the repo API contract.

## Language
Vietnamese clear; English terms parenthesized (resource/verb, pagination, idempotency, primary/partition/shard key, index, relational/NoSQL). Good.

## Findings
- **nice-to-have:** S036 answer offers "301/302 redirect" interchangeably; for a shortener 302 is usually preferred (preserves click analytics / allows later edits). Offering both is acceptable at HLD level — leave as is.
