# Content gap report: system-design-primer vs. Prep App — track System Design (SD)

_Ngày: 2026-11-03. So sánh giáo trình `D:\system-design-primer` với track SD hiện có của Prep App
(`D:\preparing\Testing\content`). Chỉ phân tích + báo cáo; không sửa lesson/check/content._

## 1. Mục đích và bối cảnh

- Mục tiêu: tìm **chỗ trống nội dung (content gap)** giữa primer và track SD, để biết nên thêm bài tập
  nào. Primer là nguồn tham khảo kinh điển (18 topic lý thuyết + 8 case study HLD + 6 bài OOD/LLD).
- SD là **concept track**: bài tập chấm theo **điểm 0-3** qua check item kiểu `concept` / `read_code`
  (có `answer_md` + `rubric_md`), **không** phải `write_code`. Schema:
  `content/schemas/check.schema.json` (type `concept` bắt buộc `answer_md`; `read_code` bắt buộc
  `code` + `expected_output`). Mẫu rubric tốt: `content/checks_extra/ml.system_design.framework.yaml`.
- **Hiện trạng coverage rất rộng**: 86 lesson `published` trên 11 module, mỗi lesson trỏ tới 3 check
  item `mastery_check: {l1, l2, l3}` ở độ khó 1/2/3. **Mọi subtopic SD đã có concept item với rubric**
  (sinh ra ở `content/checks/sd.*.yaml` từ `source/assessment.json`, cộng bản author-added ở
  `content/checks_extra/sd.*.yaml`). Vì vậy gap **không** nằm ở "thiếu subtopic", mà ở (a) vài topic
  primer còn mỏng/ẩn trong lesson khác, (b) vài case study chưa có archetype riêng, (c) toàn bộ nhánh
  OOD/LLD chưa có.
- **Pipeline (ghi nhớ khi thêm item):** item mới đặt ở `content/checks_extra/<subtopic_id>.yaml`
  (cùng schema `subtopic_id` + `items`), rồi `make checks` chạy `tools/convert_checks.py` merge vào
  `content/checks/*`. **Không** sửa tay file sinh ra `content/checks/*` và **không** sửa
  `source/assessment.json`. Id phải không đụng assessment (assessment dùng `S###`, `Q`/`W` dành cho
  convert): dùng tiền tố khác, ví dụ `X001` (trùng id là lỗi validator).

## 2. Mapping 18 topic lý thuyết của primer → module SD

Nguồn: `D:\system-design-primer\README.md`, mục "Index of system design topics" + "How to approach".

