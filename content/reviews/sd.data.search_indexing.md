# Review: sd.data.search_indexing

**Verdict: PASS** (độc lập) — chính xác, cập nhật 2026, không có con số sai, không cần sửa.

## Nội dung & tính đúng
- b01-b02 B-tree chỉ nhanh tiền tố (`LIKE 'x%'`), từ ở giữa (`LIKE '%x%'`) quét toàn bảng; inverted index = term→posting list, truy vấn nhiều từ = giao danh sách: đúng. Ví dụ D1/D2/D3 và phép giao `{D1,D2}∩{D1,D3}={D1}` chính xác.
- b03 analysis (tokenization, normalization, stop words, stemming) + "cùng bộ phân tích cho index lẫn query, đổi thì reindex": đúng.
- b04 quiz answer `[a]` đúng; (b)/(c) bác chuẩn.
- b05-b06 BM25 ở mức ý tưởng (TF tăng giảm dần, document frequency thấp = từ hiếm = điểm cao, length normalization): đúng; b06 answer `[a]` đúng (từ hiếm tăng điểm), (b)/(c) bác chuẩn.
- b07-b08 CDC (nghe WAL/binlog, cập nhật bất đồng bộ → eventual consistency, index là bản phụ, DB gốc là sự thật): đúng; b08 answer `[a]` đúng, (b)/(c) bác chuẩn.
- b09-b10 shard (chia dữ liệu, scatter-gather) vs replica (throughput đọc + chịu lỗi): đúng; b10 answer `[a]` đúng, (b) đảo vai trò, (c) sai.
- **Currency**: Elasticsearch/OpenSearch (fork, Lucene), BM25 là mặc định Elasticsearch — đúng 2026.

## Mastery items
- S064 diff1 (inverted index là gì, vì sao hơn B-tree) — recall, đúng cấp.
- S065 diff2 (ES↔Postgres: CDC, eventual consistency, đọc bài vừa tạo từ DB gốc) — scenario, chỉ test ý đã dạy.
- S066 diff3 (thiết kế tìm kiếm đủ 4 lớp: inverted index, BM25, CDC, shard/replica) — khớp mastery_bar_vi; answer_md + rubric chính xác.

## Ngôn ngữ
Tiếng Việt rõ, thuật ngữ English mở ngoặc (inverted index, posting list, tokenization, stemming, BM25, CDC, shard, replica, scatter-gather). Đạt.

**MUST-FIX: none.**
