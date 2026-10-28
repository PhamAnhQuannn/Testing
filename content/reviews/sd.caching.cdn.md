# Review: sd.caching.cdn (independent reviewer pass)

**Verdict: OK** (no must-fix; egress arithmetic verified correct)

11 blocks; graded: b03 (mcq), b05 (fill), b08 (mcq). mastery_check l1 [S085], l2 [S086], l3 [S087].
mastery_bar_vi: "thiết kế chiến lược CDN (cache key, TTL, cách cập nhật file) cho web hoặc video và ước tính chi phí egress" — S087 covers all.

## Technical accuracy (verified)
- CDN = edge/PoP replicas of static/media near users; origin = source. Two benefits (latency, origin offload); first-request miss (pull from origin, keep), later hit. Correct.
- Pull (edge pulls on first miss — default, user-generated/large unknown-hot) vs push (pre-push important rarely-changing files). Correct.
- Cache key = URL (+ meaningful query string; `Vary` adds headers e.g. Accept-Encoding; drop meaningless query to protect hit ratio). Correct.
- `Cache-Control: max-age` = TTL; on expiry revalidate with ETag → 304 Not Modified (no body). Correct.
- File update: versioned/fingerprinted URL (`app.9f3c1a.js`, immutable, very long TTL, new URL = new cache key) as the default; purge/invalidation only for emergencies (slow propagation, metered/limited). Correct.
- Web asset (fingerprint + very long TTL; HTML short TTL/revalidate) vs video (HLS/DASH segments, each immutable → long TTL; manifest ABR; live manifest short TTL, VOD long). Correct.

## Egress arithmetic (RE-CHECKED — all correct)
- Lesson b10: 100 TB = 100,000 GB; CDN 100,000 × $0.05 = **$5,000**; 95% hit → origin 5% = 5,000 GB × $0.09 = **$450**; no-CDN 100,000 × $0.09 = **$9,000**. All correct and internally consistent.
- S087: 200 TB = 200,000 GB; CDN 200,000 × $0.05 = **$10,000**; 90% hit → origin 10% = 20,000 GB × $0.09 = **$1,800**; no-CDN 200,000 × $0.09 = **$18,000**. All correct.
- Model (origin serves only the miss fraction of bytes; CDN and origin per-GB prices differ) is a sound teaching approximation, stated as such.

## Quiz / mastery correctness
- b03 [b] user-upload avatars → pull CDN: correct; (a) push-waste, (c) "private so no CDN" refuted correctly (signed URL noted).
- b05 fill: TTL + cache key: correct; accept lists cover variants.
- b08 [b] fingerprint + long TTL vs purge-every-deploy: correct; (a) purge-free/instant and (c) short-TTL-faster refuted correctly.
- S085 (L1 recall): CDN + 2 benefits + miss vs hit. Sensible.
- S086 (L2 gate): stale `app.js` — why (TTL/max-age), fingerprint fix (new URL = new cache key, long TTL), when to purge. Good score-2; answer correct. (Note: S086 itself has no egress numbers — the arithmetic lives in b10 + S087, both verified.)
- S087 (L3 interview): full CDN strategy (cache key/TTL/update, pull/push) + egress estimate 200 TB. Matches mastery_bar; numbers correct.

## Coverage discipline
Mastery items test only taught ideas (pull/push, cache key, TTL/ETag, fingerprint/purge, egress). No leakage.

## Language
Vietnamese clear; English terms parenthesised (CDN, edge/PoP, origin, pull/push, cache key, Cache-Control/max-age, TTL, ETag, 304, fingerprint/cache busting, purge/invalidation, HLS/DASH, segment, manifest, ABR, egress, signed URL). Good.

## Findings
None blocking. Accurate; all egress numbers correct.