| # | Primer section | App module/lesson | Covered | Ghi chú (mỏng/thiếu gì) |
|---|---|---|---|---|
| 1 | How to approach (4 bước + back-of-envelope) | `sd.framework.*` (6 lesson: overview, requirements, estimation, api_data_model, hld_diagram, deep_dive_tradeoffs) | **Yes** | Sâu hơn primer; khung 7 bước. |
| 2 | Performance vs scalability | `sd.fundamentals.scalability`, `sd.fundamentals.performance_metrics` | **Yes** | Vertical/horizontal + stateless + lộ trình 5 bước. |
| 3 | Latency vs throughput | `sd.fundamentals.performance_metrics` | **Yes** | |
| 4 | Availability vs consistency (CAP) | `sd.fundamentals.cap_consistency` | **Yes** | CP/AP có trong fundamentals + `distributed.*`. |
| 5 | Consistency patterns (weak/eventual/strong) | `sd.fundamentals.cap_consistency`, `sd.data.replication`, `sd.distributed.conflict_resolution` | **Yes** | |
| 6 | Availability patterns (fail-over, replication, "9s", in-seq vs in-parallel) | `sd.reliability_ops.fault_tolerance`, `sd.data.replication` | **Partial** | Thiếu rõ **active-passive vs active-active** và **toán số 9 (99.9%…), nhân availability nối tiếp/song song**. |
| 7 | Domain name system (DNS) | nhắc trong `sd.networking.load_balancing`, `sd.networking.service_discovery_mesh`, `sd.framework.hld_diagram` | **Partial** | Không có lesson/subtopic DNS riêng; thiếu round-robin/GeoDNS, latency/TTL, nhược điểm DNS. |
| 8 | Content delivery network (CDN) | `sd.caching.cdn` | **Yes** | Push vs pull CDN có. |
| 9 | Load balancer (L4/L7, active-*, horizontal) | `sd.networking.load_balancing` | **Yes** | |
| 10 | Reverse proxy (web server) | `sd.networking.reverse_proxy_gateway` | **Yes** | Có cả LB vs reverse proxy, API gateway. |
| 11 | Application layer (microservices, service discovery) | `sd.networking.service_discovery_mesh`, nhiều `sd.archetypes.*` | **Yes** | |
| 12 | Database (RDBMS, replication, federation, sharding, denormalization, SQL tuning; NoSQL 4 họ; SQL-or-NoSQL) | `sd.data.sql_vs_nosql`, `sd.data.sharding`, `sd.data.replication`, `sd.data.data_modeling`, `sd.technologies.stores` | **Partial** | NoSQL 4 họ + SQL-or-NoSQL + scale limit **rất mạnh**. Thiếu/mỏng: **federation (functional partitioning)**, **denormalization**, **SQL tuning** (index, query cache, schema) chưa được gọi tên như topic riêng. |
| 13 | Cache (các tầng + 4 policy ghi) | `sd.caching.patterns`, `sd.caching.eviction_invalidation`, `sd.caching.distributed_cache`, `sd.caching.failure_modes`, `sd.caching.cdn` | **Yes** | cache-aside/write-through/write-behind/refresh-ahead có; thêm thundering herd/stampede. |
| 14 | Asynchronism (message queue, task queue, back pressure) | `sd.async.*` (7 lesson: queues_pubsub, task_workers, delivery_guarantees, kafka_log, stream_processing, batch_processing, event_driven_patterns) | **Yes** | Sâu hơn primer nhiều. |
| 15 | Communication (HTTP, TCP, UDP, RPC, REST) | `sd.api.api_styles`, `sd.networking.realtime_protocols` | **Yes** | REST/RPC/gRPC + WebSocket/SSE/long-poll. |
| 16 | Security | rải rác: `sd.archetypes.identity_auth`, `sd.framework.requirements`, `sd.networking.*` | **Partial** | Không có lesson security riêng (TLS, authn/authz, rate-limit ở edge, OWASP). _Lưu ý: mục Security của primer cũng chỉ là stub "under development"._ |
| 17 | Appendix (powers of two, latency numbers) | `sd.framework.estimation` | **Yes** | Có bảng lũy thừa 2 + latency numbers + back-of-envelope. |
| 18 | NoSQL chi tiết (KV/document/wide-column/graph) | `sd.data.sql_vs_nosql`, `sd.data.consistent_hashing`, `sd.technologies.stores` | **Yes** | Đủ 4 họ kèm ví dụ (Redis/Mongo/Cassandra/Neo4j) + giới hạn quy mô. |

**Kết luận mục 2:** lý thuyết cốt lõi gần như phủ hết và thường **sâu hơn** primer (async, data, framework).
Bốn chỗ còn mỏng: **DNS**, **availability patterns (failover modes + toán số 9)**, **federation/
denormalization/SQL tuning**, **security**.

## 3. Case study primer → archetype App

### 3.1. 8 case study HLD (`solutions/system_design/*`)

