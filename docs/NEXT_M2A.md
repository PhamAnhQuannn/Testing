# NEXT_M2A: kế hoạch làm M2a (cho Claude Code trên VS Code)

Nguồn: `docs/SPEC.md` mục 7 (M2a), `docs/OVERVIEW.md`, `docs/API_M1.md`. Đọc `CLAUDE.md` trước.
Mục tiêu M2a: Quan làm hết nhóm 1-3 của plan (16 subtopic) trong app theo nhịp tự do, có mở khoá,
mastery check/Test out, ôn Leitner, "Học tiếp", onboarding, UI backup và placement tối thiểu.
Dự kiến 7-10 ngày. Quy tắc làm việc: mỗi task một nhánh `m2a/<task>`, PR nhỏ, `make ci` xanh,
subagent (Sonnet) làm, một lượt review độc lập trước khi merge; không đổi luật điểm/unlock/Leitner
nếu không sửa SPEC cùng PR. Claude tự push, mở PR và squash-merge (`gh pr merge --squash`) khi review độc lập và CI + e2e xanh; chỉ hỏi Quan khi đổi SPEC/luật điểm hoặc quyết định đánh dấu "hỏi Quan".

## 0. Hiện trạng cần biết trước khi bắt đầu

- Có sẵn từ M1: `apps/api/app/services/{scoring,unlock,leitner,progress,content_loader}.py` (hàm thuần),
  routers `content/learning/problems/resume/system`, `/map`, `/lessons`, `/quiz`, `/attempts`,
  `/drafts`, `/resume`, `/health`, `/backups*`. Web: routes `Home`, `LessonPage`, `ProblemPage`.
- Bảng đã có (migration `0001`): subtopics, lessons, problems, quiz_items, users, settings, user_subtopic, lesson_runs, quiz_answers, problem_state, attempts, check_results, review_cards, review_log, drafts, events, resume_state, idempotency_keys. Chưa có: `check_sessions`, `study_time`, `placement_sessions`, `plan_order`/`plan_milestones` (kiểm `content_loader.py`; mọi bảng mới qua Alembic).
- Chưa có: `content/checks/`, `tools/convert_checks.py`, `/checks/*`, `/review/*`, `/next`,
  `/activity/ping`, `PUT /profile`, `/placement/*`, các màn S1, S2, S3, S4, S5, S8, S9, S11 (backup UI), S12 (banner "Tiếp tục").
- Sai lệch M1 phải xử lý: D1 (không có check nên 1 AC sạch = điểm 2). D2 (`quiz_best`) đã sửa ở M1; chỉ còn thiếu test bảng 3 ví dụ SPEC 5.2 (làm trong A2).
  Xem `docs/API_M1.md` "Deviations".
- Nội dung: 2/16 lesson của nhóm 1-3 đã `published` (`py.datastructs.list`, `py.datastructs.dict`).

## 1. Thứ tự task và ranh giới PR

Thứ tự theo phụ thuộc (SPEC 7 liệt kê T2.1a trước nhưng nội dung chạy song song với code).
Các PR code (A) và PR nội dung (C) độc lập nhau, trừ khi ghi chú.

| PR | Task | Phụ thuộc | Cỡ |
|---|---|---|---|
| A1 | T2.2a `tools/convert_checks.py` + schema/validator cho check | không | vừa |
| A2 | T2.2b API checks + `check_sessions` + bỏ fallback D1 + test bảng 3 ví dụ SPEC 5.2 | A1 | lớn, tách 2 PR nếu cần |
| A3 | T2.2c UI `/check/:id` (flow C, D) | A2 | vừa |
| A4 | T2.3 unlock + `/map` + S5 + chế độ xem trước (editor/Submit tắt) | A2 (cho `tested_out`) | vừa |
| A5 | T2.4a Leitner + `/review/*` API | A2 | vừa |
| A6 | T2.4b UI `/review` (S9) + banner backlog | A5 | vừa |
| A7 | T2.5 `/next` + `/activity/ping` + `study_time` + Home S4 | A4, A5 | vừa |
| A8 | T2.7 onboarding S1 + `PUT /profile` + `GET /me.onboarding` + banner "Tiếp tục" | A7 | vừa |
| A9 | T2.8 UI backup trong Settings (S11 phần backup) | không | nhỏ |
| A10 | T2.9a-1 `services/placement.py` + API `/placement/*` | A2, A4, A7 | lớn |
| A11 | T2.9a-2 S2 + S3 rút gọn, bật nút "Đánh giá" ở S1 | A10, A8 | vừa |
| C1..C5 | T2.1a nội dung 14 lesson (mục 3) | A1 cho phần check; validator hiện có | mỗi PR 2-3 mục |

