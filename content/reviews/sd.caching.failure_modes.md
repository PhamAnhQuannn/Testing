# Review: sd.caching.failure_modes (independent reviewer pass)

**Verdict: OK** (no must-fix; clean)

11 blocks; graded: b03 (mcq), b05 (mcq), b07 (fill), b09 (mcq). mastery_check l1 [S079], l2 [S080], l3 [S081].
mastery_bar_vi: "gọi tên đủ 4 tai nạn cache, nêu cách chữa từng cái và áp đúng vào một thiết kế đang bàn" — S081 covers all.

## Technical accuracy (verified)
- Four failure modes correctly distinguished by cause, not just symptom:
  - **Stampede / thundering herd**: one hot key expires, many requests recompute one value → fix single-flight / request coalescing lock, or early recomputation before expiry. Correct.
  - **Penetration**: queries for non-existent keys always miss to DB → fix null/negative caching (short TTL) + Bloom filter. Correct; Bloom filter claim accurate ("never false negative", can false-positive) → safe to use for blocking.
  - **Avalanche**: many keys expire together (same TTL) or whole cluster dies → fix TTL jitter, layered L1/L2 cache, DB protection (rate limit / circuit breaker / warm-up). Correct.
  - **Hot key**: one key over-queried, concentrated on one node (cache still hits) → fix local/client-side replica (short TTL) and/or key splitting key_1..key_N. Correct.
- Cascading-failure framing (DB sized for cache-offloaded load) correct.

## Quiz / mastery correctness
- b03 [b] stampede + single-flight/early-recompute: correct; (a) penetration, (c) hot-key/TTL refuted correctly.
- b05 [a] penetration mechanism + null caching: correct; (b) RAM-wrong, (c) avalanche refuted correctly.
- b07 fill: "avalanche" + "random/jitter": correct; accept list covers VI/EN.
- b09 [b] hot key → local replica + key split: correct; (a) null-caching=penetration, (c) single-flight=stampede refuted correctly. Key distinction (hot key = hit, not expiry) made explicit.
- S079 (L1 recall): name 4 + when each occurs. Sensible.
- S080 (L2 gate): 3 observed symptoms → name + one direct fix each (avalanche/penetration/hot key). Good score-2 matching exercise; answers correct.
- S081 (L3 interview): e-commerce product page survives all 4 — name, where it appears in the design, fix applied, plus Redis-down fallback. Matches mastery_bar ("áp đúng vào thiết kế"); correct.

## Coverage discipline
Mastery items test only taught ideas (4 modes + fixes + fallback). No leakage.

## Language
Vietnamese clear; English terms parenthesised (thundering herd, cache stampede/penetration/avalanche, hot key, single-flight / request coalescing, null/negative caching, Bloom filter, TTL jitter, layered cache, circuit breaker, warm-up, key replication). Good.

## Findings
None blocking. Accurate and interview-correct.