| Primer case study | Archetype/lesson App tương ứng | Covered | Gap |
|---|---|---|---|
| Pastebin.com (or Bit.ly) | `sd.archetypes.url_shortener` (S169-171), `sd.archetypes.object_store` | **Partial** | Phần Bit.ly đủ (counter+base62, 301/302, cache). Thiếu phần **Pastebin thuần**: lưu blob paste lớn ở object store + expiry + analytics như một luồng riêng. |
| Twitter timeline & search | `sd.archetypes.news_feed`, `sd.archetypes.search_engine`, `sd.archetypes.typeahead` | **Yes** | Fan-out-on-write vs read đã có trong news_feed. |
| Web crawler | `sd.archetypes.web_crawler` | **Yes** | Trùng khớp hoàn toàn (đã có concept item). |
| Mint.com | — (không có archetype) | **No** | Không có archetype **tổng hợp tài khoản tài chính** (account aggregation, phân loại giao dịch, cảnh báo ngân sách, batch category). Gần nhất chỉ là `sd.archetypes.data_pipeline`. |
| Social network data structures | — (gần: `sd.archetypes.likes_comments`, `news_feed`) | **No** | Thiếu bài **social graph**: mô hình đồ thị bạn bè, **BFS tìm đường ngắn nhất giữa 2 người**, sharding đồ thị. (Graph DB có nhắc ở `sd.data.sql_vs_nosql` nhưng không có bài thiết kế.) |
| KV cache cho web queries (query_cache) | `sd.archetypes.kv_store`, `sd.caching.distributed_cache`, `sd.caching.patterns` | **Yes** | LRU + hashing + eviction đã có. |
| Amazon sales rank by category | gần: `sd.archetypes.leaderboard`, `sd.archetypes.ad_click_aggregation`, `sd.data.analytics_storage` | **Partial** | Leaderboard là realtime; thiếu luồng **batch MapReduce xếp hạng theo category** (đọc log bán hàng → tổng hợp định kỳ). |
| Scale to millions on AWS | `sd.fundamentals.scalability`, `sd.reliability_ops.*`, `sd.archetypes.cloud_compute` | **Yes** | Lộ trình tiến hóa hạ tầng đã có trong fundamentals + reliability_ops. |

### 3.2. 6 bài OOD/LLD (`solutions/object_oriented_design/*`)

| Primer OOD | Có bài App? | Gap |
|---|---|---|
| hash_table | một phần `dsa.arrays_strings.hash_tables` (góc DSA, không phải OOD) | **No (OOD)** |
| lru_cache | một phần ở DSA/`sd.archetypes.kv_store` (concept HLD, không phải thiết kế lớp) | **No (OOD)** |
| call_center | — | **No** |
| deck_of_cards | — | **No** |
| parking_lot | — | **No** |
| online_chat | gần: `sd.archetypes.chat_presence` (HLD, không phải LLD lớp) | **No (OOD)** |

**Kết luận mục 3:** track SD **không có nhánh OOD/LLD** nào. Đây là gap mang tính cấu trúc: cả 6 bài
đều chưa có bài tập thiết kế **lớp/quan hệ (class design)** — dạng phù hợp với `read_code` (đưa code
lớp sẵn để phê bình/trace) hoặc `concept` (rubric chấm thiết kế lớp). Cũng chưa có bài tận dụng 3 bộ
Anki `resources/flash_cards/*.apkg` (OO Design, System Design, System Design Exercises) làm nguồn
prompt nhanh độ khó 1.

## 4. Backlog ưu tiên (concept/read_code + rubric cần thêm)

Mọi item mới → `content/checks_extra/<subtopic_id>.yaml`, id `X###` (tránh đụng `S/Q/W`), rồi
`make checks`. Hầu hết nên là `type: concept` (thiết kế thì chấm rubric hợp hơn trace output).

