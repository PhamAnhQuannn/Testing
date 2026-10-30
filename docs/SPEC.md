# SPEC: Ứng dụng học và luyện phỏng vấn cá nhân ("Prep App")

Phiên bản 0.7 · 2026-10-24 (v0.7: sửa theo review v0.6, xem cuối `review.md`; v0.6: thêm quy trình từ lần mở đầu tiên, đánh giá trình độ đầu vào, lưu và tiếp tục sau khi tắt máy, xem `UI_SPEC.md` và `review.md`; v0.4 học tự do nhịp độ của Quan, v0.5 sửa theo re-check) · Chủ sở hữu: Quan · Ngôn ngữ tài liệu: tiếng Việt (thuật ngữ, code, tên field, đường dẫn giữ tiếng Anh)

Tài liệu này mô tả sản phẩm và kiến trúc. Không chứa code ứng dụng. **Quy trình từ lần mở đầu tiên, đánh giá trình độ đầu vào (placement), toàn bộ UI từng màn hình và cơ chế lưu/tiếp tục sau khi tắt máy nằm ở [`UI_SPEC.md`](UI_SPEC.md)** (luật điểm, mở khoá, Leitner vẫn chỉ định nghĩa ở mục 5 của tài liệu này). Mọi quyết định ở đây là mặc định đã chọn; chỉ những điểm còn thật sự mở mới nằm ở mục 8.

## Tóm tắt 2 phút

- **Vòng lặp**: học một lesson ngắn (8-15 phút) → gõ code ngay cạnh bài → kiểm tra (quiz, Submit hidden test, mastery check) → ôn lặp ngắt quãng. Đơn vị duy nhất là một **subtopic** (mục nhỏ), 40 mục ở MVP.
- **Điểm 0-3 mỗi mục**: 0 chưa học · 1 đã đọc lesson và quiz đạt ≥ 70% · 2 làm được bài cơ bản **sạch** (xem định nghĩa dưới) · 3 làm được bài mức phỏng vấn **và** còn nhớ sau ≥ 7 ngày (nên không thể đạt trong ngày học đầu). Không có nút tự chấm; điểm chỉ lên khi có sự kiện đo được và **không tự giảm**.
- **Mở khoá**: mục sau mở khi mọi mục tiền đề đạt điểm 2, hoặc khi Quan "Test out" (làm thẳng bài kiểm tra mức 2). Mở rồi là **mở luôn**, không bị khoá lại. Mục khoá vẫn đọc xem trước được.
- **Ôn tập**: 5 hộp Leitner, lần ôn lúc D+1, D+3, D+7, D+14, D+28 kể từ ngày học, sau đó mỗi 30 ngày. Khoảng cách tính theo **ngày lịch** vì đó là quy luật quên, không phải khối lượng việc. **Không có trần thẻ/ngày**: mọi thẻ đến hạn đều hiện, quá hạn nhiều nhất trước; làm bao nhiêu tuỳ ý, thẻ chưa làm vẫn đến hạn và không bị phạt.
- **Nhịp học tự do**: app không có số lượng cố định mỗi ngày; có ngày học nhiều, có ngày học ít, có ngày nghỉ. Plan 30 ngày chỉ là **thứ tự gợi ý** của subtopic/bài, không phải lịch. Màn chính là "Học tiếp" (việc kế tiếp theo thứ tự plan + thẻ đến hạn + bài gợi ý); không có ngân sách giờ, không có thông báo "trễ lịch", không có streak phạt ngày học nhẹ.
- **Bắt đầu và tiếp tục**: lần đầu mở app đi qua hồ sơ ngắn rồi (tuỳ chọn) bài đánh giá trình độ 30-45 phút, thích nghi theo đồ thị tiền đề, chỉ gieo điểm bằng đúng luật mục 5 (đậu mức 2 sạch = điểm 2, không bao giờ gieo điểm 3). Mọi tiến độ ghi ngay vào SQLite; nháp code có bản sao IndexedDB và hàng đợi gửi lại, backup tự động, docker tự khởi động lại; mở app lại là banner "Tiếp tục nơi bạn dừng" (mục 5.6, 6.7, `UI_SPEC.md`).
- **Chạy code**: Python chạy ngay trong trình duyệt (Pyodide, tự host), chấm tức thì, không cần máy chủ chấm.
- **Từ cần biết**: *AC* = Accepted (qua hết hidden test) · *WA* = Wrong Answer · *TLE* = Time Limit Exceeded · *RE* = Runtime Error · *CE* = Compile Error · *clean* = AC mà không xem lời giải, dùng ≤ 1 gợi ý và không quá 1,5 lần thời gian mục tiêu · *mastery check* = bài kiểm tra theo mức 1-3 lấy từ `assessment.json` · *hidden test* = test ẩn chỉ tải về lúc Submit. Ví dụ tính điểm cụ thể ở mục 5.2.

---

## 1. Mục tiêu & phạm vi

### 1.1 Mục tiêu

Quan là người gần như mới bắt đầu, chuẩn bị phỏng vấn Meta intern/new-grad SWE và AI engineer (Python trước, Java sau). Bộ dữ liệu đã có (cây kiến thức 530 mục, kế hoạch 30 ngày, 254 item đánh giá, 10.888 câu hỏi thật) nhưng đang là file tĩnh. App biến chúng thành một vòng lặp học theo nhịp riêng của Quan (không có định mức mỗi ngày):

```
 học (lesson ngắn) ──► luyện (code ngay cạnh bài) ──► kiểm tra (quiz + Submit hidden test + mastery check)
        ▲                                                         │
        └────────── ôn lặp ngắt quãng (review queue) ◄────────────┘
```

Nguyên tắc sản phẩm:

1. **Một mục nhỏ (subtopic) là đơn vị duy nhất.** Id `<sec>.<module>.<sub>` trong `skill_tree.json` là khoá chung của lesson, problem, quiz, điểm, thẻ ôn. Không tạo id song song.
2. **Học ít, làm nhiều.** Một lesson đọc 8-15 phút; ít nhất một nửa thời gian học là gõ code.
3. **Điểm phải có bằng chứng.** Điểm 0-3 chỉ tăng khi có sự kiện đo được (quiz đạt, bài Accepted, mastery check đạt, ôn lặp đạt). Không có nút "tự chấm" cho mục có code (ngoại lệ hẹp: item `concept`, mục 5.1). **Mục concept** (System Design và track AI engineer LLM — không có bài code để đo, mục 5.2) là ngoại lệ rộng hơn: bằng chứng điểm 2/3 của chúng là item `concept`/`read_code` tự giải thích, và ôn lặp (review) tính cả thẻ `recall`. Điểm không bao giờ tự giảm.
4. **Nội dung là file trong git**, kiểm tra tự động bằng script; app chỉ hiển thị và ghi tiến độ.
5. **Chạy được trên máy Quan với chi phí 0 đồng**, nhưng không đóng cửa đường mở rộng (Java, nhiều người dùng).
6. **Quyết đoán, ít cấu hình.** Mỗi chức năng có một cách làm mặc định.
7. **Tự điều chỉnh nhịp học (quyết định của Quan, 2026-10-24).** Không có số lượng cố định mỗi ngày; có ngày học nhiều, có ngày học ít. Plan chỉ là thứ tự gợi ý, không là lịch. App không đặt mục tiêu ngày, không báo "trễ", không phạt ngày nghỉ hay ngày học nhẹ; học tiếp bao lâu tuỳ ý và dừng lúc nào cũng được. Phần duy nhất tính theo lịch là khoảng cách ôn tập (Leitner, mục 5.4) vì nó mô hình sự quên chứ không phải khối lượng việc.

### 1.2 MVP và các giai đoạn sau

| | MVP (M0-M3) | Sau MVP |
|---|---|---|
| Nội dung | 40 subtopic = tuần 1 + ngày 8-12 của kế hoạch Meta (mục 4.1). Python + DSA nền tảng | M4: ngày 13-14 (6 subtopic) + quiz tuần + mock. M5: Java. M6: toàn bộ 530 mục. M7: nhiều người dùng |
| Màn hình | Dashboard / skill map, split view lesson + editor, danh sách bài, review queue, tiến độ, "Học tiếp" (thứ tự gợi ý từ plan) | Mock interview, so sánh Python/Java, ghi chú |
| Chạy code | Python, trong trình duyệt (Pyodide) | Java qua server sandbox |
| Chấm | Run (sample test), Submit (hidden test), quiz, mastery check, điểm 0-3, unlock, Leitner review | Chấm mock theo rubric, phân tích điểm yếu |
| Người dùng | 1 người (Quan). Bảng nào cũng có `user_id` | Auth cắm vào sau (không spec ở đây) |

Ngoài phạm vi MVP và không spec: đăng nhập, host công khai, thanh toán, giấy phép nội dung, ứng dụng di động native, social/leaderboard.

### 1.3 Người dùng

Một người dùng thực: Quan, đọc tiếng Việt tốt, đề phỏng vấn thật bằng tiếng Anh. Quyết định: **đề bài song ngữ** (`statement_en_md` là bản chính để quen đề thật, `statement_vi_md` là bản giải thích, bật/tắt bằng một nút). Lesson viết tiếng Việt, thuật ngữ giữ tiếng Anh như trong `skill_tree.json`.

### 1.4 Ghi chú về bản quyền đề bài

Cho mục đích cá nhân, đề của MVP được phép bám sát LeetCode (field `source.type: leetcode`, `source.lc: <số>`, `source.rewrite_required: true`). **Trước bất kỳ bản phát hành công khai nào (kể cả cho bạn bè dùng chung) mọi problem có `rewrite_required: true` phải viết lại đề, đổi tên hàm và ví dụ, và validator sẽ chặn build `public` nếu còn cờ này.** Lời giải và test case do ta viết nên không bị ảnh hưởng.

---

## 2. Trải nghiệm người dùng

### 2.1 Danh sách màn hình

| Route | Màn hình | Mục đích |
|---|---|---|
| `/welcome` (+ `/welcome/profile`, `/welcome/start`) | Chào mừng, hồ sơ, chọn cách bắt đầu | Chỉ lần đầu (`onboarding.profile_done=false`): kiểm tra Pyodide, hồ sơ 4 câu, chọn Đánh giá trình độ hoặc Bắt đầu từ đầu |
| `/placement/:sessionId` · `/placement/:sessionId/result` | Đánh giá trình độ đầu vào và kết quả | Mục 5.6 và `UI_SPEC.md` mục 2; tạm dừng/tiếp tục được |
| `/` | Học tiếp (Next up) | Subtopic mở khoá kế tiếp theo thứ tự plan, thẻ ôn đến hạn, bài luyện gợi ý, mốc mock khi đã mở, banner "Tiếp tục nơi bạn dừng" (`GET /resume`). Không có ngày hiện tại, không có định mức |
| `/map` | Skill map | Cây 40 mục, trạng thái khoá/mở, điểm 0-3 |
| `/s/:subtopicId` | Subtopic (split view) | Lesson bên trái, editor + kết quả bên phải |
| `/p/:problemId` | Problem (split view) | Đề bên trái, editor bên phải |
| `/check/:subtopicId` | Mastery check / Test out | Chế độ tập trung chạy flow C/D (cùng component item với placement) |
| `/problems` | Danh sách bài | Lọc theo subtopic, độ khó, trạng thái |
| `/review` | Review queue | Phiên ôn tập: toàn bộ thẻ đến hạn, làm bao nhiêu tuỳ ý |
| `/progress` | Tiến độ | Điểm theo mục, lịch sử thời gian học (tổng theo tuần, heatmap lịch), biểu đồ |
| `/settings` | Cài đặt | Hồ sơ, múi giờ, giao diện, cỡ phiên ôn gợi ý (tuỳ chọn), ngưỡng cảnh báo backlog, backup/khôi phục, export/import, reset, lịch sử đánh giá |

Chi tiết từng màn hình (layout, component, nguồn dữ liệu, mọi trạng thái, hành động ghi gì) và design system: `UI_SPEC.md` mục 3.

### 2.2 Wireframes

**Học tiếp (`/`)**

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Prep App         Học tiếp · Map · Bài tập · Ôn tập (24) · Tiến độ   [VI] │
├──────────────────────────────────────────────────────────────────────────┤
│ Hôm nay 1h20 · tuần này 6h05 (chỉ để xem, không có mục tiêu)             │
│ ⚠ 24 thẻ đang đến hạn. Nên ôn trước khi học bài mới.  [Ôn ngay] [Bỏ qua] │
│   (cảnh báo mềm, chỉ hiện khi vượt ngưỡng backlog; không chặn gì)        │
│                                                                          │
│ CẦN LÊN ĐIỂM 2 ĐỂ MỞ MỤC SAU                                             │
│  ◐ memory_model [Điểm 1] → mở arrays   bài gợi ý: Swap Variables (E)     │
│                                                                          │
│ HỌC TIẾP (theo thứ tự plan)               LUYỆN GỢI Ý                    │
│  ◐ hash_tables            [Điểm 1] ▶        ☐ Isomorphic Strings     E   │
│  ☐ hashing_patterns [khoá: cần              ☐ Group Anagrams         M   │
│     hash_tables≥2 · Test out]                                            │
│  ◐ big_o [chờ làm lại check đến 14:30]  (xếp dưới các mục làm được ngay) │
│  ... [xem thêm]                                                          │
│                                                                          │
│ ÔN TẬP ĐẾN HẠN (24) · quá hạn nhiều nhất trước                           │
│  list · tuple_namedtuple · dict · ...                                    │
│  [Ôn tất cả 24]  [Phiên ngắn (preset)]   Dừng lúc nào cũng được          │
│                                                                          │
│ Mốc: Mock 1 (I1, 45 phút) mở sau khi xong các mục tuần 1   [còn 11 mục]  │
└──────────────────────────────────────────────────────────────────────────┘
```

Ghi chú v0.6: trên cùng màn `/` có banner "Tiếp tục nơi bạn dừng" (khi `GET /resume` có việc dở) và, sau placement, nhóm "Có thể đã biết" (mục `likely_known`, nút Test out nhanh, xếp dưới danh sách học); mục `known_basic` gắn nhãn "đã biết sơ" và có lesson rút gọn (không đổi điều kiện `lesson_done`). Wireframe đầy đủ ở `UI_SPEC.md` S4.

Ghi chú: nhóm "Cần lên điểm 2 để mở mục sau" chỉ hiện khi có (mục 5.5). Dòng trên cùng là thông tin trung tính (thời gian học hôm nay và tuần này, không có mục tiêu theo ngày). Danh sách "Học tiếp" là các subtopic mở khoá kế tiếp theo thứ tự `plan.json`; bấm vào mục nào cũng được, không bắt buộc đúng thứ tự (mục khoá vẫn xem trước được). Số thẻ ôn, nút "Phiên ngắn" và banner backlog xem mục 5.4.

**Skill map (`/map`)**: danh sách module theo thứ tự, mỗi mục là một "chip"; mũi tên prerequisite hiện khi di chuột/chọn.

```
 py.core            [getting_started 3]──[variables_types 3]──[operators 2]...
 py.datastructs     [list 2]─[dict 1]─[comprehensions 0]─[heapq_bisect 0]
 dsa.arrays_strings [arrays 2]─►[hash_tables 1]─►[hashing_patterns 🔒]─►[prefix_sum 🔒]
 Chú giải: số = điểm 0-3 · 🔒 khoá (hover: thiếu prerequisite nào; mục không có prerequisite như heapq_bisect không bao giờ khoá) · ● có thẻ ôn đến hạn
 Chọn chip → panel phải: summary_vi, mastery_bar_vi, prerequisite, [Học] [Test out]
