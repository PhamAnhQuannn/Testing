# Review: sd.archetypes.web_crawler

**Verdict: APPROVE** (no must-fix). Reviewer: independent content pass, 2026-10-27.

## Technical accuracy & currency
- Crawler-as-BFS framing + four blocks (URL frontier, fetcher workers, dedup, store) correct.
- **URL frontier + per-domain politeness verified**: durable queue, per-domain sub-queues + per-domain rate limit (avoid DoS-ing a host), scheduler picks next host. Correct and current.
- Fetcher workers stateless, scale by adding machines; **DNS caching** correctly flagged as an easily-missed bottleneck (resolve by TTL in local cache/resolver). Correct.
- **Bloom-filter URL dedup verified and consistent with sd.data.probabilistic_structures**: membership structure, false positive possible / no false negative; FP consequence correctly stated as skipping a new page (not duplicate fetch, not infinite loop); paired with an exact store (on-disk/DB hash) when certainty needed. Error direction correct throughout.
- **robots.txt** (fetch + cache per domain, respect before fetching) correct. Content dedup: hash for exact duplicates, simhash for near-duplicates — correct. **Crawler traps** (infinite spaces: calendars, nested URLs) -> depth cap + per-domain URL cap + repeated-pattern detection — correct. Re-crawl by change frequency (freshness vs cost) correct.
- **Fetcher estimate verified**: 1,000 pages/s, 0.2 s/fetch -> 1/0.2 = 5 pages/s per fetcher -> 1,000/5 = 200 fetchers (Little's Law L = 1000 x 0.2 = 200 concurrent). Correct, incl. "throughput bound by I/O parallelism, not CPU".

## Checks
- Quiz b03 (b, per-domain queue for politeness), b06 (b, FP -> skip a page, acceptable), b08 fill (Bloom filter / false negative) — all answers + explanations correct. b06 distractor (a) correctly labeled as wrong error-direction.
- S184 diff1 recall (frontier + politeness): correct; rubric sensible.
- S185 diff2 score-2 scenario (billion-URL seen-set): answer correct (Bloom filter, FP not FN, skip a page acceptable); rubric correctly penalizes reversing the error direction.
- S186 diff3 interview: matches mastery_bar level 3 (per-site frontier, URL + content dedup, re-crawl policy, fetcher count). Rubric aligns, incl. the exact ~200 fetcher result. Good.

## Pedagogy / language
- Reuses prerequisites (probabilistic_structures, queues_pubsub) by applying; Bloom filter explicitly cited back to sd.data.probabilistic_structures, not re-taught.
- Vietnamese clear; English terms parenthesized consistently.

No corrections required.
