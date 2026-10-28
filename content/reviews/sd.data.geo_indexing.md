# Review: sd.data.geo_indexing

**Verdict: PASS** (độc lập) — chính xác, cập nhật 2026, con số đúng, không cần sửa.

## Kiểm tra con số
- 1 triệu tài xế / 4 giây ≈ **250.000 ghi/giây**: đúng (b08, S069).
- Ô biên: ô của mình + **8 ô kề** = **3×3 = 9 ô**: đúng (b06, b07, S068, S069).

## Nội dung & tính đúng
- b01 B-tree hỏng cho 2D (sắp một chiều, điểm cùng vĩ độ "kề nhau" dù xa; chỉ mục ghép (lat,lng) cũng không thành khoảng liên tục): đúng. Ý tưởng chung chia ô có tên: đúng.
- b02-b03 geohash (xen kẽ bit → base32, tiền tố = ô bao, chung tiền tố dài ⇒ gần; Redis GEO dùng geohash): đúng. b03 answer `[a]` đúng, (b)/(c) bác chuẩn. Ví dụ phân cấp `w3gv ⊃ w3gvk ⊃ w3gvk7` đúng (chuỗi dài hơn = ô nhỏ hơn).
- b04-b05 quadtree (chia 4, chia tiếp ô đông ⇒ adaptive theo mật độ, cây động) và S2 (phủ mặt cầu, Hilbert curve, id 64-bit, lân cận tốt; H3 lục giác): đúng, hiện hành. b05 answer `[a]` đúng.
- b06-b07 boundary cell problem + lọc khoảng cách thật + chọn cỡ ô ~ bán kính: đúng. b07 answer `[a]` đúng, (b)/(c) bác chuẩn.
- b08 moving objects: giữ vị trí mới nhất trong RAM/ghi đè, không ghi lịch sử vào DB chính; lưới cố định (geohash/S2) cập nhật rẻ hơn quadtree (phải tách/gộp nút): đúng.

## Mastery items
- S067 diff1 (B-tree 2D + ý tưởng chia ô) — recall, đúng cấp.
- S068 diff2 (geohash bỏ sót quán 50m → boundary cell, sửa bằng 8 ô kề, lọc khoảng cách thật) — scenario, chỉ test ý đã dạy.
- S069 diff3 (gọi xe 1M/4s: chọn cấu trúc theo ràng buộc, ô biên cho k-nearest, tải cập nhật) — khớp mastery_bar_vi; answer_md + rubric chính xác (gồm nới vòng ô khi thiếu k).

## Ngôn ngữ
Tiếng Việt rõ, thuật ngữ English mở ngoặc (geohash, quadtree, S2, Hilbert curve, boundary cell, adaptive, k-nearest, Redis GEO). Đạt.

**MUST-FIX: none.**
