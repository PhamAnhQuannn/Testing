# Review: sd.caching.patterns (independent reviewer pass)

**Verdict: OK** (no must-fix; clean)

10 blocks; graded: b03 (mcq), b05 (mcq), b07 (fill), b09 (mcq). mastery_check l1 [S073], l2 [S074], l3 [S075].
mastery_bar_vi: "chọn pattern cache theo tỉ lệ đọc/ghi, tính được hit ratio cần đạt và nêu rủi ro mất dữ liệu của write-back" — S075 covers all three.

## Technical accuracy (verified)
- Read patterns correct: cache-aside (lazy load, app controls, survives cache death by reading DB; first read misses) vs read-through (cache/provider loads on miss; on critical path). Correct.
- Write patterns correct: write-through (sync cache+DB, consistent, slower write), write-back/write-behind (cache first, ack early, batch to DB → fast but data loss if cache dies before flush; DB temporarily stale), write-around (write DB only, cache filled later by read path). All accurate.
- Hit-ratio formula hit ≥ 1 − (DB capacity / total read load) correct.
  - b06 example: 20,000 reads/s, DB 2,000/s → miss ≤ 10% → hit ≥ 90%. Correct.

## Quiz / mastery correctness
- b03 [b] cache-aside safe default (survives cache death): correct; (a) hit-ratio-not-pattern and (c) write-through-consistency refuted correctly.
- b05 [b] write-back signature risk = acked writes lost if cache dies pre-flush: correct; (a)=write-through, (c) wrong refuted correctly.
- b07 fill: 10,000 reads/s, DB 500/s → miss ≤ 5% → hit ≥ 95%. Correct; regex/accept list handles "95%", "0.95", ">=95%".
- b09 [b] view-counter → write-back: correct; (a) write-through too slow, (c) write-around doesn't reduce write load refuted correctly.
- S073 (L1 recall): cache-aside vs write-through read/write distinction. Sensible.
- S074 (L2 gate): product page read-heavy + must-see-new-price → cache-aside + write-through (or write+invalidate), plus write-back risk. Good scenario, score-2 level. Answer correct.
- S075 (L3 interview): 40,000/4,000 → hit ≥ 90% (formula shown), cache-aside + write-back by r/w ratio, write-back loss + mitigation. Arithmetic correct, matches mastery_bar.

## Coverage discipline
Mastery items test only taught ideas (patterns, hit-ratio formula, write-back loss). No leakage.

## Language
Vietnamese clear; English terms parenthesised (cache-aside/lazy loading, read-through, write-through/back/behind/around, hit ratio, read/write ratio, flush, ack). Good.

## Findings
None blocking. Accurate and interview-correct.