| # | Việc thêm | Đặt vào (subtopic) | Nguồn primer seed | Loại | Effort |
|---|---|---|---|---|---|
| P1 | DNS: round-robin/GeoDNS, TTL/latency, nhược điểm DNS | `sd.networking.service_discovery_mesh` hoặc tạo lesson `sd.networking.dns` | README "Domain name system" | concept x1-2 | **S** |
| P2 | Availability patterns: active-passive vs active-active, **toán số 9** + availability nối tiếp/song song | `sd.reliability_ops.fault_tolerance` | README "Availability patterns" / "Availability in numbers" | concept x1-2 | **S** |
| P3 | Federation (functional partitioning) + denormalization + SQL tuning (index/query cache) | `sd.data.sharding`, `sd.data.data_modeling` | README "Database" (federation, denormalization, SQL tuning) | concept x2 | **S-M** |
| P4 | Security cơ bản: TLS, authn/authz, rate-limit ở edge, input sanitize/OWASP | `sd.archetypes.identity_auth` hoặc `sd.networking.reverse_proxy_gateway` | README "Security" (stub) + kiến thức ngoài | concept x1-2 | **M** (primer mỏng, cần nguồn ngoài) |
| P5 | Pastebin thuần: blob store cho paste lớn + expiry + đếm view async | `sd.archetypes.url_shortener` hoặc `sd.archetypes.object_store` | `solutions/system_design/pastebin` | concept x1 | **M** |
| P6 | Sales-rank-by-category: batch/MapReduce tổng hợp log bán → xếp hạng theo category | `sd.archetypes.leaderboard` hoặc `sd.data.analytics_storage` | `solutions/system_design/sales_rank` | concept x1 | **M** |
| P7 | Social graph: mô hình đồ thị + **BFS đường ngắn nhất giữa 2 user** + sharding graph | tạo `sd.archetypes.social_graph` (hoặc mở rộng `likes_comments`) | `solutions/system_design/social_graph` | concept x1-2 | **M** |
| P8 | Mint.com: aggregation tài khoản + phân loại giao dịch + ngân sách/alert | tạo `sd.archetypes.finance_aggregation` (hoặc mở rộng `data_pipeline`) | `solutions/system_design/mint` | concept x1-2 | **L** |
| P9 | OOD/LLD: 6 bài (parking_lot, call_center, deck_of_cards, online_chat, lru_cache, hash_table) dạng thiết kế lớp | **nhánh mới** `lld.*` (quyết định track) hoặc `read_code` items | `solutions/object_oriented_design/*` + Anki "OO Design" | read_code/concept | **L** (cần quyết định có mở track LLD) |

Thứ tự đề xuất: P1→P2→P3 (vá nhanh lý thuyết mỏng, effort S), rồi P5→P6→P7 (case study có sẵn chỗ
nhét), cuối là P4/P8/P9 (cần nguồn ngoài hoặc quyết định cấu trúc track).

## 5. Tóm tắt 5 gap lớn nhất

1. **OOD/LLD hoàn toàn trống** — cả 6 bài object-oriented design của primer (parking_lot, call_center,
   deck_of_cards, online_chat, lru_cache, hash_table) chưa có bài thiết kế lớp nào trong track SD;
   cần quyết định mở nhánh `lld.*` hay thêm `read_code` items (effort L).
2. **4 case study HLD thiếu/mỏng** — Mint.com (**No**), social graph + BFS giữa 2 user (**No**),
   sales-rank-by-category batch (**Partial**), Pastebin thuần ngoài phần Bit.ly (**Partial**).
3. **DNS** chưa có subtopic riêng — chỉ nhắc rải rác; thiếu round-robin/GeoDNS, TTL, nhược điểm DNS.
4. **Availability patterns mỏng** — thiếu active-passive vs active-active và **toán số 9**
   (99.9%…, nhân availability nối tiếp/song song) ở `sd.reliability_ops.fault_tolerance`.
5. **Database (federation/denormalization/SQL tuning)** và **Security** chưa được gọi tên như topic
   riêng (NoSQL/sharding thì đã rất mạnh; Security của chính primer cũng chỉ là stub).

_Lưu ý ngược lại: nhiều module App **vượt** primer (async 7 lesson, framework 7 bước, data với 4 họ
NoSQL + scale limit, 35 archetype) — primer không phải superset của App._
