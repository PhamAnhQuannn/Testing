# Review: sd.data.probabilistic_structures

**Verdict: PASS** (độc lập) — chính xác, mọi con số đã tính lại và đúng, không cần sửa.

## Kiểm tra con số (SPECIAL — tính lại từng cái)
- Bloom m/n = −ln(p)/(ln2)², (ln2)² ≈ 0,48:
  - p=1% → −ln(0,01)/0,48 = 4,6/0,48 = **9,585 ≈ 9,6 bit/phần tử**: đúng.
  - p=0,1% → 6,9/0,48 = **14,38 ≈ 14,4 bit/phần tử**: đúng.
  - Mỗi lần giảm p 10× thêm ln(10)/0,48 ≈ **4,79 ≈ 4,8 bit**: đúng (b03).
- k tối ưu = (m/n)·ln2: 9,6×0,69 = 6,64 ≈ **7** (p=1%); 14,4×0,69 = 9,97 ≈ **10** (p=0,1%): đúng.
- Cỡ dẫn xuất:
  - 10 tỉ URL @1% = 10¹⁰×9,6/8 = **12 GB**: đúng (b03, b09).
  - 1 tỉ khóa @0,1% = 10⁹×14,4/8 = **1,8 GB**: đúng (b11 answer `[a]`).
  - 2 tỉ sự kiện @1% = 2×10⁹×9,6/8 = **2,4 GB**, k≈7: đúng (S072).
  - 100 triệu ID × 8 byte = **800 MB**: đúng (b05).
- HyperLogLog: ~**2% sai số** trong ~**1,5 KB**, không phụ thuộc số phần tử — khớp con số kinh điển của bài báo HyperLogLog gốc (Flajolet), nằm trong khoảng chấp nhận 1-2%: đúng.
- Count-Min Sketch: **đếm dư, không đếm thiếu**, hỏi lấy **min**: đúng.

## Nội dung & tính đúng
- b02 Bloom: no false negative (bit chỉ bật), false positive tỉ lệ p, không xóa được (Counting Bloom để xóa): đúng.
- b04 answer `[a]` đúng (false positive, không false negative); (c) false negative sai, (b) "hỏng" sai.
- b05-b06 HLL (trực giác tung đồng xu 2²⁰≈1 triệu, nhớ số 0 đầu dài nhất, nhiều register lấy trung bình, gộp được, không liệt kê lại): đúng; b06 answer `[b]` đúng, (a) 800MB thừa, (c) sai mục đích.
- b07-b08 CMS (d hàng, +1 mỗi hàng, hỏi lấy min, over-count; top-K = CMS + heap): đúng; b08 answer `[a]` đúng, (b) ngược dấu, (c) sai.
- b09-b10 bảng chọn + ứng dụng (crawler dedup, cache penetration, unique viewers, top-K) + giới hạn "không dùng làm nguồn sự thật cho số tính tiền": đúng.

## Mastery items
- S070 diff1 (ghép 3 câu hỏi ↔ 3 cấu trúc) — recall, đúng cấp.
- S071 diff2 (crawler Bloom: no false negative, hậu quả false positive, chọn p~1%) — scenario, chỉ test ý đã dạy.
- S072 diff3 (unique→HLL, top-K→CMS+heap, dedup→Bloom + tính cỡ 2,4 GB + giới hạn tính tiền) — khớp mastery_bar_vi; answer_md con số đúng, rubric chốt cỡ Bloom đúng.

## Ngôn ngữ
Tiếng Việt rõ, thuật ngữ English mở ngoặc (Bloom filter, false positive/negative, HyperLogLog, cardinality, Count-Min Sketch, heavy hitters, heap). Đạt.

**MUST-FIX: none.**
