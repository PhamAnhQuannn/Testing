# Review: sd.archetypes.url_shortener

**Verdict: APPROVE** (no must-fix). Reviewer: independent content pass, 2026-10-27.

## Technical accuracy & currency
- 4-step frame (requirements+estimation -> API+data model -> read/write flows -> archetype-specific decisions) is correct and current for 2026.
- Estimation verified: 100e6/(30x86400) = 38.6 -> ~40 writes/s; 100:1 -> ~4,000 reads/s; 6e9 records x 500 B = 3e12 = 3 TB. All exact.
- **length math verified**: 62^7 = 3,521,614,606,208 ~= 3.5e12 ("3,5 nghìn tỷ"). Correct Vietnamese (nghìn tỷ = 10^12), and > 6e9 links. Good.
- counter+base62 (unique, guessable, counter bottleneck -> range allocation / key-generation service / pre-generated keys) vs hash+collision-check: correct.
- **301 vs 302 verified**: 302 keeps server in loop -> analytics/control; 301 browser-cached -> loses click counting. Recommends 302 for analytics. Correct.
- read-heavy -> cache-aside + CDN/edge + key-value store (lookup by primary key): correct and matches special check. Click counting pushed to queue/async: correct.

## Checks
- Quiz b06 (b, counter uniqueness vs hash collision), b08 (b, 302 for counting), b09 fill (read-heavy / cache / key-value) — all answers + explanations correct.
- S169 diff1 recall: correct; rubric requires uniqueness reason + one drawback + 62^7 number. Sensible.
- S170 diff2 score-2 scenario (100:1 + click counting): answer correct (cache-aside, 302, async queue); rubric sensible.
- S171 diff3 interview: matches mastery_bar level 3 (self-draw create->redirect flow, non-colliding code gen with length math, 301 vs 302). Rubric aligns. Good.

## Pedagogy / language
- Reuses prerequisites (estimation, caching.patterns, sql_vs_nosql) by naming/applying, not re-teaching.
- Vietnamese clear; English terms parenthesized consistently.

No corrections required.