Có thể làm C-PR song song với A-PR bằng subagent riêng; mỗi PR nội dung chỉ chạm
`content/lessons`, `content/problems`, không đụng code.

## 2. Chi tiết từng task

### T2.2a (A1) `convert_checks.py` và mastery check
- Mục tiêu: chuyển `assessment.json` thành `content/checks/<subtopic_id>.yaml` (schema
  `content/schemas/check.schema.json`: `id, difficulty, type, minutes, prompt_md, problem_id | code+expected_output | answer_md, rubric_md`)
  và sinh problem `kind: check` cho mọi item `write_code` (61 item MVP; 14 thuộc nhóm 1-3, xem mục 4).
- Input: `source/assessment.json` (field `id, subtopic_id, difficulty, type, minutes, prompt, answer, rubric, reference, driver, expected_output`;
  chú ý: đọc kỹ các field `reference`/`driver` thật sự có trong file; script bỏ qua item ngoài 40 mục MVP,
  lọc theo `content/index/subtopics.json`).
- Output: `content/checks/*.yaml`; `content/problems/<subtopic_id>/<slug>/` với `kind: check`, mode `stdout`/`function`,
  1 sample + >= 5 hidden sinh từ `reference` bằng `gen_hidden.py` (đừng gõ expected tay); `minutes` thành time-box.
  Slug đặt theo id item (ví dụ `check-q023`) và ghi quy ước vào `content/schemas`/docstring của tool.
- Chạm: `tools/convert_checks.py` (mới, theo phong cách `tools/gen_lesson_stubs.py`), `tools/validate_content.py`
  (quy tắc: lesson đang validate phải có >= 1 item mức 2 `write_code`; check >= 5 hidden; lesson `mastery_check` khớp `content/checks`),
  `Makefile` (target `checks`), test trong `tools/tests/`.
- Nghiệm thu: tool idempotent (chạy lại ra đúng file cũ); validator bắt thiếu item `write_code` mức 2; 61 check problem + 51 item
  không code chuyển được; `make validate` xanh. Các file `content/checks/*` là sinh ra, không sửa tay.
- Lưu ý: 9 item `write_code` mức 2 bổ sung (SPEC 3.4) do author tự soạn, không có trong `assessment.json`; trong M2a có 5 (mục 5).

### T2.2b (A2) API mastery check
- Mục tiêu: flow C (thang bậc mức 2 rồi 3, trượt thì mức 1 chẩn đoán) và flow D (Test out), làm lại sau 24 giờ,
  `tested_out` ghi `unlocked_at` cho chính mục, bỏ fallback D1 (một AC sạch không còn đủ cho điểm 2).
- Chạm: `apps/api/app/routers/` (router mới `checks.py`), `services/` (`checks.py` mới; `scoring.py` dùng `check_results`),
  `models/tables.py` + migration Alembic mới (`check_sessions`, cột `attempt_no`, `gave_up`, `context`), `docs/API_M1.md` (hoặc `API_M2A.md`).
- Endpoint: `POST /checks/{subtopic_id}/start` (tiếp tục phiên dở trong 24h), `POST /checks/{subtopic_id}/answer`,
  `POST /checks/{session_id}/heartbeat` (SPEC 6.4). Có `Idempotency-Key`.
- Nghiệm thu: thêm test bảng cho 3 ví dụ SPEC 5.2 (`apps/api/tests/test_scoring.py`); test cho bảng 5.2 (clean = AC, không xem lời giải, <= 1 hint, <= 1,5 x time target); khoá làm lại 24 giờ
  (`check_retry_locked`, trả `retry_after`); trượt không lộ `reference`; `concept` tự chấm nhưng không bao giờ là bằng chứng điểm 2;
  `tested_out` cho điểm 2 và mở khoá một chiều; điểm luôn `== scoring(events)` sau khi tính lại.

### T2.2c (A3) UI `/check/:subtopicId` (S8)
- Chạm: `apps/web/src/routes/CheckPage.tsx` (mới), `App.tsx` route, `lib/api.ts`, tái dùng `EditorPanel`, `TestResultPanel`,
  runner Pyodide. Chế độ tập trung, đồng hồ time-box, nút "Không biết" (ghi `gave_up`), nút Test out từ lesson/map/Học tiếp.
