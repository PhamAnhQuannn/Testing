# Review: sd.caching.distributed_cache (independent reviewer pass)

**Verdict: OK with one coverage gap** (one should-fix vs mastery_bar; no factual errors)

10 blocks; graded: b04 (mcq), b06 (fill), b09 (mcq). mastery_check l1 [S082], l2 [S083], l3 [S084].
mastery_bar_vi: "chọn đúng kiểu Redis cho leaderboard, rate limit, session, viết các lệnh chính với đúng tham số và giải thích cách cluster chia khóa **và xử lý hết RAM**."

## Technical accuracy (verified)
- Memcached (multithreaded, key-value, no persistence, string get/set) vs Redis (rich types, single-threaded command execution → atomic, persistence/replication/pub-sub) correct.
- **Redis commands correct**:
  - Leaderboard ZSET: `ZADD board 150 an` (ZADD key score member, upsert), `ZREVRANGE board 0 9` (top 10 high→low, WITHSCORES optional), `ZREVRANK board an` (rank, 0 = highest). All correct; O(log n)/top-K rationale correct.
  - Rate limit: `INCR rl:user7` (returns new value, atomic) + `EXPIRE rl:user7 60` only on first call (INCR==1); >100 → reject 429; window resets when key expires. Correct pattern and params.
  - Session: `SET session:abc "<json>" EX 1800` (string+TTL), `GET`, alt `HSET ... / EXPIRE 1800`, sliding renew via EXPIRE. Correct.
- **Cluster**: 16384 hash slots, `CRC16(key) mod 16384` → one slot, node holds a slot range (+replica), adding a node moves only some slots (no full rehash). Correct.
- **Cross-slot**: multi-key command only runs when all keys share a slot; else `CROSSSLOT` rejection; hash tag `{...}` forces co-location (`user:{7}:profile`/`user:{7}:session` same slot). Correct.
- **Single-threaded**: slow command blocks all; `KEYS *` blocks server → use `SCAN`; avoid O(n) on huge sets on hot path. Correct.

## Quiz / mastery correctness
- b04 [b] ZSET for top-10 + rank: correct; (a) JSON-string resort, (c) list refuted correctly.
- b06 fill: INCR + EXPIRE: correct params.
- b09 [b] CROSSSLOT because keys hash to slots on different nodes + hash tag: correct; (a) "max 2 keys" and (c) "rehash all" refuted correctly.
- S082 (L1 recall): Memcached vs Redis + 3 type mappings. Sensible.
- S083 (L2 gate): rate-limiter — type + commands w/ params, why EXPIRE once, next-minute reset. Good score-2; answers correct.
- S084 (L3 interview): 3 problems + exact commands + cluster key split + CROSSSLOT. Correct — but see gap below.

## Coverage gap (vs mastery_bar)
- mastery_bar_vi level-3 requires explaining **"xử lý hết RAM"** (out-of-RAM handling = `maxmemory` + eviction policies such as `allkeys-lru` / `volatile-ttl` / `noeviction`). The lesson (b01-b10) never teaches maxmemory eviction, and S084 never asks for it. So the advertised level-3 bar is only ~2/3 met. `key_concepts` in subtopics.json also lists "maxmemory eviction policies" and "persistence: RDB vs AOF" — neither maxmemory handling is taught. (RDB/AOF is referenced only glancingly.)

## Coverage discipline
Items otherwise test only taught ideas (types/commands, cluster slots, single-thread). No leakage; the gap is under-coverage, not over-reach.

## Language
Vietnamese clear; English terms parenthesised (distributed cache, key-value, multithreaded, single-threaded, sorted set/ZSET, hash slot, CRC16, CROSSSLOT, hash tag, SCAN/KEYS, atomic). Good.

## Findings
See must-fix: lesson + S084 do not cover "xử lý hết RAM" (maxmemory eviction) required by the level-3 mastery bar.
