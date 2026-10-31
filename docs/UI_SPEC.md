# UI_SPEC: Quy trình, giao diện và lưu trạng thái của Prep App

Phiên bản 0.2 (đi kèm `SPEC.md` v0.7; v0.2 sửa theo review v0.6: dừng sớm khi "Không biết", `retention_ok` chỉ nhận bài code, named volume, tách T2.9a/T2.9b, phạm vi lưu bền M1 so với M3) · 2026-10-24 · Chủ sở hữu: Quan · Ngôn ngữ: tiếng Việt (thuật ngữ, tên field, route giữ tiếng Anh)

Tài liệu này là phần bổ sung của `SPEC.md`: mô tả **hành trình từ lần mở app đầu tiên**, **bài đánh giá trình độ đầu vào (placement)**, **toàn bộ UI** và **cơ chế nhớ dữ liệu, tiếp tục sau khi thoát hoặc tắt máy**. Luật điểm, mở khoá, Leitner nằm ở `SPEC.md` mục 5 và **không bị đổi** ở đây; mọi chỗ tài liệu này cải tiến `SPEC.md` đều được đánh dấu **[SPEC↑]** và đã được áp vào `SPEC.md` v0.6 (liệt kê ở mục 5).

Quyết định nền (không nhắc lại lý do): một người dùng (Quan), tự chọn nhịp học, plan chỉ là thứ tự gợi ý, MVP 40 subtopic, chạy cục bộ bằng `docker compose`, React+Vite / FastAPI+SQLite / Pyodide trong Web Worker, Python trước.

## Mục lục nhanh

1. Quy trình từ đầu đến cuối (sơ đồ hành trình, vòng đời một subtopic, vòng lặp hằng ngày)
2. Đánh giá trình độ đầu vào (placement): thuật toán, luật dừng, cách gieo điểm
3. Hệ thống UI: design system, phím tắt, responsive, accessibility, rồi 13 màn hình
4. Ghi nhớ dữ liệu và tiếp tục sau khi thoát / tắt máy
5. Thay đổi cần đưa vào `SPEC.md` (đã áp dụng) và mâu thuẫn đã xử lý

---

## 1. Quy trình từ đầu đến cuối

### 1.1 Sơ đồ hành trình

```
 LẦN ĐẦU MỞ APP (GET /me → onboarding.profile_done = false)
 ┌──────────────┐   ┌──────────────────┐   ┌───────────────────────────────┐
 │ S1 Welcome   │──►│ S1 Hồ sơ ngắn    │──►│ S1 Chọn cách bắt đầu          │
 │ kiểm tra     │   │ vai trò, track,  │   │ [Đánh giá trình độ] (khuyên)  │
 │ Pyodide,     │   │ ngôn ngữ, kinh   │   │ [Bắt đầu từ đầu]              │
 │ xin lưu trữ  │   │ nghiệm tự đánh   │   └───────┬──────────────┬────────┘
 │ bền vững     │   │ giá (4 câu)      │           │              │
 └──────────────┘   └──────────────────┘           ▼              │ skip
                                          ┌──────────────────┐    │ (không gieo điểm,
                                          │ S2 Placement     │    │  placement.status
                                          │ A cổng → B biên  │    │  = skipped)
                                          │ → C mức 3 (tuỳ)  │    │
                                          │ 45 phút mềm/60   │    │
                                          │ cứng, tạm dừng   │    │
                                          │ được             │    │
                                          └────────┬─────────┘    │
                                                   ▼              │
                                          ┌──────────────────┐    │
                                          │ S3 Kết quả       │    │
                                          │ skill map đã gieo│    │
                                          │ mạnh/yếu, điểm   │    │
                                          │ bắt đầu, giờ còn │    │
                                          └────────┬─────────┘    │
                                                   ▼              ▼
                                          ┌─────────────────────────────┐
                                          │ S4 Học tiếp (/)             │
                                          │ mục đầu tiên cần học        │
                                          └──────────────┬──────────────┘
                                                         ▼
 ┌────────────────────────────── VÒNG LẶP HẰNG NGÀY (tự chọn nhịp) ─────────┐
 │ mở app → (banner "Tiếp tục nơi bạn dừng" nếu có) → S4 Học tiếp            │
 │   ├─► S6 Lesson + editor ─► S7 Problem ─► S8 Mastery check / Test out     │
 │   ├─► S9 Review (thẻ đến hạn, làm bao nhiêu tuỳ ý)                        │
 │   └─► S5 Map / S10 Progress / S11 Settings (xem, backup, export)          │
 │ dừng bất cứ lúc nào: đóng tab, tắt máy → mọi thứ đã lưu (mục 4)           │
 └───────────────────────────────────────────────────────────────────────────┘
 MỞ LẠI SAU KHI TẮT: docker tự khởi động → GET /resume → S4 + banner → đúng block
```

Trạng thái `onboarding` (từ `GET /me`) quyết định app mở vào đâu: `profile_done=false` → `/welcome`; `placement=none` sau khi có hồ sơ → hỏi lại ở bước chọn cách bắt đầu; `placement=in_progress` → banner "Đánh giá đang dở"; còn lại → `/`.

### 1.2 Vòng đời một subtopic

```
                 ┌─ placement/Test out: check L2 clean ─────────────────────┐
                 │  (ghi unlocked_at cho chính mục) [SPEC↑ 5.3]             │
 locked ──prereq đều ≥2──► unlocked ──mở lesson──► in_progress             │
   │  ▲ xem trước (editor tắt)  (điểm 0)     (ghi lesson_opened_at)        │
   │  └─ không bao giờ quay lại locked                │                     ▼
   │                          lesson_done + quiz_best ≥ 0.7                │
   │                                                  ▼                    │
   │                                  điểm 1 (thẻ ôn hộp 1, due +1)        │
   │                       practice_ok AND check2_ok  │                    │
   │                                                  ▼                    │
   └──────────────────────────────────────────► điểm 2 ◄──────────────────┘
                                                  │ (mở mục phụ thuộc)
                      level3_ok AND retention_ok  ▼ (≥ D+7, ôn BẰNG BÀI CODE đạt ở hộp ≥3)
                                               điểm 3
 Cờ phụ (không đổi điểm): known_basic (đã biết sơ, từ placement L1) → lesson rút gọn
                          placement_hint = likely_known | likely_gap (chỉ gợi ý hiển thị)
 Trạng thái hiển thị: locked | unlocked | in_progress | done (điểm ≥ max(1, target_intern))
 Lớp ôn tập chạy song song: thẻ hộp 1→5 (D+1,3,7,14,28, rồi 30 ngày), đến hạn → S9
```

### 1.3 Vòng lặp hằng ngày (không có định mức)

1. Mở `localhost:8080`. Nếu có việc đang dở, banner "Tiếp tục nơi bạn dừng" hiện ngay (mục 3.8, S12). Bấm là về đúng màn hình và block.
2. Không có việc dở: `/` (S4) liệt kê **Cần lên điểm 2 để mở mục sau**, **Học tiếp**, **Ôn tập đến hạn**. Quan chọn bất kỳ.
3. Làm việc: lesson, bài, check, ôn. Mỗi sự kiện ghi ngay xuống server (hoặc vào outbox nếu server tắt). Không có nút "Lưu".
4. Dừng lúc nào cũng được. Lần sau mở lại, không có "nợ", không có thông báo trễ; chỉ thẻ ôn tới hạn tiếp tục hiện (không phạt).

---

## 2. Đánh giá trình độ đầu vào (placement)

### 2.1 Nguyên tắc (tái dùng mục 5 của SPEC, không thêm luật điểm mới)

- Placement là **mastery check xếp theo đồ thị tiền đề**, chạy bằng cùng engine `check_sessions` của flow C/D. Nó chỉ ghi `check_results`; điểm luôn do `scoring.py` tính lại từ sự kiện, nên **không thể cao hơn luật cho phép**.
- Qua mức 2 sạch (`clean`: không gợi ý, không xem lời giải, ≤ 1,5 × `minutes`) = `tested_out` → **điểm 2** + mở khoá (flow D). Qua mức 3 sạch (chỉ item `write_code`) = `level3_ok` nhưng **điểm vẫn 2** (cần thêm `retention_ok` từ ôn lặp bằng bài code, không phải thẻ nhớ nhanh). **Placement không bao giờ ghi điểm 3 và không ghi điểm 1** (điểm 1 đòi `lesson_done` + quiz).
- Chỉ biết mức 1 (đọc code, khái niệm) = **không có điểm**, đặt cờ `known_basic` ("đã biết sơ") để rút gọn lesson (không đổi điều kiện `lesson_done`, `quiz_best`).
- Suy luận theo đồ thị (đậu mục khó thì mục tiền đề "có thể đã biết", trượt mục gốc thì mục phụ thuộc "có thể chưa biết") **chỉ là nhãn hiển thị** `placement_hint`, không bao giờ thành điểm.
- Trượt thật (đã nộp bài) tính như trượt check mức 2: `attempt_no`, khoá làm lại 24 giờ, mở lối thoát `check2_ok` của 5.2. Bấm "Không biết" (không nộp) ghi `gave_up=true`: không khoá, không tính là trượt **về điểm và khoá**, nhưng **được tính để dừng sớm** (luật S1, mục 2.4). E2 trượt mở sẵn lối thoát `check2_ok` là chủ đích (vô hại: lối thoát vẫn cần 2 practice AC).

### 2.2 Nguồn item và phạm vi

| Vai trò | Lấy từ | Quy tắc chọn |
|---|---|---|
| **E2** (item vào) | `assessment.json` bank `diag`, `difficulty=2`, `type=write_code` | ngắn nhất theo `minutes`; item cổng (`gate`) ưu tiên. Item `W*` (bank `weekly`) **không dùng** (dành cho quiz tuần M4 và làm item thay thế khi làm lại) |
| **E1** (chẩn đoán) | bank `diag`, mức 1 (`read_code` hoặc `concept`) | dùng khi trượt E2; 5 mục không có mức 1 (`hashing_patterns`, `ll_manipulation`, `stack_problems`, `parsing_strings`, `sorting_applications`) thì dừng ở "cần học lesson" |
| **E3** (mức 3) | bank `diag`, mức 3, `write_code` | chỉ ở Phase C, chỉ khi E2 đã qua; 15/40 mục có (16 mục có mức 3, trừ `big_o` chỉ có `concept` Q043 tự chấm) |

- Mục **placeable** = có E2 `write_code` đã chuyển thành check problem `published`. Item mức 2 dạng `concept`/`read_code` **không bao giờ là E2** (đó là điểm tự chấm, không đủ làm bằng chứng điểm 2; khớp 3.4 của SPEC). Hiện có 31/40 mục placeable; 9 mục thiếu `write_code` mức 2 (SPEC 3.4) trở thành placeable ngay khi item bổ sung của chúng `published` (5 ở M2a, 3 ở M2b, `interview_method` ở M3). Cuối M2a có 36 mục placeable, đủ cho cả 7 cổng. Mục chưa placeable luôn ở trạng thái `not_assessed`.
- Phạm vi: `scope=all` (lần đầu) hoặc `scope=module:<module_id>` (làm lại, mục 2.8). Mục đã có điểm ≥ 2 bị loại (không có gì để thêm); mục đang trong khoá 24 giờ `check_retry_locked` bị loại và ghi "chờ đến <giờ>".
- 7 **cổng** (từ `clusters` của `assessment.json`, thứ tự chuỗi độ khó): `Q012 strings` (C1, 6 phút) → `Q023 dict` (C2, 6) → `Q258 hash_tables` (C3, 6) → `Q070 two_pointers` (C4, 6) → `Q079 ll_basics` (C5, 6) → `Q095 binary_search_basics` (C6, 6) → `Q105 tree_basics` (C7, 6). Cụm `cluster(n)` của mục MVP lấy từ `clusters[].nodes`.
- Chi phí `cost(n)` = `minutes` của E2 (mục bổ sung chưa có số liệu: 8 phút). Tổng 40 E2 ≈ 354 phút nên **không thể đo hết**; thiết kế chấp nhận chỉ đo 5-12 mục rồi suy luận nhãn (so với 116-180 phút của "Day 0" gốc).

### 2.3 Đồng hồ và ngân sách