- Nghiệm thu: vitest cho các trạng thái chính (UI_SPEC S8); e2e `apps/web/e2e/real.cjs` thêm kịch bản Test out (tuỳ chọn, nên có).

### T2.3 (A4) Unlock + Skill map (S5)
- Mục tiêu: mở khoá theo SPEC 5.3 (`unlocked_at` một chiều, `assumed`, `blocked_missing_content`), `/map` đủ trạng thái,
  S5 hiện khoá/mở/điểm; mục khoá đọc xem trước, editor và Submit tắt, có nút Test out (D3: server không ép khoá).
- Chạm: `services/unlock.py` (đã có; nối vào `progress.py`), `routers/content.py` (`/map`), `apps/web/src/routes/MapPage.tsx` (mới),
  `LessonPage.tsx`/`ProblemPage.tsx` (tắt editor khi khoá), test `apps/api/tests/`.
- Nghiệm thu: unit test `unlocked_at` một chiều (điểm prerequisite đổi sau đó không khoá lại); `lock_reasons` đúng;
  trên nhóm 1-3 hầu hết prerequisite rỗng nên mở hết, nhớ test với đồ thị tuần 1 (`hash_tables` cần `arrays` >= 2) bằng fixture.

### T2.4 (A5, A6) Leitner + `/review`
- Mục tiêu: thẻ tạo khi mục đạt điểm >= 1 lần đầu (`lesson_done` hoặc check pass); `gap = {1:1, 2:2, 3:4, 4:7, 5:14}` rồi 30 ngày,
  tính từ ngày ôn thật; trượt về hộp 1, `lapses += 1`; không trần thẻ; hộp 1-2 dùng item nhớ nhanh, hộp 3-5 dùng bài code
  (ưu tiên `review_hint` từ plan: `plan.days[N].review`). Preset "Phiên ngắn" (mặc định cỡ 6, tối đa 2 thẻ code), banner backlog > 20.
- Chạm: `services/leitner.py` (có sẵn), `routers/review.py` (mới: `GET /review/queue`, `POST /review/{subtopic_id}/result`),
  `models/tables.py` (`review_cards`, `review_log` đã có từ migration `0001_m1_tables.py`; chỉ thêm cột nếu cần, bằng migration mới), `apps/web/src/routes/ReviewPage.tsx` (S9).
- Nghiệm thu: mô phỏng 30 ngày khớp D+1/3/7/14/28; ôn trễ thì hạn kế tính từ ngày ôn thật; queue đủ thẻ, đúng thứ tự
  (quá hạn nhiều nhất trước, tie-break điểm thấp); `retention_ok` chỉ nhận lần đạt ở hộp >= 3 bằng `item_kind = code`.
- Lưu ý nội dung: mỗi mục cần item nhớ nhanh cho hộp 1-2 (quiz/`read_code` của lesson hoặc check mức 1).

### T2.5 (A7) "Học tiếp" và `study_time`
- Mục tiêu: `GET /next` trả `must_raise` (prerequisite đang chặn, kèm mục sẽ mở và bài gợi ý) rồi danh sách mục mở khoá chưa `done`
  theo khoá `(N, vị trí)` của `plan_order`; mục `in_progress` lên đầu; mục `check_retry_locked` xếp sau. `POST /activity/ping` cộng
  `min(now - last_ping, 60s)` vào `study_time` (bỏ qua khoảng > 2 phút; `last_ping` theo `user_id`).
- Chạm: `routers/` (`next.py`, `activity.py` mới), `services/next_up.py`, `plan_order`/`plan_milestones` từ `content/index/plan.json`
  (kiểm `content_loader.py`), `apps/web/src/routes/Home.tsx` (S4), hook ping 30 giây.
- Nghiệm thu: thứ tự đúng nhóm 1-3 kể cả khi học 5 mục trong một ngày hay nghỉ nhiều ngày; không chỗ nào hiện "trễ" hay định mức.

### T2.7 (A8) Onboarding + Tiếp tục
- Mục tiêu: S1 `/welcome` (kiểm tra Pyodide, hồ sơ 4 câu: `target_role`, `track`, `language`, `experience`), `PUT /profile`,
  `GET /me.onboarding`, banner "Tiếp tục nơi bạn dừng" dựa trên `GET /resume` (đã có từ M1). Nút "Đánh giá" bật khi A11 xong.
