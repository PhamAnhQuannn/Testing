# OVERVIEW: Mô tả tổng hợp yêu cầu, quyết định, spec và hiện trạng của Prep App

Cập nhật: 2026-10-25 (bản trong repo, thêm PR #3) · Chủ sở hữu: Quan · Ngôn ngữ: tiếng Việt (thuật ngữ kỹ thuật giữ tiếng Anh)

> **Bản sao trong repo.** Tài liệu này gốc nằm ở project folder của team (ngoài repo). Mọi chỗ nhắc `project folder`, `mem:*` hay `review.md` là tài liệu ngoài repo; Claude Code trên VS Code không có chúng, nên các quyết định cần thiết đã được tóm ở đây, trong `CLAUDE.md` và `docs/NEXT_M2A.md`. Việc tiếp theo: `docs/NEXT_M2A.md`.

Tài liệu này gom lại những gì Quan đã yêu cầu và những gì đang xây, để đọc một lần là nắm được. **Không chép lại chi tiết**; mỗi mục có con trỏ tới file gốc. Nguồn viết tắt dùng trong cả tài liệu:

| Viết tắt | Nguồn |
|---|---|
| `mem:<tên>` | Project memory của team, nằm ngoài repo (không có cho Claude Code ở VS Code; nội dung cần thiết đã được tóm vào tài liệu này và `CLAUDE.md`) (`learning-app`, `interview-prep-model`, `interview-research-scope`, `interview-research-outputs`, `agent-roles`) |
| `SPEC §x` | `docs/SPEC.md` v0.7 |
| `UI §x` | `docs/UI_SPEC.md` v0.2 |
| `REV` | `review.md` trong project folder (không có trong repo; lịch sử review và changelog v0.1 đến v0.7) |
| `repo` | Code đã build: repo này (GitHub `PhamAnhQuannn/Testing`), `README.md`, `docs/API_M1.md`, `git log` |
| `plan` | `source/plan.md`, `source/plan.json`, `source/assessment.json` trong repo (bản gốc: `interview-prep/plans/meta_1month/` ở project folder, không có trong repo; `review.md` của plan chỉ có ở project folder) |

Quy ước: số nào không có nguồn đi kèm là số tôi đếm lại trực tiếp lúc viết (ghi rõ "đếm lại"). Chỗ nào là suy ra từ spec chứ không phải số có sẵn thì ghi "suy ra".

---

## 0. Tóm tắt 1 trang

**Mục tiêu.** Một ứng dụng học và luyện phỏng vấn kiểu Coddy/HackerRank/GeeksforGeeks cho riêng Quan: bài học ngắn (lesson) và bài code nằm cạnh nhau (split view), chạy và chấm code ngay trong trình duyệt, điểm 0-3 cho từng mục nhỏ (subtopic), mở khoá mục sau theo mục cần học trước (prerequisite), ôn lặp ngắt quãng. Nội dung lấy từ cây kiến thức 530 mục, kế hoạch Meta 30 ngày và ngân hàng đánh giá đã làm sẵn. Quan học theo nhịp tự do, không có định mức mỗi ngày. (`mem:learning-app`, `SPEC §1`)

**Phạm vi hiện tại.** Một người dùng (Quan). MVP = 40 subtopic (Python + DSA nền tảng, kế hoạch Meta ngày 1-12). Thiết kế sẵn cho nhiều người dùng sau này (mọi bảng tiến độ có `user_id`) nhưng chưa làm auth, hosting công khai, giấy phép. (`mem:learning-app`, `SPEC §1.2`)

**Đang ở đâu (2026-10-25).**

| Hạng mục | Tình trạng |
|---|---|
| Spec | SPEC v0.7 + UI_SPEC v0.2, đã qua nhiều vòng review (`REV`) |
| M0 (khung repo, schema, validator) | Xong, merge PR #1 |
| M1 (lát cắt dọc: học trọn 1 mục trong app) | Xong, merge PR #2 (2026-10-24) |
| Dữ liệu nguồn | Xong, merge PR #3: thư mục `source/` (skill_tree, plan, assessment) đã nằm trong repo |
| Bàn giao | 2026-10-25: Quan tiếp tục M2a cục bộ bằng VS Code + Claude Code (nhánh `vscode-handoff` thêm `CLAUDE.md`, `docs/NEXT_M2A.md`, `.vscode/`) |
| Nội dung | 3/40 lesson và 5/63 problem đã `published`; 37 lesson còn là stub nháp |
| Kiểm thử | 203 test pytest + 42 test vitest đều qua (đếm lại bằng cách chạy 2026-10-25); e2e thật `make e2e` ở job CI riêng |
| Chưa có trong app | Onboarding, placement, mastery check, Test out, Leitner/review, "Học tiếp", skill map đầy đủ S5 (T2.3) và việc tắt editor/Submit khi mục bị khoá, progress, mock |

**Việc tiếp theo: M2a** (SPEC §7): soạn lesson cho ngày 1-3 (16 mục, 2 mục đã xong), mastery check + Test out, unlock + skill map, Leitner + `/review`, màn "Học tiếp", onboarding, backup UI và placement tối thiểu. Dự kiến 7-10 ngày (SPEC §7). Sau đó M2b, M3 (MVP dùng được), rồi M4-M7.

**Cách làm việc.** Sonnet agent làm toàn bộ việc, Fable chỉ kiểm tra/review, Claude tự merge từng PR khi CI xanh (squash qua REST, vì tính năng auto-merge của GitHub đang tắt trên repo; cụm "auto-merge on" trong MEMORY chỉ quy trình này). Trả lời Quan bằng tiếng Việt. (`mem:agent-roles`) **Khi làm cục bộ trong VS Code + Claude Code:** dùng subagent (Sonnet) để làm, một lượt review độc lập bằng model mạnh hơn trước khi merge, và chỉ merge khi Quan yêu cầu (xem `CLAUDE.md`).

---

## 1. Bối cảnh và mục tiêu tổng

### 1.1 Bức tranh lớn: từ dataset đến app

```
interview-research/      dataset quy trình phỏng vấn (10.888 câu, 571 process / 174 công ty)
        │
interview-prep/          mô hình 4 tầng
  tầng 1 cây kiến thức (530 mục)  ──►  tầng 2 đánh giá 0-3  ──►  tầng 3 bài học  ──►  tầng 4 mock + ôn
        │                                                                              
plans/meta_1month/       kế hoạch 30 ngày Meta intern/new-grad + bộ đánh giá (254 item)
interview-research/meta_2026/mock/   bộ mock Word (10 mock intern + new grad)
        │
learning-app/ + repo Testing   ◄── ứng dụng học: biến các file tĩnh trên thành vòng lặp học tương tác
```

### 1.2 Dataset quy trình phỏng vấn (`mem:interview-research-scope`, `mem:interview-research-outputs`)

- **Mục tiêu (Quan, 2026-10-10)**: dataset quy trình phỏng vấn của các công ty tech ở 4 nhóm (big tech, large, mid-size gồm công ty Việt Nam, startup), các cấp intern / fresher / junior / senior, gồm các vòng và ngân hàng câu hỏi.
- **Vai trò và ngôn ngữ**: software engineer và AI engineer; Python và Java.
- **Phương pháp**: Sonnet subagent nghiên cứu nhiều góc, rồi debate + QA, Opus/Fable tổng hợp cuối. Mọi câu hỏi phải có URL nguồn (không chấp nhận câu bịa hay không nguồn).
- **Quy mô sau crawl v2 (2026-10-13)**: 10.888 câu hỏi (5.357 có đủ nội dung, 5.531 chỉ có tiêu đề từ PracHub), 9.148 câu gắn năm 2025-26, 571 process / 174 công ty (khoảng 520 công ty xuất hiện tổng cộng). Vị trí: `interview-research/` (project folder, không có trong repo) (`interview_processes.xlsx`, `question_bank.md`, ...).
- **Kiểm tra Meta 2026 (2026-10-24)**: `meta_2026/` gồm kiểm chứng 20 claim từ một bài viết Quan dán vào và danh sách câu dự đoán theo vòng. Kết luận chính: vòng AI-enabled coding thay một trong hai vòng onsite coding; AI chỉ chat, không chèn code vào editor.

### 1.3 Mô hình chuẩn bị 4 tầng (`mem:interview-prep-model`, `interview-prep/README.md` (project folder, không có trong repo))

| Tầng | Nội dung | Trạng thái |
|---|---|---|
| 1. Cây kiến thức | 9 section, 88 module, **530 mục (subtopic)** sau vòng sửa 3; QA v1.0 xong 2026-10-20 | Đã làm |
| 2. Đánh giá | Chấm 0-3 từng mục, câu thích nghi | Chưa làm đầy đủ trên toàn cây (cần tự soạn ~900 item, chủ yếu ngôn ngữ Python/Java, theo `analysis/question_gaps.md`); bản cho Meta đã có: 254 item |
| 3. Bài học | Mỗi mục một bài: cốt lõi, ví dụ, bài luyện, kiểm tra lại | Chưa làm; **app học chính là nơi viết tầng 3** (40 mục đầu) |
| 4. Mock + ôn | Mock theo công ty, ôn lặp ngắt quãng | Bộ mock Word đã có; ôn lặp sẽ nằm trong app (Leitner) |

- Thang điểm dùng mọi nơi: **0** chưa biết/không cần, **1** biết lý thuyết, **2** làm được bài cơ bản, **3** mức phỏng vấn.
- Id mục `<section>.<module>.<mục>` (ví dụ `dsa.linked_list.basics`) là khoá chung của mọi tầng và của app.
- Cây kiến thức được kiểm bằng người học giả lập (Fable đóng vai sinh viên "An"): độ dễ hiểu 2,21/5 (vòng 1) lên 4,07/5 (vòng 2) lên 4,25/5 (vòng 3). Ngân sách tải: SWE-Python intern 109 mục / 288h, fresher 231 / 750h (`mem:interview-prep-model`).

### 1.4 Kế hoạch Meta 30 ngày và bộ mock (`plan`, `mem:interview-prep-model`, `mem:interview-research-outputs`)

- **Kế hoạch (2026-10-24)**: intern/new-grad Meta, SWE + Python. 30 ngày = 4 tuần + 2 ngày buffer, 4h ngày thường + 6h cuối tuần, tổng khoảng 131h (131,25h trên tối đa 136h, `plan/review.md`). Giữ **82 subtopic** ở mức điểm 2 (khoảng 91,5h nội dung; `plan/plan.md` mục 0 và 2.1). Review của kế hoạch: **DUYỆT**, còn 3 nit không chặn (`plan/review.md`).
- **Bộ đánh giá kèm theo**: 254 item (`assessment.json`; `mem:interview-prep-model`), Day 0 là bài chẩn đoán đầu vào, quiz cuối mỗi tuần, rubric chấm mock.
- **Mock**: file Word `meta_2026/mock/Meta_2026_Intern_NewGrad_Mock.docx`, **10 mock** (I1-I4 cho intern, N1-N6 cho new grad), 284 trang. Quan thu hẹp từ bản đầu 8 mock mọi cấp (251 trang) xuống chỉ intern + new grad. Chỉ các mock có trong lịch (I1-R1, I3, N1, N2, N6-R1 mức 1-2) được "để dành", phần còn lại thả vào kho bài luyện (`mem:interview-prep-model`).

### 1.5 App học (`mem:learning-app`)

Quan hỏi (2026-10-24) cần gì để làm một UI học đầy đủ, dễ dùng, trộn bài học kiến thức với luyện code, dựa trên cây kiến thức, ngân hàng câu hỏi, mock và kế hoạch/đánh giá 30 ngày. Quyết định phạm vi: một người dùng trước, nhiều người sau. Quan không muốn tự quản lý file hay IDE: Claude viết, test và push; VS Code chỉ là tuỳ chọn. Repo: `https://github.com/PhamAnhQuannn/Testing`.

---

## 2. Tất cả yêu cầu của Quan

Cột "Ngày" lấy từ memory hoặc từ changelog `REV`. Cột "Nguồn" cho biết yêu cầu được ghi ở đâu và đã đi vào spec chỗ nào. Tôi chỉ liệt kê những gì có trong nguồn, không suy diễn thêm yêu cầu.

### 2.1 Phạm vi và người dùng

| # | Yêu cầu | Ngày | Nguồn |
|---|---|---|---|
| R1 | Dataset quy trình phỏng vấn: startup, small/mid, large, big tech; intern, fresher, junior, senior; các vòng và ngân hàng câu hỏi | 2026-10-10 | `mem:MEMORY`, `mem:interview-research-scope` |
| R2 | Tập trung AI engineer và software engineer, Python và Java | 2026-10-10 (thu hẹp) | `mem:interview-research-scope` |
| R3 | Mô hình chuẩn bị 4 tầng (cây kiến thức, đánh giá 0-3, bài học từng mục, mock + ôn lặp) | 2026-10-13 | `mem:interview-prep-model` |
| R4 | Một người dùng (Quan) trước; thiết kế để mở cho nhiều người sau, nhưng chưa làm auth, hosting công khai, giấy phép | 2026-10-24 | `mem:learning-app`, `SPEC §1.2` |
| R5 | Quan không tự quản lý file hay IDE; Claude viết, test, push (VS Code tuỳ chọn) | 2026-10-24 | `mem:learning-app` |
| R6 | Đề bài được bám sát LeetCode cho mục đích cá nhân, nhưng phải viết lại trước khi công khai | 2026-10-24 | `mem:learning-app`, `SPEC §1.4` (cờ `rewrite_required`, validator chặn build `public`) |

### 2.2 Nội dung

| # | Yêu cầu | Ngày | Nguồn |
|---|---|---|---|
| R7 | Chữ phải dễ và ngắn cho người mới hoàn toàn; kiểm bằng learner sim | 2026-10-14 | `mem:interview-prep-model` |
| R8 | Giữ sửa tầng 1 (vòng 3) trước khi làm tầng 2 | 2026-10-19 | `mem:interview-prep-model` |
| R9 | Kế hoạch ôn Meta 30 ngày intern/new-grad + đánh giá kiểu tầng 2 | 2026-10-24 | `mem:interview-prep-model`, `plan` |
| R10 | Gói mock phỏng vấn Meta (Word), sau đó chỉ giữ intern + new grad | 2026-10-24 | `mem:interview-research-outputs` |
| R11 | Kiểm tra claim về quy trình Meta 2026 | 2026-10-24 | `mem:interview-research-outputs` |
| R12 | Đề bài song ngữ trong app (EN là bản chính, VI là bản giải thích, bật/tắt một nút); lesson viết tiếng Việt, thuật ngữ giữ tiếng Anh | quyết định spec, không phải lời Quan (2026-10-24) | `SPEC §1.3` |

### 2.3 Trải nghiệm học (Coddy-style)

| # | Yêu cầu | Ngày | Nguồn |
|---|---|---|---|
| R13 | UI kiểu Coddy/HackerRank/GeeksforGeeks, kết hợp bài học kiến thức với luyện code | 2026-10-24 | `mem:learning-app` |
| R14 | Split view: lesson bên trái, editor bên phải | 2026-10-24 | `mem:learning-app`, `SPEC §2`, `UI §3.5` (từ 1280 px, thiết kế quanh 1366) |
| R15 | Chạy code (Run) và nộp (Submit) có test; chấm tự động | 2026-10-24 | `mem:learning-app`, `SPEC §2.3` Flow B |
| R16 | Chấm điểm 0-3 cho từng mục | 2026-10-24 | `mem:learning-app`, `SPEC §5.2` |
| R17 | Mở khoá mục sau theo prerequisite | 2026-10-24 | `mem:learning-app`, `SPEC §5.3` |
| R18 | Ôn lặp ngắt quãng (spaced review) | 2026-10-24 | `mem:learning-app`, `SPEC §5.4` |

### 2.4 Nhịp học tự do

| # | Yêu cầu | Ngày | Nguồn |
|---|---|---|---|
| R19 | Không có số lượng cố định mỗi ngày; có ngày học nhiều, ngày ít, ngày nghỉ. Kế hoạch chỉ là thứ tự gợi ý | 2026-10-24 | `mem:learning-app`, `SPEC §1.1` nguyên tắc 7, `REV` changelog v0.4 |
| R20 | Không có trần thẻ ôn mỗi ngày, không báo "trễ lịch", không streak phạt. Phần duy nhất theo lịch là khoảng cách Leitner (D+1/3/7/14/28) vì mô hình sự quên | 2026-10-24 | `mem:learning-app`, `SPEC §5.4` |

### 2.5 Đánh giá trình độ đầu vào

| # | Yêu cầu | Ngày | Nguồn |
|---|---|---|---|
| R21 | Hoàn chỉnh quy trình từ điểm bắt đầu: đánh giá trình độ đầu vào (placement), gieo điểm cho mục đã biết | 2026-10-24 | `mem:learning-app`, `REV` changelog v0.6, `UI §2`, `SPEC §5.6` |
| R22 | Người mới hoàn toàn không bị "ép" làm bài khó: nhánh người mới chỉ khoảng 6-9 phút và khuyên "Bắt đầu từ đầu" | quyết định spec/review v0.6, không phải lời Quan (2026-10-24) | `mem:learning-app`, `UI §2.7` |

### 2.6 UI chi tiết

| # | Yêu cầu | Ngày | Nguồn |
|---|---|---|---|
| R23 | Mô tả chi tiết toàn bộ UI từng màn hình (layout, component, nguồn dữ liệu, mọi trạng thái, hành động ghi gì) | 2026-10-24 | `REV` changelog v0.6, `UI §3` (design system + 13 màn hình S1-S13) |

### 2.7 Lưu dữ liệu và tiếp tục sau khi tắt máy

| # | Yêu cầu | Ngày | Nguồn |
|---|---|---|---|
| R24 | Hệ thống ghi nhớ dữ liệu; tiếp tục làm việc kể cả khi thoát app hoặc tắt máy | 2026-10-24 | `REV` changelog v0.6, `UI §4`, `SPEC §6.7`, `SPEC §2.3` Flow H |

### 2.8 Quy trình làm việc

| # | Yêu cầu | Ngày | Nguồn |
|---|---|---|---|
| R25 | Từ giờ mọi việc do Sonnet agent làm; Fable chỉ kiểm tra/review; phiên Opus điều phối không tự sửa nội dung. Lời Quan: "từ giờ phần công việc là của sonet agents, và fable đóng vai trò kiểm tra" | 2026-10-20 | `mem:agent-roles`, `mem:MEMORY` |
| R26 | PR của repo app: Sonnet review, Fable kiểm, CI xanh thì tự merge ("auto merge"; "chuẩn là sonet review fable check and merge") | 2026-10-24 | `mem:agent-roles`, `mem:MEMORY` |
| R27 | Trả lời Quan bằng tiếng Việt (Quan viết tiếng Việt) | ghi trong memory outputs (file sửa 2026-10-13) | `mem:interview-research-outputs` |

---

## 3. Quyết định đã chốt và câu hỏi còn mở

### 3.1 Quyết định đã chốt (SPEC §8.3 + `REV`)

| Chủ đề | Quyết định | Từ phiên bản | Nguồn |
|---|---|---|---|
| Mở khoá | Một chiều: ghi `unlocked_at`, mở rồi không khoá lại | v0.2 | `SPEC §5.3, §8.3` |
| Điểm tự giảm (decay) | Không có ở MVP; điểm chỉ tăng theo sự kiện đo được. Thẻ ôn trượt chỉ về hộp 1 và `lapses += 1` | v0.2 | `SPEC §5.2` |
| `tested_out` | = đậu check mức 2 "sạch" (clean); công thức `s2 = tested_out OR (s1 AND practice_ok AND check2_ok)` | v0.2 | `SPEC §8.3` |
| Làm lại check | Sau 24 giờ, không giới hạn lần, mỗi lần một `attempt_no`; trượt không hiện `reference` | v0.2 | `SPEC §8.3` |
| Leitner | 5 hộp, gap {1:1, 2:2, 3:4, 4:7, 5:14} rồi 30 ngày, tính từ ngày ôn thật (nên trễ hạn không dồn nợ) | v0.2 | `SPEC §5.4` |
| `retention_ok` | Chỉ nhận lần ôn đạt ở hộp >= 3 **bằng bài code** (`item_kind = code`); `level3_ok` chỉ nhận item `write_code` | v0.7 | `SPEC §8.3`, `REV` P2 |
| Pyodide | Tự host, ghim phiên bản, CSP `script-src 'self' 'wasm-unsafe-eval'; worker-src 'self'`; `solution.py` <= 0,3 x `time_ms` native | v0.2 | `SPEC §8.3` |
| Stack | React + TS + Vite + CodeMirror 6; FastAPI + SQLite (WAL); Python chạy trong trình duyệt. Chọn phương án A (Next.js + Postgres và SPA thuần local-first bị loại) | v0.1 | `SPEC §6.1` |
| Chấm Python | Pyodide cho MVP (miễn phí, an toàn mặc định, chấm tức thì); Judge0 CE tự host cho Java (M5) và nhiều người dùng (M7), đặt sau interface `Runner` | v0.1 | `SPEC §6.2` |
| Nhịp học | Học tự do; màn "Học tiếp" thay "Hôm nay"; bỏ ngày bắt đầu plan, con trỏ ngày, trần thẻ, ngân sách giờ, thông báo trễ, streak | v0.4 (Quan) | `SPEC §8.3`, `REV` |
| Mock | Mở theo tiến độ (xong 28 mục tuần 1, trừ mục `target_intern = 0`), không theo ngày | v0.4-v0.5 | `SPEC §5.5` |
| Placement | Ở M2 (tối thiểu T2.9a cuối M2a, đầy đủ T2.9b ở M2b); chỉ item mức 2 `write_code`; chỉ gieo điểm 2 (không bao giờ 1 hoặc 3); suy luận đồ thị chỉ là nhãn `placement_hint` | v0.6-v0.7 | `SPEC §8.3`, `UI §2.9` |
| Màn hình | Split view từ 1280 px; 768-1279 hai tab; dưới 768 chỉ đọc lesson + ôn thẻ nhớ nhanh | v0.6 | `UI §3.5` |
| Lưu bền | `synchronous=FULL`, DB trong named volume `app_data`, `restart: unless-stopped`, backup tự động mỗi 6 giờ (giữ 20 + 1 bản/ngày trong 30 ngày), nháp debounce 2 giây + IndexedDB | v0.6-v0.7 | `SPEC §6.7`, `UI §4` |
| Phạm vi M1 vs M3 | M1 giữ PRAGMA, IndexedDB, `Idempotency-Key`, `resume_state`, backup; hoãn service worker, outbox đầy đủ, `draft_versions` + 409 sang M3 (T3.5) | v0.7 | `SPEC §8.3`, `REV` N1 |
| Mục thiếu `write_code` mức 2 | 9 mục được soạn thêm item (5 ở M2a, 3 ở M2b, `interview_method` ở M3) | v0.2 | `SPEC §3.4, §7` |

### 3.2 Câu hỏi còn mở (SPEC §8.2) và mặc định đang áp dụng

Spec ghi rõ các điểm này đã có mặc định; trong nguồn tôi đọc **không thấy Quan trả lời trực tiếp**, nên coi là "mặc định đang áp dụng, chờ Quan xác nhận".

| # | Câu hỏi | Mặc định đang áp dụng | Tình trạng |
|---|---|---|---|
| 1 | Phạm vi MVP: 40 mục (ngày 1-12) hay 46 mục (thêm ngày 13-14: heap, binary search variants, sliding window, backtracking)? | **40 mục**; phần còn lại ở M4 | Đã áp dụng mặc định: repo build đúng 40 stub |
| 2 | Chạy ở đâu: chỉ máy cá nhân, hay cần điện thoại/máy khác (VPS + Tailscale)? | **Chỉ máy cá nhân** (`docker compose up`, bind `127.0.0.1`) | Đã áp dụng mặc định |
| 3 | Chấp nhận giới hạn Pyodide (không ép bộ nhớ, hidden test có thể xem trong DevTools) cho một người dùng? | **Chấp nhận** | Đã áp dụng mặc định (M1 chạy Pyodide 0.29.5, `mem:learning-app`) |
| 4 | Tên/chế độ repo; đưa nội dung `interview-prep/` vào repo hay tách riêng? | Spec đề xuất `prep-app` private và **tách riêng**, đồng bộ bằng `sync_tree.py` | Quan đã cho repo `PhamAnhQuannn/Testing` (tên khác đề xuất; độ riêng tư không thấy trong nguồn). Repo đang dùng snapshot `content/index/` + `sync_tree.py`, tức là theo hướng "tách riêng" |
| 5 | Thời điểm làm Java: sau MVP luôn (M5) hay sau tuần 2 của plan thật? | **Sau MVP (M5)** | Đã áp dụng mặc định; kế hoạch hiện chỉ có `java_variant` ghi chú |

Rủi ro liên quan tới các câu hỏi này nằm ở mục 8.

---

## 4. Spec sản phẩm tóm tắt

Từ cần biết: **AC** = Accepted (qua hết hidden test); **clean** = AC mà không xem lời giải, dùng <= 1 gợi ý, không quá 1,5 lần thời gian mục tiêu; **hộp Leitner** = mức ôn 1-5, lên hộp khi ôn đạt, trượt về hộp 1, hộp càng cao khoảng cách ôn càng dài.

Chi tiết đầy đủ: `SPEC §1-5` và `UI_SPEC §1-3`. Dưới đây là phần cần nhớ.

### 4.1 Luồng người dùng từ lần đầu mở app (`SPEC §2.3` Flow G-H, `UI §1`)

```
Lần đầu mở ──► /welcome: kiểm tra Pyodide, hồ sơ 4 câu
               (target_role intern/new_grad · track swe/ai · language python · experience none/some/solid)
          ──► chọn: [Đánh giá trình độ] (placement) hoặc [Bắt đầu từ đầu] (không gieo điểm)
          ──► (placement) kết quả: skill map đã gieo, mạnh/yếu, mục bắt đầu, giờ còn lại
          ──► "/" Học tiếp ──► học lesson ──► làm bài ──► kiểm tra ──► ôn lặp ──┐
                                   ▲                                              │
                                   └──────────────────────────────────────────────┘
Thoát/tắt máy bất kỳ lúc nào ──► mở lại: GET /resume ──► banner "Tiếp tục nơi bạn dừng"
```

Các flow chính (`SPEC §2.3`): A học một mục; B làm một problem (Run, 3 nấc gợi ý, Submit hidden test, verdict AC/WA/TLE/RE/CE); C mastery check (thang bậc mức 2 rồi 3, sai thì mức 1 để chẩn đoán); D Test out (đậu mức 2 sạch thì điểm 2, tối đa 2); E ôn tập; F "Học tiếp" theo thứ tự plan; G lần đầu và placement; H tiếp tục sau khi thoát.

### 4.2 Các màn hình (`SPEC §2.1`, `UI §3.8` S1-S13)

| Route | Màn hình | UI_SPEC |
|---|---|---|
| `/welcome` | Chào mừng, hồ sơ, chọn cách bắt đầu | S1 |
| `/placement/:id`, `/placement/:id/result` | Đánh giá đầu vào và kết quả | S2, S3 |
| `/` | Học tiếp (Next up), thẻ đến hạn, banner tiếp tục | S4, S12 |
| `/map` | Skill map (40 mục, khoá/mở, điểm) | S5 |
| `/s/:subtopicId` | Lesson (trái) + editor (phải) | S6 |
| `/p/:problemId` | Đề (trái) + editor (phải) | S7 |
| `/check/:subtopicId` | Mastery check / Test out (chế độ tập trung) | S8 |
| `/review` | Phiên ôn tập | S9 |
| `/progress` | Điểm theo mục, giờ theo tuần, heatmap | S10 |
| `/settings` | Hồ sơ, múi giờ, giao diện, backup/khôi phục, export/import, reset | S11 |
| `/problems` | Danh sách bài, lọc | S13 |

Design system (`UI §3.1`): nền sáng/tối theo `prefers-color-scheme`, tương phản >= 4,5:1, font Inter + JetBrains Mono có tiếng Việt, mỗi mức điểm 0-3 có một cặp màu riêng và luôn kèm số/chữ (màu không là kênh duy nhất). Phím tắt: `UI §3.4`.

### 4.3 Mô hình nội dung (`SPEC §3`)

- Nội dung là **file trong git**: `content/lessons/<sec>/<id>.yaml`, `content/problems/<subtopic>/<slug>/{problem.yaml, solution.py, brute.py, wrong/, slow/, tests/}`, `content/checks/<id>.yaml`, kèm JSON Schema và validator. YAML cho lesson/problem, JSONL cho test.
- **Lesson**: 8-15 phút đọc, khoảng 8-11 block (text, code_sample, quiz, code_exercise...), mỗi lesson có ít nhất 3 block `graded` (validator bắt buộc). Ví dụ đầy đủ: `SPEC §3.5` (`py.datastructs.dict`).
- **Problem**: đề song ngữ, starter, 3 sample + khoảng 9 hidden test, 3 nấc gợi ý, `time_target_min`, nguồn (`source.lc`, `rewrite_required`). Ví dụ: `ransom-note` (`SPEC §3.6`).
- **Check item**: lấy từ `assessment.json`, 3 loại `write_code` (chấm bằng engine problem), `read_code` (predict output, tự động), `concept` (tự chấm, ngoại lệ duy nhất cho nguyên tắc "không có nút tự chấm"; mức 2 luôn có `write_code`).
- **Validator** (`SPEC §4.4`): chạy reference, brute-force độc lập, wrong/slow solution; test ẩn phải làm hỏng mọi lời giải sai.

### 4.4 Quy tắc điểm 0-3, mở khoá, Leitner (`SPEC §5`)

| Điểm | Điều kiện (rút gọn) |
|---|---|
| 0 | Chưa học |
| 1 | Hoàn thành lesson và `quiz_best >= 0,7`; hoặc đã `tested_out` |
| 2 | `tested_out` (đậu check mức 2 sạch), hoặc (điểm 1 + đủ practice AC + `check2_ok`). Đây là mức mở khoá mục sau |
| 3 | Điểm 2 + `level3_ok` (đậu mức 3 `write_code` sạch) + `retention_ok` (ôn bằng bài code đạt ở hộp >= 3); nên **không thể đạt trong ngày đầu**, sớm nhất khoảng D+7 |

- "Sạch" (clean) = AC mà không xem lời giải, dùng <= 1 gợi ý, và không quá 1,5 lần thời gian mục tiêu (`SPEC §5.1`).
- Điểm tính lại từ bảng sự kiện (`attempts`, `quiz_answers`, `check_results`, `review_log`); cột `score` chỉ là cache. Điểm không bao giờ giảm.
- **Mở khoá**: `unlocked(n)` khi mọi prerequisite có điểm >= 2 (hoặc nằm trong `assumed`, hiện chỉ `cs.onramp.computer_programming_model`), hoặc Quan Test out. Mục khoá vẫn đọc xem trước được (editor và Submit tắt). `done` = điểm >= max(1, `target_intern`). Mục có `target_intern = 0` hiển thị "tuỳ chọn".
- **Leitner 5 hộp**: tạo thẻ khi mục đạt điểm >= 1 lần đầu; đạt thì lên hộp, trượt về hộp 1; lịch lý tưởng D+1, D+3, D+7, D+14, D+28, rồi mỗi 30 ngày. Hộp 1-2 dùng câu nhớ nhanh, hộp 3-5 dùng bài code. **Không có trần thẻ**; preset "Phiên ngắn" (mặc định cỡ 6) và banner backlog mềm (> 20 thẻ) chỉ là gợi ý.
- **Placement** (`SPEC §5.6`, `UI §2`): mastery check xếp theo đồ thị prerequisite, 3 phase (cổng C1-C7 mỗi cổng 6 phút; biên prerequisite; mức 3 tuỳ chọn), ngân sách một lần ngồi 45 phút mềm / 60 phút cứng thời gian hoạt động, chỉ ghi `check_results` nên điểm luôn tính lại bằng cùng `scoring.py`. Mô phỏng thời gian (cận trên, `UI §2.7`): hồ sơ yếu ~6-9 phút, trung bình 40-47 phút, mạnh 42-44 phút. Ở thời điểm spec, 31/40 mục "placeable" (có item mức 2 `write_code`).

### 4.5 Nhịp học và "Học tiếp" (`SPEC §5.5`)

`GET /next` trả hai nhóm: (1) "Cần lên điểm 2 để mở mục sau" (prerequisite đang chặn, kèm bài gợi ý và nút Test out), (2) danh sách mục đã mở nhưng chưa `done` theo thứ tự plan `(N, vị trí)`. Không có ngày hiện tại, không so sánh với lịch. Thẻ ôn sinh từ sự kiện thật nên học nhanh, chậm hay nghỉ dài đều không làm hỏng hàng đợi.

---

## 5. Kiến trúc kỹ thuật tóm tắt

Chi tiết: `SPEC §6`, `UI §4`, `docs/API_M1.md`.

### 5.1 Stack

| Lớp | Lựa chọn |
|---|---|
| Frontend | React 18 + TypeScript + Vite; CodeMirror 6; `react-markdown` + `remark-gfm` + `shiki`; `react-resizable-panels`; TanStack Query; Zustand |
| Backend | Python 3.12 + FastAPI + SQLAlchemy/SQLModel + Alembic; SQLite (WAL) |
| Chạy code | Pyodide trong Web Worker, tự host (bản 0.29.5 ở M1, `mem:learning-app`), có watchdog giết worker khi quá giờ |
| Đóng gói | Một container (uvicorn phục vụ API và bản build web), `docker compose up` hoặc `make dev` |
| Tooling nội dung | Python, chạy bằng `uv run` (`tools/`) |

### 5.2 Runner Pyodide (`SPEC §6.2`)

- Đặt sau interface `Runner` (language, `run({code, io, tests, limits})`), nên M5 thêm runner server (Judge0 CE) cho Java mà không đổi UI/API.
- Giới hạn chấp nhận được cho một người: không ép được bộ nhớ (chỉ cảnh báo); kết quả do client báo; hidden test có thể bị xem trong DevTools. Hidden test chỉ được tải về khi Submit (token 15 phút).
- Một file `harness.py` dùng chung cho worker trong trình duyệt và `tools/run_problem.py` để "pass ở validator" và "pass trong app" luôn cùng nghĩa.

### 5.3 Data model (`SPEC §6.3`)

- **Bảng nội dung** (nạp từ file lúc khởi động, upsert theo `content_hash`): `subtopics`, `lessons`, `problems`, `quiz_items`, `plan_order`, `plan_milestones`.
- **Bảng người dùng** (đều có `user_id`): `users`, `settings`, `study_time`, `user_subtopic` (score cache, `unlocked_at`, `known_basic`, `placement_hint`), `quiz_answers`, `attempts`, `check_results`, `check_sessions`, `placement_sessions`, `review_cards`, `review_log`, `drafts`, `draft_versions`, `feedback`, `events` (append-only), `resume_state`, `idempotency_keys`.
- Nguyên tắc: điểm luôn tính lại từ sự kiện; logic điểm/unlock/Leitner là hàm thuần trong `services/` có unit test theo bảng ví dụ của `SPEC §5`.

### 5.4 API (`SPEC §6.4`)

Prefix `/api`, JSON; MVP dùng user cố định `id = 1` qua `current_user()` (M7 chỉ đổi hàm này sang đọc token). Nhóm endpoint: hồ sơ/placement (`/me`, `/profile`, `/placement/*`), học (`/map`, `/subtopics`, `/lessons`, `/quiz/answers`, `/problems`, `/attempts`, `/drafts`), kiểm tra (`/checks/*`), ôn (`/review/*`), điều hướng (`/next`, `/resume`), thống kê (`/stats`, `/activity/ping`), vận hành (`/health`, `/backups*`, `/export`, `/import`, `/reset`). Quy ước: mọi POST ghi trạng thái nhận `Idempotency-Key`; lỗi dạng `{error: {code, message}}`; thời gian ISO 8601 UTC.

### 5.5 Lưu bền và backup (`SPEC §6.7`, `UI §4`)

- SQLite `journal_mode=WAL`, `synchronous=FULL`, mỗi sự kiện một transaction (ghi `events` và cập nhật điểm/thẻ cùng lúc). Khi khởi động, app **từ chối chạy** nếu `journal_mode` không phải `wal` hoặc thư mục dữ liệu nằm trên ổ mạng (nfs/cifs/smb/9p/vboxsf/fuse); rồi `quick_check`, hỏng thì hiện màn khôi phục.
- DB nằm trong named volume `app_data` (bind mount của Docker Desktop không bảo đảm `fsync`); backup là file thường ghi ra `./backups`.
- **Backup tự động**: lúc khởi động (nếu bản mới nhất > 1 giờ), mỗi 6 giờ, trước migration/import/restore/reset, khi tắt êm; giữ 20 bản gần nhất + 1 bản đầu mỗi ngày trong 30 ngày. Khôi phục một cú nhấp (UI ở T2.8).
- Nháp code: IndexedDB sau 300 ms, server sau 2 giây không gõ (tối đa 10 giây), cộng flush khi `blur`/`pagehide`. Với thiết kế M1, tắt máy mất tối đa ~0,3 giây gõ dở (IndexedDB), bản trên server chậm tối đa ~2 giây; mọi sự kiện đã hiện "Đã lưu" thì còn nguyên.

### 5.6 Triển khai (`SPEC §6.7`)

Mặc định chạy cục bộ: `docker compose up` rồi mở `http://127.0.0.1:8080` (`mem:learning-app`); `restart: unless-stopped`, healthcheck `GET /api/health`. Muốn dùng nhiều thiết bị: VPS nhỏ hoặc Fly.io + Tailscale/Cloudflare Access, **không** mở internet công cộng.

### 5.7 CI và e2e (`Makefile`, `.github/workflows/ci.yml`)

- `make ci` = `install` + `lint` (ruff, eslint) + `test` (pytest + vitest) + `validate` (`tools/validate_content.py --pyodide`, stress test chạy dưới Pyodide trong Node) + `web-build` (type-check + Vite build).
- Job CI riêng `e2e` chạy `make e2e`: build web, khởi động uvicorn + SQLite tạm, điều khiển Chromium/Pyodide qua Playwright (`apps/web/e2e/real.cjs`), không mock. Có thêm `make web-e2e` (smoke với API mock, không nằm trong CI). `make validate-public` là cổng chặn bản công khai khi còn `rewrite_required`.

---

## 6. Hiện trạng (đối chiếu repo ngày 2026-10-25)

### 6.1 Lịch sử và nhánh

`git log` trên `main` (4 commit): `1963250` Initial commit, `a160e05` **M0** (#1), `e6b6acc` **M1** (#2), `be29d68` thêm `source/` (#3). Working tree sạch, main đồng bộ với `origin/main`. Theo `mem:learning-app`, M1 merge 2026-10-24.

README đã được cập nhật sang trạng thái M1 xong.

### 6.2 Đã có trong repo

| Phần | Nội dung | Nguồn |
|---|---|---|
| M0 | Monorepo, Makefile, CI, JSON Schema (lesson/problem/check), `tools/sync_tree.py`, `validate_content.py`, `harness.py`, 40 lesson stub từ cây kiến thức, problem mẫu `ransom-note` | `README.md`, `SPEC §7` M0 |
| API M1 | FastAPI + SQLite/Alembic; content loader, `/map`, `/lessons`, `/quiz`, `/problems`, `/attempts`, `/drafts`, `/resume`, `/health`, `/backups*`, `/settings`, `/me`; scoring service; idempotency; backup tự động + restore | `docs/API_M1.md` |
| Web M1 | Routes `Home`, `LessonPage`, `ProblemPage` (split view, CodeMirror, panel kết quả, lesson renderer), Pyodide runner trong worker, nháp IndexedDB | `apps/web/src`, `SPEC §7` M1 |
| Validator | Đầy đủ theo `SPEC §4.4` (gen, brute-force cross-check, wrong/slow, giới hạn thời gian, `--pyodide`, `--public`) | `Makefile`, `mem:learning-app` |
| Docker | `Dockerfile` + `docker-compose.yml`, chạy bằng `docker compose up` | `mem:learning-app` |

**Test (đếm lại 2026-10-25, chạy trực tiếp)**: `uv run pytest` = **203 passed** (70-80 giây); vitest = **42 passed** (4 file). `make e2e` (e2e thật) tôi không chạy lại; theo `README.md` nó bao phủ: lesson, quiz, exercise, Submit AC, điểm, reload, TLE, kill -9, idempotency, backup restore (nghiệm thu M1 ở `SPEC §7`).

### 6.3 Dữ liệu nội dung

| Hạng mục | Đã có | Cần cho MVP | Nguồn |
|---|---|---|---|
| Lesson `published` | **3**: `py.datastructs.dict`, `py.datastructs.list`, `dsa.arrays_strings.arrays` | 40 | đếm lại trong `content/lessons`; 37 file còn lại chưa `published` |
| Lesson stub | 40 file tổng (3 published + 37 nháp) | 40 | đếm lại |
| Problem `published` | **5**: `ransom-note` (dict), `concatenation-of-array` (list), `find-numbers-with-even-number-of-digits`, `duplicate-zeros`, `max-consecutive-ones` (arrays) | **63** practice (59 bài chính + 4 bổ sung) | đếm lại; `SPEC §4.3` |
| Check problem | 0 (thư mục `content/checks` chưa tồn tại) | 70 (61 chuyển từ `assessment.json` + 9 bổ sung) | `SPEC §4.3`, `API_M1.md`, mục Deviations, điểm 8 |

Nội dung MVP là 40 subtopic, khoảng 43h theo kế hoạch, gồm tuần 1 (ngày 1-7) 28 mục và ngày 8-12 12 mục (`SPEC §4.1`).

### 6.4 Các sai lệch tạm thời (deviations)

| # | Sai lệch | Vì sao | Hết khi nào |
|---|---|---|---|
| D1 | `mastery_check` rỗng nên **một AC practice sạch đã cho điểm 2** (không cần đậu check mức 2). Cache điểm/quiz_best/thẻ ôn được tính lại từ bảng sự kiện mỗi lần khởi động | Chưa có `content/checks/` | Khi M2a thêm `convert_checks.py` + mastery check |
| D2 | `quiz_best` = số câu đúng / **tất cả** block graded (SPEC §5.1 nói "tỉ lệ đúng cao nhất trên các block graded" theo lượt, tối thiểu 3 câu đã trả lời) | Cách tính M1 đơn giản hoá | Cần đối chiếu khi viết test M2a; ghi nhận trong `mem:learning-app` |
| D3 | Server **không ép khoá** (`/map` chỉ báo `unlocked`/`lock_reasons`, UI quyết định) nên học `py.datastructs.dict` end to end vẫn được dù prerequisite còn điểm 0 | Đúng ý SPEC §5.3 "xem trước" và phục vụ nghiệm thu M1 | Giữ nguyên; UI sẽ tắt editor/Submit ở M2a |
| D4 | Chưa có: `PUT /profile`, placement, checks, review, `/next`, `/activity/ping`, `/stats`, `/feedback`, `/export`, `/import`, `/reset`; `GET /me` luôn trả `placement: "none"` | Thuộc M2a/M2b | M2a, M2b |
| D5 | Thêm so với SPEC §6.4: `GET /drafts/{problem_id}`, `POST /resume`, bảng `problem_state`, bảng `lesson_runs`, `check_results.item_type`; token Submit giữ trong bộ nhớ (restart server thì mất); đáp án và giải thích quiz ở lại server | Cần thực tế cài đặt | Ghi ở `API_M1.md` "Deviations" |
| D6 | M1 chưa có service worker, outbox replay, `draft_versions` + 409; drafts "bản mới hơn thắng" | Quyết định N1 của v0.7 | M3 (T3.5) |
| D7 | Repo tên `Testing`, spec nói `prep-app` | Quan tạo repo | Không cần đổi |
| D8 | (Không phải lỗi, quyết định có chủ ý) thẻ ôn hộp 3-5 trên thiết bị không có editor dùng item nhớ nhanh nên không tính `retention_ok` | Quyết định v0.7 | Vĩnh viễn (có chủ ý) |

### 6.5 Quy trình PR đã chạy

Sonnet build và review, Fable kiểm, Claude tự merge từng PR khi CI xanh (squash qua REST, vì tính năng auto-merge của GitHub tắt trên repo; "auto-merge on" trong MEMORY chỉ quy trình này). Đã áp dụng cho PR #1 (M0) và PR #2 (M1) (`mem:agent-roles`, `mem:learning-app`). Ghi chú kỹ thuật: bản clone là shallow single-branch; đặt `remote.origin.fetch` thành `+refs/heads/*:refs/remotes/origin/*` trước khi dùng worktree (`mem:learning-app`).

---

## 7. Lộ trình còn lại

Thời gian là ước lượng của spec, giả định agent chạy song song (`SPEC §7`).

### 7.1 Đến MVP

| Mốc | Thời gian | Việc chính | Nghiệm thu chính | Nội dung phải soạn (suy ra từ SPEC) |
|---|---|---|---|---|
| **M2a** Ngày 1-3 + vòng lặp | 7-10 ngày | T2.1a wave 1a 16 mục; T2.3 unlock + `/map`; T2.4 Leitner + `/review`; T2.5 "Học tiếp" + `study_time`; T2.2 mastery check/Test out; T2.7 onboarding + banner tiếp tục; T2.8 UI backup; T2.9a placement tối thiểu | Quan làm hết nhóm 1-3 (16 mục) theo nhịp bất kỳ mà không bị báo trễ/phạt; thẻ D+1 hiện đúng ngày, mô phỏng 30 ngày khớp bảng Leitner; Test out hoạt động; hồ sơ yếu xong placement <= 9 phút, hồ sơ mạnh <= 45 phút; kill tab rồi mở lại tiếp đúng item (sai <= 15 giây) | 16 lesson (2 đã có) = 14 mới, khoảng 25 problem, 5 item `write_code` mức 2 bổ sung (`getting_started`, `variables_types`, `tuple_namedtuple`, `copying_mutability`, `lambda_hof`) |
| **M2b** Hết tuần 1 + đánh giá đầy đủ | 5-7 ngày | T2.1b wave 1b 12 mục ngày 4-7; T2.6 `/problems`, `/progress`, báo lỗi, export/import; T2.9b placement đầy đủ (Phase B/C, nhãn suy luận, sweep, rải thẻ, làm lại theo module, S3 đầy đủ) | 28/28 lesson tuần 1 `published`; unlock chặn `hashing_patterns` tới khi `hash_tables >= 2`; mô phỏng 3 hồ sơ xong placement <= 60 phút hoạt động; không mục nào đạt 3 do placement | 12 lesson (`arrays` đã xong nên 11 mới), khoảng 44 problem tuần 1 tính luỹ kế, 3 item `write_code` bổ sung (`big_o`, `memory_model`, `scope_closures`) |
| **M3** MVP dùng được | 1 tuần | T3.1 wave 2 12 mục ngày 8-12 + item cho `interview_method`; T3.2 đóng gói compose + README; T3.5 offline đầy đủ (service worker, outbox, `draft_versions` + 409); T3.3 đánh bóng (phím tắt, dark mode, responsive 3 mức, axe-core); T3.4 kiểm thử mạch cuối (tài khoản giả lập đi hết nhóm 1-12, 20 lần tắt máy ngẫu nhiên) | **Definition of Done MVP**: 40 lesson, 63 practice + 70 check problem, tất cả `published` và qua validator; Quan đi trọn nhóm 1-12; điểm/unlock/review đúng `SPEC §5` có test tự động; không còn lỗi chặn; backup/restore thử thành công | 12 lesson mới, 1 item bổ sung; tổng MVP còn lại khoảng 37 lesson mới (suy ra: 40 - 3 đã có) |

Khối lượng nội dung tổng của MVP (`SPEC §4.3`): 40 lesson; khoảng 160 quiz item mới (4 mỗi lesson); khoảng 60 code exercise (khoảng 240 test); 63 practice problem; 61 + 9 = 70 check problem; 51 check item không code (31 read_code + 20 concept); khoảng 1.200 hidden test (khoảng 90% sinh bằng script); 133 reference solution (61 đã có trong `assessment.json`); khoảng 190 wrong/slow solution; 63 x 3 gợi ý. Đã xong: 3 lesson và 5 problem.

### 7.2 Sau MVP (`SPEC §7`)

| Mốc | Nội dung |
|---|---|
| **M4** Hoàn thiện tuần 2 + mock | 6 mục ngày 13-14 (`heap_ds`, `heap_top_k`, `binary_search_variants`, `sliding_window_fixed`, `sliding_window_variable`, `backtracking_core`) + 4 mục `bh.*` (text/quiz, không code); quiz tuần; `tools/import_mock.py` biến `content_ng/*.json` thành problem `kind: mock`; màn "Mock" mở theo tiến độ, 2 bài, đồng hồ cứng 45 phút, tắt hint, tự chấm theo `rubric_vi`, kết quả ghi `mock_sessions` và đóng góp bằng chứng điểm |
| **M5** Java | Runner server Judge0 CE tự host (trong compose hoặc VPS); `starter.java`, ánh xạ `py.* -> java.*` từ `java_variant`; lesson Java theo `lang_prereqs`; editor chọn ngôn ngữ |
| **M6** Toàn bộ 530 mục | Soạn theo section (01 py, 04 dsa, 03 cs, 02 java, ...); section `ml` dùng Pyodide + numpy/pandas cho bài code, phần torch/LLM là quiz hoặc runner server; dùng `bank_topics` kéo câu thật; `question_gaps.md` thành backlog soạn câu |
| **M7** Nhiều người dùng | Auth (OIDC/OAuth) vào `current_user()`; SQLite sang Postgres; chuyển hoàn toàn sang runner server (không gửi hidden test/lời giải cho client); rate limit; viết lại mọi đề `rewrite_required`, kiểm giấy phép; quyền truy cập nội dung theo gói (nếu có) |

---

## 8. Rủi ro chính

| Rủi ro | Giảm thiểu (nguồn: `SPEC §8.1` trừ khi ghi khác) |
|---|---|
| Làm app tốn thời gian học thật | Học song song theo `plan.md`; app chỉ cần đủ cho ngày 1-3 (M2a) trước khi mở rộng |
| LLM viết test/đáp án sai | Expected luôn do reference tính + brute-force độc lập + wrong/slow solution (`SPEC §4.4`) |
| Pyodide chậm hoặc không ép bộ nhớ; hidden test xem được trong DevTools | Hệ số thời gian x3 kèm `solution.py` <= 0,3 x `time_ms`; chấp nhận cho một người; runner server ở M5/M7 |
| Khối lượng nội dung lớn (133 problem, khoảng 1.200 test, 40 lesson) | Pipeline song song theo mục; ưu tiên tuần 1; chuyển check từ assessment bằng script. Đây là việc chiếm phần lớn M2a-M3 |
| Đề bám LeetCode | Chỉ dùng cá nhân; cờ `rewrite_required` + `make validate-public` chặn build công khai |
| Điểm 3 đòi 7 ngày nên cảm giác lâu | Giải thích trên UI; `target_intern` đa số là 2-3 |
| Học tự do dễ để backlog ôn tồn hoặc nghỉ dài rồi quên | Banner backlog mềm (> 20 thẻ), preset "Phiên ngắn", thẻ trễ không bị phạt; không streak |
| Không có lịch cứng nên dễ trôi | `/progress` chỉ hiện "đã xong X / 40 mục", mục kế tiếp, giờ theo tuần |
| Mất dữ liệu khi tắt máy hoặc ổ đĩa sai | `synchronous=FULL`, named volume, từ chối chạy trên ổ mạng, backup tự động, IndexedDB (`SPEC §6.7`) |
| Thời gian placement thực so với time-box chưa kiểm | Mô phỏng chỉ cho 6-47 phút (`UI §2.7`: yếu ~6-9 / 12-18, trung bình 40-47, mạnh 42-44); subset tiếng Việt của JetBrains Mono chưa xác minh, kiểm khi cài đặt (`REV` changelog v0.6) |
| Điểm lệch do deviation M1 (D1, D2 ở mục 6.4) | Sửa ở M2a cùng mastery check; viết test bảng ví dụ `SPEC §5.2` |
| Mặc định 5 câu hỏi mở chưa được Quan xác nhận | Hỏi Quan trước M3 ít nhất câu 1 (40 hay 46 mục) và câu 2 (cần dùng ngoài máy chính không) vì ảnh hưởng đóng gói (T3.2) |

---

## 9. Danh mục tài liệu và đường dẫn

### 9.1 App học (spec và code)

| Tài liệu | Đường dẫn |
|---|---|
| Tổng quan này | `docs/OVERVIEW.md` (bản trong repo) |
| SPEC v0.7 (sản phẩm + kiến trúc + lộ trình) | `docs/SPEC.md` |
| UI_SPEC v0.2 (quy trình, placement, 13 màn hình, lưu bền) | `docs/UI_SPEC.md` |
| Lịch sử review, changelog v0.1 đến v0.7 | `review.md` (project folder, không có trong repo) |
| Code đã build (M0 + M1) | Repo này; GitHub `https://github.com/PhamAnhQuannn/Testing` (PR #1 M0, PR #2 M1, PR #3 `source/`, đã merge) |
| API như đã cài ở M1 + danh sách sai lệch | `docs/API_M1.md` |
| Hướng dẫn chạy, kiểm thử, công cụ nội dung | `README.md`, `Makefile` |

Lệnh hay dùng: `docker compose up` (mở `http://127.0.0.1:8080`), `make ci`, `make e2e`, `make validate`, `make validate-public`, `make dev-api`.

### 9.2 Dữ liệu nguồn của app

| Tài liệu | Đường dẫn |
|---|---|
| Mô hình 4 tầng | `interview-prep/README.md` (project folder, không có trong repo) |
| Cây kiến thức (530 mục) | `interview-prep/layer1_skill_tree/` (project folder, không có trong repo) (`skill_tree.json`, `README.md`, `raw/qa_v1/qa_v1_summary.md`) |
| Phân tích thiếu hụt câu hỏi | `interview-prep/analysis/question_gaps.md` (project folder, không có trong repo) |
| Kế hoạch Meta 30 ngày + đánh giá + review | `interview-prep/plans/meta_1month/` (project folder, không có trong repo) (`plan.md`, `plan.json`, `assessment.json`, `review.md`) |
| Dataset phỏng vấn | `interview-research/` (project folder, không có trong repo) (`interview_processes.xlsx`, `question_bank.md`) |
| Kiểm tra Meta 2026 | `interview-research/meta_2026/` (project folder, không có trong repo) (`README.md`, `claims_verification.md`, `predicted_questions.md`) |
| Mock Word intern + new grad | `interview-research/meta_2026/mock/Meta_2026_Intern_NewGrad_Mock.docx` (project folder, không có trong repo) (`MOCK_SPEC_NG.md`, `review_ng.md`) |

### 9.3 Memory của team

Memory của team (project memory, không có trong repo; các file `learning-app.md`, `interview-prep-model.md`, `interview-research-scope.md`, `interview-research-outputs.md`, `agent-roles.md`). Quyết định quan trọng đã được chép vào tài liệu này và `CLAUDE.md`.