- Mỗi lần ngồi làm (một *sitting*) có **ngân sách mềm 45 phút** và **cứng 60 phút** thời gian hoạt động (`active_ms`: tab hiện, có thao tác trong 2 phút gần nhất; đóng app thì **đồng hồ dừng**). Đồng hồ item `elapsed_ms` cũng chỉ tính thời gian hoạt động của chính item đó.
- Không bắt đầu item mới nếu `active_ms + cost(item) > ngân sách` (mềm cho Phase B, cứng cho Phase A/C). Item đang làm không bị cắt bởi ngân sách tổng, chỉ bởi time-box riêng.
- Time-box item: đếm ngược `minutes`; qua 0 sang vùng "quá giờ" (màu cảnh báo) đến 1,5 × `minutes`, hết đó **tự nộp** bản hiện tại. Đậu trong ≤ 1,5 × là `clean` (placement không có gợi ý và không có xem lời giải nên chỉ còn điều kiện thời gian).
- Muốn đo thêm sau khi hết ngân sách: nút "Đánh giá thêm 30 phút" ở màn kết quả mở sitting mới (`kind=continue`) tiếp trên cùng trạng thái, không làm lại từ đầu.

### 2.4 Thuật toán (quy tắc đánh số, thực thi trong `services/placement.py`)

Trạng thái mỗi mục trong phiên: `unknown` · `measured` (có check_results) · `likely_known` · `likely_gap` · `not_assessed`. Bắt đầu: mọi mục placeable là `unknown`.

**Phase A: bậc thang cổng (≤ 7 item, tối đa 42 phút time-box)**

- **A1** Cổng vào theo `experience` (chỉ là *điểm xuất phát*, không là điểm số): `none` → C1, `some` → C2, `solid` → C3. Với `experience=none` placement **chỉ chạy C1 → C2** (không Phase B/C): đậu C1 thì hỏi C2, dừng ở lần trượt/không biết đầu tiên (~6-9 phút), và bước 3 của S1 đổi nút khuyên dùng thành "Bắt đầu từ đầu" (placement vẫn chọn được).
- **A2** Đi lên: đậu cổng k thì hỏi cổng k+1 (bỏ qua cổng đã `measured`/`likely_gap`). Dừng Phase A khi: hết 7 cổng; hoặc có một cổng trượt **và** đã thử cổng liền dưới nó (nếu chưa đo thì hỏi đúng một cổng liền dưới); hoặc 2 cổng trượt liên tiếp. Trong luật này "trượt" nghĩa là `failed OR gave_up`. **Nếu một cổng trượt/không biết mà cổng liền dưới nó đã trượt/không biết hoặc không tồn tại (C1) thì dừng ngay và bỏ qua Phase B.**
- **A3** Mỗi cổng là một node: chạy thang bậc của flow C (E2; đậu → xong, trượt → E1 nếu có).
- **A4** Cập nhật nhãn sau mỗi node (bảng suy luận bên dưới).

**Phase B: biên tiền đề (đến khi chạm ngân sách mềm)**

- **B1** Ứng viên = mục placeable ở trạng thái `unknown` hoặc `likely_known`.
- **B2** Chọn ứng viên có **nhiều mục phụ thuộc chưa xác định nhất** (đếm hậu duệ `unknown`/`likely_known` trong đồ thị `prereqs`), hoà thì theo thứ tự plan. Ý nghĩa: ưu tiên mục chặn nhiều mục khác (vd `arrays`, `memory_model`) vì đó là nơi kết quả mở khoá được nhiều nhất.
- **B3** Chạy flow C cho mục đó (E2, rồi E1 nếu trượt). Lặp.

**Phase C: mức 3 (tuỳ chọn, chỉ khi còn ≥ 10 phút ngân sách mềm và đã đậu ≥ 3 mục)**

- **C1** App hỏi "Thử mức 3 cho mục đã đậu? (tối đa 5 mục, mỗi mục ~10 phút)". Đồng ý thì lấy E3 của mục đã đậu E2, mục `hot` trước (`readiness_table[].hot` trong `assessment.json`), rồi theo plan.
- **C2** Đậu E3 sạch → `level3_ok` (điểm vẫn 2). Trượt E3 → không đổi gì ngoài `check_results` (khoá làm lại E3 24 giờ).

**Bảng suy luận nhãn (chỉ ghi `user_subtopic.placement_hint`)**

| Sự kiện | Mục bị gắn nhãn | Nhãn |
|---|---|---|
| Node X đậu E2 | mọi tiền đề (đệ quy) của X chưa `measured`; mục cùng cụm đứng trước X theo thứ tự plan | `likely_known` |
| Node X trượt E2 | mọi hậu duệ của X chưa `measured` (bị **bỏ qua**, không hỏi); mục cùng cụm đứng sau X theo thứ tự plan | `likely_gap` |
| Mục có bằng chứng thật về sau (check, lesson_done, AC) | chính mục đó | xoá nhãn |

**Luật dừng (kết thúc sitting, tính theo thứ tự ưu tiên)**

- **S1** 2 node trượt E2 liên tiếp, hoặc 3 node trượt trong cùng sitting; ở đây mỗi lần "Không biết" cũng tính như một lần trượt (`failed OR gave_up`, chỉ để dừng, không để khoá 24 giờ): dừng sớm, thông báo "Chưa cần đo thêm; bắt đầu từ nền tảng sẽ hiệu quả hơn" (tránh làm nản).
- **S2** Hết ứng viên, hoặc item kế tiếp vượt ngân sách (mềm với B, cứng với A/C).
- **S3** Người dùng bấm "Kết thúc sớm" hoặc "Dừng và lưu" (xem mục 2.6 về tiếp tục).
- Khi dừng: tạo kết quả (`GET /placement/{id}/result`); mục chưa đo là `not_assessed`.

### 2.5 Cách gieo điểm (đầu ra ghi xuống DB)

| Kết quả node | Ghi | Điểm sau `scoring.py` | Hệ quả |
|---|---|---|---|
| E2 đậu sạch | `check_results(level=2, passed, clean, context=placement)` | **2** (`tested_out`) | ghi `unlocked_at` cho chính mục và mở khoá hậu duệ đủ điều kiện; tạo thẻ ôn hộp 1 (xem dưới) |
| + E3 đậu sạch | `check_results(level=3, passed, clean)` | vẫn 2 | `level3_ok`; 3 cần `retention_ok` |
| E2 trượt (có nộp) rồi E1 đậu | fail E2 (`attempt_no`, khoá 24 giờ) + pass E1 | 0 | `known_basic=true`: lesson rút gọn |
| E2 trượt rồi E1 trượt, hoặc mục không có E1 | fail E2 (+ fail E1) | 0 | "cần học"; nếu mục chỉ có 1 item mức 2, lối thoát `check2_ok` của 5.2 đã mở |
| "Không biết" | `check_results(gave_up=true, passed=false)` | 0 | không khoá, không tính trượt |
| Không được hỏi | không ghi gì | 0 | chỉ có `placement_hint` |

