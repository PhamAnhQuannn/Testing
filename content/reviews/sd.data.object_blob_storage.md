# Review: sd.data.object_blob_storage

**Verdict: PASS** (độc lập) — chính xác kỹ thuật, cập nhật 2026, mọi con số đúng, không cần sửa.

## Kiểm tra con số (SPECIAL)
- Chép 3 bản = **3x** dung lượng, chịu mất **2** bản (còn 1 đọc được): đúng (b07, b08, b09, S060).
- Erasure coding 10+4 = 14 mảnh → 14/10 = **1,4x**, cần 10 mảnh bất kỳ nên chịu mất **4** mảnh: đúng và nhất quán ở mọi chỗ (objectives, b07, b08 quiz, b09 callout, b11 summary, S060).

## Nội dung & tính đúng
- b01-b02: định nghĩa object storage (key→object phẳng, metadata, HTTP, ghi đè cả object không sửa tại chỗ, 11 số 9 độ bền) — đúng, hiện hành.
- b03 quiz answer `[b]` đúng; giải thích (a) sai vì DB vẫn lưu được BLOB, (c) sai vì không sửa tại chỗ — chuẩn.
- b04-b06 presigned URL + multipart: luồng 4 bước đúng, b06 answer `[b]` đúng (app server chỉ ký + ghi metadata, không truyền byte).
- b08 answer `[a]` đúng; distractor (b) đúng là số của chép-3-bản, (c) sai về chịu lỗi — chuẩn.
- b10 CDN trước kho cho đọc nóng: hợp lý.

## Mastery items
- S058 diff1 (recall object storage + blob/DB split) — đúng cấp độ, chỉ test ý b01-b02.
- S059 diff2 (scenario presigned URL + multipart, score-2 gate) — đúng, chỉ test ý đã dạy.
- S060 diff3 (vẽ luồng + so sánh độ bền bằng con số) — khớp mastery_bar_vi; rubric chốt con số đúng (3x/2 lỗi, 1,4x/4 lỗi).
- answer_md và rubric_md của cả ba: chính xác, hợp lý.

## Ngôn ngữ
Tiếng Việt rõ, thuật ngữ English có mở ngoặc (object, key, bucket, presigned URL, multipart, erasure coding, parity shards, durability, CDN...). Đạt.

**MUST-FIX: none.**