- Nghiệm thu: lần đầu mở app đi hết hồ sơ và vào `/`; thoát giữa lesson rồi mở lại: banner về đúng block, nháp còn nguyên.

### T2.8 (A9) UI backup
- Chạm: `apps/web/src/routes/SettingsPage.tsx` (S11 phần backup): danh sách, "Sao lưu ngay", "Khôi phục" (API đã có: `GET/POST /backups`,
  `POST /backups/{name}/restore`). Nghiệm thu: làm hỏng DB rồi `Khôi phục` từ Settings thành công (có thể thêm vào e2e).

### T2.9a (A10, A11) Placement tối thiểu (làm cuối, sau T2.2/T2.3/T2.5)
- Mục tiêu: `services/placement.py` Phase A (cổng C1-C7, 6 phút mỗi cổng) + luật dừng (kể cả "Không biết"); gieo `tested_out` qua
  `check_results` (`context=placement`); `POST /placement`, `/skip`, `/answer`, `/heartbeat`, `/finish`, `GET /placement/{id}/result` rút gọn;
  S2 và S3 rút gọn (mục đã đo, mục bắt đầu trong các lesson đã `published`, trạng thái "nội dung tiếp theo đang soạn").
- Đọc: `docs/UI_SPEC.md` mục 2 (thuật toán, ngân sách thời gian) và `docs/SPEC.md` 5.6 (luật gieo điểm).
- Nghiệm thu (SPEC 7): hồ sơ yếu (`experience=none`) xong <= 9 phút; hồ sơ mạnh <= 45 phút; `score == scoring(events)` và không mục nào do
  placement đạt 3; kill tab giữa item rồi mở lại tiếp đúng item (sai <= 15 giây); "bắt đầu từ đầu" không ghi điểm.
  Placement chỉ dùng item `write_code` mức 2 (31/40 mục placeable); đậu mức 1 đặt `known_basic`, không đổi điểm.

## 3. Backlog soạn nội dung T2.1a (nhóm 1-3 của plan, 16 subtopic)

Quy trình mỗi subtopic (SPEC 4.4): author subagent soạn lesson + toàn bộ problem; `make validate`; reviewer subagent độc lập (không thấy chat
của author) ghi `content/reviews/<id>.md`; `status: published`. Model chuẩn: `content/lessons/py/py.datastructs.dict.yaml` và
`content/problems/py.datastructs.dict/ransom-note/`. Mỗi lesson: 8-11 block, >= 3 block `graded`, ~4 quiz item, 1-2 code exercise.
Lesson tiếng Việt, thuật ngữ giữ tiếng Anh, chỉ dùng thuật ngữ đã học (xem `prerequisites`).

| Ngày | Subtopic | Lesson | Problem chính (plan) |
|---|---|---|---|
| 1 | `py.core.getting_started` | draft | LC2235 Add Two Integers |
| 1 | `py.core.variables_types` | draft | LC1512 Number of Good Pairs |
| 1 | `py.core.operators` | draft | LC1281 Subtract the Product and Sum of Digits |
| 1 | `py.core.conditionals` | draft | LC412 Fizz Buzz |
| 1 | `py.core.loops` | draft | LC263 Ugly Number |
| 1 | `py.core.strings` | draft | không có bài chính; SPEC 4.3: lấy 1 bài từ extra (LC709, LC344, LC58, LC14) |
| 1-2 | `py.datastructs.list` | **published** | LC1929 Concatenation of Array (đã có `concatenation-of-array`) |
| 2 | `py.datastructs.tuple_namedtuple` | draft | LC832 Flipping an Image |
| 2 | `py.datastructs.dict` | **published** | LC383 Ransom Note (đã có `ransom-note`) |
| 2 | `py.datastructs.comprehensions` | draft | LC1365 How Many Numbers Are Smaller Than the Current Number |
| 2 | `py.datastructs.collections_module` | draft | LC169 Majority Element |
| 3 | `py.datastructs.copying_mutability` | draft | LC118 Pascal's Triangle; LC189 Rotate Array (M, cần `brute.py`) |
| 3 | `py.datastructs.heapq_bisect` | draft | không có trong plan: SPEC 4.3 yêu cầu 1 bài mới tự soạn |
| 3 | `py.functions.def_args` | draft | LC1389 Create Target Array in the Given Order; LC509 Fibonacci Number |
| 3 | `py.functions.lambda_hof` | draft | LC1051 Height Checker |
| 3-4 | `py.functions.sorting_keys` | draft | bài chính LC937 nằm ở ngày 4 (M2b); lesson thuộc ngày 3 (part 1) nên soạn lesson ở M2a, problem để M2b hoặc làm sớm nếu muốn |