- **Thẻ ôn từ placement**: theo 5.4 quy tắc 1, thẻ tạo ngày đạt, `due = ngày đạt + 1`. Để tránh dồn 20+ thẻ vào một ngày sau khi đo mạnh, thẻ do placement tạo được **rải**: `due = ngày đạt + 1 + ⌊k / 8⌋` với k là thứ tự (từ 0) theo plan trong phiên **[SPEC↑ 5.4#1]**. Đây không phải trần thẻ: mỗi thẻ vẫn có hạn và không bị phạt.
- Chống nhầm: không có bước nào của placement cộng `quiz_best`, `lesson_done` hay `review_log`; vì vậy test tự động chỉ cần khẳng định `score_after == scoring(events)` và `score ≤ 2` cho mọi mục sau placement.

### 2.6 Tạm dừng, tiếp tục, bỏ qua

- **Tạm dừng** (nút hoặc đóng tab, tắt máy): session giữ `phase`, trạng thái mục, item đang làm (`check_sessions.current_item_id`), `active_ms`, nháp code (mục 4). Mở lại: banner "Đánh giá đang dở: 3/7 cổng · còn ~28 phút ngân sách" → vào đúng item, đồng hồ item tiếp từ `elapsed_ms` đã lưu (sai số ≤ 15 giây do heartbeat).
- **Bỏ dở**: không hoạt động ≥ 7 ngày thì session thành `stale`; lần mở sau hỏi "Tiếp tục (giữ kết quả đã đo) / Chốt kết quả hiện có / Làm lại từ đầu". Mục đã đo vẫn là bằng chứng thật (đã nằm trong `check_results`). Item đang làm dở khi quá 24 giờ không hoạt động bị đánh `expired`: không ghi trượt, đưa về cuối hàng.
- **Bắt đầu từ đầu** (bỏ qua): `placement_sessions.status=skipped`, **không gieo gì**, điểm xuất phát là mục đầu theo plan. Hồ sơ vẫn lưu. Làm placement sau này từ Settings hoặc Map (2.8).

### 2.7 Ước lượng thời gian (mô phỏng trên đồ thị 40 mục thật, mọi item dùng đủ time-box nên là cận trên)

| Hồ sơ giả lập | Số item | Thời gian (time-box) | Kết quả |
|---|---|---|---|
| Yếu / người mới (trượt hoặc "Không biết" ngay cổng đầu; `experience=none`) | 1 (+1 item mức 1) | ~6-9 phút | dừng ngay, không Phase B; ~28 mục `likely_gap`, bắt đầu từ mục đầu plan |
| Yếu nhưng khai `some`/`solid` (trượt C2/C3 rồi cổng liền dưới) | 2 (+ item mức 1) | ~12-18 phút | dừng theo luật Phase A, không Phase B |
| Trung bình (đậu 20 mục đầu theo plan) | 5-6 | 40-47 phút | 2-3 mục điểm 2, 9-14 mục `likely_known`, 2-3 trượt |
| Mạnh (đậu tất cả) | 7 | 42-44 phút | 7 mục điểm 2 (các cổng), 14-21 mục `likely_known`; tiếp tục "đánh giá thêm" nếu muốn đo nốt |

(Hồ sơ "yếu" của v0.1 mất ~31 phút cho 3 câu trượt; luật dừng v0.2 chặn việc đó.) Thực tế người làm xong item sớm hơn time-box nên 30-45 phút là điển hình. Trần tuyệt đối của một sitting: 60 phút hoạt động.

### 2.8 Làm lại và đo thêm

- **Đo thêm** (`kind=continue`): từ màn kết quả, thêm 30 phút ngân sách, cùng trạng thái, cùng thuật toán.
- **Làm lại theo module** (`kind=retake`, `scope=module:<id>`): từ Map (menu của module) hoặc Settings. Chỉ các mục chưa ≥ 2 của module và tiền đề chưa ≥ 2; Phase A bỏ qua (không có cổng), chạy Phase B trên phạm vi đó. Mục có lần trượt E2 chưa quá 24 giờ bị loại và ghi "chờ đến <giờ>". Item của lần làm lại: nếu mục có item mức 2 thứ hai (bank `weekly`, vd `W185` cho `strings`), dùng item đó; không thì dùng lại E2 (sau 24 giờ, luật 5.2).
- Luôn khả dụng "Test out" từng mục (flow D) bất kể placement.

### 2.9 Vì sao tách: T2.9a cuối M2a, T2.9b ở M2b

- **Phụ thuộc đã đủ ở M2a**: engine mastery check và `convert_checks.py` chuyển đủ 61 check problem (T2.2), unlock (T2.3), `GET /next` (T2.5). Cả 7 cổng đều là item có sẵn trong `assessment.json`, nên **Phase A chạy được ngay cuối M2a** (T2.9a: Phase A + luật dừng + gieo `tested_out` + S3 rút gọn). Quan muốn bắt đầu bằng đánh giá, nên không để chờ đến M2b.
- **Điểm bắt đầu chỉ chọn trong lesson đã `published`** (`result.start`). Cuối M2a mới có 16 lesson (ngày 1-3); nếu hồ sơ mạnh vượt hết phần đó, S3 hiện "Nội dung các mục tiếp theo đang soạn; dùng Test out cho các mục đã đo `likely_known`" thay vì một điểm bắt đầu.
- **T2.9b ở M2b**: Phase B/C, nhãn suy luận, nhóm "Có thể đã biết"/`sweep`, rải thẻ, đo thêm, làm lại theo module, S3 đầy đủ; thêm khi M2b có 28/28 lesson tuần 1 và 8/9 item bổ sung.
- **Không để sang M3**: M3 là đóng gói/đánh bóng.
- **Cầu nối chỉ còn ở M1** (không có onboarding ở M1); từ M2a nút "Đánh giá trình độ" bật khi T2.9a xong. Placement đến sau khi Quan đã học một phần thì các mục điểm ≥ 2 tự loại khỏi phạm vi, mục điểm 0-1 vào phạm vi.

### 2.10 Pha khái niệm (track System Design / AI-engineer)

Chạy sau bậc thang cổng code (mục 2.4) cho track `swe` hoặc `ai`; luật điểm ở SPEC 5.6 mục 7. Phiên chuyển `phase`: `code` → `concept_offer` → `concept` → kết thúc.

- **Màn tự báo module** (`phase=concept_offer`, `view.concept_offer`, `awaiting_modules`): tiêu đề "Bạn đã biết module nào?", danh sách checkbox theo module của track (chỉ module đã có item), tối đa 4 ô được chọn, nút chính "Đo các module đã chọn" (`POST /placement/{id}/modules`) và nút phụ "Bỏ qua phần này" (gửi danh sách rỗng, kết thúc theo lý do dừng của pha code). Không có item nào đang mở nên đồng hồ item dừng; ngân sách còn lại vẫn hiển thị.
- **Bước concept**: mỗi module một cổng `K1..K4`, hiển thị như cổng code nhưng đầu bước ghi tên module. Rung đầu là `mcq` mức 1 (1 phút), đậu thì tới `mcq` mức 2 (2 phút); trượt hoặc "Không biết" thì sang module kế, không hỏi mức 2. Không có "thử cổng dưới". Hết module là màn kết quả (S3) với thông báo "Đã đo xong các module khái niệm bạn chọn."
- **Kết quả**: mỗi hub hiện điểm (1 hoặc 2) cùng nhãn `likely_known`/`likely_gap` của các mục quanh nó (chỉ là gợi ý hiển thị).

---

## 3. Hệ thống UI

### 3.1 Design system

**Layout và lưới.** Thanh điều hướng trên cùng cao 56 px, không có sidebar (nhường chiều ngang cho split view). Trang thường (Map, Progress, Settings, Học tiếp) dùng lưới 12 cột, `max-width: 1200px`, gutter 24 px, lề 16 px dưới 768 px. Split view dùng toàn chiều ngang (`react-resizable-panels`, mặc định 45/55, giới hạn mỗi bên ≥ 360 px). Thang khoảng cách bội 4 px: `4 8 12 16 24 32 48`. Bo góc: `6` (nút, input), `10` (card, modal). Độ cao (shadow) chỉ cho modal và toast; card dùng viền 1 px.

**Màu (CSS variables ở `:root`, ghi đè trong `[data-theme="dark"]`; mặc định theo `prefers-color-scheme`, đổi tay ở Settings, lưu `settings.ui_prefs.theme`).**

| Token | Light | Dark | Dùng cho |
|---|---|---|---|
| `--bg` / `--surface` | `#FAFAF8` / `#FFFFFF` | `#0F1214` / `#171B1F` | nền trang / card, panel |
| `--border` | `#E4E4E0` | `#2A3037` | viền |
| `--text` / `--muted` | `#1B1F23` / `#5B6470` | `#E6E8EB` / `#9AA4AF` | chữ chính / phụ |
| `--primary` / `--on-primary` | `#2457D6` / `#FFFFFF` | `#7AA2FF` / `#0B1020` | nút chính, link, focus |
| `--success` · `--warn` · `--danger` | `#1F7A4D` · `#9A6200` · `#B42318` | `#4CC38A` · `#F0B84A` · `#FF7B72` | AC/đạt · cảnh báo/quá giờ · WA/RE/lỗi |
| `--score-0` (nền / chữ) | `#F1F2F4` / `#5B6470` | `#252A30` / `#9AA4AF` | điểm 0 |
| `--score-1` | `#FFF1CC` / `#8A5A00` | `#3A2E0B` / `#F5C451` | điểm 1 |
| `--score-2` | `#D6F3EC` / `#0F6B5C` | `#0F3A33` / `#5FD3BC` | điểm 2 |
| `--score-3` | `#E3E4FF` / `#3B3FB8` | `#25285C` / `#A5A9FF` | điểm 3 |
| `--hint-known` · `--hint-gap` | viền nét đứt `--score-2` · viền nét đứt `--muted` | như bên | nhãn `likely_known` · `likely_gap` |

Yêu cầu: tương phản chữ/nền ≥ 4,5:1 (axe-core trong CI kiểm tra mọi route ở cả hai theme); màu không bao giờ là kênh thông tin duy nhất (điểm có số, trạng thái có icon và chữ).

**Chữ.** UI: `Inter` (self-host woff2, có subset `latin`, `latin-ext` và `vietnamese`; fallback `system-ui`). Code và editor: `JetBrains Mono` (cùng cách self-host; fallback `Cascadia Mono`, `Consolas`, `monospace`), ligature tắt. Kích thước: nền 16 px, lesson 17 px/1,7, editor mặc định 14 px (13-20 chỉnh được), tiêu đề 28/22/18. Phải qua smoke test hiển thị chuỗi `Tiếng Việt: ặ ở ữ ế ộ` ở cả UI lẫn editor (đo dấu không bị cắt, không rơi sang font dự phòng). CSP bổ sung **[SPEC↑ 6.2]**: `font-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:` (CodeMirror 6 chèn thẻ `<style>`).

### 3.2 Điều hướng

Thanh trên: logo · `Học tiếp` · `Map` · `Bài tập` · `Ôn tập (N)` · `Tiến độ` · (đẩy phải) chip đồng bộ · công tắc EN/VI của đề bài · `⚙` Settings. `N` = số thẻ đến hạn (`/next.due_count`). Chip đồng bộ có 4 trạng thái: `✓ Đã lưu` · `⟳ Đang lưu` · `⚠ 3 thay đổi chưa đồng bộ` (server không phản hồi, bấm để xem) · `⛔ Lỗi`. Breadcrumb ở split view: `◄ Map  ›  hash_tables`. Dưới 768 px nav thành thanh tab dưới đáy 5 mục.

### 3.3 Component

| Component | Quy ước |
|---|---|
| **Button** | `primary` (một nút mỗi màn hình/khối), `secondary` (viền), `ghost`, `danger` (cần confirm). Cao 36 px (32 px trong editor), có trạng thái `loading` (spinner, chặn bấm đôi), `disabled` luôn kèm tooltip lý do |
| **Card** | viền 1 px, padding 16/24, tiêu đề + hành động ở hàng đầu |
| **ScoreBadge 0-3** | hình tròn 24 px, số ở giữa, màu `--score-N`; `aria-label="Điểm 2 trên 3"`. Biến thể `target`: vòng đích mảnh quanh badge khi điểm < target. Biến thể `hint`: viền nét đứt + dấu `?` (placement_hint, chưa có điểm) |
| **LockState** | icon khoá + chữ lý do ("cần hash_tables ≥ 2"); chip mờ 60%; luôn có hai nút phụ: `Xem trước`, `Test out` |
| **Progress bar** | 6 px, track `--border`, fill `--primary`; thanh thời gian placement đổi sang `--warn` khi vượt 80% ngân sách mềm |
| **Toast** | góc dưới phải, tự đóng 4 giây (lỗi: 8 giây, có nút `Thử lại`), tối đa 3, `role="status"` (lỗi: `role="alert"`) |
| **Modal** | khoá cuộn nền, đóng bằng `Esc`, focus trap, nút nguy hiểm không phải focus mặc định; confirm "gõ từ khoá" cho thao tác huỷ dữ liệu |
| **Banner** | dải ngang dưới nav, có `✕` ẩn trong phiên; ba loại: `resume` (xanh), `backlog` (vàng, SPEC 5.4#7), `offline` (đỏ nhạt, không ẩn được) |
| **CodeEditorPanel** | CodeMirror 6, Python; số dòng, auto-indent 4 space, tab = 4 space, bracket matching, tìm kiếm `Ctrl+F`; thanh dưới: `▶ Run`, `✔ Submit`, `💡 Gợi ý n/3`, `⟲ Reset về starter` (confirm), `⏱ elapsed`, chip lưu nháp `Đã lưu 14:02:11` |
| **TestResultPanel** | tab `Kết quả / stdout / stderr`; mỗi test một dòng `Sample 3 ✘`; mở rộng dòng sai thấy `input / expected / got`; verdict AC/WA/TLE/RE/CE là chip màu; vùng `aria-live="polite"` đọc "5 trên 5 test qua" |
| **Skeleton** | khung xám nhấp nháy cho danh sách/lesson, không dùng spinner toàn trang |
| **EmptyState** | icon + 1 câu giải thích + 1 hành động |

### 3.4 Phím tắt (Mac: `Ctrl` → `⌘`)

| Phím | Hành động | Ghi chú |
|---|---|---|
| `Ctrl+Enter` | Run (sample test) | ghi đè `insertBlankLine` của CodeMirror; hoạt động cả khi focus ở lesson nếu có bài đang nạp |
| `Ctrl+Shift+Enter` | Submit | mở hidden test; không xác nhận (Submit không phạt) |
| `Ctrl+S` | Lưu nháp ngay | chặn hộp thoại lưu của trình duyệt; toast "Đã lưu" |
| `Alt+→` / `Alt+←` | block kế / trước trong lesson | cuộn tới block, đặt focus; `Alt+→` trên quiz chưa trả lời không bị chặn |
| `Ctrl+'` | chuyển focus Bài học ↔ Editor | |
| `Ctrl+Shift+L` | đổi đề bài EN ↔ VI | |
| `Esc` rồi `Tab` | thoát bẫy Tab của editor | accessibility |
| `g` rồi `n` · `m` · `r` · `p` | tới Học tiếp · Map · Ôn tập · Tiến độ | chỉ khi focus không ở ô nhập |
| `?` | bảng phím tắt | |

### 3.5 Responsive

| Chiều rộng | Layout | Khả năng |
|---|---|---|
| **≥ 1280 px** (thiết kế quanh 1366) | split view 45/55, kéo được | đầy đủ |
| 768-1279 | hai tab `Bài học / Code`, tab nhớ vị trí cuộn | đầy đủ nhưng khuyến nghị máy ≥ 1366 (hiện gợi ý một lần) **[SPEC↑ 2.2: ngưỡng cũ 1024 → 1280]** |
| < 768 (tablet dọc, điện thoại) | **chỉ đọc lesson, làm quiz/predict, làm review thẻ nhớ nhanh**; ẩn editor, Submit, mastery check | màn bài/check hiện "Mở trên máy tính để viết code" kèm nút `Gửi link` (copy URL). Thẻ ôn hộp 3-5 dùng item nhớ nhanh (`item_kind=recall`): đạt thì lên hộp nhưng **không tính cho `retention_ok`** (cần bài code); không rớt hạn |

Máy khác truy cập qua mạng LAN cần đặt `BIND=0.0.0.0` trong `.env` (mặc định chỉ `127.0.0.1`); trang HTTP qua IP không phải secure context nên không có service worker (vẫn có IndexedDB). **Chế độ < 768 px chỉ dùng được khi `BIND=0.0.0.0`** (mặc định điện thoại không vào được app), nên không ưu tiên trong MVP; chỉ cần CSS không vỡ.

### 3.6 Accessibility

Điều hướng toàn bộ bằng bàn phím, focus ring 2 px `--primary` không bao giờ bị `outline: none`; skip-link "Tới nội dung"; heading phân cấp; mọi icon-button có `aria-label`; kết quả test và toast qua `aria-live`; tôn trọng `prefers-reduced-motion` (không animation) và `prefers-color-scheme`; zoom chữ 200% không vỡ layout; `lang="vi"` toàn trang và `lang="en"` cho `statement_en_md`; timer có thể ẩn (vẫn ghi) cho người bị căng thẳng vì đếm giờ.

### 3.7 Mẫu trạng thái dùng chung cho mọi màn hình

| Trạng thái | Cách hiển thị |
|---|---|
| **Loading** | Skeleton đúng khung nội dung; không chặn nav |
| **Empty** | EmptyState có hành động ("Chưa có thẻ nào đến hạn. [Học tiếp]") |
| **Error API** (4xx/5xx) | khối lỗi trong vùng nội dung: tiêu đề, `error.message`, `[Thử lại]`, mã lỗi nhỏ; không mất dữ liệu đang nhập |
| **Offline / server down** | banner đỏ nhạt "Mất kết nối server. Bạn vẫn đọc, gõ code và Run được; thay đổi được giữ trên máy và gửi lại khi server chạy lại." Hành động cần server (Submit, mở check, xin gợi ý/lời giải) disable kèm tooltip "Cần server" |
| **Locked** | LockState + lý do + `Xem trước`/`Test out` |
| **First-time** | hướng dẫn một lần (tooltip 3 bước tại lần đầu vào S6/S7), bật lại ở Settings |

### 3.8 Các màn hình

Quy ước mỗi màn: **Mục đích · Vào từ · Wireframe · Component → nguồn dữ liệu · Trạng thái · Hành động và thứ được ghi**. Mọi POST gửi header `Idempotency-Key` (mục 4.4). "Ghi" luôn là ghi server; khi server tắt, ghi vào outbox (mục 4.5).

#### S1. Welcome và hồ sơ (`/welcome`, `/welcome/profile`, `/welcome/start`)

Mục đích: lần đầu mở app, thu hồ sơ tối thiểu rồi chọn cách bắt đầu. Vào từ: tự chuyển khi `GET /me → onboarding.profile_done=false`. Nav đầy đủ vẫn hiện; bấm link điều hướng sẽ về `/` nhưng Home tự redirect lại /welcome tới khi xong hồ sơ, nên người dùng vẫn ở trong onboarding.

```
┌───────────────────────── 1 ─ 2 ─ 3 ─────────────────────────┐
│  Chào Quan. Prep App giúp bạn học, luyện và ôn phỏng vấn.   │
│  ✓ Tự chọn nhịp, không có định mức hay thông báo trễ        │
│  ✓ Điểm 0-3 chỉ lên khi có bài làm được đo, không tự chấm   │
│  ✓ Dữ liệu nằm trên máy bạn (data/app.db), có backup tự động│
│  Chuẩn bị trình chạy code ......... [██████░░░░] 62% (12 MB)│
│  Lưu trữ bền vững (không bị trình duyệt xoá) ... ✓ đã cấp   │
│                                              [Tiếp ►]       │
├──────────────────────── Bước 2: hồ sơ ─────────────────────┤
│ Mục tiêu    (•) Intern ( ) Fresher ( ) Junior ( ) Senior    │
│ Track       (•) SWE      ( ) AI engineer  ⓘ MVP chỉ có nền  │
│                              tảng Python + DSA dùng chung   │
│ Ngôn ngữ    (•) Python   ( ) Java (sắp có, M5)  [tắt]       │
│ Kinh nghiệm ( ) Mới bắt đầu  ( ) Biết ít (đã học cú pháp)   │
│             ( ) Khá (đã giải bài LeetCode easy)             │
│ Tên hiển thị [Quan____]  Múi giờ [Asia/Ho_Chi_Minh ▾]       │
│                                    [◄ Quay lại] [Tiếp ►]    │
├──────────────────────── Bước 3: cách bắt đầu ──────────────┤
│ ┌ Đánh giá trình độ (khuyên dùng) ┐ ┌ Bắt đầu từ đầu ────┐ │
│ │ ~30-45 phút, dừng/tiếp tục được │ │ Vào mục đầu của    │ │
│ │ bỏ qua phần bạn đã biết         │ │ plan, đi theo thứ  │ │
│ │ [Bắt đầu đánh giá]              │ │ tự. [Bắt đầu học]  │ │
│ └─────────────────────────────────┘ └────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

| Component | Nguồn / ghi |
|---|---|
| Tiến trình Pyodide | client: tải `public/pyodide/` (cache HTTP bất biến từ M1; service worker từ M3); không ghi server |
| Xin lưu trữ bền vững | `navigator.storage.persist()`; kết quả hiện ✓ hoặc cảnh báo "Trình duyệt có thể xoá dữ liệu cục bộ; dữ liệu chính vẫn an toàn trong server" |
| Hồ sơ | ghi `PUT /profile` → `settings.target_role` (`intern`\|`fresher`\|`junior`\|`senior`), `track` (`swe`\|`ai`), `language`, `experience` (`none`\|`some`\|`solid`), `display_name`, `tz`, `onboarded_at` |
| Lựa chọn bước 3 | "Đánh giá" → `POST /placement` (kind=initial) rồi `/placement/:id`; "Bắt đầu từ đầu" → `POST /placement/skip` (ghi `placement_sessions.status=skipped`) rồi `/` |

Trạng thái: **loading** (kiểm tra Pyodide); **lỗi tải Pyodide** (nút `Thử lại`, vẫn cho qua bước và học phần không cần code); **server down** (màn "Server chưa chạy. Chạy `docker compose up`" với nút `Kiểm tra lại`); nút Đánh giá bật khi T2.9a xong; `experience=none` thì nút khuyên dùng ở bước 3 là "Bắt đầu từ đầu". `target_role`/`track` chỉ đổi *vòng đích hiển thị* (`targets[track][role]`) và bảng "mục yếu"; `done`, mở khoá và thứ tự học **không đổi** (vẫn `target_intern`) để giữ luật SPEC 5.3 **[SPEC↑ 6.3 `subtopics.targets`]**. Thoát giữa chừng: hồ sơ lưu từng bước, mở lại vào đúng bước.

#### S2. Placement (`/placement/:sessionId`)

Mục đích: làm bài đánh giá thích nghi (mục 2). Vào từ: S1, banner S12, Học tiếp S4 (nút "Đánh giá lại năng lực"), Settings, Map (làm lại module). Layout tập trung nhưng **vẫn hiện nav đầy đủ** trên cùng (về Trang chủ/Map/Ôn tập/Cài đặt được từ mọi trang), kèm thanh trạng thái.

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Đánh giá đầu vào · Giai đoạn A: Cổng 3/7   Đã dùng 14:20 / 45:00 [██▌░░░] │
│ ● py.core.strings ● dict ◐ hash_tables ○ ○ ○ ○     [⏸ Tạm dừng] [Kết thúc sớm]│
├────────────────────────────────┬─────────────────────────────────────────┤
│ Câu: dsa.arrays_strings.       │ ┌ editor (starter) ───────────────────┐ │
│ hash_tables · mức 2 · Q258     │ │ def first_unique(s): ...            │ │
│ ⏱ 03:41 còn lại (6 phút)       │ └─────────────────────────────────────┘ │
│ Đề: ... (không có gợi ý, không │ [▶ Run] [✔ Nộp bài]    [Không biết]     │
│ có lời giải trong lúc làm)     │ ┌ Kết quả ────────────────────────────┐ │
│                                │ │ Sample 1 ✔  Sample 2 ✔              │ │
│                                │ └─────────────────────────────────────┘ │
└────────────────────────────────┴─────────────────────────────────────────┘
```

**Ba dạng item** (cùng khung, vùng phải đổi theo `type`):

| Dạng | Vùng làm bài | Nút | Chấm |
|---|---|---|---|
| `write_code` (E2, E3) | editor + panel kết quả, split như S7, `starter` từ check problem | `Run` (sample), `Nộp bài` (hidden, nhiều lần trong time-box), `Không biết` | AC ở Nộp = đậu; hết time-box (1,5 × `minutes`) tự nộp bản cuối |
| `read_code` (E1) | code chỉ đọc + ô nhập output (nhiều dòng) | `Kiểm tra`, `Không biết` | so `expected_output` sau chuẩn hoá khoảng trắng cuối dòng |
| `concept` (E1) | câu hỏi + ô "tự giải thích" | `Xem đáp án` rồi `Đủ ý` / `Chưa đủ` | tự chấm (chỉ chẩn đoán mức 1, không bao giờ làm bằng chứng điểm) |

| Component | Nguồn dữ liệu |
|---|---|
| Thanh phase + chip mục | `GET /placement/:id` → `phase`, `nodes[{id,status}]`, `active_ms`, `budget_soft_ms`, `budget_hard_ms` |
| Item hiện tại | `check_sessions.current_item` (id, `type`, `prompt`, `starter`, `minutes`, `elapsed_ms`) |
| Đồng hồ item | client đếm, gửi `elapsed_ms` tuyệt đối trong heartbeat 15 giây |
| Hidden test | cùng đường `start-submit` token của SPEC 6.4 (item kind `check`) |

Trạng thái: **loading item** (skeleton); **quá giờ** (đồng hồ vàng, vùng 1,0-1,5 ×); **tự nộp**; **server down giữa chừng** (editor + Run vẫn chạy, `Nộp bài` disabled "Cần server", draft ở IDB, đồng hồ vẫn đếm; khi server lên, tiếp tục); **chạm ngân sách mềm** (modal "Đã dùng 45 phút. Xem kết quả hay làm thêm item này?"); **dừng sớm S1** (modal giải thích). Hành động ghi: mỗi item xong → `POST /placement/:id/answer` ghi `check_results` (kèm `session_id`, `context=placement`, `attempt_no`, `gave_up`), cập nhật `placement_sessions.state`; `POST /placement/:id/heartbeat` ghi `active_ms`, `elapsed_ms`; `⏸ Tạm dừng` ghi `status` giữ `in_progress` và về `/` (banner S12 vẫn mời tiếp tục); `Kết thúc sớm` → `POST /placement/:id/finish`.

#### S3. Kết quả placement (`/placement/:sessionId/result`)

Mục đích: cho Quan thấy mình đứng đâu và việc kế tiếp. Vào từ: tự động khi `finish`; `Settings → Lịch sử đánh giá`.

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Kết quả đánh giá · 41 phút · đo 7 mục                                    │
│ [Đã đo: 7] [Có thể đã biết: 15] [Cần học: 3] [Chưa đo: 15]               │
│ Skill map (chip = điểm đã gieo; nét đứt = suy luận, chưa có điểm)        │
│  py.core      [strings 2][dict 2][operators ?][loops ?] ...              │
│  dsa.arrays   [arrays ?][hash_tables 2][hashing_patterns 0] ...          │
│ Điểm mạnh: dict (2) · hash_tables (2, mức 3 ✔)   Còn yếu: hashing_patterns│
│ ┌ Bắt đầu từ đây ──────────────────────────────────────────────────┐    │
│ │ hashing_patterns · ước ~3 giờ · [Bắt đầu học]                    │    │
│ └──────────────────────────────────────────────────────────────────┘    │
│ Có thể đã biết: Test out nhanh 15 mục (~2 giờ)   [Test out theo thứ tự] │
│ Khối lượng còn lại ~29 giờ học (từ 43 giờ của plan; không phải hạn chót)  │
│ [Đo thêm 30 phút] [Xem skill map đầy đủ] [Vào Học tiếp]                  │
└──────────────────────────────────────────────────────────────────────────┘
```

| Component | Nguồn dữ liệu |
|---|---|
| 4 ô số | `result.counts{measured, likely_known, need_learn, not_assessed}` |
| Skill map thu nhỏ | `result.nodes[{id, score, level3_ok, known_basic, hint, state}]`; chip `?` = không có điểm |
| Mạnh/yếu | mạnh: `score ≥ 2` theo thứ tự plan (tối đa 5); yếu: `state=failed` hoặc `known_basic=false` đã trượt |
| Điểm bắt đầu | `result.start{subtopic_id, est_hours}`: mục đầu tiên theo `plan_order` có lesson `published`, `score < max(1, target_intern)`, không `likely_known` |
| Test out nhanh | `result.sweep[{id, minutes}]` = mục `likely_known` theo plan, mỗi mục chạy flow D (E2 đã có) |
| Giờ còn lại | `result.est_hours_remaining` (công thức dưới) |

Giờ còn lại = Σ `plan_hours(n) × f(n)`, `plan_hours` lấy từ `plan.json`; `f = 0` nếu `score ≥ max(1, target_intern)`; `0,3` nếu score 2 nhưng target 3; `0,4` nếu `likely_known`; `0,6` nếu `known_basic`; `1,0` cho phần còn lại. Hiển thị "khối lượng còn lại ~X giờ học", không phải lịch hay hạn chót (nguyên tắc 1.1#7).

Trạng thái: **empty** (placement bị skip: không có màn này); **không đo được mục nào** (dừng sớm S1: "Bắt đầu từ nền tảng", điểm bắt đầu = mục đầu plan); **mục chưa có lesson** (mục `start` chỉ chọn trong mục đã `published`; mục khác ghi "đang soạn"). Ghi: không ghi thêm điểm; `GET` đọc `placement_sessions.result` (cache); `Vào Học tiếp` ghi `placement_sessions.acknowledged_at`.

#### S4. Học tiếp (`/`)

Mục đích: màn chính, chọn việc kế tiếp. Layout và quy tắc giữ nguyên SPEC 2.2/5.5; bổ sung **[SPEC↑ 2.2]**: banner S12 trên cùng, nhóm "Có thể đã biết" và nhãn lesson rút gọn.

```
┌──────────────────────────────────────────────────────────────────────────┐
│ ▶ Tiếp tục nơi bạn dừng: hash_tables · bài 2/3 "Đếm tần suất" [Tiếp tục] │
│ Hôm nay 1h20 · tuần này 6h05 (chỉ để xem)                                │
│ ⚠ 24 thẻ đến hạn ... [Ôn ngay] [Bỏ qua]            (chỉ khi > backlog_warn)│
│ CẦN LÊN ĐIỂM 2 ĐỂ MỞ MỤC SAU     ◐ memory_model → mở arrays  [Test out]  │
│ HỌC TIẾP (thứ tự plan)             LUYỆN GỢI Ý                           │
│  ◐ hash_tables [1] ▶ · ⚡đã biết sơ    ☐ Isomorphic Strings E           │
│  ☐ hashing_patterns 🔒 cần hash_tables ≥ 2 · Test out                    │
│ CÓ THỂ ĐÃ BIẾT (từ đánh giá): arrays?, lib_toolkit? [Test out nhanh]     │
│ ÔN TẬP ĐẾN HẠN (24) ... [Ôn tất cả] [Phiên ngắn]                         │
│ Mốc: Mock 1 mở sau khi xong 11 mục nữa                                   │
└──────────────────────────────────────────────────────────────────────────┘
```

| Component | Nguồn |
|---|---|
| Banner tiếp tục | `GET /resume → primary` |
| Các nhóm | `GET /next` (`must_raise`, `list`, `suggested_problems`, `due_count`, `backlog`, `milestones`) + mới `sweep[]` (mục `likely_known`, xếp **dưới** danh sách học) |
| Thời gian | `GET /stats → today_s, week_s` |

**Đánh giá lại năng lực.** Header S4 có nút phụ **"Đánh giá lại năng lực"** (luôn hiện sau onboarding) → mở modal chọn **Mức kinh nghiệm** (none/some/solid), mặc định = mức đã lưu trong hồ sơ (`GET /me → settings.experience`). Bấm "Bắt đầu đánh giá" gọi `POST /placement` với `experience` đã chọn rồi vào `/placement/:id`. Làm lại **không gieo/không hạ điểm**: điểm luôn recompute từ evidence append-only (SPEC 5), nên chỉ thêm bằng chứng. Nếu còn phiên `in_progress`, `POST /placement` trả về chính phiên đó (resume) — nhất quán với banner S12/PlacementStrip.

Trạng thái: **loading** skeleton 3 nhóm; **empty** (xong 40 mục: "Bạn đã đi hết MVP", hiện Progress); **không còn thẻ**; **server down** (banner offline, hiển thị bản `GET /next` cache lần cuối trong IDB và nhãn "dữ liệu lúc 14:02"); **first-time sau skip placement** (hộp "Muốn đo trình độ? [Làm đánh giá]" một lần, ghi `settings.ui_prefs.hide_placement_tip`). Ghi: không ghi gì trừ ping thời gian.

#### S5. Skill map (`/map`)

Mục đích: nhìn toàn cảnh 40 mục, chọn mục, làm lại module. Vào từ: nav, S3, S4. Layout giữ như SPEC 2.2; chip có ScoreBadge, 🔒, `●` thẻ đến hạn, vòng đích `target`, và (mới) nhãn `hint` nét đứt cho `likely_known`/`likely_gap`.

```
 py.datastructs                              [⋯ menu: Đánh giá lại module]
  [list 2][tuple 1][dict 2●][comprehensions ?][heapq_bisect 0]   panel phải:
 dsa.arrays_strings                          ┌ hash_tables ─────────────────┐
  [arrays ?]─►[hash_tables 2]─►[hashing 🔒]  │ summary_vi, mastery_bar_vi   │
                                             │ Điểm 1/3 · target 2          │
                                             │ prereq: arrays (? chưa đo)   │
                                             │ [Học] [Test out] [Xem trước] │
                                             └──────────────────────────────┘
```

Nguồn: `GET /map` (`status`, `score`, `unlocked`, `due_cards`, `lock_reason`, `known_basic`, `placement_hint`, `targets`) và `GET /subtopics/{id}` cho panel. Trạng thái: loading skeleton chip; lỗi API (khối lỗi + `Thử lại`); offline (dùng bản cache); mục khoá: hover và panel nêu thiếu prerequisite nào. Hành động: `Học` → S6; `Test out` → S8 (`POST /checks/{id}/start`); `Đánh giá lại module` → `POST /placement` (kind=retake, scope=module). Map chỉ đọc nên không ghi.

#### S6. Lesson + editor (`/s/:subtopicId`)

Mục đích: học, gõ code ngay cạnh bài. Vào từ: S4, S5, banner S12. Split ≥ 1280 px như wireframe SPEC 2.2.

```
┌───────────────────────────────┬─────────────────────────────────────────┐
│ ◄ Map › hash_tables  ●●○ 1/3  │ Bài tập 2/3 "Đếm tần suất"      ⏱ 04:12│
│ Bài học│Bài tập│Kiểm tra      │ [CodeEditorPanel]                       │
│ ⚡ Bài rút gọn [Hiện đầy đủ]   │ [▶ Run] [✔ Submit] [💡 0/3] [⟲]         │
│ b05 ▌code_sample [▶ Chạy]     │ [TestResultPanel]                       │
│ b06 ▣ quiz_fill ___ [Kiểm tra]│                                         │
│ [◄ Block trước] 6/11 [Tiếp ►] │ chip lưu nháp · chip đồng bộ            │
└───────────────────────────────┴─────────────────────────────────────────┘
```

| Component | Nguồn / ghi |
|---|---|
| Nội dung & block | `GET /lessons/{id}` (blocks có `id` bền vững); điều hướng block bằng thanh `6/11`, `Alt+→/←` |
| Vị trí | client ghi `resume` (`block_id`, `scroll_in_block`, tab) qua ping/`PUT /resume` |
| Quiz (`quiz_mcq`/`quiz_fill`/`predict_output`) | chọn đáp án giữ ở IDB `quiz_inflight` tới khi bấm `Kiểm tra`; `POST /quiz/answers` ghi `quiz_answers(run_no)`; hiện đúng/sai + `explain_md` ngay (chấm cục bộ từ bundle, thay bằng phản hồi server khi có) |
| `code_sample` | nút `Chạy` tại chỗ (Pyodide), bản sửa của Quan chỉ lưu IDB (`sample:<sub>:<block>`), không lên server |
| `code_exercise` | `Làm bài này` nạp starter vào editor phải; Run; qua hết sample → block tick xanh (client, ghi `events type=exercise_done`, không tính điểm) |
| `Hoàn thành bài học` | `POST /lessons/{id}/complete` → trả `quiz_best`, điểm mới, thẻ ôn |
| `Làm lại lượt` | `POST /lessons/{id}/runs` → `run_no+1` |
| Bài rút gọn | hiện khi `known_basic=true`: ẩn `text`/`callout beginner`/`code_sample`, giữ `quiz`, `code_exercise`, `summary`, `problem_ref`; `Hiện đầy đủ` nhớ theo mục ở localStorage. **Không đổi** điều kiện `lesson_done` (vẫn cần ≥ 3 block graded và `quiz_best ≥ 0.7`) |

Trạng thái: **loading** skeleton; **locked/xem trước** (banner "Đang xem trước: cần X ≥ 2", editor và Submit tắt, `Test out` hiện); **lesson chưa soạn** (`content_status != published`: "Bài này đang soạn" + link problem nếu có); **offline** (lesson đã xem được cache; quiz chấm cục bộ, câu trả lời vào outbox); **first-time** tooltip 3 bước (block, Run, Hoàn thành); **quiz chưa đạt** (liệt kê quiz sai + `Làm lại lượt`). Tab "Kiểm tra" mở khi có ≥ 1 bài AC (SPEC Flow A#7) và dẫn sang S8.

#### S7. Problem (`/p/:problemId`)

Mục đích: giải một bài (Flow B). Vào từ: S6 tab Bài tập, `/problems`, thẻ ôn hộp 3-5, S4 gợi ý.

```
┌───────────────────────────────┬─────────────────────────────────────────┐
│ ◄ Bài tập  Ransom Note  E     │ ⏱ 04:12 (ẩn được)  [EN|VI]              │
│ [EN|VI] Given two strings...  │ [CodeEditorPanel python]                │
│ Ví dụ 1..3 · Constraints      │ [▶ Run] [✔ Submit] [💡 Gợi ý 1/3] [⟲]   │
│ Gợi ý đã mở: (1) ...          │ ┌ Kết quả: AC 12/12 · 38 ms ───────────┐│
│ Độ phức tạp mục tiêu: ẩn tới  │ │ [Xem lời giải mẫu ▾]                 ││
│ khi AC                        │ └──────────────────────────────────────┘│
└───────────────────────────────┴─────────────────────────────────────────┘
```

| Thành phần | Nguồn / ghi |
|---|---|
| Đề, ví dụ, starter, sample, hint đã mở | `GET /problems/{id}` (không hidden, không lời giải) |
| Nháp | IDB + `PUT /drafts/{id}` (mục 4.3); khôi phục khi mở lại, kèm `elapsed_ms` đã cộng dồn |
| `Run` | Pyodide chạy sample; ghi `POST /attempts` mode=`run` (verdict, passed, total, `elapsed_ms`; không lưu stdout) |
| `Submit` | `POST /problems/{id}/start-submit` → hidden test → chạy worker → `POST /attempts` mode=`submit`; server tính `clean`, cập nhật điểm; hiển thị `passed/total`, tên test đầu sai, input/expected với test nhỏ |
| `Gợi ý n/3` | `POST /problems/{id}/hints` mỗi nấc một lần, tăng `hints_used`; nấc đã mở giữ qua phiên |
| `Xem lời giải mẫu` | **modal xác nhận**: nếu chưa AC: "Xem lời giải sẽ khiến bài này không còn tính 'clean' và không thể làm bằng chứng điểm 2/3. Xem?" `[Huỷ] [Vẫn xem]` → `GET /problems/{id}/solution` ghi `solution_viewed=true`; nếu đã AC: mở thẳng, ghi `solution_viewed=false` giữ nguyên |

Trạng thái: **loading**; **worker đang khởi động lại** sau TLE (nút Run "Đang chuẩn bị…" ~3 giây); **TLE/RE/CE** hiện traceback hoặc "Quá thời gian ở test <tên>"; **locked** (mục khoá: xem trước, Submit tắt); **offline** (Run được, Submit tắt "Cần server", nháp ở IDB); **AC** (chip xanh, `elapsed`, "clean" hoặc lý do không clean, so sánh độ phức tạp). `kind=check` không đi qua màn này (dùng S8).

#### S8. Mastery check / Test out (`/check/:subtopicId`) **[SPEC↑ 2.1]**

Mục đích: chạy flow C/D tập trung, cùng component item với S2. Vào từ: tab "Kiểm tra" (S6), `Test out` (S4, S5), S3 sweep.

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Test out: hash_tables · Mức 2 (bước 1/≤3)     ⏱ 06:00 → quá giờ 09:00    │
│ [đề + editor + Run + Nộp bài như S2]                [Không biết] [Thoát] │
│ Trượt mức 2: chỉ hiện test sai, KHÔNG hiện reference · làm lại sau 24 giờ│
└──────────────────────────────────────────────────────────────────────────┘
```

Nguồn: `POST /checks/{id}/start` tạo/tiếp tục `check_sessions` (trả `session_id`, item, `elapsed_ms`); `POST /checks/{session}/answer` trả item kế hoặc kết quả. Trạng thái: **check_retry_locked** (nút disabled "Làm lại được sau 14:30", đường khác: `check2_ok`); **không có item mức 1** (dừng và "cần học lesson"); **kết quả** (đậu mức 2: điểm 2, mục phụ thuộc mở; hiện danh sách mục vừa mở; trượt: test sai + khoá 24 giờ); **thoát giữa chừng** (session giữ, banner S12; hết hạn sau 24 giờ không hoạt động: item `expired`, không tính trượt). Ghi: `check_results`, `user_subtopic.unlocked_at`, `review_cards` theo luật 5.4.

#### S9. Review (`/review`)

Mục đích: ôn thẻ đến hạn, làm bao nhiêu tuỳ ý (Flow E). Vào từ: S4, nav.

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Thẻ 2 · còn 7 đến hạn · hash_tables · hộp 3 (quá hạn 2 ngày)    [Dừng]   │
│ ┌ Predict output / bài code ngắn (như S7 thu gọn) ─────────────────────┐ │
│ │ ... Đáp án [__________]                         [Kiểm tra] [Bỏ qua]  │ │
│ └──────────────────────────────────────────────────────────────────────┘ │
│ Đúng → hộp 4, lần sau +7 ngày · Sai → hộp 1, mai ôn lại                  │
└──────────────────────────────────────────────────────────────────────────┘
```

Nguồn: `GET /review/queue` (toàn bộ, hoặc `?preset=1`); khi mở thẻ server chọn `item_ref` và **ghim** vào `review_cards.current_item_ref` để mở lại vẫn cùng item. Ghi: `POST /review/{subtopic}/result` (`success`, `item_ref`) cập nhật `review_cards`, `review_log`. Trạng thái: **empty** ("Hết thẻ đến hạn", nút Học tiếp); **xong preset** (nút `Ôn tiếp`); **phone** (chỉ item nhớ nhanh); **offline** (thẻ đã mở làm được; kết quả vào outbox, thẻ kế tiếp lấy từ queue cache; không mở thẻ code mới khi chưa có item cache); `Dừng` về S4, tiến độ phiên không mất (mỗi thẻ ghi ngay). `Bỏ qua` không ghi gì, thẻ giữ hạn.

#### S10. Progress (`/progress`)

Mục đích: xem tiến độ trung tính (không streak, không so lịch). Nguồn: `GET /stats`. Thành phần: heatmap 40 mục (màu theo điểm), cột "tuần này" (AC, phút code, thẻ đã ôn, giờ học), biểu đồ giờ theo tuần, heatmap lịch `study_time`, bảng "mục yếu" (điểm < target hoặc nhiều `lapses`), "đã xong X / 40 mục" và mục kế tiếp, độ đúng theo hộp (`review_log`), lịch sử đánh giá đầu vào (`placement_sessions`, mở S3). Trạng thái: **empty** (chưa có dữ liệu: "Học bài đầu tiên để thấy biểu đồ"), loading (skeleton biểu đồ), offline (cache). Không ghi.

Ghi chú: trang "Hồ sơ kỹ năng" (`/profile`) dùng `GET /diagnosis` (`tracks[]`, `domains[]` > `modules[]` với `level`, `coverage`, `tier`, `strong`, `improve`; luật ở SPEC 5.7; chọn vai trò bằng nút track SWE/AI + select level intern/fresher/junior/senior, kèm hàng readiness `levels[]` cho 4 level, level chỉ đổi target của view này); chỉ hiển thị, không đổi điểm. Mỗi thẻ module có nút "Đo sâu" mở phiên placement `deep_dive` của module đó (SPEC 5.6 mục 8); kết quả có link "Xem hồ sơ kỹ năng" (`/profile`).

#### S11. Settings (`/settings`)

Mục đích: cài đặt và quản trị dữ liệu. Tab: `Chung` · `Dữ liệu & backup` · `Đánh giá`.

```
┌─ Chung ──────────────────────────────────────────────────────────────────┐
│ Hồ sơ: mục tiêu [Intern▾] track [SWE▾] tên [Quan] múi giờ [..▾]          │
│ Giao diện: theme [Tự động▾] cỡ chữ editor [14▾] bố cục [45/55] gợi ý lần đầu [Bật]│
│ Ôn tập: cỡ "Phiên ngắn" [6 | tắt]  ngưỡng cảnh báo backlog [20]           │
├─ Dữ liệu & backup ───────────────────────────────────────────────────────┤
│ Trạng thái: ✓ đồng bộ · 0 thay đổi chờ gửi · DB 2,4 MB · WAL bật          │
│ Backup tự động: mỗi [6] giờ, giữ [20] bản + 1 bản/ngày trong 30 ngày      │
│  14:02 hôm nay (2,4 MB) [Tải về] [Khôi phục]   08:02 ...                  │
│ [Sao lưu ngay] [Export JSON] [Import JSON…]                              │
│ Thay đổi chưa đồng bộ (outbox): 0 · Lỗi vĩnh viễn: 0 [Xem] [Thử lại]      │
│ Vùng nguy hiểm: [Xoá toàn bộ tiến độ…] (gõ RESET, tự backup trước)        │
├─ Đánh giá ───────────────────────────────────────────────────────────────┤
│ Lần gần nhất 24/10: 41 phút, đo 7 mục [Xem kết quả] [Làm lại theo module▾]│
└──────────────────────────────────────────────────────────────────────────┘
```

Ghi: `PUT /settings` (tz, review_preset, backlog_warn, `ui_prefs`, hồ sơ), `POST /backups`, `POST /backups/{name}/restore` (modal: "Sẽ thay toàn bộ dữ liệu bằng bản 08:02; dữ liệu sau đó mất. Tự backup bản hiện tại trước. Gõ KHOI PHUC"), `GET /export`, `POST /import` (modal tương tự, chọn file, kiểm `schema_version`), `POST /reset`. Trạng thái: **server down** (tab Dữ liệu chỉ hiện outbox, các nút cần server disable); **lỗi restore/import** (giữ nguyên DB hiện tại, hiện lý do); **import sai phiên bản** (từ chối, nói rõ); **first-time** không có backup nào ("Backup đầu tiên sẽ chạy lúc khởi động").

#### S12. Banner "Tiếp tục nơi bạn dừng" (toàn cục)

Mục đích: đưa Quan về đúng chỗ sau khi thoát hoặc tắt máy. Nguồn: `GET /resume` lúc khởi động app và khi tab quay lại sau ≥ 30 phút không hoạt động. Quy tắc:

- Hiện **một banner chính** theo ưu tiên: placement/check đang dở > bài/lesson ở màn cuối > thẻ ôn đang mở. Phần còn lại vào dấu `+2 việc khác`.
- Ở `/` hiện thẻ lớn trên cùng; ở route khác hiện dải mảnh; không hiện nếu route hiện tại đúng là đích của banner.
- Nội dung: loại việc, tên mục/bài, vị trí (`block 6/11`, `bài 2/3`, `thẻ 2/9`, `còn ~28 phút`), thời điểm ("2 giờ trước"). Nút `Tiếp tục` (điều hướng kèm `block_id`, nạp nháp, khôi phục cuộn) và `✕` (ẩn trong phiên; không xoá `resume_state`).
- Trạng thái: không có `resume_state` (không hiện); mục đã `done` hoặc bài đã AC kể từ đó (hiện "Mở lại" hoặc bỏ banner nếu việc đã xong); server down (dùng `resume` cache từ IDB, nhãn "chưa xác nhận với server").

#### S13. Danh sách bài (`/problems`)

Giữ nguyên SPEC 2.2 (lọc theo subtopic, độ khó, trạng thái, nguồn; `kind=check` ẩn mặc định). Nguồn `GET /problems`; trạng thái empty ("Không có bài khớp bộ lọc" + `Xoá lọc`), loading skeleton, offline (cache danh sách). Bấm một dòng → S7; dòng khoá hiện LockState. Không ghi; bộ lọc nhớ ở localStorage.

---

## 4. Ghi nhớ dữ liệu và tiếp tục sau khi thoát / tắt máy

### 4.1 Nguyên tắc

1. **Server SQLite là nguồn sự thật** cho mọi thứ tính điểm. Mọi sự kiện học được ghi **ngay khi xảy ra**, không đợi "lưu", không có nút Lưu.
2. **Trình duyệt giữ bản sao cục bộ (IndexedDB) cho những gì chưa chắc đã lên server**: nháp code, hàng đợi sự kiện (outbox), việc dở. Mất kết nối server không làm mất công sức.
3. **Heartbeat gửi giá trị tuyệt đối** (tổng `elapsed_ms`, `active_ms`, vị trí) nên gửi lại bao nhiêu lần cũng đúng (server lấy `max`/ghi đè theo `updated_at`). **Sự kiện gửi kèm `Idempotency-Key`** nên gửi lại không cộng đôi.
4. **Phạm vi theo mốc**: M1 có PRAGMA bền, nháp IndexedDB (flush `pagehide`), `Idempotency-Key`, `resume_state`, backup tự động. **M3** thêm service worker, outbox replay đầy đủ có `outbox_dead`, `draft_versions` + `rev` + 409. **Với thiết kế M1 không có chữ nào đã gõ bị mất khi mất điện** ngoài khoảng ~300 ms cuối (IndexedDB, độ bền `strict`); bản trên server trễ tối đa ~2 giây và được đẩy bù khi mở lại, vì server và trình duyệt cùng chạy trên một máy nên tắt máy là cả hai cùng tắt.
5. Mất tối đa vài giây gõ dở khi mất điện đột ngột; mọi sự kiện đã hiển thị "Đã lưu" thì còn nguyên sau khi tắt máy.

### 4.2 Bảng: cái gì, lưu ở đâu, khi nào

| Dữ liệu | Nơi lưu | Khi nào ghi | Khôi phục khi mở lại |
|---|---|---|---|
| Sự kiện tiến độ: `quiz_answers`, `attempts`, `check_results`, `review_log`, `lesson_done`, hint, solution_viewed | Server SQLite (WAL, `synchronous=FULL`), kèm bản ghi `events` | Ngay mỗi sự kiện, trong cùng transaction với cập nhật `user_subtopic`/`review_cards`; điểm tính lại trong transaction | Đọc lại từ DB; không cần thao tác |
| Code nháp theo bài (`drafts`) | IDB `drafts` (local, tức thì) + server `drafts` | IDB: debounce **300 ms**. Server: debounce **2 giây** sau lần gõ cuối, tối đa **10 giây** nếu gõ liên tục; ngoài ra khi `blur`, `visibilitychange→hidden`, `pagehide` (`fetch keepalive`, fallback `sendBeacon`), `Ctrl+S` | M1: bản có `updated_at` mới hơn thắng; M3: theo `rev` (4.3); nạp vào editor kèm vị trí con trỏ |
| Nháp bài trong lesson (`code_exercise`, sample đã sửa) | IDB `drafts` (khoá `ex:<sub>:<block>`) | như trên, chỉ local | Nạp lại khi mở block; sample sửa ở IDB |
| Vị trí học (`resume_state`): route, `subtopic_id`/`problem_id`, `block_id`, `scroll_in_block`, tab, loại việc | Server `resume_state` (1 dòng/user) + IDB `resume` | `PUT /resume` debounce 3 giây khi đổi block/tab/route; kèm trong `POST /activity/ping` mỗi 30 giây; flush khi `pagehide` | `GET /resume` → S12 (4.6) |
| Quiz đang chọn dở (chưa bấm Kiểm tra) | IDB `quiz_inflight` | khi đổi lựa chọn (debounce 300 ms) | Điền lại lựa chọn; **câu đã trả lời** nằm ở `quiz_answers` nên không đổi |
| Đồng hồ bài (`elapsed_ms`) | server `drafts.elapsed_ms` (qua heartbeat; chép sang `attempts.elapsed_ms` lúc Run/Submit vì trước lần Run đầu chưa có dòng `attempts`) + IDB | mỗi 15 giây khi bài đang hiển thị và tab hiện | cộng dồn tiếp; mất tối đa ~15 giây |
| Placement dở | `placement_sessions` (`phase`, `state`, `active_ms`) + `check_sessions` (`current_item_id`, `elapsed_ms`) | mỗi item xong ghi ngay; heartbeat 15 giây cho đồng hồ | Banner S12 → đúng item; đồng hồ **dừng khi app đóng** (chỉ tính thời gian hoạt động) |
| Mastery check dở | `check_sessions` | như trên | tiếp item đang làm trong 24 giờ; sau đó `expired` (không tính trượt, nháp code còn) |
| Phiên ôn tập | mỗi thẻ ghi ngay (`review_cards`, `review_log`); item đang mở ghim ở `review_cards.current_item_ref`; cỡ phiên/tiến độ ở `resume_state.context` | khi mở thẻ; khi trả lời | `/review` lấy lại queue (thẻ xong đã rời hạn); thẻ đang mở hiện lại **cùng item**, đáp án gõ dở lấy từ IDB |
| Thời gian học (`study_time`) | Server | `POST /activity/ping` mỗi 30 giây khi tương tác | cộng dồn theo SPEC 6.4 |
| Giao diện: theme, cỡ chữ, tỉ lệ split, tab nhớ, bộ lọc `/problems`, cờ "bài rút gọn" | localStorage (nhanh, đồng bộ) + mirror `settings.ui_prefs` | khi đổi (debounce 1 giây mirror) | đọc localStorage trước khi render (không nháy giao diện); trống thì lấy `ui_prefs` từ server |
| Hàng đợi chờ gửi (outbox) **(M3)** | IDB `outbox` | trước khi gửi mọi POST ghi trạng thái | replay (4.5). M1: sự kiện thất bại báo toast "Chưa lưu được" + `Thử lại`; dữ liệu nguồn (code, lựa chọn quiz) vẫn ở IDB |
| Lesson/problem công khai, bundle Pyodide **(M3)** | Cache Storage (service worker) | lần đầu truy cập | app mở được dù server tắt |

### 4.3 Nháp code và đối chiếu bản

**M1**: đối chiếu đơn giản, bản có `updated_at` mới hơn thắng (một thiết bị), `PUT /drafts` ghi đè. **`rev`, 409 và `draft_versions` dưới đây là M3 (T3.5).**

- Mỗi nháp có `rev` (số nguyên tăng dần do **server** cấp) và `updated_at`. Client giữ `base_rev` = rev cuối đã biết của server.
- `PUT /drafts/{problem_id}` gửi `{code, base_rev, updated_at, cursor}`. Server chấp nhận khi `base_rev == rev hiện tại` (trả `rev` mới); khác thì trả 409 kèm bản server.
- Khi 409 hoặc lúc mở bài thấy IDB và server khác nhau: lấy bản có `updated_at` mới hơn làm bản chính; **bản kia không bị bỏ** mà đẩy vào `draft_versions` (giữ 5 bản gần nhất mỗi bài), và editor hiện chip "Có bản nháp khác (14:02) [Xem / Khôi phục]". Vì chỉ một người, một thiết bị là phổ biến, hầu hết trường hợp là IDB mới hơn (server tắt) và được đẩy lên im lặng.
- Gửi lại bản nháp giống hệt là no-op; không cần idempotency key (ghi đè theo `rev`).

### 4.4 Idempotency (chống đếm đôi khi replay)

- Client sinh `Idempotency-Key: <uuid v4>` **tại lúc tạo sự kiện** và lưu cùng sự kiện trong outbox trước khi gửi. Áp dụng cho mọi POST thay đổi trạng thái: `/attempts`, `/quiz/answers`, `/lessons/*/complete`, `/lessons/*/runs`, `/checks/*`, `/placement/*` (trừ heartbeat), `/review/*/result`, `/problems/*/hints`, `/feedback`.
- Server có bảng `idempotency_keys(key PK, user_id, method, path, status, response JSON, created_at)`. Gặp key đã có: trả lại đúng phản hồi đã lưu, **không chạy lại logic**. Giữ 30 ngày. Hai request cùng key đến song song: bảo vệ bằng `INSERT` khoá duy nhất rồi mới xử lý.
- (Cảnh báo, N3) `occurred_at` bị kẹp ở `received_at − 7 ngày`; nếu outbox nằm quá 7 ngày, ngày ôn có thể lệch, với một người dùng chấp nhận và chỉ hiện cảnh báo.
- Sự kiện mang thời điểm thật: body có `occurred_at` (giờ client, ISO UTC); server kẹp vào `[received_at − 7 ngày, received_at + 5 phút]`, lưu cả `received_at`. Leitner dùng ngày của `occurred_at` theo `tz` (ôn lúc server tắt vẫn đúng ngày). Thứ tự áp dụng theo `occurred_at`.
- Cần server, không xếp hàng được: `Submit` (cần token hidden test), xem lời giải, bắt đầu check/placement, lấy item ôn mới. Các thao tác này disable khi offline thay vì xếp hàng.

### 4.5 Offline outbox (M3, T3.5)

M1 chưa có replay đầy đủ: lỗi gửi thì báo và cho thử lại, dữ liệu nguồn vẫn nằm ở IndexedDB. Phần dưới là bản đầy đủ của M3.

- IDB `outbox` giữ `{key, method, path, body, occurred_at, tries, state}`. Ghi bằng transaction `durability: 'strict'` (Chrome mặc định "relaxed" có thể mất vài giây khi mất điện).
- Gửi **tuần tự theo thứ tự tạo**, khi: khởi động app, sự kiện `online`, tab hiện lại, và mỗi 15 giây nếu hàng đợi không rỗng (backoff 2 → 60 giây). Thành công (2xx hoặc replay của key cũ) thì xoá khỏi outbox.
- Lỗi 5xx/mạng: giữ, thử lại. Lỗi 4xx (dữ liệu bị từ chối, vd bài đã đổi phiên bản): chuyển sang `outbox_dead`, toast "1 thay đổi không gửi được", xem và thử lại/bỏ ở Settings. Không bao giờ tự xoá im lặng.
- Chip đồng bộ (3.2) phản ánh số mục còn lại. Khi server sống lại, điểm và thẻ ôn trên màn hình được tải lại từ server (nguồn sự thật), không tin kết quả dự đoán cục bộ.
- **Server tắt hoàn toàn khi mở app**: service worker phục vụ app shell + bundle Pyodide + lesson/problem đã xem từ cache; banner offline; đọc, gõ code, Run, làm quiz (chấm cục bộ từ bundle, sự kiện vào outbox) vẫn dùng được. Không có cache cho lesson chưa từng mở: màn "Cần server".

### 4.6 Tiếp tục nơi đã dừng (`GET /resume`)

- Ghi: như bảng 4.2. `resume_state(user_id PK, mode, route, ref JSON, context JSON, updated_at, device_id)`. `mode` ∈ `lesson | problem | check | placement | review | other`. `ref` ví dụ lesson: `{subtopic_id, block_id, scroll_in_block: 0.4, tab: "lesson"}`; problem: `{problem_id, cursor}`; review: `{subtopic_id, item_ref}`.
- `GET /resume` trả `{primary, others[], in_progress: {placement, check, review}}` với `primary` theo ưu tiên S12. Khi đích đã không còn hợp lệ (mục đã `done` hoặc đã AC kể từ lúc đó) server đánh `stale: true` và client hạ cấp thành "Mở lại" hoặc bỏ.
- **Thế nào là bỏ dở**: placement không hoạt động ≥ 7 ngày → `stale` (giữ kết quả đã đo, hỏi lại); check dở ≥ 24 giờ → `expired`; lesson/problem không bao giờ hết hạn (chỉ là vị trí đọc, nháp giữ vô thời hạn); phiên ôn không có khái niệm hết hạn (thẻ chưa làm vẫn đến hạn).
- Đồng hồ: bài (`elapsed_ms`) và placement/check (`active_ms`) **chỉ đếm thời gian hoạt động**; đóng app hoặc tắt máy là dừng, mở lại tiếp từ giá trị đã lưu (sai số ≤ 15 giây). Đây là hệ thống dựa trên sự trung thực của một người dùng; app ghi `pauses` để Quan tự thấy.

### 4.7 An toàn khi mất điện và khi server chưa chạy

| Lớp | Cấu hình |
|---|---|
| **Container tự dậy** | `docker-compose.yml`: `restart: unless-stopped`, `healthcheck` gọi `GET /api/health` mỗi 10 giây (mở được DB, trả `journal_mode`), cổng `127.0.0.1:8080:8080`. Máy khởi động lại thì Docker khởi động lại container; cần bật "Start Docker Desktop when you sign in" (Windows/macOS) hoặc `systemctl enable docker` (Linux). README ghi rõ điều này |
| **Nơi đặt DB (P3)** | DB trong **named volume** `app_data:/app/data` (mặc định mọi hệ điều hành); bind mount `./data` chỉ dùng trên Linux native, vì bind mount của Docker Desktop không bảo đảm `fsync` xuống đĩa thật. Backup là file thường nên ghi ra thư mục host `./backups` (bind) và `BACKUP_MIRROR_DIR`. README cảnh báo: không đặt repo/`data/` trên ổ mạng hoặc thư mục đồng bộ cloud |
| **SQLite bền** | `PRAGMA journal_mode=WAL; synchronous=FULL; foreign_keys=ON; busy_timeout=5000`; một worker uvicorn (một writer), mỗi sự kiện một transaction ngắn. `synchronous=FULL` đảm bảo giao dịch đã trả về thì còn sau mất điện (WAL + FULL chấp nhận chậm thêm vài ms, không đáng kể với một người) | **Lúc khởi động**: `PRAGMA journal_mode=WAL` phải trả `wal` và thư mục dữ liệu không được nằm trên hệ tệp mạng (nfs, cifs/smb, fuse, 9p, vboxsf); nếu không app dừng với lỗi rõ ràng, không chạy ở chế độ kém bền |
| **Kiểm tra khi khởi động** | `PRAGMA quick_check`; nếu hỏng: không ghi gì, hiện màn "Cơ sở dữ liệu lỗi" với bản backup mới nhất hợp lệ và nút `Khôi phục` |
| **Backup tự động** | Dùng SQLite online backup API (không copy file đang ghi). Chạy: lúc app khởi động (nếu bản mới nhất cũ hơn 1 giờ), mỗi `backup_every_hours` (mặc định **6**), **trước** mọi migration/import/restore/reset, và khi tắt êm (SIGTERM). Giữ **20** bản gần nhất + **1 bản đầu mỗi ngày trong 30 ngày**. Tên `data/backups/app-YYYYmmdd-HHMMSS.db`. Nếu đặt `BACKUP_MIRROR_DIR` (vd thư mục OneDrive/Dropbox) thì mỗi bản được chép thêm sang đó để sống sót khi hỏng ổ đĩa |
| **Khôi phục một cú nhấp** | Settings → danh sách bản → `Khôi phục` → server tự backup bản hiện tại, kiểm `integrity_check` và `schema_version` của bản chọn, nạp vào DB đang chạy bằng backup API, xoá cache `GET /next`; client nạp lại trang. Outbox chưa gửi vẫn được replay sau đó |
| **Export / Import JSON** | `GET /export` gồm `schema_version`, `app_version`, `exported_at`, mọi bảng của user. `POST /import` (mode `replace`, MVP): tự backup trước, kiểm phiên bản, ghi trong **một** transaction (lỗi giữa chừng thì không đổi gì). Dùng để chuyển máy |
| **Mất điện lúc ghi** | Transaction chưa commit tự bị huỷ khi mở lại; client không nhận 2xx nên báo "Chưa lưu được" và nguồn dữ liệu còn ở IDB (M1); outbox replay tự động với cùng key từ M3 |

### 4.8 Không được giữ lại (và vì sao chấp nhận)

- **Bộ nhớ trình thông dịch Pyodide** (biến, import, hàm đã định nghĩa trong phiên chạy): mỗi lần Run khởi tạo môi trường sạch từ code trong editor, nên không bao giờ cần. Worker bị `terminate()` sau TLE hoặc đóng tab là mất, có chủ đích.
- **Output chưa gửi của lần Run (stdout/traceback đầy đủ)**: chỉ kết quả tóm tắt (verdict, passed/total) đi vào `attempts`; output dài gây phình DB mà không có giá trị chấm điểm. Mở lại bài hiện "Lần chạy cuối: 2/3 sample lúc 14:02" và Quan bấm Run lại (mất < 1 giây).
- **Lịch sử undo/redo của editor**, vùng chọn: mất khi nạp lại; vị trí con trỏ vẫn được khôi phục.
- **Tab Kết quả đang mở, vị trí cuộn ở màn không phải lesson**: trả về mặc định.
- **Request HTTP đang bay** lúc tắt máy: sự kiện chưa được server xác nhận thì dữ liệu nguồn vẫn ở IndexedDB (M1) hoặc trong outbox (M3); không có ghi nửa chừng nhờ transaction.

### 4.9 Nhiều người dùng sau này (cùng thiết kế, thêm `user_id` và đồng bộ)

- Mọi bảng đã có `user_id`; `resume_state` và `placement_sessions` khoá theo `(user_id, device_id)`/`user_id`; IDB đổi tên `prep-app:<user_id>`; outbox gắn token/`user_id`; `idempotency_keys` khoá theo `user_id`.
- Đồng bộ nháp giữa thiết bị dùng đúng cơ chế `rev` (4.3); `GET /resume` chọn hoạt động mới nhất giữa các `device_id` và gợi ý "Tiếp tục trên thiết bị này".
- SQLite → Postgres: backup bằng `pg_dump`, `GET /export` theo user giữ nguyên; `synchronous=FULL` tương ứng `synchronous_commit=on`.

---

## 5. Thay đổi cần đưa vào `SPEC.md` (đã áp dụng ở v0.6)

### 5.1 Mục 2.1, 2.2, 2.3 (màn hình)

- **2.1**: thêm route `/welcome` (+ `/welcome/profile`, `/welcome/start`), `/placement/:sessionId`, `/placement/:sessionId/result`, `/check/:subtopicId`; cột mục đích của `/` nhắc banner "Tiếp tục"; `/settings` thêm backup/restore/reset và tab Đánh giá; liên kết tới `UI_SPEC.md`.
- **2.2**: ngưỡng split view từ **≥ 1024** đổi thành **≥ 1280** (thiết kế quanh 1366), 768-1279 hai tab, < 768 chỉ đọc lesson/quiz và ôn thẻ nhớ nhanh; wireframe `/` thêm banner "Tiếp tục nơi bạn dừng" và nhóm "Có thể đã biết".
- **2.3**: thêm **Flow G** (lần đầu mở app → hồ sơ → placement/bỏ qua) và **Flow H** (tiếp tục sau khi thoát/tắt máy).

### 5.2 Mục 5 (chỉ làm rõ, không đổi luật điểm)

- **5.3**: thêm câu "khi `tested_out` ghi `unlocked_at` cho chính mục đó" (trước đây chỉ nói mở khoá các mục phụ thuộc; Test out trên mục đang khoá cần kết quả này).
- **5.4 quy tắc 1**: thẻ tạo hàng loạt bởi placement được rải `due = ngày đạt + 1 + ⌊k/8⌋`. Không phải trần thẻ.
- **5.6 mới "Placement"**: sáu quy tắc gieo điểm (mục 2.1/2.5 ở đây), trỏ về `UI_SPEC.md` mục 2 cho thuật toán.

### 5.3 Mục 6.3 (dữ liệu)

| Bảng / cột | Thay đổi |
|---|---|
| `settings` | thêm `target_role`, `track`, `language`, `experience`, `display_name`, `onboarded_at`, `backup_every_hours` (6), `backup_keep` (20), `ui_prefs` (JSON) |
| `subtopics` | `target_intern`, `target_ai` → thêm `targets` (JSON `{swe:{intern,fresher}, ai:{intern,fresher}}`); `done` vẫn dùng `target_intern` |
| `user_subtopic` | thêm `known_basic`, `placement_hint` (`likely_known`\|`likely_gap`\|null), `placement_session_id` |
| `placement_sessions` (mới) | `id`, `user_id`, `scope`, `kind` (`initial`\|`retake`\|`continue`), `status` (`in_progress`\|`finished`\|`skipped`\|`stale`), `experience_prior`, `phase`, `state` (JSON), `result` (JSON), `active_ms`, `budget_soft_min` (45), `budget_hard_min` (60), `parent_id`, `started_at`, `last_active_at`, `finished_at`, `acknowledged_at` |
| `check_sessions` (mới) | `id`, `user_id`, `subtopic_id`, `context` (`mastery`\|`test_out`\|`placement`), `placement_session_id`, `order_no`, `status` (`in_progress`\|`done`\|`expired`), `ladder` (JSON), `current_item_id`, `elapsed_ms`, `started_at`, `last_active_at` |
| `check_results` | thêm `session_id`, `context`, `gave_up` (khoá 24 giờ chỉ tính `passed=false AND gave_up=false`) |
| `review_log` | thêm `item_kind` (`code`\|`recall`); `retention_ok` chỉ nhận `code` (v0.7) |
| `resume_state` (mới) | `user_id` PK, `mode`, `route`, `ref`, `context`, `updated_at`, `device_id` |
| `idempotency_keys` (mới) | `key` PK, `user_id`, `method`, `path`, `status`, `response`, `created_at` |
| `drafts` | thêm `cursor`, `elapsed_ms`, `started_at` (M1); `rev` và bảng `draft_versions` (5 bản/bài) ở M3 |
| `review_cards` | thêm `current_item_ref`, `current_item_opened_at` |
| `events` | thêm `occurred_at`, `received_at`, `idem_key` |

### 5.4 Mục 6.4 (API)

`PUT /profile` · `POST /placement` (tạo; body `scope`, `kind`) · `POST /placement/skip` · `GET /placement/current` · `GET /placement/{id}` · `POST /placement/{id}/answer` · `POST /placement/{id}/heartbeat` · `POST /placement/{id}/finish` · `GET /placement/{id}/result` · `GET /resume` · `PUT /resume` (+ `POST /resume` cho `sendBeacon`) · `GET /health` · `GET /backups` · `POST /backups` · `POST /backups/{name}/restore` · `GET /backups/{name}` (tải) · `POST /reset`. Mở rộng: `GET /me` trả `onboarding{profile_done, placement}`; `POST /activity/ping` nhận thêm `resume`; `POST /checks/{id}/start` trả `session_id` và có `POST /checks/{session}/heartbeat`; mọi POST ghi trạng thái nhận `Idempotency-Key`; `GET /next` thêm `sweep[]`.

### 5.5 Mục 6.7, 8.3

- **6.7**: thay đoạn triển khai cục bộ bằng cấu hình compose (restart, healthcheck, volume, bind 127.0.0.1), named volume + kiểm `journal_mode`/ổ mạng, chế độ SQLite bền, chính sách backup (6 giờ / giữ 20 + 1 bản ngày trong 30 ngày / mirror), khôi phục một cú nhấp.
- **8.3**: ghi các quyết định v0.6 (placement T2.9a/T2.9b, ngưỡng 1280 px, rải thẻ placement, nháp 2 giây, `synchronous=FULL`).

### 5.6 Mục 7 (lộ trình)

| Mốc | Task mới | Nghiệm thu bổ sung |
|---|---|---|
| **M1** | **T1.7 Lưu bền**: PRAGMA, kiểm `journal_mode`/ổ mạng, named volume, `idempotency_keys` + middleware, IDB drafts (flush `pagehide`, `updated_at` thắng), `resume_state` + `GET/PUT /resume`, `GET /health`, backup tự động + restore | tắt container giữa lúc gõ: mở lại không mất quá 3 giây code; gửi lại cùng sự kiện 5 lần chỉ ghi 1; `data/` trên ổ mạng thì app từ chối chạy; hỏng DB rồi khôi phục thành công |
| **M2a** | **T2.7 Onboarding + Tiếp tục** (S1, `PUT /profile`, banner S12, `/check/:id`, `check_sessions`); **T2.8** UI backup trong Settings; **T2.9a Placement tối thiểu** (Phase A, luật dừng, `tested_out`, S2, S3 rút gọn) ở cuối M2a | mở app lần đầu đi hết S1 và vào `/`; thoát giữa lesson, mở lại: banner về đúng block; người mới xong placement ≤ 9 phút; `score == scoring(events)` |
| **M2b** | **T2.9b Placement đầy đủ**: Phase B/C, nhãn suy luận, sweep, đo thêm, làm lại module, S3 đầy đủ | mô phỏng 3 hồ sơ ≤ 60 phút hoạt động; không mục nào ≥ 3 do placement; nhãn không đổi điểm |
| **M3** | T3.2 (compose, README cảnh báo ổ mạng/cloud), **T3.5 offline đầy đủ** (service worker, outbox replay + `outbox_dead`, `draft_versions` + `rev` + 409); T3.3: responsive 3 mức, phím tắt, smoke test diacritics, axe-core; T3.4: kịch bản tắt máy ngẫu nhiên | tắt máy ngẫu nhiên 20 lần giữa phiên học: không mất sự kiện đã hiển thị "Đã lưu"; app tự dậy sau khởi động lại |

Ước lượng: M1 +1 ngày (bớt ~1 ngày so với v0.6 nhờ hoãn offline), M2a 7-10 ngày, M2b 5-7 ngày, M3 +1-2 ngày cho T3.5.

### 5.7 Mâu thuẫn đã tìm thấy và cách xử lý

| Mâu thuẫn | Xử lý |
|---|---|
| SPEC 2.2/T3.3: split view từ 1024 px; yêu cầu mới: laptop 1366 là mức tối thiểu | Ngưỡng split = 1280 (đệm cho thanh cuộn); 768-1279 dùng hai tab |
| SPEC 6.3: `drafts` tự lưu "mỗi 3 giây" | Đổi thành debounce 2 giây (tối đa 10 giây) + flush khi `blur`/`pagehide` + bản sao IDB |
| SPEC Flow D: Test out trên mục đang khoá "mở khoá mục và các mục phụ thuộc" nhưng 5.3 chỉ tính theo điểm prerequisite | Làm rõ: `tested_out` ghi `unlocked_at` cho chính mục |
| SPEC 5.4#1: thẻ `due = ngày + 1` sẽ dồn 20+ thẻ sau placement mạnh | Rải 8 thẻ/ngày chỉ cho thẻ tạo bởi placement; luật còn lại giữ |
| SPEC 3.4/Flow C: mục thiếu `write_code` mức 2 vẫn dùng được mastery check bằng `concept`/`read_code` | Placement chỉ dùng E2 `write_code`; mục thiếu thì `not_assessed` đến khi item bổ sung `published` |
| SPEC 5.4#4: thẻ hộp 3-5 là bài code, nhưng điện thoại/tablet dọc và preset "Phiên ngắn" dùng thẻ nhớ nhanh | Thẻ nhớ nhanh đạt vẫn lên hộp nhưng `retention_ok` chỉ nhận `review_log.item_kind=code`; `level3_ok` chỉ nhận `write_code` (v0.7) |
| v0.6: `data/` bind mount + WAL | Named volume trên mọi OS, kiểm `journal_mode` và ổ mạng lúc khởi động, README cảnh báo (v0.7) |
| v0.6: "Không biết" không tính để dừng nên người mới bị hỏi hết ngân sách | "Không biết" tính để dừng sớm; `experience=none` chỉ chạy C1-C2 (v0.7) |
| SPEC 6.4: `POST /quiz/answers` trả `correct` | Giữ; client hiển thị tạm kết quả chấm cục bộ từ bundle (đáp án quiz không bí mật) để chạy được offline, rồi thay bằng phản hồi server |
| SPEC dùng `target_intern`; hồ sơ mới có vai trò New-grad và track AI | Chỉ đổi vòng đích hiển thị; `done`, unlock, thứ tự học vẫn theo `target_intern` (MVP chưa có nội dung riêng cho AI) |
| SPEC 6.2 CSP không nói font/style | Thêm `font-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:` |
| SPEC 8.2 câu 2 (dùng từ máy khác): mặc định chỉ cục bộ | Giữ; chỉ thêm tuỳ chọn `BIND=0.0.0.0` cho LAN, không có service worker trên HTTP qua IP |