```

**Split view subtopic (`/s/dsa.arrays_strings.hash_tables`)**: màn hình chính, ≥ 1280px (thiết kế quanh laptop 1366px) chia 45/55, kéo được thanh chia; 768-1279px thành 2 tab (Bài học | Code); dưới 768px chỉ đọc lesson, làm quiz và ôn thẻ nhớ nhanh (ẩn editor, Submit, mastery check). Chi tiết responsive: `UI_SPEC.md` mục 3.5.

```
┌───────────────────────────────┬─────────────────────────────────────────┐
│ ◄ Map   hash_tables   ●●○ 1/3 │ Bài tập 2/3: "Đếm tần suất"      ⏱ 04:12│
│ ─ Bài học ─ Bài tập ─ Kiểm tra│ ┌─────────────────────────────────────┐ │
│                               │ │ 1 def freq(words):                  │ │
│ ## Dict là hash table         │ │ 2     d = {}                        │ │
│ Python dict tra khoá O(1)...  │ │ 3     # TODO                        │ │
│                               │ │ 4     return d                      │ │
│ ┌ code_sample ─────────────┐  │ │ (CodeMirror 6, Python)              │ │
│ │ d = {}                   │  │ └─────────────────────────────────────┘ │
│ │ ...            [▶ Chạy]  │  │ [▶ Run]  [✔ Submit]  [💡 Gợi ý 0/3]  [⟲] │
│ └──────────────────────────┘  │ ┌ Kết quả ────────────────────────────┐ │
│                               │ │ Sample 1 ✔  Sample 2 ✔  Sample 3 ✘  │ │
│ ▣ Quiz 1: Chọn đáp án đúng    │ │ Sample 3: expected [1,2] got [2,1]  │ │
│   ○ A ○ B ○ C        [Kiểm tra]│ │ stdout: ...                         │ │
│                               │ └─────────────────────────────────────┘ │
│ [Tiếp ►]                      │                                         │
└───────────────────────────────┴─────────────────────────────────────────┘
```

Quy tắc UI của khối code trong lesson: `code_sample` có nút Chạy chạy tại chỗ; `code_exercise` nạp starter vào editor bên phải khi người học bấm "Làm bài này", để lesson và editor luôn song song.

**Danh sách bài (`/problems`)**

```
 Lọc: [subtopic ▾] [E|M|H] [Chưa làm|Đang làm|Accepted] [Nguồn: plan|check|mock]
 ─────────────────────────────────────────────────────────────────────────────
  ✔ Ransom Note            E  py.datastructs.dict           lần 1  02:41
  ◐ Isomorphic Strings     E  dsa.arrays_strings.hash_tables  2 lần nộp
  ☐ Group Anagrams         M  dsa.arrays_strings.hash_tables
  🔒 Two Sum               E  dsa.arrays_strings.hashing_patterns (khoá)
```

**Review queue (`/review`)**: một thẻ một lần; hiện tổng số thẻ đến hạn, xếp quá hạn nhiều nhất trước rồi điểm thấp trước. Làm bao nhiêu tuỳ ý, bấm "Dừng" lúc nào cũng được.

```
 Thẻ 2 (còn 7 đến hạn) · hash_tables · hộp 3 (đến hạn 2 ngày trước)       [Dừng]
 ┌────────────────────────────────────────────────────────────────┐
 │ Predict output:   d = {}                                       │
 │                   for w in "a b a".split(): d[w] = d.get(w,0)+1│
 │                   print(d)                                     │
 │ Đáp án: [____________________]                  [Kiểm tra]     │
 └────────────────────────────────────────────────────────────────┘
 Kết quả → đúng: hộp 4, lần sau +7 ngày · sai: về hộp 1, mai ôn lại
 Thẻ chưa làm khi dừng vẫn đến hạn, không bị phạt.
