# Review: sd.data.data_modeling (independent reviewer pass)

**Verdict: OK** (no must-fix; clean)

12 blocks; graded: b03 (mcq), b05 (mcq), b07 (mcq), b09 (mcq). mastery_check l1 [S046], l2 [S047], l3 [S048].
mastery_bar_vi: "từ 3 truy vấn viết bảng + index, chỉ rõ chỗ phi chuẩn hóa và đánh đổi, dùng UNIQUE chặn đặt trùng" — S048 covers all four.

## Technical accuracy (verified)
- Access-pattern-first design framed correctly ("model for how you read").
- Relationship modelling correct: one-to-many → FK on the "many" side; many-to-many → junction table with two-column PK (`follows`, `likes`).
- Normalization vs denormalization trade-off correct: write amplification + update anomaly as the price; "normalize first, denormalize when join is a measured bottleneck". Correct.
- Composite index `(user_id, created_at)` and column-order reasoning correct (filter then sort); "index not free, slows writes" correct.
- UNIQUE as a data-layer invariant beating app-level check-then-insert (race condition) — correct and well-argued.

## Quiz / mastery correctness
- b03 [b] junction table for follow: correct; (a) one FK only one-to-many, (c) comma-list anti-pattern correctly refuted.
- b05 [b] denormalization cost = write amplification + update anomaly: correct; (a) inverted, (c) false correctly refuted.
- b07 [b] `(user_id, created_at)`: correct; (a) created_at-only and (c) full scan refuted correctly.
- b09 [b] UNIQUE(room_id, night): correct; (a) race window, (c) app-queue correctly refuted.
- S046 (L1 recall): access-pattern design vs clean-first. Sensible.
- S047 (L2 gate): denormalize author_name — name it, two costs, when worth it. Good gate.
- S048 (L3 interview): 3 queries → tables (incl. junction), index + column order, one denormalization point + trade-off, UNIQUE for dup-like. Matches mastery_bar; answers correct.

## Coverage discipline
Mastery items test taught ideas. Minor: S048(3) uses a `like_count` counter column; the lesson body teaches denormalization generically (author_name example) but not the counter pattern explicitly (it is in index concepts_vi). It is a direct application of the taught trade-off, so acceptable — noted, not blocking.

## Language
Vietnamese clear; English terms parenthesised (foreign key, junction table, normalization/denormalization, write amplification, update anomaly, index, UNIQUE, race condition). Good.

## Findings
None blocking. Accurate and interview-correct.