Phạm vi con số: 16 lesson (2 đã xong, 14 mới). Problem tối thiểu: 13 bài chính mới + `strings` (1 từ extra) + `heapq_bisect` (1 mới)
= 15 mới, cộng 2 đã có. SPEC 7 ước tính ~25 problem cho 16 mục: phần chênh lấy từ `extra_problems` của plan, ưu tiên mục chỉ có 1 bài
(vì `practice_ok` cần `min(2, số bài practice)` AC phân biệt). Extra có sẵn trong `source/plan.json` (`days[0..2].extra_problems`):
getting_started LC1920; variables_types LC2011; operators LC9; conditionals LC2413; strings LC709/344/58/14; list LC1470/1480/1672;
tuple LC561; dict LC387; comprehensions LC1431; collections LC349. Quyết định mục nào có bài thứ hai: hỏi Quan hoặc theo ngân sách ~25.
Cờ `source.rewrite_required: true` cho mọi đề bám LeetCode.

Gợi ý chia PR nội dung: C1 = ngày 1 (6 mục, tách 2 PR nếu lớn: C1a `getting_started`+`variables_types`+`operators`, C1b `conditionals`+`loops`+`strings`),
C2 = ngày 2 (`tuple_namedtuple`, `comprehensions`, `collections_module`), C3 = `copying_mutability`+`heapq_bisect`,
C4 = `def_args`+`lambda_hof`+`sorting_keys`. Trước khi merge C-PR cần `make ci` xanh (validator chạy cả stress test dưới Pyodide).

## 4. Check item của nhóm 1-3 (input cho T2.2a)

Từ `source/assessment.json` (38 item): 14 `write_code`, 20 `read_code`, 4 `concept`.

| Subtopic | Item (mức, loại) |
|---|---|
| getting_started | Q001 L1 concept; Q002 L2 read_code (thiếu write_code mức 2: cần item bổ sung) |
| variables_types | Q003 L1 read; Q004 L2 read (cần bổ sung) |
| operators | Q005 L1 read; Q006 L2 write |
| conditionals | Q007 L1 read; Q008 L2 write |
| loops | Q009 L1 read; Q010 L2 write |
| strings | Q011 L1 read; Q012 L2 write; W185 L2 write; Q013 L3 write |
| list | Q018 L1 read; Q019 L2 write; W184 L2 read |
| tuple_namedtuple | Q020 L1 read; Q021 L2 concept (cần bổ sung) |
| dict | Q022 L1 read; Q023 L2 write; Q024 L3 write; W183 L2 read |
| comprehensions | Q025 L1 read; Q026 L2 write |
| collections_module | Q027 L1 read; Q028 L2 write |
| copying_mutability | Q029 L1 read; Q030 L2 concept (cần bổ sung) |
| heapq_bisect | Q031 L1 read; Q032 L2 write |
| def_args | Q033 L1 read; Q034 L2 write; W186 L2 read |
| lambda_hof | Q035 L1 read; Q036 L2 concept (cần bổ sung) |
| sorting_keys | Q037 L1 read; Q038 L2 write |

## 5. 9 subtopic cần thêm item `write_code` mức 2 (SPEC 3.4) - phần của M2a

Chín mục có mọi item mức 2 gốc chỉ là `concept`/`read_code`: `py.core.getting_started`, `py.core.variables_types`,
`py.datastructs.tuple_namedtuple`, `py.datastructs.copying_mutability`, `py.functions.lambda_hof`, `cs.complexity.big_o`,
`dsa.foundations.memory_model`, `py.functions.scope_closures`, `dsa.foundations.interview_method`.
**M2a làm 5 mục đầu** (đều thuộc ngày 1-3): getting_started, variables_types, tuple_namedtuple, copying_mutability, lambda_hof.
`big_o`, `memory_model`, `scope_closures` thuộc M2b (T2.1b); `interview_method` thuộc M3.