```

**Tiến độ (`/progress`)**: lưới heatmap 40 mục (màu theo điểm), cột "tuần này": số bài Accepted, phút code, thẻ ôn đã làm, tổng thời gian học; biểu đồ tổng giờ theo tuần và heatmap lịch thời gian học (ô đậm = học nhiều, ô nhạt = học ít, ô trống = nghỉ; trung tính, không có chuỗi ngày liên tiếp, không phạt ngày nghỉ); bảng "mục yếu" (điểm < target hoặc nhiều lapse); tiến độ plan chỉ là "đã xong X / 40 mục" và mục kế tiếp, không so với ngày kế hoạch và không có thông báo trễ.

### 2.3 User flows (từng bước)

**Flow A, học một mục mới**

1. Mở `/` thấy "HỌC TIẾP: hash_tables (mở khoá)". Bấm vào.
2. Split view mở tab "Bài học". Cuộn qua block text/code_sample; chạy code mẫu tại chỗ.
3. Gặp quiz block: trả lời, nhận phản hồi và giải thích ngay; kết quả lưu (`quiz_answers`, kèm `run_no` của lượt đang làm).
4. Gặp `code_exercise`: bấm "Làm bài này", editor bên phải nạp starter; Run để thử sample test; qua hết thì block tick xanh.
5. Cuối lesson bấm "Hoàn thành bài học". Nếu `quiz_best ≥ 0.7` thì điểm = 1 và tạo thẻ ôn hộp 1 (đến hạn ngày mai). Nếu chưa đạt: báo quiz nào sai, bấm "Làm lại lượt" (`run_no` + 1; `quiz_best` lấy lượt tốt nhất).
6. Tab "Bài tập" liệt kê problem của mục (theo plan); xem flow B.
7. Tab "Kiểm tra" trong lesson mở khi đã có ít nhất 1 bài Accepted (hoặc mục không có bài); xem flow C. (Điều kiện AC chỉ áp cho tab này; "Test out" ở flow D chạy check mà không cần AC.)
8. Xong mục thì quay lại `/`: mục kế tiếp theo thứ tự plan hiện lên ngay. Quan học tiếp bao lâu tuỳ ý hoặc dừng; không có khái niệm "hết việc trong ngày".

**Flow B, làm một problem**

1. Mở problem: đề (EN/VI), constraints, ví dụ; editor nạp `starter.python`; đồng hồ chạy (chỉ ghi nhận, không cưỡng chế). `elapsed` = tổng thời gian editor của bài đang hiển thị (tạm dừng khi `document.hidden`), cộng dồn qua các phiên, tính từ lần mở đầu tiên (`attempts.started_at`) đến Submit AC đầu tiên; client gửi `elapsed_ms` kèm `POST /attempts`.
2. **Run**: chạy các sample test (hiển thị input/expected/got/stdout/traceback). Không tính vào điểm, không giới hạn số lần. Ghi `attempts` mode `run`.
3. **Gợi ý**: 3 nấc (nudge, hướng tiếp cận, giả mã). Mỗi nấc bấm một lần, tăng `hints_used`.
4. **Submit**: client xin hidden test từ API, chạy trong worker, gửi kết quả về. Kết quả chỉ hiện `passed/total`, tên test đầu tiên sai, và với test sai nhỏ thì input/expected (test lớn chỉ hiện tên). Verdict: `AC`, `WA`, `TLE`, `RE`, `CE`.
5. AC: hiện "Xem lời giải mẫu" và so sánh độ phức tạp; ghi `solution_viewed=false` nếu chưa xem. Chưa AC mà xem lời giải: ghi `solution_viewed=true`, bài đó không còn tính "clean".
6. Cập nhật điểm mục (mục 5) ngay sau Submit.

**Flow C, mastery check (kiểm tra điểm 2/3)**

1. Nút "Kiểm tra" chạy thang bậc của `assessment.json`: bắt đầu item mức 2 (ưu tiên item `write_code`); đúng thì (nếu có) item mức 3; sai thì item mức 1 để chẩn đoán. Nếu mục không có item mức 1 thì dừng và báo "cần học lesson". Tối đa 3 item, mỗi item có time-box theo trường `minutes` của item.
2. Item `write_code` dùng cùng engine như problem (kind `check`); item `read_code` là predict-output, chấm tự động; item `concept` là "tự giải thích rồi xem đáp án, bấm Đúng/Sai" (loại tự chấm, chiếm 20/112 item gốc). **Mục có code**: item `concept` được ghi nhưng không bao giờ `clean`, nên không là bằng chứng điểm 2/3; mọi mục MVP (40 mục py/dsa/cs) đều có item `write_code` mức 2, nên bằng chứng điểm 2 ở đó không bao giờ chỉ là tự chấm. **Mục concept** (toàn bộ `sd` và 4 module `ml.llm`/`ml.rag_agents`/`ml.llm_eval_serving`/`ml.system_design` — không có bài code): một lần pass `concept` đúng, trong time-box là `clean` và chính là bằng chứng điểm 2/3 (mục 5.2). Đây là nới rộng có chủ đích của nguyên tắc 1.1#3 cho các track không-code.
3. Kết quả ghi `check_results` (kèm `attempt_no`); điểm cập nhật theo mục 5.
4. **Trượt mức 2**: không hiện `reference`, chỉ hiện test sai (như Submit). Được làm lại sau 24 giờ, không giới hạn số lần, mỗi lần là một `attempt_no` mới. Trong lúc chờ, đường khác là fallback `check2_ok` (mục 5.2).

**Flow D, test out (bỏ qua mục đã biết)**

Mục đang khoá hoặc chưa học có nút "Test out": chạy flow C. Đạt mức 2 sạch (`tested_out`) thì điểm = 2 (tối đa 2 bằng test out), mục và các mục phụ thuộc được mở khoá. Muốn lên 3 vẫn cần `level3_ok` + `retention_ok`. Thẻ ôn tạo từ ngày đạt (mục 5.4).

**Flow E, ôn tập (theo nhu cầu, không có trần)**

1. `/review` lấy **tất cả** thẻ đến hạn, xếp quá hạn nhiều nhất trước, tie-break điểm thấp trước. Quan làm bao nhiêu tuỳ ý trong một phiên và bấm "Dừng" lúc nào cũng được. Thẻ chưa làm vẫn đến hạn, không phạt. Có hai nút tuỳ chọn: "Ôn tất cả" và "Phiên ngắn" (preset cỡ phiên, mục 5.4 quy tắc 5).
2. Mỗi thẻ là một item của mục: hộp 1-2 là câu nhớ nhanh (quiz/predict), hộp 3-5 là một bài code ngắn (mục 5.4). Trong preset "Phiên ngắn" tối đa 2 thẻ code, thẻ hộp 3-5 còn lại dùng câu nhớ nhanh (đạt vẫn lên hộp nhưng **không** tính cho `retention_ok`, mục 5.2).
3. Đạt: lên hộp, hẹn lần sau (tính từ ngày ôn thật). Trượt: về hộp 1. Cập nhật `review_cards`, ghi `review_log`.
4. Nếu số thẻ đến hạn vượt ngưỡng backlog, `/` hiện banner mềm gợi ý ôn trước khi học bài mới (có nút [Bỏ qua]); không chặn bài học.

**Flow F, học tiếp theo thứ tự plan**

`/` (Học tiếp) tính danh sách bằng `GET /next`: các subtopic mở khoá chưa `done`, xếp theo thứ tự trong `plan.json` (mục 5.5), kèm bài luyện gợi ý, số thẻ đến hạn và mốc mock đã mở. Không có ngày hiện tại, con trỏ ngày hay nút "sang ngày kế": xong mục nào thì mục tiếp theo tự lên đầu danh sách. Quan nghỉ nhiều ngày rồi quay lại, hay học 5 mục trong một ngày, đều thấy đúng mục kế tiếp; không có nợ, không có thông báo trễ.

**Flow G, lần đầu mở app và đánh giá đầu vào**

1. `GET /me` có `onboarding.profile_done=false` thì app vào `/welcome`: kiểm tra Pyodide, xin lưu trữ bền vững, thu hồ sơ (`target_role` intern/new_grad, `track` swe/ai, `language` python, `experience` none/some/solid) bằng `PUT /profile`.
2. Chọn **Đánh giá trình độ** (`POST /placement`) hoặc **Bắt đầu từ đầu** (`POST /placement/skip`, không gieo điểm). Placement chạy theo `UI_SPEC.md` mục 2 và gieo điểm theo mục 5.6.
3. Kết quả (`/placement/:id/result`): skill map đã gieo, mạnh/yếu, mục bắt đầu theo thứ tự plan, giờ còn lại ước tính; rồi vào `/`. Có thể đo thêm hoặc làm lại theo module bất cứ lúc nào; Test out từng mục luôn có.

**Flow H, tiếp tục sau khi thoát hoặc tắt máy**

Mọi sự kiện đã ghi ngay (mục 6.7, `UI_SPEC.md` mục 4). Mở lại app: `GET /resume` trả việc dở (lesson + block, bài + nháp, check/placement đang làm, thẻ ôn đang mở) và banner đưa về đúng chỗ. Nháp code, đồng hồ bài, quiz đang chọn dở được khôi phục; server tắt thì thay đổi nằm trong outbox và tự gửi lại khi server chạy.

---

## 3. Mô hình nội dung

### 3.1 Cấu trúc thư mục nội dung

```
content/
  index/
    subtopics.json        snapshot các node MVP lấy từ skill_tree.json (+ source_hash)
    plan.json             snapshot plan.json (chỉ days 1-14)
    assumed.json          prerequisite coi như đã đạt: ["cs.onramp.computer_programming_model"]
  lessons/<sec>/<subtopic_id>.yaml          vd lessons/dsa/dsa.arrays_strings.hash_tables.yaml
  problems/<subtopic_id>/<slug>/
    problem.yaml
    solution.py           reference solution (không bao giờ vào public bundle)
    brute.py              lời giải vét cạn độc lập (bắt buộc với medium, tuỳ chọn với easy); dùng để cross-check
    wrong/*.py            1-3 lời giải sai (validator: mỗi cái phải rớt ít nhất 1 hidden test)
    slow/*.py             (tuỳ chọn) lời giải chậm, phải TLE ở stress test
    tests/sample.jsonl    3 test hiển thị
    tests/gen.py          sinh hidden test (seed cố định) từ solution.py; phải export thêm `small_inputs(seed, n)` (input ≤ 12 phần tử) cho brute-force
    tests/hidden.jsonl    kết quả sinh, commit vào git
  checks/<subtopic_id>.yaml                 item mastery check (từ assessment.json, chuẩn hoá)
  reviews/<subtopic_id>.md                  ghi chú reviewer
  schemas/lesson.schema.json  problem.schema.json  check.schema.json
```

Định dạng chọn **YAML cho lesson/problem** (nhiều đoạn văn dài và code nên dùng `|` dễ đọc hơn JSON, agent ít hỏng escape) và **JSONL cho test**. Mọi file được validate bằng JSON Schema sau khi load.

### 3.2 Lesson (tầng 3)

Mỗi lesson ứng với đúng một subtopic id. Trường:

| Field | Kiểu | Ghi chú |
|---|---|---|
| `id` | string | = subtopic id, phải tồn tại trong `content/index/subtopics.json` |
| `version`, `status` | int, enum | `status`: `draft` → `validated` → `reviewed` → `published`; build chỉ lấy `published` |
| `title_vi` | string | lấy từ `name_vi` của tree, được phép chỉnh |
| `est_minutes` | int | 8-15 cho phần đọc, không tính bài tập |
| `objectives_vi` | string[] | 2-4 câu, tách từ `mastery_bar_vi` |
| `blocks` | Block[] | thứ tự hiển thị; mỗi block có `id` bền vững (dùng cho tiến độ) |
| `problems` | `{practice: [id], extra: [id]}` | `practice` = bài chính trong plan, `extra` = bài thêm |
| `mastery_check` | `{l1: [item], l2: [item], l3: [item]}` | id item đánh giá, lấy từ `assessment.json` |
| `checkpoint` | `{pass_ratio: 0.7, min_items: 3}` | ngưỡng quiz để đạt điểm 1 |
| `source` | object | `tree_hash`, `authored_by`, `reviewed_by`, ngày |

Các loại block (`type`):

| type | Trường chính | Hành vi |
|---|---|---|
| `text` | `md` | Markdown (GFM); thuật ngữ lần đầu viết `**đậm (english)**` |
| `callout` | `kind: tip|warning|beginner|interview`, `md` | `beginner` lấy từ `beginner_note_vi`; `interview` là mẹo phỏng vấn |
| `code_sample` | `lang`, `code`, `runnable`, `expected_output?` | Hiển thị code, nút Chạy chạy tại chỗ (có thể sửa) |
| `quiz_mcq` | `prompt_md`, `options[{id,text_md}]`, `answer[]`, `multi`, `explain_md` | Chấm tự động, lưu mỗi lần trả lời |
| `quiz_fill` | `prompt_md` (chỗ trống `___`), `blanks[{accept[], regex?}]`, `explain_md` | So khớp sau khi trim; `accept` là danh sách chấp nhận |
| `predict_output` | `code`, `expected_output`, `explain_md` | Người học gõ output; sau khi đúng hoặc sai hiện kết quả thật (đã verify bằng runner khi build) |
| `code_exercise` | `starter`, `entry`, `tests[]` (3-5), `hint_md`, `solution` | Bài nhỏ ngay trong lesson, chạy ở editor bên phải; chỉ có Run |
| `problem_ref` | `problem_id` | Liên kết sang problem đầy đủ |
| `summary` | `bullets_vi[]` | Cuối lesson, 3-6 gạch đầu dòng |

Chỉ `quiz_*` và `predict_output` có `graded: true` (mặc định) tính vào `quiz_best`. `code_exercise` trong lesson không tính điểm riêng; bài đánh giá là problem và mastery check.

### 3.3 Problem

| Field | Ghi chú |
|---|---|
| `id` | slug duy nhất toàn cục, vd `ransom-note` |
| `subtopic_id`, `secondary_subtopics[]` | mục chính (dùng cho điểm và ôn tập) và mục liên quan |
| `kind` | `practice` (bài plan/extra), `check` (từ assessment), `mock` (sau MVP), `lesson` (code_exercise, không có file riêng) |
| `title`, `title_vi`, `difficulty` | `easy|medium|hard`; map từ `E|M|H` trong plan |
| `source` | `{type: leetcode|original|mock, lc: 383, rewrite_required: true}` |
| `statement_en_md`, `statement_vi_md` | đề; bản VI giải thích bằng lời, không dịch từng chữ |
| `constraints[]`, `examples[]` | `examples[{input, output, explain_vi}]` hiển thị; ví dụ đầu tiên luôn là sample test 1 |
| `io` | cách gọi hàm, xem dưới |
| `starter.python` | khung code; `starter.java` thêm ở M5 |
| `limits` | `time_ms` (mỗi test, chuẩn native; `solution.py` phải chạy ≤ 0.3 × `time_ms`, mục 4.4), `memory_mb`, `time_multiplier.pyodide: 3` |
| `time_target_min` | thời gian "sạch" (xem mục 5); easy 10, medium 25 |
| `hints[3]` | nudge, approach, pseudo-code |
| `solution` | `{file: solution.py, approach_vi, complexity: "O(n) time, O(n) space"}` |
| `tests` | đường dẫn sample/hidden và `generator` |
| `tags[]` | vd `hash-map`, `counting`; dùng cho lọc |
| `status`, `version` | như lesson |

`io.mode` hỗ trợ 4 kiểu (đủ cho toàn bộ 133 problem MVP):

- `function`: gọi `entry(*args)`, so với `expected`. `compare`: `exact` | `unordered` (so sánh dạng multiset) | `float_tol` | `custom` (file `checker.py` khi có nhiều đáp án đúng, vd Two Sum).
- `inplace`: gọi hàm sửa trực tiếp tham số thứ `inplace_arg`, so sánh tham số đó (Rotate Array, Duplicate Zeros).
- `class_ops`: đề thiết kế class (Min Stack, Queue using Stacks): test là chuỗi `ops` và `args`, so sánh danh sách kết quả.
- `stdout`: chương trình in ra, so output sau khi trim cuối dòng (bài nhập môn `py.core.*`), có `stdin` tuỳ chọn.

Kiểu đặc biệt cho tham số/kết quả: `list_node` và `tree_node` (test viết dạng list `[1,2,3]` hoặc `[1,null,2]`, harness dựng `ListNode`/`TreeNode` trước khi gọi và chuyển ngược khi so sánh).

Định dạng test (JSONL, mỗi dòng một test): `{"id":"h07","args":["aa","aab"],"expected":true,"tags":["edge"]}`. Test lớn được sinh bởi `gen.py` nên file có thể lớn; ngưỡng cứng: mỗi `hidden.jsonl` ≤ 1 MB.

### 3.4 Check item (mastery check)

Chuẩn hoá từ `assessment.json` (field thật: `id, subtopic_id, difficulty 1-3, type, minutes, prompt, answer, rubric, score_if_pass, score_if_fail_max, reference, driver, expected_output`):

- `write_code` (61 item MVP, đều có `reference`, `driver`, `expected_output`): script `tools/convert_checks.py` sinh `problem.yaml` kind `check` với mode `stdout`/`function` và 1 sample + ≥5 hidden (sinh từ reference), giữ `minutes` làm time-box.
- `read_code` (31): `predict_output` với `code`, `expected_output`.
- `concept` (20 gốc + item tự soạn cho các track concept): thẻ tự giải thích (`prompt`, `answer` hiện sau khi người học viết/nói ra, tự bấm Đúng/Sai). Trên mục có code đây là tự chấm không tính bằng chứng; trên **mục concept** (mục 5.2) một lần pass đúng trong time-box là `clean` và là bằng chứng điểm 2/3. Các mục `sd.*` và 4 module `ml` không có item nào trong `assessment.json`, nên toàn bộ item của chúng viết tay qua `content/checks_extra/<id>.yaml` (mỗi mục: item recall mức 1, 1 item `concept` mức 2 là cổng điểm 2, 1 item `concept` mức 3 là cổng điểm 3).
- `write_code` mức 2 **bổ sung** (9 item, tự soạn) cho 9 mục mà mọi item mức 2 gốc chỉ là `concept`/`read_code`: `py.core.getting_started`, `py.core.variables_types`, `py.datastructs.tuple_namedtuple`, `py.datastructs.copying_mutability`, `py.functions.lambda_hof`, `cs.complexity.big_o`, `dsa.foundations.memory_model`, `py.functions.scope_closures`, `dsa.foundations.interview_method`. Mỗi mục đúng một item, cùng định dạng problem kind `check`, có `solution.py` + hidden test; author agent viết khi viết lesson của mục. Validator chặn nếu mục đang được validate (có lesson) thiếu item `write_code` mức 2; mục chưa soạn lesson không bị chặn.

### 3.5 Ví dụ hoàn chỉnh: lesson `py.datastructs.dict`

File `content/lessons/py/py.datastructs.dict.yaml` (rút gọn ở phần lặp lại, mọi code đã được chạy kiểm tra):

```yaml
id: py.datastructs.dict
version: 1
status: draft
title_vi: "Dict và set (dictionary & set)"
est_minutes: 12
objectives_vi:
  - "Tạo, tra cứu, thêm và duyệt dict; dùng .get để tránh KeyError."
  - "Dùng dict để đếm và nhóm, dùng set để loại trùng và tìm phần chung."
  - "Giải thích vì sao tra dict nhanh (O(1) trung bình) còn list không làm khoá được."
blocks:
  - id: b01
    type: text
    md: |
      **Dict (dictionary, từ điển)** lưu cặp *khoá → giá trị*. Giống danh bạ điện thoại:
      bạn tra theo **tên** (khoá) để ra **số** (giá trị), không cần biết vị trí.
  - id: b02
    type: code_sample
    lang: python
    runnable: true
    code: |
      sdt = {"An": "0901", "Binh": "0902"}
      sdt["Chi"] = "0903"           # thêm khoá mới
      sdt["An"] = "0911"            # sửa giá trị
      print(sdt["An"], "Binh" in sdt, sdt.get("Dung", "không có"))
    expected_output: "0911 True không có"
  - id: b03
    type: callout
    kind: beginner
    md: |
      `sdt["Dung"]` (khoá không tồn tại) báo **KeyError**; `sdt.get("Dung")` trả `None`
      hoặc giá trị mặc định bạn đưa vào. Phỏng vấn viên rất hay hỏi điểm này.
  - id: b04
    type: quiz_mcq
    prompt_md: "Đoạn `d = {}; d['x'] += 1` cho kết quả gì?"
    options:
      - {id: a, text_md: "`d` thành `{'x': 1}`"}
      - {id: b, text_md: "`KeyError: 'x'`"}
      - {id: c, text_md: "`d` thành `{'x': 0}`"}
    answer: [b]
    explain_md: "`+=` đọc `d['x']` trước, khoá chưa có nên lỗi. Dùng `d['x'] = d.get('x', 0) + 1`."
  - id: b05
    type: code_sample
    lang: python
    runnable: true
    code: |
      dem = {}
      for w in "a b a c b a".split():
          dem[w] = dem.get(w, 0) + 1
      print(dem, max(dem, key=dem.get))
    expected_output: "{'a': 3, 'b': 2, 'c': 1} a"
  - id: b06
    type: quiz_fill
    prompt_md: "Điền vào chỗ trống để đếm: `dem[w] = dem.___(w, 0) + 1`"
    blanks: [{accept: ["get"]}]
    explain_md: "`get(khoá, mặc_định)` không bao giờ ném KeyError."
  - id: b07
    type: predict_output
    code: |
      s = {1, 2, 3}; t = {2, 3, 4}
      print(s & t, sorted(s ^ t))
    expected_output: "{2, 3} [1, 4]"
    explain_md: "`&` giao, `^` hiệu đối xứng. Set không có thứ tự nên in qua `sorted`."
  - id: b08
    type: callout
    kind: interview
    md: "Hỏi: *vì sao list không làm khoá dict?* Đáp: list **mutable**, không hashable; dùng tuple."
  - id: b09
    type: code_exercise
    md: "Viết `unique_sorted(nums)` trả list các số khác nhau, tăng dần."
    entry: unique_sorted
    starter: |
      def unique_sorted(nums):
          # TODO: dùng set
          pass
    tests:
      - {args: [[3, 1, 3, 2]], expected: [1, 2, 3]}
      - {args: [[]], expected: []}
      - {args: [[5, 5, 5]], expected: [5]}
    hint_md: "Chuyển sang `set` để bỏ trùng rồi `sorted(...)`."
    solution: "def unique_sorted(nums):\n    return sorted(set(nums))\n"
  - id: b10
    type: problem_ref
    problem_id: ransom-note
  - id: b11
    type: summary
    bullets_vi:
      - "Dict: khoá → giá trị; tra/ghi/kiểm tra khoá đều O(1) trung bình."
      - "Dùng `.get(k, mặc_định)`; đếm tần suất bằng `d[k] = d.get(k, 0) + 1`."
      - "Set: loại trùng, giao/hợp/hiệu; khoá dict phải hashable (tuple được, list không)."
problems: {practice: [ransom-note], extra: []}
mastery_check: {l1: [Q022], l2: [Q023], l3: [Q024]}
checkpoint: {pass_ratio: 0.7, min_items: 3}
```

Ghi chú: ví dụ lấy `concepts_vi` và `examples_vi` của node (dict, set, đếm chữ cái, loại trùng, phần chung) và item `Q022/Q023/Q024` trong `assessment.json`. `Q023` là Two Sum bằng dict; trong plan Two Sum (LC 1) nằm ở ngày 6 (`hashing_patterns`), nên nó chỉ xuất hiện như check item ở mục này, không lặp trong danh sách bài.

### 3.6 Ví dụ hoàn chỉnh: problem `ransom-note`

File `content/problems/py.datastructs.dict/ransom-note/problem.yaml`:

```yaml
id: ransom-note
subtopic_id: py.datastructs.dict
secondary_subtopics: []
kind: practice
title: "Ransom Note"
title_vi: "Thư tống tiền"
difficulty: easy
source: {type: leetcode, lc: 383, rewrite_required: true}
statement_en_md: |
  Given two strings `ransom_note` and `magazine`, return `true` if `ransom_note` can be
  constructed by using the letters from `magazine`, and `false` otherwise.
  Each letter in `magazine` can only be used once.
statement_vi_md: |
  Cho hai chuỗi `ransom_note` và `magazine`. Trả về `true` nếu có thể ghép ra
  `ransom_note` bằng cách cắt các chữ cái trong `magazine`, mỗi chữ cái trong
  `magazine` chỉ được dùng một lần; ngược lại trả về `false`.
constraints:
  - "1 <= len(ransom_note), len(magazine) <= 10^5"
  - "Chỉ gồm chữ cái tiếng Anh thường"
examples:
  - {input: 'ransom_note = "a", magazine = "b"', output: "false", explain_vi: "magazine không có 'a'."}
  - {input: 'ransom_note = "aa", magazine = "ab"', output: "false", explain_vi: "Cần 2 chữ 'a', chỉ có 1."}
  - {input: 'ransom_note = "aa", magazine = "aab"', output: "true", explain_vi: "Đủ hai chữ 'a'."}
io:
  mode: function
  entry: can_construct
  params: [{name: ransom_note, type: str}, {name: magazine, type: str}]
  returns: bool
  compare: exact
starter:
  python: |
    def can_construct(ransom_note: str, magazine: str) -> bool:
        # TODO
        pass
limits: {time_ms: 1000, memory_mb: 256, time_multiplier: {pyodide: 3}}
time_target_min: 10
hints:
  - "Bạn cần biết mỗi chữ cái xuất hiện bao nhiêu lần trong magazine."
  - "Đếm tần suất của magazine vào một dict, rồi trừ dần theo từng chữ của ransom_note."
  - "Duyệt ransom_note; nếu đếm của chữ đó là 0 thì trả False, ngược lại giảm 1. Hết vòng lặp trả True."
solution:
  file: solution.py
  approach_vi: "Dict đếm tần suất của magazine, trừ dần khi duyệt ransom_note. O(n + m) thời gian, O(1) bộ nhớ phụ (tối đa 26 khoá)."
  complexity: "O(n + m) time, O(1) space"
tests:
  sample: tests/sample.jsonl
  hidden: tests/hidden.jsonl
  generator: tests/gen.py
tags: [hash-map, counting, strings]
status: draft
version: 1
```

`solution.py` (đã chạy với 3 ví dụ và trường hợp rỗng):

```python
def can_construct(ransom_note: str, magazine: str) -> bool:
    have = {}
    for ch in magazine:
        have[ch] = have.get(ch, 0) + 1
    for ch in ransom_note:
        if have.get(ch, 0) == 0:
            return False
        have[ch] -= 1
    return True
```

`tests/sample.jsonl`:

```
{"id":"s1","args":["a","b"],"expected":false}
{"id":"s2","args":["aa","ab"],"expected":false}
{"id":"s3","args":["aa","aab"],"expected":true}
```

Hidden test (12 test, tất cả `expected` do `solution.py` tính; `gen.py` thêm các test ngẫu nhiên có seed):

| id | Ý đồ | Ví dụ |
|---|---|---|
| h01 | note dài hơn magazine | `("abc","ab")` |
| h02 | note rỗng | `("","abc")` |
| h03 | magazine rỗng, note khác rỗng | `("a","")` |
| h04 | đúng số lượng từng chữ | `("aabbc","cbbaa")` |
| h05 | thiếu đúng 1 chữ | `("aab","ab")` |
| h06 | bằng nhau tuyệt đối | `("xyz","xyz")` |
| h07 | magazine thừa nhiều | `("ab","zzzabzzz")` |
| h08 | 26 chữ cái đủ | alphabet vs alphabet đảo |
| h09 | một chữ lặp nhiều | `("a"*50, "a"*49)` |
| h10 | ngẫu nhiên nhỏ, seed 1 (true) | sinh bởi gen.py |
| h11 | stress 10^5 ký tự, đủ chữ (true) | sinh bởi gen.py; bắt giải pháp O(n·m) như `str.replace`/`list.remove` |
| h12 | stress 10^5, thiếu 1 chữ (false) | sinh bởi gen.py |

Lời giải sai trong `wrong/`: `no_count.py` (chỉ kiểm tra tập chữ `set(note) <= set(mag)`, rớt h05, h09), `off_by_one.py` (so `<` thay vì `<=`, rớt h06). Lời giải chậm trong `slow/`: dùng `magazine = magazine.replace(ch, '', 1)` trong vòng lặp, phải vượt giới hạn ở h11.

---

## 4. Ánh xạ dữ liệu có sẵn → nội dung app

### 4.1 40 subtopic của MVP

Chọn từ `plan.json` ngày 1-12 (`days[].subtopics[].id`, bỏ `bh.*`, mỗi id tính một lần ở ngày xuất hiện đầu tiên). Ngày 13-14 (6 mục kỹ thuật: `heap_ds`, `heap_top_k`, `binary_search_variants`, `sliding_window_fixed`, `sliding_window_variable`, `backtracking_core`) và 4 mục `bh.*` để M4, vì MVP giới hạn ở "khoảng 30-40 mục". Tuần 1 (ngày 1-7) = 28 mục, ngày 8-12 = 12 mục. Tất cả 40 id đã kiểm tra tồn tại trong `skill_tree.json`. Tổng giờ kế hoạch 43h. Cột "Nhóm plan (ngày)" chỉ là vị trí trong thứ tự gợi ý của plan, không phải lịch: Quan có thể học nhiều nhóm trong một ngày hoặc một nhóm trong nhiều ngày.

| # | Nhóm plan (ngày) | subtopic id | Bài chính | Bài thêm | Item ĐG | Prereq trong MVP |
|---|---|---|---|---|---|---|
| 1 | 1 | `py.core.getting_started` | 1 | 1 | 2 | - |
| 2 | 1 | `py.core.variables_types` | 1 | 1 | 2 | - |
| 3 | 1 | `py.core.operators` | 1 | 1 | 2 | - |
| 4 | 1 | `py.core.conditionals` | 1 | 1 | 2 | - |
| 5 | 1 | `py.core.loops` | 1 | 0 | 2 | - |
| 6 | 1 | `py.core.strings` | 0 | 4 | 4 | - |
| 7 | 1 | `py.datastructs.list` | 1 | 3 | 3 | - |
| 8 | 2 | `py.datastructs.tuple_namedtuple` | 1 | 1 | 2 | - |
| 9 | 2 | `py.datastructs.dict` | 1 | 1 | 4 | - |
| 10 | 2 | `py.datastructs.comprehensions` | 1 | 1 | 2 | - |
| 11 | 2 | `py.datastructs.collections_module` | 1 | 1 | 2 | - |
| 12 | 3 | `py.datastructs.copying_mutability` | 2 | 0 | 2 | - |
| 13 | 3 | `py.datastructs.heapq_bisect` | 0 | 0 | 2 | - |
| 14 | 3 | `py.functions.def_args` | 2 | 0 | 3 | - |
| 15 | 3 | `py.functions.lambda_hof` | 1 | 0 | 2 | - |
| 16 | 3 | `py.functions.sorting_keys` | 1 | 0 | 2 | - |
| 17 | 4 | `cs.complexity.big_o` | 2 | 0 | 4 | - |
| 18 | 4 | `dsa.foundations.memory_model` | 1 | 0 | 2 | - |
| 19 | 4 | `dsa.foundations.lib_toolkit` | 1 | 1 | 2 | `cs.complexity.big_o` |
| 20 | 4 | `dsa.arrays_strings.arrays` | 3 | 0 | 4 | `dsa.foundations.memory_model`, `dsa.foundations.lib_toolkit` |
| 21 | 5 | `dsa.arrays_strings.hash_tables` | 2 | 2 | 5 | `dsa.arrays_strings.arrays` |
| 22 | 5 | `dsa.arrays_strings.hashing_patterns` | 3 | 3 | 3 | `dsa.arrays_strings.hash_tables` |
| 23 | 6 | `dsa.arrays_strings.prefix_sum` | 2 | 3 | 4 | `dsa.arrays_strings.hashing_patterns` |
| 24 | 6 | `dsa.arrays_strings.strings_basics` | 2 | 3 | 3 | `dsa.arrays_strings.arrays` |
| 25 | 6 | `dsa.arrays_strings.string_algorithms` | 2 | 1 | 3 | `dsa.arrays_strings.strings_basics`, `dsa.arrays_strings.hashing_patterns` |
| 26 | 6 | `py.functions.scope_closures` | 0 | 0 | 2 | - |
| 27 | 7 | `dsa.arrays_strings.array_techniques` | 1 | 2 | 4 | `dsa.arrays_strings.arrays` |
| 28 | 7 | `dsa.two_pointers_window.two_pointers` | 3 | 7 | 4 | `dsa.arrays_strings.arrays` |
| 29 | 8 | `py.oop.classes_basics` | 0 | 2 | 2 | - |
| 30 | 8 | `dsa.linked_list.ll_basics` | 2 | 3 | 3 | `dsa.foundations.memory_model`, `dsa.arrays_strings.arrays` |
| 31 | 8 | `dsa.linked_list.ll_manipulation` | 3 | 3 | 3 | `dsa.linked_list.ll_basics` |
| 32 | 9 | `dsa.stack_queue.stack_queue_ds` | 3 | 1 | 3 | `dsa.arrays_strings.arrays`, `dsa.foundations.lib_toolkit` |
| 33 | 9 | `dsa.stack_queue.stack_problems` | 3 | 5 | 3 | `dsa.stack_queue.stack_queue_ds` |
| 34 | 10 | `dsa.stack_queue.parsing_strings` | 3 | 1 | 2 | `dsa.arrays_strings.strings_basics`, `dsa.stack_queue.stack_problems` |
| 35 | 10 | `dsa.foundations.interview_method` | 0 | 1 | 2 | - |
| 36 | 11 | `dsa.recursion_backtracking.recursion_basics` | 2 | 3 | 4 | `cs.complexity.big_o`, `dsa.foundations.memory_model` |
| 37 | 11 | `dsa.searching_sorting.binary_search_basics` | 2 | 3 | 4 | `dsa.arrays_strings.arrays` |
| 38 | 12 | `dsa.searching_sorting.sorting_algorithms` | 1 | 1 | 3 | `dsa.recursion_backtracking.recursion_basics`, `dsa.arrays_strings.arrays` |
| 39 | 12 | `dsa.searching_sorting.sorting_applications` | 1 | 1 | 2 | `dsa.searching_sorting.sorting_algorithms` |
| 40 | 12 | `dsa.trees.tree_basics` | 1 | 4 | 3 | `dsa.recursion_backtracking.recursion_basics`, `dsa.stack_queue.stack_queue_ds` |

Ghi chú bảng: "Bài chính" = `days[].problems` (59 bài), "Bài thêm" = `days[].extra_problems` (65 bài, tuỳ chọn), "Item ĐG" = số item trong `assessment.json` gắn với mục (tổng 112: 61 write_code, 31 read_code, 20 concept). Prerequisite ngoài MVP duy nhất là `cs.onramp.computer_programming_model` (plan đã miễn; ghi ở `assumed.json`). Năm mục không có bài chính trong plan: `py.core.strings`, `py.datastructs.heapq_bisect`, `py.functions.scope_closures`, `py.oop.classes_basics`, `dsa.foundations.interview_method` (xem 4.3).

### 4.2 Field nguồn → màn hình

| Nguồn | Field | Dùng ở |
|---|---|---|
| `skill_tree.json` node | `id`, `name_vi`, `order` | Map, tiêu đề lesson, khoá chung mọi bảng |
| | `prerequisites` | Rule unlock, mũi tên trên Map |
| | `summary_vi`, `mastery_bar_vi` | Panel phải của Map; `objectives_vi` (agent tách) |
| | `concepts_vi[]` (có `level`: `co_ban`/`nang_cao`) | Nguyên liệu viết block `text`; mức `nang_cao` vào callout |
| | `examples_vi[]` | Ví dụ code_sample / code_exercise |
| | `beginner_note_vi` | Callout `beginner` (15/40 mục MVP có) |
| | `starter_code_vi` | Gợi ý cho `code_sample` đầu tiên (chỉ 3/40: heapq_bisect, scope_closures, classes_basics) |
| | `example_problems`, `key_concepts` | Gợi ý đề bài và `tags` |
| | `target_swe.intern`, `target_ai.intern` | Điểm mục tiêu hiển thị trên Map (vòng tròn đích); Progress "đạt target" |
| | `est_hours`, `est_hours_beginner` | Ước lượng thời gian: `est_hours` có đủ 40/40 mục MVP; `est_hours_beginner` thiếu ở 13/40 (khi thiếu dùng `est_hours`; thời lượng gợi ý của mục lấy từ `plan_hours`, chỉ để hiển thị, không là ngân sách giờ) |
| | `bank_topics`, `bank_counts` | M4+: chọn câu thật từ question bank cho mock/ôn tập |
| | `lang_prereqs`, `lang_notes` | Chọn ngôn ngữ (M5) |
| `plan.json` | `days[].subtopics[]` (`hours`, `part`) | Màn "Học tiếp": thứ tự gợi ý của subtopic (ngày chỉ là nhóm thứ tự, không là lịch) |
| | `days[].problems`, `extra_problems` | `lesson.problems.practice/extra` và danh sách bài |
| | `days[].review` (`D+1`, `D+3`, `D+7`) | Bài ôn gợi ý gắn với subtopic (`review_hint`, mục 5.5), không gắn với ngày |
| | `weeks[].mock_detail`, `mocks_reserved` | M4: mock 1 và mock 2 (ở plan là ngày 7, 14) mở theo tiến độ, không theo ngày (mục 5.5); các bài mock không đưa vào luyện thường |
| | `java_variant[]` | M5: map `py.*` → `java.*` |
| `assessment.json` | `items[]` | Quiz nhớ, mastery check, thẻ ôn |
| | `adaptive_rules`, `clusters` | Thang bậc mức 1→2→3 của flow C |
| | `weekly_quizzes`, 42 item `W*` | M4: quiz tuần (tuần 1 dùng chủ yếu `W183-W194`) |
| | `review_schedule` (D+1/3/7/14/28) | Dải khoảng cách Leitner (mục 5.4) |
| `tracking.csv` | `target_intern`, `tuan`, cột lần chấm | Seed `user_subtopic` ban đầu (import một lần) |
| `question_gaps.md` | phần "Ngôn ngữ" | Biết trước: Python core gần như không có câu thật, phải tự soạn |
| `questions.csv` | `leetcode`, `text_fidelity`, `section`, `subcategory` | Tra đề gốc khi viết problem; **không có test/lời giải**; 51% dòng `title_only` |
| `meta_2026/mock/content_ng/*.json` | `rounds[].questions[]` | M4 (mục 7.3) |

### 4.3 Phải tự soạn mới (khối lượng MVP)

| Hạng mục | Số lượng | Nguồn ý tưởng | Ghi chú |
|---|---|---|---|
| Lesson (YAML) | **40** | `concepts_vi`, `examples_vi` | ~8-11 block mỗi bài |
| Quiz item mới trong lesson | **~160** (4/lesson) | tự soạn | MCQ, fill, predict_output; 15-25% là predict_output |
| Code exercise trong lesson | **~60** (1-2/lesson), ~240 test | `examples_vi` | Test nhỏ, chạy bằng Run |
| Practice problem | **63** = 59 bài chính + 4 bài bổ sung | `plan.json` + 4 bài mới | 4 bài cho `strings` (lấy 1 từ extra), `heapq_bisect`, `scope_closures`, `classes_basics` (lấy 1 từ extra); `interview_method` chỉ có quiz quy trình, không có bài code |
| Check problem (kind `check`) | **61** | `assessment.json` `write_code` | Chuyển bằng script từ `reference` + `driver` |
| Check problem bổ sung (kind `check`, mức 2, `write_code`) | **9** | tự soạn | 1 item cho mỗi mục trong danh sách 9 mục ở mục 3.4; tổng check problem = 70 |
| Check item không code | 51 (31 read_code + 20 concept) | `assessment.json` | Chuẩn hoá bằng script |
| Hidden test | **~1.200** = 63 × ~12 (3 sample + 9 hidden) + 70 × ~6 | sinh từ `solution.py` + `gen.py` | ~90% sinh bằng script; tay chỉ viết các trường hợp biên |
| Reference solution | 133 | tự viết (agent) | 61 cái đã có trong `assessment.json`; thêm `brute.py` cho mọi bài medium |
| Wrong/slow solution | ~190 | tự viết | 1-3 mỗi problem, dùng để kiểm tra bộ test |
| Hints | 63 × 3 | tự viết | |

Nếu tính cả 5 bài `extra` quan trọng mỗi tuần thì thêm ~20 problem, hoãn sang sau MVP; 65 bài thêm còn lại để M4+.

### 4.4 Pipeline nội dung

```
skill_tree.json ─► tools/sync_tree.py ─► content/index/*.json (snapshot + hash)
                                              │
        (1) Author agent (Sonnet): 1 subtopic/lượt │ input: node + items + plan problems
            ├─ lessons/…/<id>.yaml
            └─ problems/<id>/<slug>/{problem.yaml, solution.py, brute.py (medium), wrong/, tests/gen.py}
                                              ▼
        (2) tools/validate_content.py   (script, không phải LLM) — fail thì trả về agent
            ├─ schema + id tồn tại + prerequisite không vòng + block id không trùng
            ├─ chạy mọi code_sample/predict_output và so expected_output
            ├─ chạy gen.py → hidden.jsonl; solution.py phải qua 100% sample+hidden
            ├─ cross-check: brute.py (bắt buộc medium, tuỳ chọn easy) khớp solution.py trên 200 input từ `small_inputs(seed, n)` của gen.py (≤ 12 phần tử)
            ├─ mỗi wrong/*.py phải rớt ≥ 1 hidden; mỗi slow/*.py phải TLE ở stress test
            ├─ giới hạn thời gian: solution.py ≤ 0.3 × time_ms (native) trên mọi test; slow/*.py ≥ 3 × time_ms
            ├─ lesson có ≥ `min_items` (3) block `graded`
            ├─ mục có lesson đang validate phải có ≥ 1 item mastery check mức 2 loại write_code (9 mục ở 3.4); không chặn mục chưa soạn
            ├─ starter code chạy được và KHÔNG qua test (tránh đề lộ đáp án)
            ├─ code_exercise: solution qua test của nó
            ├─ sample ≥ 3 (practice/mock) / ≥ 1 (check, xem 3.4), hidden ≥ 8 (practice) / ≥ 5 (check), có test biên rỗng/1 phần tử
            └─ chặn nếu build `public` còn rewrite_required
                                              ▼   status: validated
        (3) Reviewer agent (instance khác, không thấy chat của author)
            checklist: đúng kiến thức; hợp trình độ gần mới bắt đầu; đề không mơ hồ;
            hint tăng dần, không lộ đáp án ở nấc 1; không dùng thuật ngữ chưa học
            (đối chiếu prerequisites); tiếng Việt tự nhiên. Ghi content/reviews/<id>.md
                                              ▼   status: reviewed
        (4) Quan đọc thử trong app (5 mục/tuần), nút "Báo lỗi" ghi bảng feedback
                                              ▼   status: published (commit vào main)
```

CI chạy thêm `tools/run_problem.py --engine pyodide` (Pyodide trong Node) cho các test có tag `stress`, để thời gian đo native và trong trình duyệt không lệch quá hệ số ×3.

Nguyên tắc: **LLM không bao giờ viết `expected` bằng tay**; mọi expected do `solution.py` tính, và `solution.py` được kiểm bằng brute-force độc lập. Mỗi lượt author làm một subtopic (lesson + toàn bộ problem của nó) để giữ ngữ cảnh gọn; chạy song song nhiều mục vì chúng độc lập (chỉ phụ thuộc id).

---

## 5. Chấm điểm & tiến độ

### 5.1 Định nghĩa sự kiện

- **lesson_done**: người học bấm "Hoàn thành bài học".
- **quiz_best**: tỉ lệ đúng cao nhất trên các block `graded` của lesson. Một **lượt** (`run_no`) là một lần làm lesson từ đầu; `run_no` tăng khi bấm "Làm lại lượt". Trong mỗi lượt chỉ tính lần trả lời **đầu tiên** của mỗi block, lấy lượt tốt nhất; cần ≥ `min_items` (3) block đã trả lời (validator bắt buộc lesson có ≥ 3 block `graded`).
- **AC**: Submit qua toàn bộ hidden test.
- **elapsed**: tổng thời gian editor của bài đang hiển thị (tạm dừng khi `document.hidden`), cộng dồn qua các phiên, từ lần mở đầu tiên (`attempts.started_at`) đến Submit AC đầu tiên; client gửi `elapsed_ms` kèm `POST /attempts`.
- **clean**: AC mà `solution_viewed=false`, `hints_used ≤ 1`, và `elapsed ≤ 1.5 × time_target_min` (hoặc `minutes` của check item). Bài kiểm tra "sạch" mới đủ làm bằng chứng điểm 2 và 3.
- **check pass (mức L)**: pass item mức L trong mastery check, tính "clean" theo cùng quy tắc. Trên mục có code, `concept` là tự chấm và không `clean`, nên mức 2 phải có item `write_code` (mục 3.4); trên **mục concept** một lần pass `concept`/`read_code` đúng, trong time-box là `clean`.
- **mục concept**: mục không có đường code nào — không có problem practice **và** không có item check `write_code` ở mọi mức (suy ra từ nội dung, không phải trường trong cây). Toàn bộ `sd` và 4 module `ml` là mục concept; mọi mục 40 py/dsa/cs đều có code nên không phải (luật của chúng không đổi).
- **review success**: thẻ ôn đạt (mục 5.4). `review_log.item_kind` = `code` (bài code ngắn) hoặc `recall` (thẻ nhớ nhanh); cả hai đều làm thẻ lên hộp. Chỉ `code` tính cho `retention_ok`, **trừ mục concept** thì `recall` cũng tính (vì mục concept không có bài code).

### 5.2 Quy tắc điểm 0-3 (chính xác)

```
score(subtopic, user):
  s1 = lesson_done AND quiz_best >= 0.7
  tested_out = có check pass mức 2 (clean)       # flow D
  tested_basic = có check pass mức 1 (clean) loại mcq HOẶC read_code, context=placement
                 # chỉ trong phiên placement; có đáp án trên server; concept tự chấm KHÔNG bao giờ
                 # tính; mức-1 diagnostic trong mastery KHÔNG tính (đổi bởi PR: placement leveled rungs)

  practice_ok = số problem practice khác nhau đạt AC >= min(2, số problem practice của mục)
                # mục không có problem practice: practice_ok = true
  check2_ok  = check pass mức 2 (clean)
               OR (đã trượt mức 2 >= 1 lần AND có 1 problem practice AC clean
                   AND số problem practice AC khác nhau >= min(2, số practice của mục))
               # lối thoát khi mục chỉ có 1 item mức 2; khớp practice_ok
               nếu mục không có item mức 2: 1 problem practice AC clean
               # mục concept: pass mức 2 là item concept/read_code (đã clean theo mục 5.1)
  s2 = tested_out OR (s1 AND practice_ok AND check2_ok)
       # practice chỉ cần AC thường; check mới cần clean

  level3_ok  = check pass mức 3 (clean) với item loại write_code   # concept/read_code không đủ
               nếu không có item mức 3 loại write_code (vd big_o chỉ có concept Q043):
                 1 problem practice độ khó medium AC clean
               mục concept (không có write_code): pass mức 3 (clean) item concept/read_code nếu có item mức 3, nếu không: true
               nếu cũng không có: true
  retention_ok = tồn tại review_log có success = true AND box_before >= 3
                 AND (item_kind = code OR mục là mục concept)
                 # lần ôn đạt đầu tiên ở hộp >= 3 rơi vào D+7; mục có code phải ôn bằng bài code,
                 # mục concept ôn bằng thẻ recall (không có bài code); đúng ý "còn nhớ sau >= 7 ngày"
  s3 = s2 AND level3_ok AND retention_ok

  score = 3 nếu s3; 2 nếu s2; 1 nếu s1 OR tested_out OR tested_basic; ngược lại 0
```

Hệ quả cần nhớ:

- **Điểm 1** = đã học và nhớ ý chính (kiến thức), đúng nghĩa thang "1 biết lý thuyết".
- **Điểm 2** = làm được bài cơ bản không cần xem đáp án. Đây là mức mở khoá mục sau.
- **Điểm 3** = làm được bài mức phỏng vấn **và** còn nhớ sau ≥ 7 ngày, nên điểm 3 không thể đạt trong ngày học đầu.
- Test out tối đa 2 (`tested_out` đã tính cả khi chưa học lesson; không có nhánh nào đạt 3 mà bỏ qua `level3_ok` và `retention_ok`).
- **Không có giảm điểm (decay) ở MVP**: bằng chứng điểm là vĩnh viễn, điểm không bao giờ tự giảm. Thẻ ôn trượt chỉ về hộp 1 và `lapses += 1`; `lapses` dùng để hiện bảng "mục yếu" ở `/progress`, không đổi điểm và không khoá lại mục nào.
- Điểm chỉ tính lại từ bảng sự kiện (`attempts`, `quiz_answers`, `check_results`, `review_log`), không lưu trạng thái thủ công; cột `user_subtopic.score` là cache, cập nhật sau mỗi sự kiện.

So khớp với `target_swe.intern` / `target_ai.intern`: Progress hiển thị điểm hiện tại / target; mục `target = 2` không bị coi thiếu khi đã đạt 2. Ví dụ `py.core.getting_started` có target intern 2.

**Ba ví dụ tính điểm** ("ngày N" là ngày lịch, chỉ để mô tả thời gian trôi giữa các sự kiện; ví dụ không ngụ ý Quan học đều mỗi ngày, ngày nào không học thì đơn giản không có sự kiện nào, và hạn ôn dời theo ngày ôn thật; `dict` có 1 bài practice `ransom-note`, check mức 2 = Q023, mức 3 = Q024):

1. *Đường thường, điểm 3 sớm nhất*. Ngày 2 Quan học `py.datastructs.dict`, quiz đúng 4/5 (0,8 ≥ 0,7) và bấm hoàn thành: `s1`, **điểm 1**, thẻ hộp 1 hẹn ngày 3. Cùng ngày AC `ransom-note` trong 6 phút, không xem lời giải: `practice_ok` (chỉ có 1 bài nên `min(2,1)=1`). Ngày 3 (giả sử Quan quay lại đúng hạn) làm mastery check, Q023 pass clean: `tested_out` (và `check2_ok`) nên `s2`, **điểm 2** (mở khoá mục phụ thuộc). Q024 pass clean ngay sau đó: `level3_ok` nhưng chưa `retention_ok`, vẫn điểm 2. Thẻ: ôn ngày 3 đạt (hộp 2, hẹn ngày 5), ngày 5 đạt (hộp 3, hẹn ngày 9), ngày 9 là thẻ hộp 3 nên item là một bài code ngắn (`item_kind = code`); đạt với `box_before = 3` nên `retention_ok`, **điểm 3 sớm nhất là ngày 9** (D+7). Nếu ngày 9 Quan ôn bằng thẻ nhớ nhanh (điện thoại hoặc preset "Phiên ngắn") thì thẻ vẫn lên hộp 4 nhưng `retention_ok` chưa có; lần ôn bằng bài code đạt kế tiếp (hộp 4, D+14) mới tính.
2. *Test out*. Quan đã biết `hashing_patterns` nhưng chưa học. Ngày 6 bấm Test out, giải item mức 2 trong time-box, không xem gợi ý: `tested_out`, **điểm 2 ngay** dù chưa có lesson_done, mục `prefix_sum` mở khoá; thẻ hộp 1 hẹn ngày 7 (ngày đạt + 1). Muốn lên 3 vẫn cần item mức 3 (`write_code`) và một lần ôn bằng bài code đạt ở hộp ≥ 3.
3. *Trượt rồi vẫn tiến được*. Giả sử một mục (vd `hash_tables`) chỉ có 1 item mức 2. Ngày 5 Quan trượt (WA), app chỉ hiện test sai, không hiện `reference`; `attempt_no = 1`. Bấm lại trước 24 giờ bị từ chối. Ngày 6 Quan AC `isomorphic-strings` clean và một bài practice khác (AC không cần clean) sau khi đã học lesson (`s1`): `practice_ok` đạt (2 bài), `check2_ok` đạt qua lối thoát (đã trượt mức 2 ≥ 1 lần), nên **điểm 2** mà không cần đậu check; hoặc làm lại check sau 24 giờ (`attempt_no = 2`).

### 5.3 Rule mở khoá

```
unlocked(n) = unlocked_at(n) IS NOT NULL
              OR ∀ p ∈ prerequisites(n):
                   p ∈ assumed          # vd cs.onramp.computer_programming_model
                OR (p có trong content AND score(p) >= 2)
status(n) = locked | unlocked | in_progress | done(score >= max(1, target_intern))
```

- **`tested_out` mở khoá chính mục đó**: khi mục đạt `tested_out` (Test out hoặc placement) mà `unlocked_at` còn null thì ghi `unlocked_at = now` cho chính mục (v0.6, làm rõ Flow D).
- **Mở khoá là một chiều**: khi `unlocked(n)` lần đầu đúng (sau mỗi lần điểm của một prerequisite thay đổi) thì ghi `user_subtopic.unlocked_at = now` và không bao giờ xoá. Vì MVP không có decay, điều này chủ yếu là lưới an toàn (ví dụ khi nội dung prerequisite được sửa và tính lại).
- Mục có `target_intern = 0` (vd `py.functions.scope_closures`) hiển thị "tuỳ chọn"; `done` luôn đòi tối thiểu điểm 1, nên mục target 0 không "xong" ở điểm 0.
- Mục khoá vẫn **đọc được ở chế độ xem trước** (lesson hiện, editor và Submit tắt) và có nút Test out.
- Prerequisite không có nội dung và không nằm trong `assumed` thì mục đó `blocked_missing_content` (chỉ xảy ra khi mở rộng cây; ở MVP có đúng 1 prerequisite ngoài, đã `assumed`).
- Thứ tự plan có thể xếp một mục đứng ngay sau prerequisite mới đạt 1 (vd `hash_tables` ngay sau `arrays` vừa học xong). Màn "Học tiếp" gắn nhãn khoá kèm lý do và đưa mục mở khoá kế tiếp lên trước; hai đường ra: làm bài của prerequisite để lên 2, hoặc Test out.

### 5.4 Ôn tập ngắt quãng: Leitner 5 hộp

Chọn Leitner (đơn giản, kiểm chứng được, khớp `review_schedule` D+1/3/7/14/28 đã có trong `assessment.json`), không dùng SM-2 vì cần chấm 0-5 mỗi lần, quá nặng cho ít thẻ.

**Lưu ý về nhịp học tự do:** các khoảng cách Leitner (D+1/3/7/14/28, rồi 30 ngày) **vẫn tính theo ngày lịch**, tính từ ngày ôn thực tế. Lý do: chúng mô hình sự quên theo thời gian, không liên quan đến khối lượng việc mỗi ngày. Không có định mức học hay ôn mỗi ngày; chỉ có hạn ôn của từng thẻ.

| Hộp (mới) | Khoảng cách tới lần ôn kế, `gap(box_mới)` | Lần ôn kế rơi vào (cộng dồn từ ngày học) |
|---|---|---|
| 1 | +1 ngày | D+1 |
| 2 | +2 ngày | D+3 |
| 3 | +4 ngày | D+7 |
| 4 | +7 ngày | D+14 |
| 5 | +14 ngày | D+28 |
| đạt tiếp khi đang ở hộp 5 | +30 ngày, lặp lại | D+58, D+88, ... |

Quy tắc:

1. **Tạo thẻ** khi mục đạt điểm ≥ 1 lần đầu: `box=1`, `due = ngày của sự kiện làm điểm lần đầu ≥ 1 + 1`, trong đó sự kiện là `lesson_done` hoặc check pass (test out), cái nào đến trước. **Ngoại lệ (v0.6)**: thẻ do một phiên placement tạo hàng loạt được rải `due = ngày đạt + 1 + ⌊k/8⌋` (k = thứ tự từ 0 theo thứ tự plan trong phiên) để tránh dồn 20+ thẻ vào một ngày; không phải trần thẻ, mỗi thẻ vẫn có hạn và không bị phạt.
2. **Đạt**: `box = min(box+1, 5)`; `due = ngày ôn + gap(box_mới)` với `gap = {1:1, 2:2, 3:4, 4:7, 5:14}` (tính từ ngày ôn thật, nên trễ hạn không dồn nợ). Đạt khi đang ở hộp 5 thì `box` giữ 5 và `gap = 30`. Chuỗi lý tưởng: D+1, D+3, D+7, D+14, D+28, rồi mỗi 30 ngày.
3. **Trượt**: `box = 1`, `due = ngày ôn + 1`, `lapses += 1`.
4. **Nội dung thẻ**: hộp 1-2 lấy 1 item nhớ nhanh (quiz/predict_output/read_code, ~2-3 phút); hộp 3-5 lấy 1 problem (ưu tiên bài chưa làm sạch, rồi bài lâu nhất chưa gặp; ~10-15 phút); trong preset "Phiên ngắn" (quy tắc 5) nếu đã có 2 thẻ code thì thẻ hộp 3-5 còn lại dùng item nhớ nhanh. Đạt = trả lời đúng hoặc AC clean; trượt = sai hoặc AC không clean. Thiết bị không có editor (dưới 768px, `UI_SPEC.md` 3.5) và preset "Phiên ngắn" dùng item nhớ nhanh (`item_kind = recall`) cho thẻ hộp 3-5: đạt thì thẻ vẫn lên hộp (giữ lợi ích của điện thoại), nhưng **không tính cho `retention_ok`** (cần `item_kind = code`, mục 5.2). `review_log.item_kind` ghi loại item.
5. **Không có trần thẻ.** `/review` hiện toàn bộ thẻ đến hạn, sắp: quá hạn nhiều nhất trước, tie-break điểm thấp trước. Quan làm bao nhiêu thẻ tuỳ ý trong một phiên và dừng lúc nào cũng được; thẻ chưa làm vẫn đến hạn, không phạt, không dồn nợ (lần ôn kế tính từ ngày ôn thật, quy tắc 2). **Preset "Phiên ngắn"** là tuỳ chọn, không phải giới hạn: lấy `settings.review_preset` thẻ đầu hàng (mặc định cỡ 6, tắt được) với tối đa 2 thẻ code (~10-15 phút mỗi thẻ) + còn lại là thẻ nhớ nhanh (~2-3 phút mỗi thẻ), khoảng 30-40 phút; sau khi xong preset vẫn có nút "Ôn tiếp" để làm thêm.
6. Ngày tính theo múi giờ trong settings (mặc định `Asia/Ho_Chi_Minh`), hạn là theo ngày, không theo giờ.
7. **Cảnh báo backlog mềm**: khi số thẻ đến hạn > `settings.backlog_warn` (mặc định 20), `/` hiện banner "Đang có N thẻ đến hạn; nên ôn trước khi học bài mới" với nút [Ôn ngay] và [Bỏ qua]. Chỉ là gợi ý, không khoá bài học và không đổi điểm.

### 5.5 Thứ tự plan ↔ "Học tiếp" ↔ review queue

- **Plan chỉ là thứ tự gợi ý.** Các `days[N]` của `plan.json` được dùng như nhóm thứ tự: khoá sắp xếp của subtopic là `(N, vị trí trong ngày)`, nhóm đã nằm trong `plan_order` (mục 6.3). Không có ngày bắt đầu, không có "ngày hiện tại", không có con trỏ ngày, không so sánh với lịch.
- **Học tiếp** gồm hai nhóm, trả về bởi `GET /next`:
  1. **"Cần lên điểm 2 để mở mục sau"** (đặt trên cùng, chỉ hiện khi có): mọi prerequisite `done` hoặc đang dở nhưng điểm < 2 mà đang chặn mục `unlocked`-kế-tiếp theo thứ tự plan (vd `memory_model` có `target_intern = 1` nên `done` ở điểm 1, nhưng `arrays` cần nó ≥ 2). Mỗi dòng ghi mục nào sẽ được mở và kèm bài gợi ý (practice chưa AC, rồi nút Test out). **Bài luyện gợi ý lấy từ nhóm này trước**, rồi mới tới bài của nhóm 2. Nhóm này không đổi `done` của 5.3 (không đổi điểm hay trạng thái).
  2. **Danh sách theo thứ tự plan**: các subtopic `unlocked` chưa `done`, khoá sắp xếp `(N, vị trí)`; mục `in_progress` lên đầu, trừ mục đang bị `check_retry_locked` (chờ làm lại check 24 giờ): mục đó gắn nhãn "chờ đến <giờ>" và xếp **sau** các mục làm được ngay. Mục còn khoá hiện bên dưới kèm lý do, còn mục mở khoá kế tiếp được đưa lên trước. Bài `practice` chưa Accepted của mục đang học, rồi bài `extra`. Hiển thị vài mục kèm "xem thêm"; không giới hạn số mục học trong một ngày.
- Thẻ ôn sinh từ **sự kiện thật** (`lesson_done` hoặc check pass), không từ lịch của plan, nên học nhanh, chậm hay nghỉ đều không làm hỏng queue.
- `plan.days[N].review` (`D+1`, `D+3`, `D+7`, mỗi mục có `subtopic`, `lc`, `title`) trở thành **danh sách bài ôn gợi ý gắn với subtopic** (`review_hint`, một mục có thể có nhiều bài, không gắn ngày). Khi thẻ của `subtopic` đó đến hạn ở hộp 3-5 (cần bài code), thẻ chọn trong danh sách bài chưa làm sạch trước (rồi bài lâu nhất chưa gặp, khớp quy tắc 4 của 5.4); nếu danh sách trống hoặc hết bài hợp lệ, queue chọn item theo mục 5.4. Hộp 1-2 luôn dùng câu nhớ nhanh.
- **Mock theo tiến độ, không theo ngày.** Mock 1 (plan ngày 7) mở khi mọi subtopic của nhóm tuần 1 (28 mục) đạt `done`, **không tính mục có `target_intern = 0`** (tuỳ chọn, vd `scope_closures`; các mục này không nằm trong `unlock_after`); mock 2 (plan ngày 14) mở khi xong bộ mục của tuần 2 (M4). Khi mở, `/` hiện thẻ "Mock" (M4 mới làm được; MVP chỉ hiển thị mô tả và liên kết sang `Meta_2026_Intern_NewGrad_Mock.docx`, kèm số mục còn lại trước khi mở). Mock là gợi ý, không bắt buộc.
- Nhật ký `review_log` dùng để vẽ "đúng/sai theo hộp" ở `/progress`.

### 5.6 Placement (đánh giá trình độ đầu vào): quy tắc gieo điểm

Thuật toán chọn item, ngân sách thời gian và luật dừng nằm ở `UI_SPEC.md` mục 2. Phần dưới là phần **thuộc luật điểm** nên đặt ở đây:

1. Placement là một phiên mastery check xếp theo đồ thị tiền đề, chạy bằng cùng engine flow C/D và **chỉ ghi `check_results`** (kèm `context=placement`); điểm vẫn do `scoring.py` tính lại từ sự kiện, nên không có luật điểm riêng.
2. Mỗi cổng leo tối đa 3 **rung** (đổi bởi PR: placement leveled rungs), mỗi rung một item: **P0 kiến thức** (`mcq`, mức 1, ~1 phút, đáp án giữ trên server), **P1 truy vết** (`read_code`, mức 1, ~2 phút, "code in ra gì?", so khớp chuỗi) và **P2 code** (`write_code` mức 2 của cổng, 6-9 phút). Item P0/P1 nằm ở `content/placement/` (kho riêng, không lẫn `content/checks`); cổng chưa có P0/P1 chạy P2 như cũ. P0 trượt hoặc "Không biết" = `knowledge_gap` (không hỏi P1/P2, chỉ thử P0 của cổng ngay dưới rồi dừng); P0 đạt thì hỏi P1; P1 trượt thì dừng cổng đó (đặt `known_basic`) và thử P2 của cổng ngay dưới; P1 đạt thì hỏi P2; P2 đạt thì lên cổng kế (bắt đầu từ P0 của nó); P2 trượt thì thử P2 của cổng ngay dưới rồi dừng. Item vào mức 2 chỉ là `write_code`; `concept` không bao giờ được hỏi ở placement.
3. Đậu mức 2 sạch (P2 `write_code`) = `tested_out` → điểm 2 và mở khoá (5.3); điểm 2 **chỉ** đến từ đây (mục có code). Đậu P0 hoặc P1 sạch (item `mcq`/`read_code` mức 1) = `tested_basic` → **điểm 1** (không mở khoá). Đậu mức 3 sạch (item `write_code`) = `level3_ok`, **điểm vẫn 2** (cần `retention_ok`). Placement **không bao giờ ghi điểm 3**, và không bao giờ ghi điểm 1 từ item `concept` tự chấm (dễ bị gian lận).
4. Chỉ đậu P0/P1 (không đậu P2) = điểm 1 qua `tested_basic` và đặt `user_subtopic.known_basic = true` ("đã biết sơ") để hiển thị lesson rút gọn. Cờ này không đổi `lesson_done` hay `quiz_best`.
5. Suy luận theo đồ thị tiền đề/cụm chỉ ghi `placement_hint` (`likely_known`/`likely_gap`) để hiển thị và gợi ý Test out; không bao giờ thành điểm và bị xoá khi mục có bằng chứng thật.
6. Trượt thật (đã nộp) tính như trượt check mức 2 (`attempt_no`, khoá làm lại 24 giờ, mở lối thoát `check2_ok`); "Không biết" ghi `gave_up=true` và không khoá, không tính trượt **cho điểm/khoá** nhưng được tính để **dừng sớm** (`UI_SPEC.md` 2.4 S1). E2 trượt mở sẵn lối thoát `check2_ok` là chủ đích (vô hại: lối thoát vẫn cần 2 practice AC). Bỏ qua placement không ghi gì.
7. **Pha khái niệm (track System Design / AI-engineer, không có code)**: khi bậc thang cổng code dừng, nếu track của hồ sơ (`swe` → module System Design, `ai` → module AI) có module đã soạn item, người dùng tự báo module nào mình đã biết (`POST /placement/{id}/modules`, tối đa 4 module, theo thứ tự cây). Mỗi module chọn thành một **cổng khái niệm** trên **subtopic hub** của module (`CONCEPT_HUBS` trong `services/placement.py`), gồm 2 rung, mỗi rung một `mcq` có đáp án giữ trên server, item ở `content/placement/<hub>.yaml`: **C1** `mcq` mức 1 (nhận biết), đậu sạch = `tested_basic` → **điểm 1** trên hub; **C2** `mcq` mức 2 (áp dụng), đậu sạch = `tested_out` → **điểm 2** + mở khoá qua đường concept (hub là subtopic concept; đây là bằng chứng được duyệt, có đáp án, không tự chấm). C2 chỉ được hỏi sau khi đậu C1 nên điểm 2 cần **hai** lần đậu có đáp án (chống đoán mò MCQ). C1 trượt/"Không biết" = `knowledge_gap`, không hỏi C2, hậu duệ của hub gắn `likely_gap`; C1 đậu mà C2 trượt giữ điểm 1 và `known_basic`. C2 đậu thì tiền đề của hub gắn `likely_known`. Suy luận theo đồ thị chỉ là nhãn hiển thị (`placement_hint`), không bao giờ thành điểm. Cổng khái niệm không leo lên, không thử cổng dưới; hết cổng thì dừng với `concept_done`. Module chưa có item mức 1 và mức 2 ở hub thì không được mời.

---

## 6. Kiến trúc kỹ thuật

### 6.1 Stack chọn (một lựa chọn)

**Frontend**: React 18 + TypeScript + Vite; CodeMirror 6 (editor, nhẹ, dùng được trên điện thoại); `react-markdown` + `remark-gfm` + `shiki` (render lesson); `react-resizable-panels` (split view); TanStack Query; Zustand (state cục bộ).
**Backend**: Python 3.12 + FastAPI + SQLModel/SQLAlchemy + Alembic, **SQLite** (WAL). Quan dùng Python nên tự đọc và sửa được; agent viết Python backend + script content dùng chung ngôn ngữ.
**Chạy code Python**: Pyodide trong Web Worker (mục 6.2).
**Đóng gói**: một container (uvicorn phục vụ API và thư mục build tĩnh của frontend), `docker compose up`; hoặc chạy trực tiếp `make dev`.

| Tiêu chí | **A. React/Vite + FastAPI + SQLite (chọn)** | B. Next.js full-stack + Postgres (Supabase) | C. SPA thuần, local-first (IndexedDB), không backend |
|---|---|---|---|
| Chi phí 1 người | 0 đ (local) hoặc VPS 5 USD | 0 đ (free tier) nhưng phụ thuộc dịch vụ ngoài | 0 đ |
| Quan tự sửa được | Dễ (Python) | Trung bình (TS full-stack) | Trung bình |
| Đường lên nhiều người dùng | Thêm auth, đổi SQLite → Postgres, bật runner server | Có sẵn auth/DB | Phải viết lại toàn bộ phần lưu trữ |
| Chạy tool content/script cùng ngôn ngữ | Có (Python) | Không (TS) | Không |
| Dữ liệu tiến độ | File SQLite, backup dễ | Trên cloud | Trong trình duyệt, dễ mất |
| Offline | Local = có | Không | Có |
| Giấu hidden test/lời giải | Server giữ, chỉ gửi khi Submit | Tương tự A | Không giấu được (nằm trong bundle) |

Chọn A vì cân bằng: rẻ, Quan sửa được, sẵn đường lên nhiều người dùng, và hidden test/lời giải có chỗ để giấu.

### 6.2 Code runner: so sánh và quyết định

| Tiêu chí | **Pyodide (WASM trong Web Worker)** | Judge0 CE tự host (Docker + isolate) | Tự viết: Docker/nsjail/gVisor mỗi lần chạy |
|---|---|---|---|
| Chi phí | 0 (chạy trên máy Quan) | Cần Docker đặc quyền + máy 1-2 GB RAM (VPS ~5-10 USD/tháng) | Tương tự, kèm công bảo trì |
| An toàn | Sandbox của trình duyệt; code không chạm máy chủ | Tốt (isolate, cgroups) | Tốt nếu cấu hình đúng, dễ sai |
| Độ trễ | Lần đầu tải ~12 MB (self-host, cache sau đó), chạy tức thì | Vài trăm ms + mạng | Tuỳ |
| Giới hạn thời gian | Watchdog: giết worker | Chính xác | Chính xác |
| Giới hạn bộ nhớ | **Không ép được** (chỉ cảnh báo) | Có | Có |
| Java | Không | Có (Judge0 hỗ trợ Java) | Có |
| Gói thư viện | `numpy`, `pandas` có; `torch` không | Tuỳ image | Tuỳ image |
| Chấm đáng tin | Client tự báo kết quả; chấp nhận cho 1 người | Server chấm | Server chấm |
| Nhiều người dùng | Không đủ tin cậy | Phù hợp | Phù hợp |

**Quyết định**: MVP dùng **Pyodide** vì một người dùng, miễn phí, an toàn mặc định, chấm tức thì, không phải vận hành sandbox. Đặt sau interface `Runner` để M5 thêm runner server (Judge0 CE tự host) cho Java và M7 cho nhiều người dùng, không đổi UI hay API.

Hợp đồng `Runner` (TypeScript):

```ts
interface Runner {
  language: 'python' | 'java';
  run(req: {
    code: string;
    io: ProblemIO;             // mode/entry/params/compare như problem.yaml
    tests: TestCase[];         // sample hoặc hidden
    limits: { time_ms: number; memory_mb: number };
    onProgress?: (r: TestResult) => void;
  }): Promise<RunResult>;      // { verdict, results[], stdout, stderr, elapsed_ms }
}
```

Cách Pyodide runner làm việc:

0. **Self-host, pin phiên bản**: bản core Pyodide (~12 MB) đặt ở `apps/web/public/pyodide/`, ghim một phiên bản cụ thể trong lockfile; không nạp từ CDN (CSP `connect-src 'self'` sẽ chặn).
1. Một Web Worker giữ sẵn (khởi động nền khi mở app), nạp `harness.py` (dựng ListNode/TreeNode, so sánh theo `compare`, bắt stdout/stderr).
2. Mỗi test chạy tuần tự; worker gửi `progress` sau từng test. Luồng chính giữ watchdog `time_ms × time_multiplier.pyodide` (mặc định 3) cho mỗi test; quá hạn thì `terminate()` worker, đánh test đó TLE, bỏ qua test còn lại, dựng worker mới ở nền (~2-3 giây).
3. `sys.setrecursionlimit(1000)` giữ như CPython; `input()` được cài bằng `pyodide.setStdin` trong worker (hoặc override `builtins.input` trong `harness.py`) và đọc từ `stdin` của test.
4. CSP của trang: `script-src 'self' 'wasm-unsafe-eval'; worker-src 'self'; connect-src 'self'; font-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:` (v0.6: thêm font/style/img cho font tự host và thẻ `<style>` của CodeMirror), để code người dùng không gọi ra ngoài và WebAssembly của Pyodide vẫn chạy được; worker không có quyền DOM.
5. Sai khác cần biết: không ép được `memory_mb`; thời gian chậm hơn native 2-5 lần (hệ số nhân ×3 bù, và validator buộc `solution.py` ≤ 0.3 × `time_ms` native nên lời giải đúng không bị TLE oan; CI kiểm lại bằng Pyodide trong Node, mục 4.4); hidden test có thể xem được khi Quan mở DevTools. Với một người đang tự học, rủi ro này chấp nhận; cơ chế "xin hidden test chỉ lúc Submit" vẫn giữ để tập thói quen và sẵn cho M7.

### 6.3 Mô hình dữ liệu (SQLite; mọi bảng tiến độ có `user_id`)

Nội dung (đọc từ file, nạp vào bảng lúc khởi động, khoá ngoại tới `subtopics`):

| Bảng | Field chính |
|---|---|
| `subtopics` | `id` PK, `name_vi`, `section`, `module`, `ord`, `prereqs` (JSON), `target_intern`, `target_ai`, `targets` (JSON `{swe:{intern,fresher}, ai:{intern,fresher}}`, v0.6: chỉ để hiển thị vòng đích theo hồ sơ; `done` vẫn dùng `target_intern`), `est_hours`, `summary_vi`, `mastery_bar_vi`, `content_status` |
| `lessons` | `subtopic_id` PK/FK, `version`, `path`, `content_hash`, `est_minutes` |
| `problems` | `id` PK, `subtopic_id`, `kind`, `title`, `difficulty`, `source_type`, `lc`, `time_target_min`, `path`, `content_hash`, `version` |
| `quiz_items` | `id` PK (`<lesson>#<block>` hoặc id assessment), `subtopic_id`, `source` (`lesson`/`assessment`), `level`, `type`, `graded` |
| `plan_order` | `ord` PK (= `day` trong plan.json, chỉ là thứ tự nhóm, không là lịch), `week`, `subtopic_ids` (JSON, đã sắp thứ tự), `problem_ids` (JSON), `review_hints` (JSON: `subtopic` → danh sách bài ôn gợi ý `[problem_id...]`), `est_hours` (chỉ hiển thị, không là ngân sách) |
| `plan_milestones` | `id` PK (vd `mock1`), `kind` (`mock`), `unlock_after` (JSON: danh sách subtopic phải `done`; loại mục `target_intern = 0`), `ref` (liên kết mô tả) |

Người dùng và tiến độ:

| Bảng | Field chính |
|---|---|
| `users` | `id` PK, `name`, `created_at`. MVP: đúng một dòng `id=1` |
| `settings` | `user_id` PK, `tz`, `review_preset` (int, null = tắt nút "Phiên ngắn"; mặc định cỡ 6), `backlog_warn` (int, mặc định 20), **v0.6**: `target_role` (`intern`\|`new_grad`), `track` (`swe`\|`ai`), `language`, `experience` (`none`\|`some`\|`solid`), `display_name`, `onboarded_at`, `backup_every_hours` (6), `backup_keep` (20), `ui_prefs` (JSON: theme, cỡ chữ, bố cục). Không có ngày bắt đầu plan, con trỏ ngày hay trần thẻ |
| `study_time` | `(user_id, day)` PK (`day` theo `tz`), `seconds`. Cộng dồn thời gian tương tác thật (tab hiện, có thao tác trong 2 phút gần nhất) để vẽ tổng theo tuần và heatmap; chỉ để xem, không có mục tiêu |
| `user_subtopic` | `(user_id, subtopic_id)` PK, `score` (0-3, cache), `lesson_done_at`, `quiz_best`, `tested_out`, `unlocked_at` (null = chưa mở; ghi một lần, không xoá), `status`, `updated_at`, **v0.6**: `known_basic` (bool, từ placement mức 1), `placement_hint` (`likely_known`\|`likely_gap`\|null, chỉ hiển thị), `placement_session_id` |
| `quiz_answers` | `id`, `user_id`, `quiz_item_id`, `run_no` (lượt làm lesson), `attempt_no`, `answer` (JSON), `correct`, `answered_at` |
| `attempts` | `id`, `user_id`, `problem_id`, `mode` (`run`/`submit`), `language`, `code`, `verdict`, `passed`, `total`, `elapsed_ms` (thời gian editor hiển thị, cộng dồn), `runtime_ms`, `hints_used`, `solution_viewed`, `clean`, `started_at` (lần mở đầu tiên của bài), `submitted_at`, `problem_version` |
| `check_results` | `id`, `user_id`, `subtopic_id`, `item_id`, `level`, `attempt_no`, `passed`, `clean`, `minutes_used`, `taken_at`, **v0.6**: `session_id`, `context` (`mastery`\|`test_out`\|`placement`), `gave_up` (khoá làm lại 24 giờ chỉ tính `passed=false AND gave_up=false`) |
| `check_sessions` (v0.6) | `id`, `user_id`, `subtopic_id`, `context`, `placement_session_id`, `order_no`, `status` (`in_progress`\|`done`\|`expired`; không hoạt động 24 giờ thì `expired`, không tính trượt), `ladder` (JSON), `current_item_id`, `elapsed_ms` (chỉ thời gian hoạt động), `started_at`, `last_active_at` |
| `placement_sessions` (v0.6) | `id`, `user_id`, `scope` (`all`\|`module:<id>`), `kind` (`initial`\|`retake`\|`continue`), `status` (`in_progress`\|`finished`\|`skipped`\|`stale`; 7 ngày không hoạt động thì `stale`), `experience_prior`, `phase` (`A`\|`B`\|`C`), `state` (JSON trạng thái từng mục), `result` (JSON), `active_ms`, `budget_soft_min` (45), `budget_hard_min` (60), `parent_id`, `started_at`, `last_active_at`, `finished_at`, `acknowledged_at` |
| `review_cards` | `(user_id, subtopic_id)` PK, `box`, `due_on` (date), `last_reviewed_at`, `lapses`, `consecutive_passes`, `suspended`, **v0.6**: `current_item_ref`, `current_item_opened_at` (ghim item của thẻ đang mở để mở lại vẫn cùng item) |
| `review_log` | `id`, `user_id`, `subtopic_id`, `item_ref`, `item_kind` (`code`\|`recall`, v0.7; server suy từ `item_ref`), `box_before`, `box_after`, `success`, `reviewed_at` |
| `drafts` | `(user_id, problem_id, language)` PK, `code`, `updated_at`, **v0.6/0.7**: `cursor`, `elapsed_ms` (đồng hồ bài, chép sang `attempts` lúc Run/Submit; `attempts` chưa tồn tại trước lần Run đầu), `started_at` (lần mở đầu tiên của bài), `rev` (M3, đối chiếu bản). M1: client lưu IndexedDB sau 300 ms (độ bền `strict`), gửi server sau 2 giây không gõ (tối đa 10 giây) và khi blur/pagehide; bản mới hơn theo `updated_at` thắng (một thiết bị) |
| `draft_versions` (v0.6, làm ở M3 cùng 409) | `(user_id, problem_id, language, rev)` PK, `code`, `saved_at`; giữ 5 bản gần nhất mỗi bài (bản bị thay khi đối chiếu 409) |
| `feedback` | `id`, `user_id`, `target_type`, `target_id`, `note`, `created_at` |
| `events` | `id`, `user_id`, `type`, `payload` (JSON), `ts` (append-only, để tính lại điểm và thống kê), **v0.6**: `occurred_at` (giờ client, kẹp trong [nhận − 7 ngày, nhận + 5 phút]), `received_at`, `idem_key` |
| `resume_state` (v0.6) | `user_id` PK, `mode` (`lesson`\|`problem`\|`check`\|`placement`\|`review`\|`other`), `route`, `ref` (JSON: `subtopic_id`/`problem_id`, `block_id`, `scroll_in_block`, `tab`, `cursor`), `context` (JSON, vd cỡ phiên ôn), `updated_at`, `device_id` |
| `idempotency_keys` (v0.6) | `key` PK, `user_id`, `method`, `path`, `status`, `response` (JSON), `created_at`; giữ 30 ngày |

Chỉ mục: `attempts(user_id, problem_id, submitted_at)`, `review_cards(user_id, due_on)`, `study_time(user_id, day)`, `quiz_answers(user_id, quiz_item_id, run_no)`, `check_results(user_id, subtopic_id, level, taken_at)` (kiểm tra chờ 24 giờ). `content_hash` đổi (nội dung sửa) thì ghi `problem_version` mới; attempts cũ giữ nguyên.

### 6.4 API (JSON, prefix `/api`; MVP dùng user cố định qua dependency `current_user()`)

| Method & path | Mục đích |
|---|---|
| `GET /me` | user, settings, `onboarding{profile_done, placement: none\|in_progress\|finished\|skipped}` |
| `PUT /profile` | hồ sơ lần đầu: `target_role`, `track`, `language`, `experience`, `display_name`, `tz` (v0.6) |
| `POST /placement` · `POST /placement/skip` · `GET /placement/current` · `GET /placement/{id}` | tạo phiên (`scope`, `kind`), bỏ qua ("bắt đầu từ đầu", không gieo điểm), phiên đang dở, trạng thái phiên (v0.6; `UI_SPEC.md` mục 2) |
| `POST /placement/{id}/answer` · `POST /placement/{id}/heartbeat` · `POST /placement/{id}/finish` · `GET /placement/{id}/result` | nộp item (ghi `check_results`), heartbeat tuyệt đối `active_ms`/`elapsed_ms`, kết thúc, kết quả (skill map đã gieo, mạnh/yếu, `start`, `sweep`, `est_hours_remaining`) |
| `GET /resume` · `PUT /resume` (+ `POST /resume` cho `sendBeacon`) | việc dở để banner "Tiếp tục nơi bạn dừng": `{primary, others[], in_progress}`; ghi vị trí hiện tại (v0.6) |
| `GET /health` | healthcheck docker (mở được DB) |
| `GET /backups` · `POST /backups` · `GET /backups/{name}` · `POST /backups/{name}/restore` · `POST /reset` | danh sách, sao lưu ngay, tải về, khôi phục (tự backup bản hiện tại, kiểm `integrity_check`), xoá toàn bộ tiến độ (cần token xác nhận) (v0.6) |
| `PUT /settings` | tz, review_preset, backlog_warn |
| `GET /map` | tất cả subtopic + `status`, `score`, `unlocked`, `due_cards`, lý do khoá |
| `GET /subtopics/{id}` | metadata + trạng thái + danh sách problem/check |
| `GET /lessons/{subtopic_id}` | lesson đã build (đã loại `solution` của code_exercise) |
| `POST /lessons/{subtopic_id}/complete` | đánh dấu hoàn thành, tính `quiz_best` (theo `run_no`), tạo thẻ ôn |
| `POST /lessons/{subtopic_id}/runs` | "Làm lại lượt": mở `run_no` mới, trả `run_no` |
| `POST /quiz/answers` | lưu một câu trả lời (nhận `run_no`), trả `correct` + `explain_md` |
| `GET /problems?subtopic=&difficulty=&status=&kind=` | danh sách bài + trạng thái |
| `GET /problems/{id}` | đề, starter, sample test, hints đã mở (không có hidden, không có lời giải) |
| `GET /problems/{id}/tests/hidden` | chỉ trả sau `POST /problems/{id}/start-submit` còn hiệu lực (token 15 phút) |
| `POST /problems/{id}/hints` | mở nấc gợi ý kế tiếp (tăng `hints_used`) |
| `GET /problems/{id}/solution` | lời giải mẫu; ghi `solution_viewed=true` |
| `POST /attempts` | ghi kết quả Run/Submit từ client (`code`, `verdict`, `passed`, `total`, `elapsed_ms`, ...); server tính `clean`, cập nhật điểm |
| `PUT /drafts/{problem_id}` | lưu nháp `{code, base_rev, updated_at, cursor}`; M1 ghi đè theo `updated_at`; M3 thêm `base_rev` và 409 kèm bản server |
| `POST /checks/{subtopic_id}/start` · `POST /checks/{subtopic_id}/answer` · `POST /checks/{session_id}/heartbeat` | mastery check theo thang bậc (`start` trả `session_id` và tiếp tục phiên đang dở nếu còn trong 24 giờ); trả item kế tiếp hoặc kết quả. Trượt mức 2 không trả `reference`; `start` trong vòng 24 giờ sau lần trượt mức 2 trả lỗi `check_retry_locked` kèm `retry_after`; mỗi lần ghi `attempt_no` mới |
| `GET /review/queue` | **toàn bộ** thẻ đến hạn, sắp quá hạn nhiều nhất trước rồi điểm thấp; không có trần. `?preset=1` chỉ trả phần đầu theo `review_preset` (tối đa 2 thẻ code); `item` được chọn khi mở từng thẻ |
| `POST /review/{subtopic_id}/result` | `success` + `item_ref` → cập nhật hộp, `review_log` |
| `GET /next` | "Học tiếp": nhóm `must_raise` ("Cần lên điểm 2 để mở mục sau": prerequisite đang chặn, kèm mục sẽ mở và bài gợi ý, đặt trên đầu), rồi subtopic mở khoá kế tiếp theo thứ tự plan (mục chờ `check_retry_locked` có `retry_after`, xếp sau mục làm ngay), bài luyện gợi ý (từ `must_raise` trước), số thẻ đến hạn kèm cờ `backlog` (vượt `backlog_warn`), mốc (mock) đã mở hoặc còn thiếu bao nhiêu mục. Không có ngày, không có trạng thái "trễ" |
| `POST /activity/ping` | client gọi mỗi ~30 giây khi đang tương tác; server cộng `min(now - last_ping, 60 giây)` vào `study_time` của ngày hiện tại (theo `tz` tại thời điểm ping); bỏ qua nếu khoảng cách > 2 phút; `last_ping` lưu theo `user_id` nên nhiều tab không cộng đôi |
| `GET /stats` | dữ liệu cho `/progress`: điểm theo mục, tổng giờ theo tuần, heatmap `study_time`, mục yếu |
| `POST /feedback` | báo lỗi nội dung |
| `GET /export` · `POST /import` | dump/khôi phục toàn bộ dữ liệu của user (JSON) |

Quy ước: mọi POST ghi trạng thái nhận header `Idempotency-Key` (uuid do client sinh lúc tạo sự kiện; gửi lại cùng key trả đúng phản hồi cũ, không chạy lại logic); heartbeat gửi giá trị tuyệt đối nên gửi lại an toàn; `POST /activity/ping` nhận thêm `resume` để cập nhật `resume_state`; `GET /next` thêm nhóm `sweep[]` (mục `likely_known`); lỗi trả `{error: {code, message}}`; thời gian dạng ISO 8601 UTC; ngày ôn tập dạng `YYYY-MM-DD` theo `tz`. Multi-user (M7) chỉ đổi `current_user()` sang đọc token; handler không đổi.

### 6.5 Cấu trúc repo

Tên repo đề xuất `prep-app` (monorepo, riêng tư). Chưa tạo trên GitHub; thư mục `/mnt/project-files/learning-app/` giữ spec cho đến khi Quan tạo repo.

```
prep-app/
  README.md  Makefile  docker-compose.yml  .github/workflows/ci.yml
  apps/
    web/                       Vite + React + TS
      src/{routes,components,editor,runner,lib,state}/
      src/runner/{Runner.ts, pyodide/worker.ts, pyodide/harness.py}
      public/pyodide/          Pyodide core self-host, pin phiên bản (~12 MB)
    api/                       FastAPI
      app/{main.py, deps.py, models/, routers/, services/}
      app/services/{scoring.py, unlock.py, leitner.py, plan.py, content_loader.py}
      migrations/  tests/
  content/                     như mục 3.1
  tools/                       Python, chạy bằng `uv run`
    sync_tree.py  convert_checks.py  validate_content.py  build_bundle.py
    run_problem.py             chạy solution/wrong/slow bằng harness chung với runner (--engine native|pyodide)
    import_mock.py             (M4)
  data/                        .gitignore: app.db, backups/
  docs/                        SPEC.md (bản sao), ADR ngắn
```

Hai nguyên tắc: (1) `harness.py` là **một file duy nhất** dùng cho cả worker Pyodide trong trình duyệt lẫn `tools/run_problem.py` khi validate, để "pass ở validator" và "pass trong app" luôn cùng nghĩa; (2) logic điểm/unlock/Leitner nằm trong `services/` thuần hàm, có unit test với bảng ví dụ của mục 5.

### 6.6 Nạp nội dung

`tools/build_bundle.py` (chạy trong CI và `make build`) làm 3 việc: validate (mục 4.4), gom thành `build/content/` gồm `index.json`, `lessons/<id>.json`, `problems/<id>/public.json` (đề, starter, sample, hints đã xáo) và `private/<id>/{hidden.jsonl, solution.py}`. Thư mục `private/` chỉ API đọc (không nằm trong static dir). Lúc khởi động, `content_loader.py` đọc `index.json` và upsert các bảng nội dung theo `content_hash`; lesson/problem được phục vụ từ file, không nhét vào DB. Sửa nội dung = commit + build lại, không cần migration.

### 6.7 Triển khai cho một người

- **Mặc định: chạy cục bộ** `docker compose up` (hoặc `make dev`), dữ liệu ở `data/app.db`. Cấu hình compose (v0.6): `restart: unless-stopped` (tự dậy sau khi khởi động lại máy; cần bật Docker khởi động cùng hệ thống), `healthcheck` gọi `GET /api/health` (trả cả `journal_mode`), cổng `127.0.0.1:8080:8080` (đặt `BIND=0.0.0.0` trong `.env` nếu muốn dùng qua LAN), một worker uvicorn. **DB nằm trong named volume `app_data:/app/data`** (mặc định mọi hệ điều hành; bind mount `./data` chỉ dùng trên Linux native) vì bind mount của Docker Desktop (macOS/Windows) không bảo đảm `fsync` xuống đĩa thật. **Backup** là file thường nên ghi ra thư mục host `./backups` (bind) và `BACKUP_MIRROR_DIR`. README ghi rõ: không đặt repo hoặc dữ liệu trên ổ mạng hay thư mục đồng bộ cloud (OneDrive/Dropbox/NFS/SMB); `make export` xuất file ra host.
- **SQLite bền**: `journal_mode=WAL`, `synchronous=FULL`, `foreign_keys=ON`, `busy_timeout=5000`; mỗi sự kiện một transaction (ghi `events` và cập nhật điểm/thẻ cùng lúc); khi khởi động bắt buộc `PRAGMA journal_mode=WAL` trả đúng `wal` và thư mục dữ liệu không nằm trên hệ tệp mạng (đọc `/proc/mounts`: nfs, cifs/smb, fuse, 9p, vboxsf), nếu không thì dừng và hiện lỗi rõ ràng, không tự chạy ở chế độ kém bền; rồi `quick_check`, hỏng thì hiện màn khôi phục.
- **Backup tự động** (v0.6, thay cron): SQLite online backup API lúc app khởi động (nếu bản mới nhất > 1 giờ), mỗi `backup_every_hours` (mặc định 6), trước migration/import/restore/reset và khi tắt êm; giữ 20 bản gần nhất + 1 bản đầu mỗi ngày trong 30 ngày tại `data/backups/`; `BACKUP_MIRROR_DIR` tuỳ chọn chép thêm sang thư mục đồng bộ cloud. Khôi phục một cú nhấp ở Settings. `GET /export`/`POST /import` để chuyển máy.
- **Client**: M1: IndexedDB giữ nháp code (độ bền `strict`, flush khi `pagehide`) và việc dở, `Idempotency-Key`, `resume_state`; vì server và trình duyệt chạy cùng máy, tắt máy là cả hai cùng tắt và không có chữ nào Quan đã gõ bị mất quá ~2 giây (nháp ở IndexedDB sau 300 ms, ở server sau 2 giây). **M3**: service worker (mở app khi server tắt), outbox replay đầy đủ có `outbox_dead`, `draft_versions` + 409. Chi tiết: `UI_SPEC.md` mục 4.
- **Tuỳ chọn khi muốn dùng ở nhiều thiết bị**: một VPS nhỏ hoặc Fly.io với volume cho SQLite (~5 USD/tháng), **không** mở ra internet công cộng; đặt sau Tailscale hoặc Cloudflare Access (không cần viết auth cho app). CI build ảnh Docker và đẩy lên registry riêng.
- Chưa cần CDN/queue/cache: bundle tĩnh nhỏ, ~200 file nội dung (40 lesson + 133 problem + 40 check yaml).

---

## 7. Lộ trình triển khai

Mỗi task được cắt vừa một phiên agent (khoảng nửa ngày làm việc). Ước lượng thời gian giả định agent chạy song song; Quan chỉ cần quyết định và đọc thử.

### M0, Khởi tạo repo (1-2 ngày)

| Task | Kết quả |
|---|---|
| T0.1 Tạo monorepo, `Makefile`, CI (lint, test, validate) | repo chạy `make ci` |
| T0.2 JSON Schema cho lesson/problem/check, `tools/sync_tree.py` | `content/index/*.json` có hash |
| T0.3 `tools/validate_content.py` (khung: schema + chạy solution qua sample) + `harness.py` | validate được 1 problem mẫu; bản đầy đủ ở T1.0 |
| T0.4 Sinh 40 lesson stub từ `skill_tree.json` | 40 file `status: draft` có tiêu đề + objectives |

Nghiệm thu: clone mới, `make ci` xanh; 40 stub qua schema; `ransom-note` (mục 3.6) qua toàn bộ kiểm tra của validator.

### M1, Lát cắt dọc (4-6 ngày)

| Task | Kết quả |
|---|---|
| T1.0 `validate_content.py` đầy đủ theo 4.4 (gen, brute-force cross-check, wrong/slow/TLE, giới hạn 0.3×/3×, `run_problem.py --engine pyodide`) | validator bắt được mọi lỗi trong 4.4 trên bộ fixture |
| T1.1 API khung: `content_loader`, `/map`, `/lessons`, `/problems`, `/attempts`, SQLite + Alembic | endpoint có test |
| T1.2 Pyodide runner (worker, watchdog, progress) + `Runner` interface | chạy sample/hidden của `ransom-note` |
| T1.3 Split view + CodeMirror + panel kết quả (Run/Submit/hints) | thao tác flow B trọn vẹn |
| T1.4 Lesson renderer cho 9 loại block | render lesson `py.datastructs.dict` (mục 3.5) |
| T1.5 Scoring service (mục 5.2) + unit test bảng ví dụ | điểm 0-3 đúng trên ca kiểm thử |
| T1.6 Author 3 mục hoàn chỉnh (sau T1.0): `py.datastructs.dict`, `py.datastructs.list`, `dsa.arrays_strings.arrays` qua pipeline đầy đủ | 3 lesson `published` + problem + test |
| T1.7 Lưu bền (v0.7): PRAGMA WAL + `synchronous=FULL` + kiểm `journal_mode`/ổ mạng lúc khởi động, named volume, `idempotency_keys` + middleware, nháp IndexedDB (flush `pagehide`, bản mới hơn theo `updated_at` thắng), `resume_state` + `GET/PUT /resume`, `GET /health`, backup tự động + `POST /backups/{name}/restore` (khởi động / 6 giờ / giữ 20 + 1 bản ngày) | tắt container giữa lúc gõ rồi mở lại không mất quá 3 giây code; gửi lại cùng một sự kiện 5 lần chỉ ghi 1; đặt `data/` trên ổ mạng thì app từ chối chạy; làm hỏng DB rồi khôi phục từ backup thành công |

Nghiệm thu: Quan học trọn mục `py.datastructs.dict` trong app (đọc, quiz, exercise, Submit `ransom-note` AC, hoàn thành, thấy điểm = 1); infinite loop bị cắt trong ≤ 4 giây mà trang không đơ; reload trang không mất nháp/tiến độ; tiêu chí T1.7 đạt. (Service worker offline, outbox replay đầy đủ, `draft_versions` + 409 hoãn sang T3.5.)

### M2a, Ngày 1-3 + vòng lặp ôn + mastery check + onboarding + placement tối thiểu (7-10 ngày)

| Task | Kết quả |
|---|---|
| T2.1a Author wave 1a: 16 mục ngày 1-3 (gồm `dict`, `list` đã làm ở T1.6) song song theo mục, qua validate + review; kèm 5 item `write_code` mức 2 bổ sung cho `getting_started`, `variables_types`, `tuple_namedtuple`, `copying_mutability`, `lambda_hof` thuộc ngày 1-3 | 16 lesson `published`, ~25 problem |
| T2.3 Unlock + Skill map (`/map`) | khoá/mở đúng theo mục 5.3, gồm `unlocked_at` một chiều (kiểm bằng unit test) |
| T2.4 Leitner + `/review` (không trần, preset tuỳ chọn, banner backlog) + `review_hint` từ plan | mô phỏng 30 ngày lịch khớp D+1/3/7/14/28; ôn trễ thì hạn kế tính từ ngày ôn thật; queue hiện đủ thẻ đến hạn, sắp đúng thứ tự |
| T2.5 Màn "Học tiếp" (`/`, `GET /next`) + `study_time` | mục kế tiếp hiện đúng thứ tự plan cho nhóm 1-3, kể cả khi học 5 mục trong một ngày hay nghỉ nhiều ngày; không có chỗ nào hiện "trễ" hay định mức |
| T2.2 `convert_checks.py` + mastery check (flow C, D), policy làm lại 24 giờ; v0.6: `check_sessions`, route `/check/:id`, `tested_out` ghi `unlocked_at` | 61 check problem + 51 item không code chuyển được; validator qua được `mastery_check` của lesson |
| T2.7 Onboarding + Tiếp tục (v0.6): S1 `/welcome` (nút Đánh giá bật khi T2.9a xong), `PUT /profile`, `GET /me.onboarding`, banner "Tiếp tục nơi bạn dừng" | lần đầu mở app đi hết hồ sơ và vào `/`; thoát giữa lesson, mở lại: banner đưa về đúng block; nháp bài còn nguyên |
| T2.8 Giao diện backup trong Settings (danh sách, sao lưu ngay, khôi phục; phần backup tự động đã ở T1.7) | làm hỏng DB rồi `Khôi phục` từ Settings thành công |
| T2.9a Placement tối thiểu (v0.7, cuối M2a, sau T2.2/T2.3/T2.5): `services/placement.py` Phase A (cổng C1-C7) + luật dừng (kể cả "Không biết"), gieo `tested_out`, `POST /placement`, `/skip`, `/answer`, `/heartbeat`, `/finish`, `GET /placement/{id}/result` rút gọn; S2; S3 rút gọn (mục đã đo, mục bắt đầu trong các lesson đã `published`, trạng thái "nội dung tiếp theo đang soạn") | hồ sơ yếu (`experience=none`) xong trong ≤ 9 phút; hồ sơ mạnh ≤ 45 phút; `score == scoring(events)` và không mục nào do placement đạt 3; kill tab giữa item rồi mở lại tiếp đúng item (sai ≤ 15 giây); "bắt đầu từ đầu" không ghi điểm |

Nghiệm thu (app đã dùng được cho tuần học thật): Quan làm hết nhóm 1-3 của plan (16 mục) trong app theo nhịp bất kỳ (có ngày học nhiều, ngày học ít, ngày nghỉ) mà không bị thông báo trễ hay phạt; thẻ ôn D+1 xuất hiện đúng ngày lịch và hiện đủ, không bị cắt; mô phỏng 30 ngày đúng bảng Leitner. Điểm 2 đạt được bằng mastery check, Test out hoạt động (nên Quan không bị kẹt ở ngày 4-7 khi `lib_toolkit`, `arrays` đòi prerequisite ≥ 2).

### M2b, Hết tuần 1 + đánh giá đầy đủ (5-7 ngày)

| Task | Kết quả |
|---|---|
| T2.1b Author wave 1b: 12 mục ngày 4-7 (`arrays` đã xong ở T1.6), kèm 3 item `write_code` mức 2 bổ sung cho `big_o`, `memory_model`, `scope_closures` (9 mục bổ sung: xem 3.4; `interview_method` ở ngày 10 nên thuộc M3) | 28/28 lesson tuần 1 `published`, ~44 problem |
| T2.6 `/problems`, `/progress`, nút Báo lỗi, export/import | |
| T2.9b Placement đầy đủ (v0.7): Phase B (biên tiền đề) và C (mức 3 `write_code`), nhãn suy luận `placement_hint`, nhóm "Có thể đã biết"/`sweep`, rải thẻ ôn, đo thêm, làm lại theo module, S3 đầy đủ (skill map, mạnh/yếu, giờ còn lại) | mô phỏng 3 hồ sơ xong trong ≤ 60 phút hoạt động; sau placement `score == scoring(events)`, không mục nào ≥ 3 do placement; nhãn suy luận không bao giờ đổi điểm |

Nghiệm thu: Quan làm hết nhóm 4-7; unlock chặn `hashing_patterns` tới khi `hash_tables ≥ 2`; Test out mở khoá đúng chuỗi prerequisite ngày 4-7; tiêu chí T2.9b đạt (placement hoàn chỉnh từ hồ sơ đến kết quả).

### M3, MVP dùng được (1 tuần)

| Task | Kết quả |
|---|---|
| T3.1 Author wave 2: 12 mục ngày 8-12, kèm item `write_code` mức 2 cho `interview_method` | 40/40 lesson `published`; đủ 9 check problem bổ sung |
| T3.2 Đóng gói: docker compose (`restart: unless-stopped`, healthcheck, named volume `app_data`, bind 127.0.0.1), `BACKUP_MIRROR_DIR`, hướng dẫn `README` (bật Docker khởi động cùng máy; **cảnh báo không đặt repo/`data/` trên ổ mạng hoặc thư mục đồng bộ cloud**) | chạy bằng 1 lệnh; khởi động lại máy thì app tự dậy |
| T3.5 Offline đầy đủ (v0.7, hoãn từ M1): service worker (app shell, Pyodide, lesson đã xem), outbox replay có `outbox_dead`, `draft_versions` + `rev` + 409 | tắt server giữa phiên: đọc, gõ, Run, quiz vẫn chạy, bật lại thì outbox tự xả, điểm đúng |
| T3.3 Đánh bóng: bàn phím tắt đầy đủ (`UI_SPEC.md` 3.4), dark mode, responsive 3 mức (≥ 1280 split / 768-1279 hai tab / < 768 chỉ đọc + ôn), trạng thái lỗi/loading/offline, axe-core, smoke test dấu tiếng Việt | |
| T3.4 Kiểm thử mạch cuối bằng một tài khoản giả lập đi hết nhóm 1-12 với nhịp thay đổi (ngày nhiều, ngày ít, ngày nghỉ, backlog lớn) + review toàn bộ nội dung bằng reviewer agent + kịch bản tắt máy ngẫu nhiên (20 lần giữa phiên học, kể cả giữa placement) | báo cáo QA; không mất sự kiện đã hiển thị "Đã lưu" |

Nghiệm thu (Definition of Done của MVP): 40 lesson, 63 practice + 70 check problem (61 chuyển từ assessment + 9 bổ sung), tất cả `published` và qua validator; Quan đi trọn nhóm 1-12 trong app; điểm, unlock, review đúng quy tắc mục 5 (có test tự động); không còn lỗi chặn; backup/restore thử thành công.

### Sau MVP

| Mốc | Nội dung |
|---|---|
| **M4** Hoàn thiện tuần 2 + mock | 6 mục ngày 13-14 + 4 mục `bh.*` (lesson dạng text/quiz, không code); quiz tuần từ `weekly_quizzes`; `tools/import_mock.py` biến `content_ng/*.json` (`rounds[].questions[]`: `prompt_en`, `examples`, `constraints`, `hints_vi`, `followups`, `solution.code`, `rubric_vi`, `subtopics`) thành problem `kind: mock` (test sinh từ `solution.code`); màn "Mock": mở theo tiến độ (mục 5.5), 2 bài, đồng hồ cứng 45 phút, tắt hint, tự chấm theo `rubric_vi`, kết quả ghi `mock_sessions` và đóng góp bằng chứng cho điểm. |
| **M5** Java | `Runner` server: Judge0 CE tự host trong compose (hoặc VPS); `starter.java`, `java_variant` của plan làm cây ánh xạ `py.* → java.*`; lesson Java viết theo `lang_prereqs`; editor chọn ngôn ngữ; tests dùng chung (JSON args) với harness Java. |
| **M6** Toàn bộ 530 mục | Author theo section (thứ tự 01 py, 04 dsa, 03 cs, 02 java, ...); section `ml` dùng Pyodide + numpy/pandas cho bài code, phần torch/LLM là quiz hoặc runner server; dùng `bank_topics` kéo câu thật; chuyển `question_gaps.md` thành backlog soạn câu cho ngôn ngữ. |
| **M7** Nhiều người dùng | Thêm auth (OIDC/OAuth) vào `current_user()`; SQLite → Postgres; chuyển hoàn toàn sang runner server (không gửi hidden test/lời giải cho client); rate limit; viết lại mọi đề `rewrite_required`, kiểm tra giấy phép; quyền truy cập nội dung theo gói (nếu có). |

---

## 8. Rủi ro & câu hỏi mở

### 8.1 Rủi ro chính

| Rủi ro | Giảm thiểu |
|---|---|
| Làm app tốn thời gian học thật (Quan học theo nhịp tự do, ngày nhiều ngày ít) | Học theo `plan.md` song song; M1 giới hạn 1 tuần; app chỉ cần đủ cho ngày 1-3 (M2a) trước khi mở rộng |
| LLM viết test/đáp án sai | Expected luôn do reference tính + brute-force độc lập + wrong/slow solution (mục 4.4) |
| Pyodide chậm hoặc không ép bộ nhớ | Hệ số thời gian ×3 kèm điều kiện validator `solution.py` ≤ 0.3 × `time_ms`; chấp nhận cho 1 người; runner server ở M5 |
| Khối lượng nội dung (133 problem, ~1.200 test, 40 lesson) | Pipeline song song theo mục; ưu tiên tuần 1; chuyển check từ assessment bằng script |
| Đề bám LeetCode | Chỉ dùng cá nhân; cờ `rewrite_required` chặn build công khai |
| Điểm 3 đòi hỏi 7 ngày nên cảm giác lâu mới lên | Giải thích trên UI (mục 5.2); `target_intern` đa số là 2-3 |
| Học tự do nhịp có thể để backlog ôn tồn lớn hoặc nghỉ dài rồi quên | Cảnh báo backlog mềm (mục 5.4 quy tắc 7), preset "Phiên ngắn" cho lúc ít thời gian; thẻ trễ không bị phạt, chỉ trượt khi trả lời sai; heatmap/giờ theo tuần trung tính, không streak |
| Không có lịch cứng nên dễ trôi, khó biết đang ở đâu | `/progress` chỉ hiện "đã xong X / 40 mục", mục kế tiếp và tổng giờ theo tuần; không so với ngày kế hoạch |

### 8.2 Câu hỏi mở cho Quan (chỉ những điểm cần quyết định)

1. **Phạm vi MVP**: giữ 40 mục (ngày 1-12) hay đẩy lên 46 mục để hết tuần 2 (thêm ngày 13-14: heap, binary search variants, sliding window, backtracking)? Mặc định đã chọn: 40, phần còn lại ở M4.
2. **Chạy ở đâu**: chỉ trên máy cá nhân (mặc định), hay cần dùng từ điện thoại/máy khác (cần VPS + Tailscale)?
3. **Chấp nhận giới hạn Pyodide** (không ép bộ nhớ, hidden test có thể bị xem trong DevTools) cho giai đoạn một người dùng? Mặc định: chấp nhận.
4. **Tên và chế độ repo GitHub** (đề xuất `prep-app`, private) và bạn có muốn đưa nội dung `interview-prep/` vào cùng repo hay giữ nguồn tách riêng và đồng bộ bằng `sync_tree.py` (mặc định)?
5. **Thời điểm làm Java**: sau MVP luôn (M5) hay chỉ khi đã qua tuần 2 của plan thật? Plan hiện đã có `java_variant`.

Ghi chú v0.4: quyết định nhịp học tự do (8.3) không đổi các câu hỏi trên. Câu 1 vẫn dùng "ngày 1-12" như tên nhóm thứ tự của plan, không phải lịch.

Ghi chú v0.2: review không trả lời trực tiếp câu nào trong 5 câu trên; câu 3 chỉ được làm rõ thêm là Pyodide nay **tự host** (mục 6.2), nên rủi ro "không ép được bộ nhớ" vẫn còn nhưng không còn phụ thuộc CDN.

### 8.3 Quyết định đã chốt ở v0.2 (không còn mở)

- Mở khoá một chiều (`unlocked_at`); bỏ decay điểm ở MVP; `tested_out` = check mức 2 clean; `s2 = tested_out OR (s1 AND practice_ok AND check2_ok)`.
- Làm lại mastery check sau 24 giờ, không giới hạn, không hiện `reference` khi trượt; thêm `attempt_no`.
- Leitner: `due = ngày ôn + gap(box_mới)`, gap {1:1, 2:2, 3:4, 4:7, 5:14}, rồi 30; `retention_ok` dùng `box_before >= 3` (v0.7: và `item_kind = code`; mục concept: `recall` cũng tính).
- Pyodide tự host, pin phiên bản, CSP `script-src 'self' 'wasm-unsafe-eval'; worker-src 'self'`; `solution.py` ≤ 0.3 × `time_ms` native.
- v0.3: T2.2 (mastery check, Test out) chuyển vào M2a, T2.6 ở M2b; fallback `check2_ok` dùng `min(2, số practice)`.
- v0.4 (Quan, 2026-10-24): học tự do nhịp độ, không cố định số lượng mỗi ngày. Plan chỉ là thứ tự gợi ý; màn "Học tiếp" thay "Hôm nay"; bỏ `plan_start_date`, `plan_day_pointer`, `review_cap`, `budget_h`, "Sang ngày kế", thông báo trễ lịch và streak (thay bằng tổng giờ theo tuần + heatmap `study_time`); review queue không có trần (preset "Phiên ngắn" tuỳ chọn, cảnh báo backlog mềm); Leitner vẫn theo ngày lịch; bài ôn ghim thành `review_hint` gắn subtopic; mock mở theo tiến độ.
- v0.5 (re-check v0.4): `GET /next` có nhóm `must_raise` cho prerequisite cần lên điểm 2 (không đổi `done`); mục target 0 không chặn mock; `review_hints` là danh sách; quy tắc cộng `study_time` của ping; mục chờ làm lại check xếp sau mục làm ngay.
- v0.6 (Quan, 2026-10-24: hoàn chỉnh quy trình từ đánh giá đầu vào, UI chi tiết, lưu và tiếp tục sau khi tắt máy; xem `UI_SPEC.md`): placement ở **M2b** (cần engine M2a + 28 lesson tuần 1); chỉ dùng item mức 2 `write_code`, chỉ gieo điểm 2 (không bao giờ 1 hoặc 3), nhãn suy luận chỉ để hiển thị; thẻ ôn do placement rải 8 thẻ/ngày; split view từ 1280 px (thiết kế quanh 1366), dưới 768 px chỉ đọc + ôn; nháp code debounce 2 giây + bản sao IndexedDB + `rev`; `synchronous=FULL`, `restart: unless-stopped`, backup tự động mỗi 6 giờ (giữ 20 + 1 bản/ngày trong 30 ngày), outbox + `Idempotency-Key`; `tested_out` ghi `unlocked_at` cho chính mục; hồ sơ New-grad/AI chỉ đổi vòng đích hiển thị.
- v0.7 (review v0.6): "Không biết" tính để dừng sớm, `experience=none` chỉ chạy C1-C2 (khuyên "Bắt đầu từ đầu"), trượt/không biết ở cổng thấp nhất thì bỏ Phase B; `retention_ok` chỉ nhận ôn bằng bài code (`review_log.item_kind`), `level3_ok` chỉ nhận `write_code`; DB trong named volume + kiểm `journal_mode`/ổ mạng lúc khởi động; placement tách T2.9a (cuối M2a) và T2.9b (M2b); M1 giữ PRAGMA/IndexedDB/idempotency/resume/backup, hoãn service worker, outbox đầy đủ, `draft_versions` + 409 sang M3 (T3.5).
- 9 mục thiếu `write_code` mức 2 được soạn thêm (mục 3.4); M2 tách thành M2a/M2b; thêm T1.0.