Mỗi mục đúng 1 item: problem `kind: check`, mức 2, `write_code`, có `solution.py` + hidden test (>= 5, sinh bằng `gen_hidden.py`) +
`wrong/`; ghi vào `content/checks/<id>.yaml` cùng định dạng item đã chuyển; do author agent viết cùng lúc với lesson. Validator chặn
nếu mục có lesson mà thiếu item `write_code` mức 2 (sau A1), nên soạn item bổ sung trước hoặc cùng PR với lesson. Vì `convert_checks.py`
ghi đè `content/checks/*`, đặt item bổ sung ở nơi tool không ghi đè (ví dụ file `content/checks_extra/<id>.yaml` do tool gộp vào) và ghi
quy ước đó trong tool.

## 6. Checklist phiên đầu tiên của Quan trong VS Code

1. `git fetch && git switch vscode-handoff && git pull` (hoặc nhánh đã merge vào `main`; nếu chưa clone:
   `git clone https://github.com/PhamAnhQuannn/Testing.git`, rồi `git switch vscode-handoff`). Mở thư mục repo trong VS Code; chấp nhận
   gợi ý cài extension (`.vscode/extensions.json`).
2. Cài tiền đề:
   - **uv** (https://docs.astral.sh/uv/): tự tải Python 3.12.
   - **Node 22.12+** (kèm npm). Kiểm: `node -v`.
   - **Docker Desktop** (chỉ cần để chạy `docker compose up`): dữ liệu nằm trong named volume `app_data`, đừng đổi sang bind mount;
     thư mục `./backups` là file thường. Không để repo/`data/`/`backups/` trong OneDrive, Dropbox hay ổ mạng.
   - **Windows**: dùng WSL2 (extension "WSL"); `tools/run_problem.py` không chạy trên Windows thuần. Clone vào ổ WSL (`~/`), KHÔNG vào `/mnt/c` (kiểm tra độ bền từ chối 9p nên `make dev-api` sẽ lỗi). Trong WSL: `sudo apt install make build-essential`; bật Docker Desktop -> Settings -> Resources -> WSL integration.
   - Claude Code: cài CLI hoặc extension Claude Code cho VS Code theo hướng dẫn chính thức, đăng nhập.
3. `make install` (cài Python và npm dependencies).
4. `make ci` phải xanh (lint, test, validate, web-build; vài phút, lần đầu tải Pyodide cần mạng).
5. Chạy app: `docker compose up` rồi mở http://127.0.0.1:8080; hoặc chế độ dev: terminal 1 `make dev-api`,
   terminal 2 `cd apps/web && npm run dev` rồi mở địa chỉ Vite in ra. Thử học `py.datastructs.dict` end to end để chắc M1 chạy.
6. Mở Claude Code ở thư mục gốc repo (nó tự đọc `CLAUDE.md`), tạo nhánh `m2a/...` và dán prompt dưới đây.

### Prompt đầu tiên gợi ý (tiếng Việt)

```
Đọc CLAUDE.md, docs/NEXT_M2A.md, docs/SPEC.md (mục 3.4, 5, 7) và docs/API_M1.md. Mình muốn bắt đầu M2a theo thứ tự trong NEXT_M2A.md.
Bước 1: chạy `make ci` để xác nhận nền xanh, rồi tóm tắt cho mình bằng tiếng Việt: hiện trạng, các PR dự kiến (A1, A2, ...) và rủi ro.
Bước 2: làm PR A1 (T2.2a: tools/convert_checks.py, source/assessment.json -> content/checks/*.yaml + check problem, thêm quy tắc validator) trên nhánh
m2a/t2.2a-convert-checks. Dùng subagent Sonnet để cài đặt, sau đó một subagent review độc lập (chưa thấy lý luận của author) kiểm trước khi merge.
Không đổi luật điểm nếu không sửa SPEC.
Bước 3: sau khi A1 xong, lên kế hoạch chi tiết cho A2 (T2.2b API mastery check) và hỏi mình những điểm còn mơ hồ trước khi code.
Nhớ: trả lời mình bằng tiếng Việt; tự push/PR/merge theo quy tắc CLAUDE.md; chỉ hỏi mình khi đổi SPEC.
```

Song song (tuỳ chọn): mở một phiên Claude Code thứ hai trên nhánh `m2a/content-day1` để soạn nội dung ngày 1 theo mục 3 (C1a), vì code và nội dung
không đụng nhau.
