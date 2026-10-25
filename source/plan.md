# Kế hoạch ôn luyện phỏng vấn Meta 1 tháng (intern / new grad, SWE + Python)

> Sinh tự động bởi `build_plan.py` từ cây kiến thức (`layer1_skill_tree/skill_tree.json`), bộ mock `content_ng/*.json` và `predicted_questions.md`. Dữ liệu máy đọc: `plan.json`. Kiểm tra: `check_log.md`. Đánh giá kiến thức: `assessment.md` / `assessment.json`.

## 0. Đọc nhanh (1 phút)

- **30 ngày = 4 tuần + 2 ngày buffer**, khoảng **131 giờ** (ngày thường 4h, cuối tuần 6h; tối đa 136h).
- Cây kiến thức đầy đủ cho mock cần **117 subtopic / 544 giờ** (est_hours_beginner). Kế hoạch giữ **82 subtopic / 92 giờ** mức "làm được bài cơ bản (điểm 2)"; mức 3 đến từ mock và ôn lặp.
- Thứ tự: Python căn bản → Big-O → mảng/chuỗi/hash → prefix sum → hai con trỏ → linked list → stack/queue → binary search/sort → heap → recursion → cây → intervals → graph → AI-enabled + behavioral. **Day 0** (2-3 giờ) là bài chẩn đoán đầu vào, xem `assessment.md`.
- Cuối mỗi tuần: quiz 30 phút + một mock + chấm điểm 0-3. **Đạt khi mỗi subtopic của tuần ≥ 2**; chưa đạt thì dùng buffer, không học tiếp chủ đề mới phụ thuộc vào nó.
- **Đánh giá kiến thức** (layer 2): Day 0 chẩn đoán thích nghi, quiz mỗi cuối tuần, rubric chấm mock, bảng sẵn sàng + go/no-go: xem `assessment.md`.
- Bài luyện hằng ngày **không chứa bài của mock trong lịch** (4 bộ mock tuần + 2 buổi cuối tháng) và không chứa các biến thể/follow-up của chúng trước ngày mock (để mock còn "chưa thấy"); câu mock được liệt kê riêng ("để dành cho mock"). Các bộ mock còn lại (I2, I4, N3-N6) đã được "thả" vào kho bài luyện, xem mục 7.
- Tải bài: ngày thường 4-5 bài (≤ 3 Medium), cuối tuần 5-6 bài (≤ 4 Medium), ngày mock 3 bài; bài Hard và premium nằm ở danh sách "bài thêm" (tùy chọn). Mỗi subtopic DSA có ≥ 2 bài luyện (≥ 3 nếu thuộc Top-40).

## 1. Giả định và cách co giãn

| Giả định | Nội dung |
|---|---|
| Người học | Sinh viên CNTT/gần tốt nghiệp, đã từng viết vài chương trình nhỏ (biết chạy file, `print`, `if`, `for`). Nếu Day 0 cho thấy chưa biết: thêm 6-8 giờ tiền đề trước ngày 1 (cs.onramp + py.core). |
| Track chính | **SWE + Python**. Thuật ngữ giữ tiếng Anh. |
| Thời gian | Ngày thường 4h, thứ Bảy/Chủ nhật 6h. Ngày 29-30 là buffer. Tổng ≈ 130-136h. |
| Mục tiêu | Intern: điểm 2 mọi mục, 3 ở mục "nóng" (xem cột top40). New grad (E3): thêm mock N1/N2 và vòng AI-enabled. |
| Thang điểm | 0 chưa biết · 1 biết lý thuyết · 2 làm được bài cơ bản · 3 mức phỏng vấn (theo `interview-prep/README.md`). |
| Java | Xem mục 9 (ghi chú biến thể Java). |
| AI/ML | Xem mục 8 (gói AI/ML cho I4/N5, thêm ≈ 22 giờ). |

**Co giãn theo thời gian mỗi ngày**

| Thời gian/ngày | Cách làm |
|---|---|
| **2 giờ/ngày** (≈ 65h/tháng) | Kéo thành **8 tuần**, hoặc giữ 4 tuần nhưng chỉ học nhóm A: Python nén, arrays/hash/prefix, two pointers, stack, binary search, cây (basics + BFS), heap top-K, intervals, graph grid BFS/DFS (bỏ: matrix_traversal, sliding_window_fixed, simulation_state_machines, backtracking nâng cao, phần mở rộng của design_o1; giữ string_algorithms, bit_basics, topological_sort vì thuộc Top-40). Mỗi tuần chỉ 1 mock (xen kẽ I1, I3, N2, N1). Bỏ gói AI/ML. |
| **4 giờ/ngày** | Đúng như kế hoạch này. |
| **6 giờ/ngày** (≈ 190h) | Giữ thứ tự, thêm: (1) quay lại các subtopic đã cắt trong bảng mục 2.4 theo thứ tự ưu tiên; (2) làm thêm các mock I2/N3/N4/N6 bằng Python; (3) gói AI/ML đầy đủ; (4) mỗi tuần 2 mock thay vì 1. |

## 2. Phương pháp chọn (script `build_plan.py`)

1. **Lấy** mọi subtopic được 97 câu của 10 bộ mock (`I1..I4`, `N1..N6`) gắn vào. Với track SWE-Python bỏ `ml.*` (sang gói AI/ML) và `java.*`: còn **63** subtopic.
2. **Đóng tiền đề**: thêm mọi `prerequisites` và `lang_prereqs.python` (đệ quy) → **117** subtopic, **544 giờ** (est_hours_beginner, nếu thiếu thì est_hours).
3. **Đổi ra giờ kế hoạch**: giờ = est_hours_beginner × hệ số nén g (Python/CS nền 0.20, DSA 0.26, DSA thuộc Top-40 0.30, behavioral 0.25), làm tròn 0.5h, tối thiểu 0.5h. Riêng `py.core.*` nén còn 0.5h/mục vì Day 0 sẽ cho bỏ qua mục đã biết; mọi mục `py.*` tối đa 1h, `collections_module` và `heapq_bisect` 0.5h (được dạy lại trong hash_tables / heap_ds). Ngày 1 chưa có gì để ôn nên không có phần ôn lặp. Lý do nén: mock I1 ở ngày 7 cần xong 15 giờ Python/CS nền + 9 giờ mảng/hash/prefix/chuỗi trước ngày mock (V6 nghiêm ngặt). Ý nghĩa: đủ để đạt điểm 2 (đọc khái niệm chính + làm 3-5 bài), không đủ để đạt mức 3 của cây.
4. **Miễn (waive / assumed known)** một số mục mà chỉ kéo theo câu hiếm hoặc chuỗi tiền đề dài (bảng 2.3), mỗi mục có lý do.
5. **Chọn câu mock theo giá trị trên giờ biên**: behavioral luôn giữ; LRU Cache, Max Consecutive Ones III và Exclusive Time of Functions được ép giữ (Top-40 hoặc nằm trong mock tuần); còn lại mỗi câu có giá trị = 1 (+2 nếu LC # nằm trong Top-40 coding) (+0.5 mỗi subtopic thuộc Top-40); lần lượt thêm câu có (giá trị)/(giờ biên + 0.25) cao nhất cho tới khi hết **94 giờ** nội dung. Giờ biên = giờ của các subtopic *chưa có* trong tập đã chọn.
6. **Sắp thứ tự**: danh sách `ORDER` trong `plan_data.py` theo `learning_path` của cây (cs → py.core → py.datastructs → py.functions → cs.complexity → dsa phần 1 → py.oop/errors → dsa phần 2 → dsa.practical → bh). Script kiểm tra mọi tiền đề đứng trước.
7. **Xếp ngày**: lần lượt đổ subtopic vào ngày theo sức chứa = ngân sách ngày − ôn lặp (0.5h) − mock/chấm mock/quiz của ngày đó; subtopic có thể chia 2 ngày.

### 2.1 Kết quả

- Giữ **82** subtopic, **91.5h** nội dung; thêm mock/chấm/quiz/ôn lặp để đủ ~131h.
- Bị cắt hoặc coi như đã biết: **30 + 5** subtopic. Câu mock không còn được chuẩn bị đầy đủ: 1 câu (bảng 2.2).

### 2.2 Câu mock bị cắt vì hết giờ (làm sau tháng 1 nếu còn thời gian)

| Câu | LC | Giờ biên cần thêm |
|---|---|---|
| N5-R3-Q1 Moving Average from Data Stream | 346 | 2.5h |

Câu vẫn được chuẩn bị nhưng phần kiến thức phụ bị miễn/cắt (làm bài vẫn được, chỉ thiếu phần mở rộng):

- N1-R5-Q5 [AI] Một lần AI trả lời sai: `eng.testing_quality.code_review`
- N1-R1-Q1 Valid Palindrome II: `dsa.dp.dp_strings`
- N4-R3-Q2 Insert Delete GetRandom O(1): `dsa.design_ds.design_misc`
- N6-R4-Q1 Linked List Random Node (reservoir sampling): `dsa.math_bits.geometry_random`
- N3-R2-Q1 Random Pick with Weight: `dsa.math_bits.geometry_random`
- N1-R4-Q1 AI-enabled: Word list cleanup (đọc code, sửa bug, thêm tính năng, tối ưu): `dsa.tries.trie_problems`
- N4-R1-Q1 Pow(x, n): `dsa.math_bits.number_theory`
- I3-R1-Q1 Best Time to Buy and Sell Stock: `dsa.dp.dp_1d`
- N5-R1-Q2 Buildings With an Ocean View: `dsa.stack_queue.monotonic_stack`

Câu `N6-R1-Q1..Q2` (OA nhiều level, Level 1-2) được làm như mock buffer ở ngày 29 (giờ lấy từ 2.5h của `git_basics`, `modules_packages`, `envs_packaging` bị cắt + 0.5h dư ngày 29); `N6-R1-Q3..Q4` (Level 3-4) và các câu ML coding được bỏ khỏi track chính (ML nằm trong mục 8).

### 2.3 Mục coi như đã biết (assumed known) hoặc miễn (waived)

| Subtopic | Loại | Lý do |
|---|---|---|
| `cs.onramp.computer_programming_model` | assumed known | Bạn đã từng chạy chương trình; Day 0 có 3 câu kiểm tra. Nếu dưới 2 thì thêm 4 giờ tiền đề trước ngày 1. |
| `cs.onramp.terminal_editor_basics` | assumed known | Mở terminal, chạy python file.py, dùng 1 editor; Day 0 kiểm tra 10 phút. |
| `ml.llm.llm_basics_pretraining` | assumed known | Chỉ cần biết LLM là gì để nói chuyện AI trong behavioral; gói trong ngày ai_safety_values (15 phút). |
| `ml.nlp_transformers.tokenization` | assumed known | Chỉ là kiến thức nhận biết cho câu AI behavioral; thuộc gói AI/ML. |
| `cs.computer_basics.data_representation` | assumed known | Chỉ cần nhớ int/float/ký tự; không có câu mock nào hỏi sâu. |
| `eng.testing_quality.code_review` | cắt | Chỉ 1 câu behavioral (N1-R5-Q5); gộp vào ngày verify_ai_output, kéo theo security/networks/debugging nên bỏ nguyên chuỗi. |
| `dsa.practical.bank_ledger_systems` | cắt | OA 4-level (N6) chỉ ở mức PLAUSIBLE; để cho giai đoạn sau tháng 1. |
| `dsa.practical.oop_coding` | cắt | Chỉ phục vụ OA 4-level (N6, plausible); cắt cả inheritance_mro, abc_protocols. |
| `dsa.design_ds.design_time_versioned` | cắt | Chỉ phục vụ OA level 4 (N6, plausible). |
| `py.oop.abc_protocols` | cắt | Chỉ là tiền đề của oop_coding đã cắt. |
| `py.oop.inheritance_mro` | cắt | Chỉ là tiền đề của oop_coding đã cắt. |
| `dsa.dp.dp_strings` | cắt | DP không nằm trong 9 pattern điểm cao nhất; Valid Palindrome II giải bằng two pointers (DP chỉ cho bản mở rộng III). |
| `dsa.dp.dp_1d` | cắt | Best Time to Buy and Sell Stock giải bằng 1 lần duyệt (array_techniques); DP để sau tháng 1. |
| `dsa.heap.heap_advanced` | cắt | Median stream / sliding median là bài khó, TB; heap_top_k đã đủ cho 5 bài top-K. |
| `dsa.design_ds.design_misc` | cắt | Phần Max Stack / O(1) mở rộng; design_o1_structures đã đủ cho Insert Delete GetRandom. |
| `dsa.stack_queue.monotonic_stack` | cắt | Chỉ xuất hiện ở N5 (Buildings With an Ocean View, độ tin cậy TB); học sau tháng 1 nếu còn giờ. |
| `dsa.tries.trie_ds` | cắt | Trie chỉ xuất hiện trong 1 vòng AI-enabled (N1); ưu tiên thấp. |
| `dsa.tries.trie_problems` | cắt | Như trên. |
| `dsa.math_bits.geometry_random` | cắt | Random Pick with Weight / reservoir sampling: chỉ N3, N6; học sau. |
| `dsa.math_bits.number_theory` | cắt | Chỉ học Pow(x, n) (chia để trị) trong recursion_basics (LC 50); Count Primes / số học khác để sau tháng 1. |
| `eng.workflow.git_basics` | cắt | Đổi 1h lấy slot cho N6-R1 Level 1-2 (OA nhiều level) ở ngày 29; git chỉ cần 3 lệnh add/commit/branch, học trong ngày pytest. |
| `py.errors_modules.modules_packages` | cắt | Đổi 0.5h cho slot N6-R1 ngày 29; import module chuẩn đã dùng ở py.core, tự đóng gói để sau. |
| `py.typing_testing.envs_packaging` | cắt | Đổi 1h cho slot N6-R1 ngày 29; venv/pip để sau tháng 1 (mock chạy trong editor có sẵn). |
| `eng.workflow.first_project` | cắt | Giả định bạn có ít nhất 1 dự án trường/cá nhân (cần cho project_deep_dive); nếu chưa có thì dùng buffer để làm dự án nhỏ. |

### 2.4 Toàn bộ subtopic nằm trong đóng tiền đề nhưng không được học (thứ tự ưu tiên học thêm khi có thời gian)

| Subtopic | Giờ (beginner) | Lý do |
|---|---|---|
| `cs.networks.http` | 4 | Không còn subtopic nào được giữ cần đến nó (tiền đề của mục đã cắt) |
| `cs.networks.models` | 4 | Không còn subtopic nào được giữ cần đến nó (tiền đề của mục đã cắt) |
| `cs.networks.tcp_udp` | 5 | Không còn subtopic nào được giữ cần đến nó (tiền đề của mục đã cắt) |
| `dsa.design_ds.design_misc` | 5 | Phần Max Stack / O(1) mở rộng; design_o1_structures đã đủ cho Insert Delete GetRandom. |
| `dsa.design_ds.design_time_versioned` | 5 | Chỉ phục vụ OA level 4 (N6, plausible). |
| `dsa.dp.dp_1d` | 6 | Best Time to Buy and Sell Stock giải bằng 1 lần duyệt (array_techniques); DP để sau tháng 1. |
| `dsa.dp.dp_foundations` | 4 | Không còn subtopic nào được giữ cần đến nó (tiền đề của mục đã cắt) |
| `dsa.dp.dp_strings` | 6 | DP không nằm trong 9 pattern điểm cao nhất; Valid Palindrome II giải bằng two pointers (DP chỉ cho bản mở rộng III). |
| `dsa.heap.heap_advanced` | 6 | Median stream / sliding median là bài khó, TB; heap_top_k đã đủ cho 5 bài top-K. |
| `dsa.math_bits.geometry_random` | 3 | Random Pick with Weight / reservoir sampling: chỉ N3, N6; học sau. |
| `dsa.math_bits.number_theory` | 6 | Chỉ học Pow(x, n) (chia để trị) trong recursion_basics (LC 50); Count Primes / số học khác để sau tháng 1. |
| `dsa.practical.bank_ledger_systems` | 6 | OA 4-level (N6) chỉ ở mức PLAUSIBLE; để cho giai đoạn sau tháng 1. |
| `dsa.practical.oop_coding` | 5 | Chỉ phục vụ OA 4-level (N6, plausible); cắt cả inheritance_mro, abc_protocols. |
| `dsa.practical.stream_iterator_processing` | 6 | Chỉ phục vụ: N5-R3-Q1 (hết giờ hoặc ưu tiên thấp) |
| `dsa.recursion_backtracking.backtracking_constraints` | 6 | Không còn subtopic nào được giữ cần đến nó (tiền đề của mục đã cắt) |
| `dsa.stack_queue.monotonic_stack` | 6 | Chỉ xuất hiện ở N5 (Buildings With an Ocean View, độ tin cậy TB); học sau tháng 1 nếu còn giờ. |
| `dsa.tries.trie_ds` | 3 | Trie chỉ xuất hiện trong 1 vòng AI-enabled (N1); ưu tiên thấp. |
| `dsa.tries.trie_problems` | 5 | Như trên. |
| `eng.security.owasp` | 5 | Không còn subtopic nào được giữ cần đến nó (tiền đề của mục đã cắt) |
| `eng.testing_quality.code_review` | 5 | Chỉ 1 câu behavioral (N1-R5-Q5); gộp vào ngày verify_ai_output, kéo theo security/networks/debugging nên bỏ nguyên chuỗi. |
| `eng.testing_quality.debugging_methodology` | 6 | Không còn subtopic nào được giữ cần đến nó (tiền đề của mục đã cắt) |
| `eng.testing_quality.unit_testing` | 4 | Không còn subtopic nào được giữ cần đến nó (tiền đề của mục đã cắt) |
| `eng.workflow.first_project` | 6 | Giả định bạn có ít nhất 1 dự án trường/cá nhân (cần cho project_deep_dive); nếu chưa có thì dùng buffer để làm dự án nhỏ. |
| `eng.workflow.git_basics` | 5 | Đổi 1h lấy slot cho N6-R1 Level 1-2 (OA nhiều level) ở ngày 29; git chỉ cần 3 lệnh add/commit/branch, học trong ngày pytest. |
| `eng.workflow.linux_shell` | 5 | Không còn subtopic nào được giữ cần đến nó (tiền đề của mục đã cắt) |
| `py.errors_modules.modules_packages` | 3 | Đổi 0.5h cho slot N6-R1 ngày 29; import module chuẩn đã dùng ở py.core, tự đóng gói để sau. |
| `py.functions.iterators_generators` | 7 | Không còn subtopic nào được giữ cần đến nó (tiền đề của mục đã cắt) |
| `py.oop.abc_protocols` | 5 | Chỉ là tiền đề của oop_coding đã cắt. |
| `py.oop.inheritance_mro` | 7 | Chỉ là tiền đề của oop_coding đã cắt. |
| `py.typing_testing.envs_packaging` | 4 | Đổi 1h cho slot N6-R1 ngày 29; venv/pip để sau tháng 1 (mock chạy trong editor có sẵn). |

## 3. Tổng quan 4 tuần + 2 ngày buffer

### Tuần 1 (ngày 1-7): Nền tảng: Python căn bản, Big-O, mảng, chuỗi, hash, prefix sum

- **Mục tiêu**: Viết được lời giải cho bài easy dùng list/dict/string; nói được time/space; làm xong mock I1 Technical 1.
- **Subtopic**: `py.core.getting_started`, `py.core.variables_types`, `py.core.operators`, `py.core.conditionals`, `py.core.loops`, `py.core.strings`, `py.datastructs.list`, `py.datastructs.tuple_namedtuple`, `py.datastructs.dict`, `py.datastructs.comprehensions`, `py.datastructs.collections_module`, `py.datastructs.copying_mutability`, `py.datastructs.heapq_bisect`, `py.functions.def_args`, `py.functions.lambda_hof`, `py.functions.sorting_keys`, `cs.complexity.big_o`, `dsa.foundations.memory_model`, `dsa.foundations.lib_toolkit`, `dsa.arrays_strings.arrays`, `dsa.arrays_strings.hash_tables`, `dsa.arrays_strings.hashing_patterns`, `dsa.arrays_strings.prefix_sum`, `dsa.arrays_strings.strings_basics`, `dsa.arrays_strings.string_algorithms`, `py.functions.scope_closures`, `dsa.arrays_strings.array_techniques`, `dsa.two_pointers_window.two_pointers`
- **Mock cuối tuần**: I1 Technical 1 (ngày 7)
  - Ngày 7: *I1 - Technical 1*, 45 phút làm + 45 phút chấm. Câu: I1-R1-Q1 Find Pivot Index (LC 724); I1-R1-Q2 Add Strings (LC 415)
- **Checkpoint cuối tuần**: quiz tuần (30 phút, xem `assessment.md` mục 2) + tự chấm điểm 0-3 từng subtopic của tuần. **Qua** = mọi subtopic ≥ 2 (và điểm mock ≥ 2 ở trục Correctness). Chưa qua: xem mục 11.3.

### Tuần 2 (ngày 8-14): Hai con trỏ, linked list, stack/queue, recursion, binary search, sorting, heap top-K, sliding window

- **Mục tiêu**: Nhận ra 6 pattern cơ bản (two pointers, sliding window, linked list, stack, binary search, heap top-K) và code không bug cho bài easy-medium.
- **Subtopic**: `py.oop.classes_basics`, `dsa.linked_list.ll_basics`, `dsa.linked_list.ll_manipulation`, `dsa.stack_queue.stack_queue_ds`, `dsa.stack_queue.stack_problems`, `dsa.stack_queue.parsing_strings`, `dsa.foundations.interview_method`, `bh.method.self_intro`, `bh.method.star_carl`, `dsa.recursion_backtracking.recursion_basics`, `dsa.searching_sorting.binary_search_basics`, `dsa.searching_sorting.sorting_algorithms`, `dsa.searching_sorting.sorting_applications`, `dsa.trees.tree_basics`, `dsa.heap.heap_ds`, `dsa.heap.heap_top_k`, `dsa.searching_sorting.binary_search_variants`, `dsa.two_pointers_window.sliding_window_fixed`, `dsa.two_pointers_window.sliding_window_variable`, `bh.stories.conflict_teamwork`, `bh.stories.failure_feedback`, `dsa.recursion_backtracking.backtracking_core`
- **Mock cuối tuần**: I3 Technical 1 + 2 (ngày 14)
  - Ngày 14: *I3 - Technical 1 + 2*, 90 phút làm + 60 phút chấm. Câu: I3-R1-Q1 Best Time to Buy and Sell Stock (LC 121); I3-R1-Q2 Kth Largest Element in an Array (LC 215); I3-R2-Q1 Friends Of Appropriate Ages (LC 825); I3-R2-Q2 Simplify Path (LC 71)
- **Checkpoint cuối tuần**: quiz tuần (30 phút, xem `assessment.md` mục 2) + tự chấm điểm 0-3 từng subtopic của tuần. **Qua** = mọi subtopic ≥ 2 (và điểm mock ≥ 2 ở trục Correctness). Chưa qua: xem mục 11.3.

### Tuần 3 (ngày 15-21): Backtracking, cây (DFS/BFS/BST), design cache, intervals, matrix, file/log, graph cơ bản

- **Mục tiêu**: Tự tin với cây (đệ quy + BFS), LRU Cache, intervals, duyệt đồ thị cơ bản; làm xong phone screen + 1 vòng coding kiểu new grad (N2).
- **Subtopic**: `dsa.recursion_backtracking.backtracking_core`, `dsa.trees.tree_recursion`, `dsa.trees.tree_bfs_views_hierarchy`, `dsa.trees.bst`, `dsa.design_ds.design_cache`, `dsa.design_ds.design_o1_structures`, `dsa.greedy_intervals.interval_basics`, `dsa.greedy_intervals.interval_sweep`, `dsa.arrays_strings.matrix_traversal`, `bh.stories.ownership_leadership`, `bh.stories.prioritization_ambiguity`, `py.core.io_input`, `py.core.try_except_basics`, `py.core.regex`, `py.errors_modules.files_pathlib`, `dsa.practical.file_log_parsing`, `dsa.graphs.graph_representation`, `dsa.graphs.graph_traversal`, `dsa.graphs.grid_graphs`, `dsa.graphs.bfs_shortest_path`, `dsa.graphs.topological_sort`
- **Mock cuối tuần**: N2 Phone screen + Onsite coding 1 (ngày 21)
  - Ngày 21: *N2 - Phone screen + Onsite coding 1*, 90 phút làm + 75 phút chấm. Câu: N2-R1-Q1 Binary Tree Vertical Order Traversal (LC 314); N2-R1-Q2 Find Peak Element (LC 162); N2-R2-Q1 Subarray Sum Equals K (LC 560); N2-R2-Q2 LRU Cache (LC 146)
- **Checkpoint cuối tuần**: quiz tuần (30 phút, xem `assessment.md` mục 2) + tự chấm điểm 0-3 từng subtopic của tuần. **Qua** = mọi subtopic ≥ 2 (và điểm mock ≥ 2 ở trục Correctness). Chưa qua: xem mục 11.3.

### Tuần 4 (ngày 22-28): Shortest path, topological sort, bit, coding thực tế + pytest, AI-enabled, behavioral + AI, luyện tổng hợp, mock toàn bộ

- **Mục tiêu**: Giải bài grid/graph cơ bản, làm quen vòng AI-enabled, có đủ story behavioral; thi thử N1 (3 vòng) + N2 AI-enabled + 2 behavioral.
- **Subtopic**: `dsa.graphs.topological_sort`, `dsa.math_bits.bit_basics`, `dsa.practical.practical_format`, `dsa.practical.simulation_state_machines`, `dsa.practical.refactor_debug_review`, `py.errors_modules.exceptions`, `py.typing_testing.pytest_testing`, `dsa.practical.ai_assisted_coding`, `bh.stories.project_deep_dive`, `bh.motivation.why_company`, `bh.ai_fluency.ai_workflow`, `bh.ai_fluency.verify_ai_output`, `bh.ai_fluency.ai_safety_values`
- **Mock cuối tuần**: N1 (ngày 27), N2 AI-enabled + behavioral (ngày 28)
  - Ngày 27: *N1 - Phone screen + Onsite coding 1 + 2*, 135 phút làm + 60 phút chấm. Câu: N1-R1-Q1 Valid Palindrome II (LC 680); N1-R1-Q2 Top K Frequent Elements (LC 347); N1-R2-Q1 Merge Intervals (LC 56); N1-R2-Q2 Binary Tree Right Side View (LC 199); N1-R3-Q1 Minimum Remove to Make Valid Parentheses (LC 1249); N1-R3-Q2 Dot Product of Two Sparse Vectors (LC 1570)
  - Ngày 28: *N2 AI-enabled + N2 Behavioral + N1 Behavioral*, 150 phút làm + 75 phút chấm. Câu: N2-R4-Q1 AI-enabled: Card game "Pick 15" (sum-fifteen); N2-R5-Q1 Dự án bạn tự hào nhất; N2-R5-Q2 Hạn chót bị dời sớm; N2-R5-Q3 Vì sao Meta?; N2-R5-Q4 Nhận phản hồi khó; N2-R5-Q5 [AI] Trách nhiệm với code do AI viết; N1-R5-Q1 Project bạn tự hào nhất; N1-R5-Q2 Bất đồng với bạn cùng nhóm; N1-R5-Q3 Một lần bạn mắc lỗi hoặc thất bại; N1-R5-Q4 [AI] Bạn dùng AI khi học và làm dự án như thế nào?; N1-R5-Q5 [AI] Một lần AI trả lời sai
- **Checkpoint cuối tuần**: quiz tuần (30 phút, xem `assessment.md` mục 2) + tự chấm điểm 0-3 từng subtopic của tuần. **Qua** = mọi subtopic ≥ 2 (và điểm mock ≥ 2 ở trục Correctness). Chưa qua: xem mục 11.3.

### Ngày 29-30: Buffer + đánh giá cuối tháng

- **Mục tiêu**: Bù bài còn thiếu, làm N2 Onsite coding 2 và OA N6 Level 1-2 (chưa có bài nào dùng tới trước đó), chạy lại chẩn đoán, điền bảng sẵn sàng.
- **Subtopic**: không học mới; bù phần còn thiếu
- **Mock cuối tuần**: N2 Onsite coding 2 + N6 OA Level 1-2 (ngày 29)
  - Ngày 29: *N2 - Onsite coding 2 + N6 OA Level 1-2 (buffer)*, 90 phút làm + 45 phút chấm. Câu: N2-R3-Q1 Exclusive Time of Functions (LC 636); N2-R3-Q2 Number of Islands (LC 200); N6-R1-Q1 Level 1 - Tài khoản cơ bản: create / deposit / transfer (LC -); N6-R1-Q2 Level 2 - Top spenders (xếp hạng chi tiêu) (LC -)

## 4. Kế hoạch từng ngày

**Day 0 (trước ngày 1, 2-3 giờ)**: làm chẩn đoán đầu vào trong `assessment.md` mục 1, điền điểm 0-3 vào `tracking.csv`, rồi điều chỉnh giờ từng subtopic theo bảng 1.4 của file đó (điểm 2-3 → nén/bỏ, điểm 0 → thêm giờ). Plan bên dưới là bản chuẩn cho người ở mức điểm 1.

Quy ước: **Học** = đọc + xem ví dụ + viết lại bằng tay; **Luyện** = làm bài; **Ôn** = ôn lặp D+1/D+3/D+7 và ghi nhật ký lỗi. ★ = bài thuộc nhóm "dự đoán" của Meta (predicted_questions.md); 🔊 = nói to khi code (nói đề, ví dụ, ý tưởng, độ phức tạp, test); `(premium)` = cần LeetCode Premium, có thể thay bằng bài tương tự cùng chủ đề.

### Ngày 1 · Thứ Hai · tuần 1 · 4h: Bắt đầu; Biến, kiểu dữ liệu và dynamic typing; Toán tử, biểu thức và số ...

**Subtopic**

- `py.core.getting_started` — Bắt đầu: chạy Python, cú pháp và quy ước (getting started) · 0.5h
- `py.core.variables_types` — Biến, kiểu dữ liệu và dynamic typing (variables & types) · 0.5h
- `py.core.operators` — Toán tử, biểu thức và số (operators & numbers) · 0.5h
- `py.core.conditionals` — Rẽ nhánh và truthiness (conditionals) · 0.5h
- `py.core.loops` — Vòng lặp (loops) · 0.5h
- `py.core.strings` — Chuỗi và xử lý văn bản (strings) · 1h
- `py.datastructs.list` — Danh sách (list) — chia 2 ngày · 0.5h

**Học gì**

- Bắt đầu: chạy Python, cú pháp và quy ước: REPL: chỗ gõ từng dòng Python và thấy kết quả ngay (dấu >>>); gõ python (hoặc python3) trong terminal để vào, exit() để thoát; Script (tệp lệnh): file .py chạy cả file một lần bằng lệnh python ten.py; Indentation (thụt đầu dòng): Python dùng 4 dấu cách đầu dòng để biết lệnh nào thuộc khối nào; print() in kết quả ra màn hình; comment (chú thích) bắt đầu bằng # và Python bỏ qua
- Biến, kiểu dữ liệu và dynamic typing: Biến (variable): tên gắn với một giá trị, ví dụ ten = 'An'; gán lại thì nhãn chuyển sang giá trị mới; Kiểu dữ liệu (type): int số nguyên, float số thập phân, str chữ, bool True/False; type(x) cho biết kiểu của x; Đổi kiểu: int('5') đổi chữ thành số, str(5) đổi số thành chữ; hay dùng khi nhập số: int(input()); None: giá trị đặc biệt nghĩa là 'chưa có gì'
- Toán tử, biểu thức và số: Số học: + - * /, ** là lũy thừa; / luôn ra số thập phân (7 / 2 = 3.5); x += 1 là x = x + 1; dùng ngoặc cho rõ thứ tự; // chia lấy phần nguyên, % lấy số dư: 7 // 2 = 3 và 7 % 2 = 1 (chia 7 cái kẹo cho 2 bạn, mỗi bạn 3, còn dư 1); So sánh ==, !=, <, >=; viết nối được 1 < a < 5; kết quả là True hoặc False; and, or, not nối các điều kiện; and/or dừng ngay khi đã biết kết quả: x != 0 and 10 / x > 1 không báo lỗi chia cho 0 khi x = 0
- Rẽ nhánh và truthiness: if / elif / else: chạy khối lệnh đầu tiên có điều kiện đúng, ví dụ nếu điểm >= 5 thì in 'đậu', không thì in 'rớt'; Sau điều kiện có dấu hai chấm (:) và khối lệnh bên dưới phải thụt đầu dòng; Falsy (coi là sai): 0, chuỗi rỗng '', None (cả list rỗng, học ở mục sau); các giá trị còn lại coi là đúng; Kiểm tra None bằng x is None, không viết x == None
- Vòng lặp: for i in range(5) lặp i = 0, 1, 2, 3, 4; range(a, b) đi từ a đến b-1, range(a, b, c) nhảy c bước; for ch in 'abc' duyệt từng ký tự của chuỗi; biến lặp lấy lần lượt từng phần tử; while điều_kiện: lặp đến khi điều kiện sai, dùng khi chưa biết trước số lần; nhớ cập nhật biến để không lặp mãi; break thoát khỏi vòng lặp ngay; continue bỏ phần còn lại của lượt này và sang lượt tiếp
- Chuỗi và xử lý văn bản: Chuỗi viết trong dấu nháy: 'xin chào'; len(s) là số ký tự; s[0] là ký tự đầu, s[-1] là ký tự cuối; Slicing (cắt chuỗi): s[0:3] lấy ký tự ở vị trí 0, 1, 2; s[::-1] đảo ngược chuỗi; Chuỗi không sửa tại chỗ được (immutable): s.upper() trả về chuỗi mới, s vẫn như cũ; Method (hàm gọi bằng dấu chấm sau chuỗi, như s.upper()) hay dùng: lower, upper, strip (bỏ khoảng trắng hai đầu), replace(a, b) thay a bằng b, find(a) (xem skill_tree)
- Danh sách: Tạo và lấy phần tử: diem = [8, 9, 7]; diem[0] là 8, diem[-1] là 7; len(diem) là số phần tử; List sửa được tại chỗ (mutable): diem[1] = 10; append(5) thêm cuối; pop() lấy phần tử cuối; remove(7) xóa theo giá trị; Slicing (cắt): diem[0:2] lấy một đoạn thành list mới; diem[::-1] đảo ngược; extend nối thêm nhiều phần tử; Duyệt: for d in diem; for i, d in enumerate(diem) có thêm vị trí; zip(a, b) duyệt hai list song song

**Thời gian** (tổng 4h/4h): Học 120p · Luyện 120p · 

**Bài luyện (không phải bài mock)** · 5 bài

1. LC 2235 Add Two Integers (E) — `py.core.getting_started`
2. LC 1512 Number of Good Pairs (E) — `py.core.variables_types`
3. LC 1281 Subtract the Product and Sum of Digits of an Integer (E) — `py.core.operators`
4. LC 412 Fizz Buzz (E) — `py.core.conditionals`
5. LC 263 Ugly Number (E) — `py.core.loops`

**Bài thêm nếu còn giờ (tùy chọn, không tính vào số bài của ngày)**: LC 1920 Build Array from Permutation (E); LC 2011 Final Value of Variable After Performing Operations (E); LC 9 Palindrome Number (E); LC 2413 Smallest Even Multiple (E); LC 709 To Lower Case (E); LC 344 Reverse String (E); LC 58 Length of Last Word (E); LC 14 Longest Common Prefix (E)

### Ngày 2 · Thứ Ba · tuần 1 · 4h: Danh sách; Tuple, unpacking và namedtuple; Từ điển và tập hợp ...

**Subtopic**

- `py.datastructs.list` — Danh sách (list) (tiếp) — chia 2 ngày · 0.5h
- `py.datastructs.tuple_namedtuple` — Tuple, unpacking và namedtuple · 0.5h
- `py.datastructs.dict` — Từ điển và tập hợp (dict & set) · 1h
- `py.datastructs.comprehensions` — Comprehension và generator expression · 1h
- `py.datastructs.collections_module` — Module collections (Counter, deque, defaultdict) · 0.5h

**Học gì**

- Tuple, unpacking và namedtuple: Tuple viết (3, 4); lấy phần tử như list (t[0]) nhưng không gán lại được; tuple một phần tử viết (5,); Unpacking (tách): x, y = (3, 4) gán x = 3, y = 4; a, b = b, a hoán đổi hai biến; Hàm trả nhiều giá trị thực chất trả một tuple, bên ngoài nhận bằng unpacking; Dùng tuple cho dữ liệu cố định (toạ độ, ngày), list khi cần thêm bớt
- Từ điển và tập hợp: Dict: sdt = {'An': '0901', 'Binh': '0902'}; sdt['An'] tra theo khóa; sdt['Chi'] = '0903' thêm hoặc sửa; Tra khóa không có sẽ báo KeyError; sdt.get('X', mặc_định) trả giá trị mặc định; 'An' in sdt kiểm tra khóa; Duyệt: for k in d; d.values(); for k, v in d.items(); dict nhớ thứ tự thêm vào; Khóa phải là giá trị không đổi (số, chuỗi, tuple chỉ chứa giá trị không đổi), không phải list: Python tính từ khóa một mã số (hash) để tra rất nhanh
- Comprehension và generator expression: List comprehension: [x*2 for x in so] nhân đôi mọi số, tương đương vòng for kèm append; Thêm điều kiện lọc ở cuối: [x for x in so if x > 0] chỉ giữ số dương; if/else đặt trước for: ['chẵn' if x % 2 == 0 else 'lẻ' for x in so]; Dict và set comprehension: {w: len(w) for w in tu}, {x % 3 for x in so}
- Module collections: Module cần import trước khi dùng: from collections import Counter, defaultdict, deque; Counter('banana') đếm được a:3, n:2, b:1; most_common(2) trả hai phần tử xuất hiện nhiều nhất; defaultdict(list): tra khóa chưa có sẽ tự tạo list rỗng, tiện cho việc nhóm phần tử theo khóa; deque: hàng đợi, người vào xếp cuối và người ra từ đầu (vào trước ra trước); popleft() nhanh còn list.pop(0) chậm

**Thời gian** (tổng 4h/4h): Học 105p · Luyện 105p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p

**Bài luyện (không phải bài mock)** · 5 bài

1. LC 1929 Concatenation of Array (E) — `py.datastructs.list`
2. LC 832 Flipping an Image (E) — `py.datastructs.tuple_namedtuple`
3. LC 383 Ransom Note (E) — `py.datastructs.dict`
4. LC 1365 How Many Numbers Are Smaller Than the Current Number (E) — `py.datastructs.comprehensions`
5. LC 169 Majority Element (E) — `py.datastructs.collections_module`

**Bài thêm nếu còn giờ (tùy chọn, không tính vào số bài của ngày)**: LC 1470 Shuffle the Array (E); LC 1480 Running Sum of 1d Array (E); LC 1672 Richest Customer Wealth (E); LC 561 Array Partition (E); LC 387 First Unique Character in a String (E); LC 1431 Kids With the Greatest Number of Candies (E); LC 349 Intersection of Two Arrays (E)

**Ôn lặp**: D+1: LC 263 Ugly Number (ngày 1): viết lại không nhìn lời giải

### Ngày 3 · Thứ Tư · tuần 1 · 4h: Mutability, aliasing và sao chép; heapq và bisect; Định nghĩa hàm và đối số ...

**Subtopic**

- `py.datastructs.copying_mutability` — Mutability, aliasing và sao chép (copying) · 1h
- `py.datastructs.heapq_bisect` — heapq và bisect · 0.5h
- `py.functions.def_args` — Định nghĩa hàm và đối số (functions & arguments) · 1h
- `py.functions.lambda_hof` — Lambda và hàm bậc cao (higher-order functions) · 0.5h
- `py.functions.sorting_keys` — Sắp xếp với key và tính ổn định (sorting) — chia 2 ngày · 0.5h

**Học gì**

- Mutability, aliasing và sao chép: Mutable (sửa tại chỗ được): list, dict, set. Immutable (không sửa được, chỉ tạo giá trị mới): số, chuỗi, tuple; Aliasing (hai tên, một vật): b = a không sao chép; a.append(3) thì b cũng thấy; a is b là True; Sao chép nông (shallow copy): b = a.copy(), list(a), a[:]; chỉ chép lớp ngoài; Sao chép sâu (deep copy): import copy rồi copy.deepcopy(a) chép cả list nằm bên trong
- heapq và bisect: Heap (đống): cấu trúc luôn lấy ra phần tử nhỏ nhất rất nhanh; heapq chỉ lấy nhỏ nhất; muốn lấy lớn nhất thì đẩy số âm (-x) vào rồi đổi dấu khi lấy ra; Ví dụ: heappush lần lượt 5, 1, 3 vào heap rỗng; heappop ba lần ra 1, 3, 5 (luôn ra số nhỏ nhất còn lại); heapq.nlargest(k, ds) và nsmallest(k, ds) lấy k phần tử lớn nhất hoặc nhỏ nhất
- Định nghĩa hàm và đối số: def tinh_tong(a, b): return a + b; gọi tinh_tong(2, 3) cho 5; hàm không có return thì trả None; Tham số (parameter) là tên trong dòng def; đối số (argument) là giá trị đưa vào khi gọi; Truyền đối số theo vị trí hoặc theo tên: f(1, 2) và f(b=2, a=1); Giá trị mặc định: def chao(ten='bạn') dùng 'bạn' nếu không đưa đối số
- Lambda và hàm bậc cao: lambda x: x * 2 là hàm một dòng, tương đương def nhan_doi(x): return x * 2; chỉ chứa một biểu thức; Hàm là một giá trị: gán vào biến, đưa làm đối số cho hàm khác hoặc trả về từ hàm; Hàm bậc cao (higher-order function): hàm nhận hàm khác làm đối số hoặc trả về một hàm, như sorted(key=...), map, filter; sorted(ds, key=lambda s: len(s)) xếp theo độ dài; key cho biết 'xếp theo cái gì'
- Sắp xếp với key và tính ổn định: sorted(ds) trả list mới đã xếp, ds.sort() sửa ngay list gốc và trả None; reverse=True xếp giảm dần; chuỗi xếp theo thứ tự chữ cái, chữ hoa đứng trước chữ thường; key là hàm cho mỗi phần tử một 'khóa' để so sánh: key=len, key=lambda s: s[1]; Nhiều tiêu chí: key=lambda s: (-s[1], s[0]) xếp điểm giảm dần rồi tên tăng dần (dấu - đảo chiều số)

**Thời gian** (tổng 4h/4h): Học 105p · Luyện 105p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p

**Bài luyện (không phải bài mock)** · 5 bài

1. LC 118 Pascal's Triangle (E) — `py.datastructs.copying_mutability`
2. LC 1389 Create Target Array in the Given Order (E) — `py.functions.def_args`
3. LC 509 Fibonacci Number (E) — `py.functions.def_args`
4. LC 1051 Height Checker (E) — `py.functions.lambda_hof`
5. LC 189 Rotate Array (M) — `py.datastructs.copying_mutability`

**Ôn lặp**: D+1: LC 169 Majority Element (ngày 2): viết lại không nhìn lời giải

### Ngày 4 · Thứ Năm · tuần 1 · 4h: Sắp xếp với key và tính ổn định; Ký hiệu tiệm cận Big-O, Theta, Omega; Mô hình bộ nhớ ...

**Subtopic**

- `py.functions.sorting_keys` — Sắp xếp với key và tính ổn định (sorting) (tiếp) — chia 2 ngày · 0.5h
- `cs.complexity.big_o` — Ký hiệu tiệm cận Big-O, Theta, Omega (asymptotic notation) · 0.5h
- `dsa.foundations.memory_model` — Mô hình bộ nhớ: mảng, tham chiếu, stack và heap (memory model) · 0.5h
- `dsa.foundations.lib_toolkit` — Chọn đúng cấu trúc dữ liệu và công cụ thư viện (data structure selection) · 1.5h
- `dsa.arrays_strings.arrays` — Mảng và mảng động (array, dynamic array) — chia 2 ngày · 0.5h

**Học gì**

- Ký hiệu tiệm cận Big-O, Theta, Omega: Big-O, viết O(...): ước lượng số bước theo cỡ dữ liệu n; duyệt n phần tử một lần là O(n); Bỏ hằng số và phần nhỏ: O(2n) và O(n + 5) đều là O(n); khi n lớn chỉ phần lớn nhất quan trọng; Các mức hay gặp từ nhanh đến chậm: O(1) hằng, O(log n) chia đôi liên tục, O(n), O(n log n), O(n²) hai vòng lồng nhau, O(2ⁿ); Với n = 1000: log n ≈ 10 (log ở đây là log cơ số 2: số lần chia đôi n tới 1), n log n ≈ 10 000, n² = 1 triệu, 2ⁿ ≈ 10³⁰¹ (số khổng lồ)
- Mô hình bộ nhớ: mảng, tham chiếu, stack và heap: Ô nhớ liền nhau (contiguous memory): list lưu các phần tử sát nhau nên ô thứ i tính ra ngay từ ô đầu, do đó lấy theo chỉ số là O(1); Tham chiếu (reference): biến Python là nhãn dán vào một đối tượng, không chứa đối tượng; b = a chỉ dán thêm một nhãn; Aliasing: hai tên cùng trỏ một list, sửa qua tên này thì tên kia thấy. Ví dụ [[0]*3]*3 tạo 3 hàng là cùng một list; Truyền tham số (parameter passing): hàm nhận nhãn tới cùng đối tượng; sửa tại chỗ (append) lộ ra ngoài, gán lại (x = ...) thì không
- Chọn đúng cấu trúc dữ liệu và công cụ thư viện: Bảng chọn: cần tra theo key dùng dict; hỏi có hay không dùng set; giữ thứ tự và truy cập theo chỉ số dùng list; thêm bớt hai đầu dùng deque; Chi phí thao tác: dict/set tra O(1) trung bình; `x in list` và list.insert(0, x) là O(n); deque.popleft là O(1); Đếm và nhóm: Counter đếm số lần xuất hiện; defaultdict(list) gom các phần tử cùng khoá vào một list; Sắp xếp theo khoá: sorted(a, key=...) sắp theo nhiều tiêu chí, reverse=True để giảm dần; sắp xếp ổn định (bằng nhau giữ thứ tự cũ)
- Mảng và mảng động: Mảng cố định (fixed array) có kích thước chọn trước; mảng động (dynamic array) tự lớn thêm khi đầy. List của Python là mảng động; Lấy hoặc gán theo chỉ số là O(1); chèn hoặc xoá ở giữa là O(n) vì phải dời các phần tử phía sau; append là O(1) trung bình (amortized): khi hết chỗ, xin dãy ô mới lớn hơn nhiều lần (ví dụ gấp đôi; CPython tăng ~1,125 lần) rồi chép sang (resize); Tự cài mảng động: viết class giữ một list kích thước cố định (capacity) và biến size; đầy thì tạo list gấp đôi rồi chép sang

**Thời gian** (tổng 4h/4h): Học 75p · Luyện 135p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p

**Bài luyện (không phải bài mock)** · 5 bài

1. LC 268 Missing Number (E) — `cs.complexity.big_o`
2. LC 1313 Decompress Run-Length Encoded List (E) — `cs.complexity.big_o`
3. LC 1572 Matrix Diagonal Sum (E) — `dsa.foundations.memory_model`
4. LC 937 Reorder Data in Log Files (M) — `py.functions.sorting_keys`
5. LC 692 Top K Frequent Words (M) ★ — `dsa.foundations.lib_toolkit`

**Bài thêm nếu còn giờ (tùy chọn, không tính vào số bài của ngày)**: LC 1331 Rank Transform of an Array (E)

**Ôn lặp**: D+1: LC 189 Rotate Array (ngày 3): viết lại không nhìn lời giải · D+3: LC 2235 Add Two Integers (ngày 1): viết lại không nhìn lời giải

### Ngày 5 · Thứ Sáu · tuần 1 · 4h: Mảng và mảng động; Hash table và hash set; Pattern dùng hash

**Subtopic**

- `dsa.arrays_strings.arrays` — Mảng và mảng động (array, dynamic array) (tiếp) — chia 2 ngày · 1h
- `dsa.arrays_strings.hash_tables` — Hash table và hash set (hash table internals) · 2h
- `dsa.arrays_strings.hashing_patterns` — Pattern dùng hash: đếm tần suất, bù trừ, nhóm (hashing patterns) — chia 2 ngày · 0.5h

**Học gì**

- Hash table và hash set: Hàm băm (hash function): biến key thành một số, rồi chia dư cho số ô để ra chỉ số trong mảng; Đụng độ (collision): hai key băm ra cùng ô. Cách đơn giản (chaining): mỗi ô là một list nhỏ chứa các cặp key-value; Hệ số đầy (load factor) và băm lại (rehash): khi bảng quá đầy thì tạo bảng to hơn rồi xếp lại mọi key; Độ phức tạp: tra, thêm, xoá là O(1) trung bình, nhưng O(n) ở trường hợp xấu nhất khi mọi key đụng nhau
- Pattern dùng hash: đếm tần suất, bù trừ, nhóm: Đếm tần suất (frequency counting): dict hoặc Counter ghi mỗi phần tử xuất hiện mấy lần; Tìm số bù (complement lookup): với mỗi x, hỏi sổ xem đã gặp (target - x) chưa. Đó là bài Two Sum; Tập đã gặp (seen set): phát hiện phần tử trùng, hoặc bỏ trùng mà vẫn giữ thứ tự xuất hiện đầu tiên; Nhóm theo khoá chuẩn (canonical key): đưa các phần tử 'giống nhau' về cùng một dạng để cùng key, ví dụ sắp xếp chữ cái của từ

**Thời gian** (tổng 4h/4h): Học 75p · Luyện 135p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p

**Bài luyện (không phải bài mock)** · 5 bài

1. LC 485 Max Consecutive Ones (E) — `dsa.arrays_strings.arrays`
2. LC 1295 Find Numbers with Even Number of Digits (E) — `dsa.arrays_strings.arrays`
3. LC 1089 Duplicate Zeros (E) — `dsa.arrays_strings.arrays`
4. LC 205 Isomorphic Strings (E) — `dsa.arrays_strings.hash_tables`
5. LC 49 Group Anagrams (M) — `dsa.arrays_strings.hash_tables`

**Bài thêm nếu còn giờ (tùy chọn, không tính vào số bài của ngày)**: LC 290 Word Pattern (E); LC 128 Longest Consecutive Sequence (M)

**Ôn lặp**: D+1: LC 692 Top K Frequent Words (ngày 4): viết lại không nhìn lời giải · D+3: LC 1929 Concatenation of Array (ngày 2): viết lại không nhìn lời giải

### Ngày 6 · Thứ Bảy · tuần 1 · 6h: Pattern dùng hash; Prefix sum và difference array; Chuỗi cơ bản ...

**Subtopic**

- `dsa.arrays_strings.hashing_patterns` — Pattern dùng hash: đếm tần suất, bù trừ, nhóm (hashing patterns) (tiếp) — chia 2 ngày · 1h
- `dsa.arrays_strings.prefix_sum` — Prefix sum và difference array (prefix sums) · 1h
- `dsa.arrays_strings.strings_basics` — Chuỗi cơ bản (string fundamentals) · 1.5h
- `dsa.arrays_strings.string_algorithms` — Thuật toán chuỗi: so khớp mẫu và palindrome (string algorithms) · 1.5h
- `py.functions.scope_closures` — Scope, LEGB và closure — chia 2 ngày · 0.5h

**Học gì**

- Prefix sum và difference array: Đoạn con liên tiếp (subarray): các phần tử nằm sát nhau trong mảng, khác dãy con (subsequence) có thể bỏ phần tử ở giữa; Mảng prefix: prefix[i] là tổng i phần tử đầu. Ví dụ a=[2,1,3] cho prefix=[0,2,3,6]; tổng a[1..2] = prefix[3] - prefix[1] = 6 - 2 = 4; Truy vấn tổng đoạn (range sum query): chuẩn bị prefix một lần O(n), sau đó mỗi truy vấn chỉ là một phép trừ O(1); Đếm đoạn con có tổng bằng k: vừa đi vừa ghi vào dict số lần mỗi prefix đã gặp; tại vị trí hiện tại cộng số lần của (prefix - k)
- Chuỗi cơ bản: Chuỗi bất biến (immutable): s[0] = 'a' báo lỗi; s += c trong vòng lặp tạo chuỗi mới mỗi lần nên tổng O(n^2); Nối hiệu quả: gom các mảnh vào list rồi ''.join(parts) một lần; Mã ký tự (character code): mỗi ký tự là một số, ví dụ ord('a') = 97 (bảng ASCII), chr(97) = 'a'. Dùng để đổi chữ cái thành chỉ số 0-25; Đếm chữ cái bằng list 26 ô: count[ord(c) - ord('a')] += 1
- Thuật toán chuỗi: so khớp mẫu và palindrome: Mở rộng từ tâm (expand around center): thử từng vị trí (và từng khe giữa hai ký tự) làm tâm, nở ra hai phía khi hai ký tự còn giống; tổng O(n^2); Đếm chuỗi con đối xứng (palindromic substrings) bằng cùng ý tưởng mở rộng từ mỗi tâm; mỗi lần nở thành công là thêm một chuỗi ('aaa' có 6); Tìm chuỗi con (pattern matching): tìm mẫu needle (chuỗi nhỏ cần tìm) trong haystack (chuỗi lớn)
- Scope, LEGB và closure: Biến tạo trong hàm là biến cục bộ (local), chỉ dùng trong hàm; biến ngoài mọi hàm là biến toàn cục (global); Hàm đọc được biến toàn cục, nhưng gán cùng tên sẽ tạo biến cục bộ mới; muốn sửa biến toàn cục phải khai báo global (nên hạn chế); Python tìm tên theo thứ tự: trong hàm → hàm bao ngoài → toàn cục → có sẵn (quy tắc LEGB); Closure: hàm tang bên trong tao_dem dùng và nhớ biến dem của tao_dem, kể cả khi tao_dem đã chạy xong

**Thời gian** (tổng 6h/6h): Học 115p · Luyện 215p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p

**Bài luyện (không phải bài mock)** · 6 bài

1. LC 1 Two Sum (E) ★ 🔊 — `dsa.arrays_strings.hashing_patterns`
2. LC 217 Contains Duplicate (E) — `dsa.arrays_strings.hashing_patterns`
3. LC 242 Valid Anagram (E) — `dsa.arrays_strings.hashing_patterns`
4. LC 303 Range Sum Query - Immutable (E) — `dsa.arrays_strings.prefix_sum`
5. LC 28 Find the Index of the First Occurrence in a String (E) — `dsa.arrays_strings.strings_basics`
6. LC 5 Longest Palindromic Substring (M) — `dsa.arrays_strings.string_algorithms`

**Bài thêm nếu còn giờ (tùy chọn, không tính vào số bài của ngày)**: LC 1207 Unique Number of Occurrences (E); LC 219 Contains Duplicate II (E); LC 202 Happy Number (E); LC 525 Contiguous Array (M); LC 974 Subarray Sums Divisible by K (M); LC 304 Range Sum Query 2D - Immutable (M); LC 459 Repeated Substring Pattern (E); LC 408 Valid Word Abbreviation (E) (premium)

**Ôn lặp**: D+1: LC 49 Group Anagrams (ngày 5): viết lại không nhìn lời giải · D+3: LC 118 Pascal's Triangle (ngày 3): viết lại không nhìn lời giải

### Ngày 7 · Chủ Nhật · tuần 1 · 6h: Scope, LEGB và closure; Kỹ thuật xử lý mảng tại chỗ; Hai con trỏ

**Subtopic**

- `py.functions.scope_closures` — Scope, LEGB và closure (tiếp) — chia 2 ngày · 0.5h
- `dsa.arrays_strings.array_techniques` — Kỹ thuật xử lý mảng tại chỗ (in-place array techniques) · 1.5h
- `dsa.two_pointers_window.two_pointers` — Hai con trỏ (two pointers) · 1.5h

**Học gì**

- Kỹ thuật xử lý mảng tại chỗ: Kadane: tìm đoạn con liên tiếp có tổng lớn nhất; Boyer-Moore: tìm phần tử chiếm quá nửa. Giữ một ứng viên và biến đếm: gặp số giống thì +1, khác thì -1, về 0 thì đổi ứng viên; Xoay mảng (rotate): đảo cả mảng, rồi đảo riêng k phần tử đầu và phần còn lại, xoay k bước mà không cần mảng phụ; Cờ Hà Lan (Dutch national flag): xếp mảng 0/1/2 bằng ba chỉ số lo, mid, hi. Gặp 0: đổi a[mid] với a[lo], rồi lo++ và mid++. Gặp 1: mid++; (20 phút) Quét từ phải sang trái và giữ giá trị lớn nhất đang có: Buildings With an Ocean View (LC 1762, premium) giải được mà không cần monotonic stack.
- Hai con trỏ: Hai đầu (opposite ends): trên mảng đã sắp xếp, trái ở đầu và phải ở cuối; tổng lớn quá thì lùi phải, nhỏ quá thì tiến trái; Cùng chiều (reader/writer): một chỉ số đọc đi trước, một chỉ số ghi đi sau, dùng để lọc hoặc xoá phần tử tại chỗ; Vì sao an toàn: mỗi lần nhích một chỉ số là loại chắc chắn một loạt cặp không thể là đáp án, nên chỉ cần một lượt O(n); Hai con trỏ trên hai mảng hoặc hai chuỗi: gộp hai mảng đã sắp xếp, giao của hai mảng, kiểm tra dãy con

**Thời gian** (tổng 6h/6h): Học 75p · Luyện 135p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p + Mock: I1 - Technical 1 45p + Chấm mock + sửa lỗi 45p + Quiz cuối tuần + checkpoint 30p

**Bài luyện (không phải bài mock)** · 3 bài

1. LC 26 Remove Duplicates from Sorted Array (E) ★ 🔊 — `dsa.two_pointers_window.two_pointers`
2. LC 977 Squares of a Sorted Array (E) ★ — `dsa.two_pointers_window.two_pointers`
3. LC 167 Two Sum II - Input Array Is Sorted (M) ★ — `dsa.two_pointers_window.two_pointers`

**Bài thêm nếu còn giờ (tùy chọn, không tính vào số bài của ngày)**: LC 75 Sort Colors (M); LC 125 Valid Palindrome (E); LC 283 Move Zeroes (E); LC 392 Is Subsequence (E); LC 27 Remove Element (E); LC 88 Merge Sorted Array (E); LC 11 Container With Most Water (M); LC 15 3Sum (M)

**Để dành cho mock (chỉ làm trong giờ mock)**: I1 - Technical 1

- I1-R1-Q1 Find Pivot Index (LC 724) — Technical interview 1
- I1-R1-Q2 Add Strings (LC 415) — Technical interview 1

**Ôn lặp**: D+1: LC 5 Longest Palindromic Substring (ngày 6): viết lại không nhìn lời giải · D+3: LC 268 Missing Number (ngày 4): viết lại không nhìn lời giải

**Ôn mock sau buổi này**: D+3 → ngày 10, D+7 → ngày 14; chỉ làm lại câu bạn chấm ≤ 1.

### Ngày 8 · Thứ Hai · tuần 2 · 4h: Class, object, self và property; Danh sách liên kết đơn và đôi; Đảo, ghép, nối lại con trỏ và sao chép list

**Subtopic**

- `py.oop.classes_basics` — Class, object, self và property (classes) · 1h
- `dsa.linked_list.ll_basics` — Danh sách liên kết đơn và đôi (singly and doubly linked list) · 1.5h
- `dsa.linked_list.ll_manipulation` — Đảo, ghép, nối lại con trỏ và sao chép list (list rewiring) — chia 2 ngày · 1h

**Học gì**

- Class, object, self và property: class HocSinh: định nghĩa bản thiết kế; hs = HocSinh('An', 8) tạo một object (instance, thể hiện); __init__ chạy khi tạo object để gán dữ liệu ban đầu; self là 'chính object này', có mặt ở mọi method; Thuộc tính (attribute) lưu dữ liệu của từng object (self.ten); method là hàm thuộc class (hs.in_diem()); __str__ quy định print(obj) in gì; __repr__ là dạng dành cho lập trình viên khi debug
- Danh sách liên kết đơn và đôi: Node là một 'hộp' có giá trị và con trỏ (pointer, ở Python là tham chiếu) next tới hộp sau; node cuối có next là None; Class ListNode có val và next (mặc định None). Nối ba node: a.next = b rồi b.next = c. Giữ head là node đầu và đi bằng while cur; Truy cập hoặc tìm theo vị trí là O(n) vì phải đi từ head; mảng thì O(1); Chèn một node ngay sau node đang đứng, hoặc xoá node kế tiếp của nó, là O(1): chỉ đổi next (còn tự tìm node thì vẫn O(n))
- Đảo, ghép, nối lại con trỏ và sao chép list: Đảo list bằng vòng lặp: ba biến prev, cur, nxt; mỗi bước lưu nxt = cur.next, đổi cur.next = prev, rồi dịch cả ba lên một bước; Vì sao phải lưu next trước: đổi móc xong là mất đường tới phần còn lại của list; Ghép hai list đã sắp xếp (merge): so hai đầu, nối node nhỏ hơn vào kết quả; node giả (dummy) làm điểm đầu của kết quả; Xoá node thứ n từ cuối: dùng node giả đặt trước head; cho con trỏ nhanh đi trước n bước, rồi cả hai cùng đi tới khi nhanh ở node cuối cùng

**Thời gian** (tổng 4h/4h): Học 75p · Luyện 135p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p

**Bài luyện (không phải bài mock)** · 5 bài

1. LC 13 Roman to Integer (E) 🔊 — `dsa.arrays_strings.strings_basics`
2. LC 206 Reverse Linked List (E) — `dsa.linked_list.ll_basics`
3. LC 238 Product of Array Except Self (M) — `dsa.arrays_strings.prefix_sum`
4. LC 647 Palindromic Substrings (M) — `dsa.arrays_strings.string_algorithms`
5. LC 53 Maximum Subarray (M) — `dsa.arrays_strings.array_techniques`

**Bài thêm nếu còn giờ (tùy chọn, không tính vào số bài của ngày)**: LC 67 Add Binary (E); LC 43 Multiply Strings (M); LC 705 Design HashSet (E); LC 1603 Design Parking System (E); LC 141 Linked List Cycle (E); LC 876 Middle of the Linked List (E); LC 203 Remove Linked List Elements (E)

**Ôn lặp**: D+1: LC 167 Two Sum II - Input Array Is Sorted (ngày 7): viết lại không nhìn lời giải · D+3: LC 485 Max Consecutive Ones (ngày 5): viết lại không nhìn lời giải · D+7: LC 2235 Add Two Integers (ngày 1): viết lại không nhìn lời giải

### Ngày 9 · Thứ Ba · tuần 2 · 4h: Đảo, ghép, nối lại con trỏ và sao chép list; Stack, queue, deque và cách cài đặt; Bài toán stack

**Subtopic**

- `dsa.linked_list.ll_manipulation` — Đảo, ghép, nối lại con trỏ và sao chép list (list rewiring) (tiếp) — chia 2 ngày · 1h
- `dsa.stack_queue.stack_queue_ds` — Stack, queue, deque và cách cài đặt (stack, queue, deque) · 1.5h
- `dsa.stack_queue.stack_problems` — Bài toán stack: ngoặc, min stack, tính biểu thức (stack problems) · 1h

**Học gì**

- Stack, queue, deque và cách cài đặt: Stack (LIFO, vào sau ra trước): push đặt lên đỉnh, pop lấy từ đỉnh, peek xem đỉnh. Đời thường: nút Undo, nút Back của trình duyệt; Queue (FIFO, vào trước ra trước): enqueue thêm vào cuối, dequeue lấy ở đầu. Đời thường: hàng chờ in, hàng đợi mua vé; Python dùng list làm stack: append để push và pop để lấy đỉnh, cả hai O(1); Python dùng collections.deque làm queue: append và popleft đều O(1); list.pop(0) là O(n) vì phải dời cả mảng (đã học ở mục arrays)
- Bài toán stack: ngoặc, min stack, tính biểu thức: Ghép ngoặc (matching parentheses): gặp ( [ { thì push; gặp đóng thì pop và kiểm tra đúng loại; cuối cùng stack phải rỗng; Cấu trúc lồng nhau có cái mở sau đóng trước, đúng hành vi LIFO của stack; Min stack: thêm một stack phụ lưu giá trị nhỏ nhất tại mỗi thời điểm, nên lấy giá trị nhỏ nhất trong O(1); Biểu thức hậu tố (RPN): viết số trước dấu, '3 4 +' là 7

**Thời gian** (tổng 4h/4h): Học 75p · Luyện 135p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p

**Bài luyện (không phải bài mock)** · 5 bài

1. LC 232 Implement Queue using Stacks (E) ★ 🔊 — `dsa.stack_queue.stack_queue_ds`
2. LC 20 Valid Parentheses (E) ★ — `dsa.stack_queue.stack_problems`
3. LC 138 Copy List with Random Pointer (M) ★ — `dsa.linked_list.ll_manipulation`
4. LC 143 Reorder List (M) ★ — `dsa.linked_list.ll_manipulation`
5. LC 1209 Remove All Adjacent Duplicates in String II (M) ★ — `dsa.stack_queue.stack_problems`

**Bài thêm nếu còn giờ (tùy chọn, không tính vào số bài của ngày)**: LC 1762 Buildings With an Ocean View (M) (premium); LC 160 Intersection of Two Linked Lists (E); LC 234 Palindrome Linked List (E); LC 2 Add Two Numbers (M); LC 622 Design Circular Queue (M); LC 150 Evaluate Reverse Polish Notation (M); LC 682 Baseball Game (E); LC 844 Backspace String Compare (E); LC 739 Daily Temperatures (M); LC 496 Next Greater Element I (E)

**Ôn lặp**: D+1: LC 53 Maximum Subarray (ngày 8): viết lại không nhìn lời giải · D+3: LC 1 Two Sum (ngày 6): viết lại không nhìn lời giải · D+7: LC 1929 Concatenation of Array (ngày 2): viết lại không nhìn lời giải

### Ngày 10 · Thứ Tư · tuần 2 · 4h: Phân tích chuỗi và tính biểu thức; Quy trình giải bài phỏng vấn; Tự giới thiệu 2 phút ...

**Subtopic**

- `dsa.stack_queue.parsing_strings` — Phân tích chuỗi và tính biểu thức (string parsing) · 1.5h
- `dsa.foundations.interview_method` — Quy trình giải bài phỏng vấn (interview problem-solving method) · 1h
- `bh.method.self_intro` — Tự giới thiệu 2 phút (self-introduction) · 0.5h
- `bh.method.star_carl` — Cấu trúc trả lời STAR / CARL (answer structure) — chia 2 ngày · 0.5h

**Học gì**

- Phân tích chuỗi và tính biểu thức: Tách từ (tokenizer): cắt chuỗi thành các mảnh có nghĩa (số, dấu, ngoặc) bằng vòng lặp với chỉ số i, trước khi xử lý; atoi: chuyển chuỗi thành số theo luật: bỏ khoảng trắng đầu, đọc dấu +/-, đọc các chữ số liên tiếp, dừng ở ký tự lạ. ' -42abc' cho -42; Thứ tự ưu tiên toán tử (operator precedence): nhân chia làm trước cộng trừ; Giải mã chuỗi lồng nhau (decode string): '3[a2[c]]' thành 'accaccacc'; gặp [ thì push (chuỗi hiện tại, số lần lặp), gặp ] thì pop và nhân lên
- Quy trình giải bài phỏng vấn: Làm rõ đề (clarify): hỏi về kiểu đầu vào, giới hạn kích thước và các trường hợp mép (edge case): rỗng, 1 phần tử, trùng, số âm; Chạy ví dụ nhỏ bằng tay để hiểu đề và nhìn ra quy luật trước khi code; Brute force là cách thử hết mọi khả năng, chậm nhưng chắc đúng: nêu nó trước, rồi tối ưu bằng cách bỏ bớt việc lặp lại; Đoán dạng bài từ giới hạn của đề: n lên tới 10^5 cần O(n) hoặc O(n log n); n chỉ khoảng 20 thì thử hết mọi tập con được
- Tự giới thiệu 2 phút: Công thức Hiện tại - Quá khứ - Tương lai (Present - Past - Future): đang học gì, đã làm gì đáng kể, vì sao muốn vị trí này; Chọn 2-3 điểm liên quan tới JD (bản mô tả công việc), không đọc lại CV từng dòng; Thành tựu có số liệu, kể cả của sinh viên: điểm môn, số thành viên CLB, một dự án nhóm làm xong; Chưa có dự án nào? Nói môn học bạn thích, bài tập lớn, CLB hoặc việc tự học (ví dụ tự làm bài Python mỗi tuần); thật thà, đừng bịa
- Cấu trúc trả lời STAR / CARL: STAR: Situation (hoàn cảnh), Task (nhiệm vụ của bạn), Action (việc bạn làm), Result (kết quả). Kể theo thứ tự này; Thời gian gợi ý: khoảng 20% hoàn cảnh, 60% hành động, 20% kết quả. Phần hành động là quan trọng nhất; Nói 'tôi đã làm' thay vì 'chúng tôi': người nghe cần biết đóng góp của bạn, đó không phải khoe khoang; Kết quả có con số: điểm bài nhóm, số người tham gia, số giờ tiết kiệm. Chưa có số thì nói rõ trước và sau

**Thời gian** (tổng 4h/4h): Học 75p · Luyện 135p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p

**Bài luyện (không phải bài mock)** · 5 bài

1. LC 225 Implement Stack using Queues (E) 🔊 — `dsa.stack_queue.stack_queue_ds`
2. LC 1047 Remove All Adjacent Duplicates In String (E) — `dsa.stack_queue.stack_problems`
3. LC 1021 Remove Outermost Parentheses (E) — `dsa.stack_queue.parsing_strings`
4. LC 19 Remove Nth Node From End of List (M) — `dsa.linked_list.ll_manipulation`
5. LC 227 Basic Calculator II (M) ★ — `dsa.stack_queue.parsing_strings`

**Bài thêm nếu còn giờ (tùy chọn, không tính vào số bài của ngày)**: LC 394 Decode String (M); LC 66 Plus One (E)

**Behavioral / AI (15-20 phút, tính trong phần Ôn hoặc trong giờ của subtopic bh)**: Viết 60 giây giới thiệu bản thân (bh.method.self_intro), đọc to và đo giờ. Học khung STAR/CARL; viết STORY #1 (dự án ở trường/cá nhân): 5 câu Situation-Task-Action-Result.

**Ôn lặp**: D+3: LC 26 Remove Duplicates from Sorted Array (ngày 7): viết lại không nhìn lời giải · D+7: LC 118 Pascal's Triangle (ngày 3): viết lại không nhìn lời giải · **Ôn mock D+3**: viết lại từ đầu (không xem lời giải) mọi câu của mock ngày 7 (I1 - Technical 1) mà bạn chấm ≤ 1; thay cho bài D+1 của ngày này

### Ngày 11 · Thứ Năm · tuần 2 · 4h: Cấu trúc trả lời STAR / CARL; Đệ quy cơ bản và chia để trị; Binary search cơ bản

**Subtopic**

- `bh.method.star_carl` — Cấu trúc trả lời STAR / CARL (answer structure) (tiếp) — chia 2 ngày · 0.5h
- `dsa.recursion_backtracking.recursion_basics` — Đệ quy cơ bản và chia để trị (recursion, divide and conquer) · 2h
- `dsa.searching_sorting.binary_search_basics` — Binary search cơ bản (binary search fundamentals) · 1h

**Học gì**

- Đệ quy cơ bản và chia để trị: Điểm dừng (base case) là trường hợp nhỏ nhất trả kết quả ngay; bước đệ quy (recursive case) gọi lại hàm với đầu vào nhỏ hơn; Ví dụ giai thừa: fact(n) = n * fact(n-1), fact(0) = 1. fact(3) gọi fact(2), gọi fact(1), gọi fact(0), rồi kết quả trả ngược lên; Ngăn xếp lời gọi (call stack): máy nhớ các lần gọi hàm đang dang dở, chồng lên nhau như chồng đĩa; mỗi lần gọi tốn thêm một tầng bộ nhớ; Python chỉ cho khoảng 1000 tầng (sys.getrecursionlimit); vượt quá thì báo RecursionError. Bài cần sâu hơn thì đổi sang vòng lặp; Chia để trị: Pow(x, n) = Pow(x, n/2)^2 (xử lý n lẻ, n âm); thử với LC 50 sau khi làm xong 231/326.
- Binary search cơ bản: Ý tưởng: dãy đã sắp xếp; so với phần tử giữa rồi bỏ nửa chắc chắn không chứa đáp án; mỗi bước giảm một nửa nên O(log n); Ba biến lo, hi, mid = (lo + hi) // 2. Khuôn A: while lo <= hi, cập nhật lo = mid + 1 hoặc hi = mid - 1; Bất biến (invariant): điều luôn đúng trong lúc lặp, ví dụ 'nếu có đáp án thì nó nằm trong [lo, hi]'. Chọn một khuôn và giữ đúng nó thì không lệch một; Lỗi hay gặp: vòng lặp vô hạn khi hi = mid nhưng vẫn dùng điều kiện lo <= hi; luôn thử mảng 1 và 2 phần tử

**Thời gian** (tổng 4h/4h): Học 75p · Luyện 135p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p

**Bài luyện (không phải bài mock)** · 5 bài

1. LC 70 Climbing Stairs (E) 🔊 — `dsa.recursion_backtracking.recursion_basics`
2. LC 704 Binary Search (E) — `dsa.searching_sorting.binary_search_basics`
3. LC 155 Min Stack (M) — `dsa.stack_queue.stack_queue_ds`
4. LC 1541 Minimum Insertions to Balance a Parentheses String (M) — `dsa.stack_queue.parsing_strings`
5. LC 50 Pow(x, n) (M) ★ — `dsa.recursion_backtracking.recursion_basics`

**Bài thêm nếu còn giờ (tùy chọn, không tính vào số bài của ngày)**: LC 231 Power of Two (E); LC 326 Power of Three (E); LC 779 K-th Symbol in Grammar (M); LC 69 Sqrt(x) (E); LC 278 First Bad Version (E); LC 367 Valid Perfect Square (E)

**Ôn lặp**: D+1: LC 227 Basic Calculator II (ngày 10): viết lại không nhìn lời giải · D+3: LC 13 Roman to Integer (ngày 8): viết lại không nhìn lời giải · D+7: LC 268 Missing Number (ngày 4): viết lại không nhìn lời giải

### Ngày 12 · Thứ Sáu · tuần 2 · 4h: Thuật toán sắp xếp; Ứng dụng sort và quickselect; Cây nhị phân và duyệt cây

**Subtopic**

- `dsa.searching_sorting.sorting_algorithms` — Thuật toán sắp xếp (sorting algorithms) · 1.5h
- `dsa.searching_sorting.sorting_applications` — Ứng dụng sort và quickselect (sorting applications) · 1h
- `dsa.trees.tree_basics` — Cây nhị phân và duyệt cây (binary trees and traversals) · 1h

**Học gì**

- Thuật toán sắp xếp: Sắp xếp chậm O(n^2) (bubble, selection, insertion): so và đổi chỗ từng cặp; insertion sort giống xếp bài, nhanh khi dãy gần như đã sắp xếp; Merge sort: chia đôi, sắp từng nửa bằng đệ quy, rồi trộn hai nửa đã sắp xếp; luôn O(n log n), cần thêm O(n) bộ nhớ; Quick sort: chọn mốc (pivot), chia (partition) thành nhỏ hơn mốc và lớn hơn mốc, rồi đệ quy từng bên; Ổn định (stable): hai phần tử bằng nhau giữ thứ tự cũ. Ví dụ sort học sinh theo điểm, hai bạn cùng điểm vẫn đứng theo thứ tự ban đầu
- Ứng dụng sort và quickselect: Sắp xếp rồi quét (sort then scan): sắp xếp để các phần tử cần so sánh nằm cạnh nhau, rồi duyệt một lượt; Sắp xếp nhiều khoá: sorted(a, key=lambda x: (-x[1], x[0])) là điểm giảm dần, cùng điểm thì tên tăng dần; Sắp xếp theo tần suất (sort by frequency): đếm bằng Counter rồi sắp theo số đếm
- Cây nhị phân và duyệt cây: Node cây có giá trị và hai con trỏ left, right (hoặc None). Đời thường: cây thư mục, sơ đồ tổ chức. Code: class TreeNode(val, left=None, right=None); Thuật ngữ: gốc (root), lá (leaf), cha/con (parent/child); độ sâu (depth) = số cạnh từ gốc xuống node; Duyệt trước/giữa/sau (preorder, inorder, postorder) bằng đệ quy: cha-trái-phải, trái-cha-phải, trái-phải-cha; Duyệt theo tầng (level-order): thăm từng tầng từ trên xuống bằng queue (deque): lấy node ra, đẩy con trái rồi con phải vào

**Thời gian** (tổng 4h/4h): Học 75p · Luyện 135p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p

**Bài luyện (không phải bài mock)** · 5 bài

1. LC 21 Merge Two Sorted Lists (E) 🔊 — `dsa.linked_list.ll_basics`
2. LC 35 Search Insert Position (E) — `dsa.searching_sorting.binary_search_basics`
3. LC 1122 Relative Sort Array (E) — `dsa.searching_sorting.sorting_algorithms`
4. LC 1636 Sort Array by Increasing Frequency (E) — `dsa.searching_sorting.sorting_applications`
5. LC 104 Maximum Depth of Binary Tree (E) — `dsa.trees.tree_basics`

**Bài thêm nếu còn giờ (tùy chọn, không tính vào số bài của ngày)**: LC 148 Sort List (M); LC 179 Largest Number (M); LC 100 Same Tree (E); LC 144 Binary Tree Preorder Traversal (E); LC 145 Binary Tree Postorder Traversal (E); LC 101 Symmetric Tree (E)

**Ôn lặp**: D+1: LC 50 Pow(x, n) (ngày 11): viết lại không nhìn lời giải · D+3: LC 232 Implement Queue using Stacks (ngày 9): viết lại không nhìn lời giải · D+7: LC 485 Max Consecutive Ones (ngày 5): viết lại không nhìn lời giải

### Ngày 13 · Thứ Bảy · tuần 2 · 6h: Binary heap và priority queue; Top-K bằng heap; Binary search trên mảng xoay, 2D, peak ...

**Subtopic**

- `dsa.heap.heap_ds` — Binary heap và priority queue (binary heap) · 1h
- `dsa.heap.heap_top_k` — Top-K bằng heap (top-K with heaps) · 1h
- `dsa.searching_sorting.binary_search_variants` — Binary search trên mảng xoay, 2D, peak (binary search variants) · 1h
- `dsa.two_pointers_window.sliding_window_fixed` — Cửa sổ trượt kích thước cố định (fixed sliding window) · 1h
- `dsa.two_pointers_window.sliding_window_variable` — Cửa sổ trượt kích thước thay đổi (variable sliding window) · 1.5h

**Học gì**

- Binary heap và priority queue: Hàng đợi ưu tiên (priority queue): lấy ra phần tử 'ưu tiên nhất' (thường là nhỏ nhất) trước, không theo thứ tự vào; Min-heap: cây nhị phân đầy theo từng tầng, mỗi cha <= hai con nên phần tử nhỏ nhất luôn ở gốc; max-heap thì ngược lại; Cất cây trong list: con của ô i nằm ở 2i+1 và 2i+2, cha của ô i ở (i-1)//2; không cần node hay con trỏ; Thêm (push): đặt ở cuối rồi nổi lên (sift up). Lấy gốc (pop): chuyển phần tử cuối lên gốc rồi chìm xuống (sift down). Cả hai O(log n)
- Top-K bằng heap: Top k lớn nhất bằng min-heap kích thước k: đỉnh là 'kẻ yếu nhất trong top'; Ví dụ top 3 của [5,1,8,3,9,2]: heap lần lượt {1,5,8}, {3,5,8}, {5,8,9}; số 2 nhỏ hơn đỉnh nên bị bỏ. Kết quả 5, 8, 9; Độ phức tạp O(n log k); sắp xếp cả dãy là O(n log n), nên heap có lợi khi k nhỏ; Dòng dữ liệu (stream): số đến dần, không nhét hết vào bộ nhớ; heap xử lý từng số một và luôn giữ top-k
- Binary search trên mảng xoay, 2D, peak: Mảng xoay (rotated sorted array): mảng tăng (các giá trị khác nhau) bị dời đầu, ví dụ [4,5,6,7,0,1,2]; Tìm giá trị nhỏ nhất của mảng xoay: so phần tử giữa với phần tử cuối để biết điểm gãy nằm bên nào; Bài tương tác (First Bad Version): hàm isBad(i) chuyển từ False sang True đúng một lần; tìm vị trí chuyển
- Cửa sổ trượt kích thước cố định: Cửa sổ (window) là một đoạn con liên tiếp dài k; trượt sang phải một bước = thêm phần tử mới, bớt phần tử cũ; Tính cửa sổ đầu tiên rồi trượt, không tính lại từ đầu: tổng mới = tổng cũ + a[phải] - a[trái]; Cửa sổ tần suất: dict hoặc Counter đếm chữ cái trong cửa sổ, cộng 1 khi thêm và trừ 1 khi bớt; Độ phức tạp: mỗi phần tử vào và ra cửa sổ một lần nên O(n), thay vì O(n*k)
- Cửa sổ trượt kích thước thay đổi: Khung chung: mở rộng phải; while cửa sổ không hợp lệ: co trái; cập nhật đáp án; Chạy tay 'abcabcbb': thêm a, b, c; gặp a lặp thì co trái tới khi bỏ a; độ dài lớn nhất tìm được là 3; Dài nhất cập nhật đáp án sau khi cửa sổ đã hợp lệ; ngắn nhất cập nhật lúc vừa đủ điều kiện rồi mới co để thu nhỏ; Dict đếm 'cần' và 'đang có' (need/have) cho điều kiện kiểu 'chứa đủ các ký tự cho trước'

**Thời gian** (tổng 6h/6h): Học 115p · Luyện 215p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p

**Bài luyện (không phải bài mock)** · 6 bài

1. LC 1046 Last Stone Weight (E) 🔊 — `dsa.heap.heap_ds`
2. LC 643 Maximum Average Subarray I (E) — `dsa.two_pointers_window.sliding_window_fixed`
3. LC 973 K Closest Points to Origin (M) ★ — `dsa.heap.heap_ds`
4. LC 378 Kth Smallest Element in a Sorted Matrix (M) ★ — `dsa.heap.heap_top_k`
5. LC 373 Find K Pairs with Smallest Sums (M) ★ — `dsa.heap.heap_top_k`
6. LC 852 Peak Index in a Mountain Array (M) ★ — `dsa.searching_sorting.binary_search_variants`

**Bài thêm nếu còn giờ (tùy chọn, không tính vào số bài của ngày)**: LC 1337 The K Weakest Rows in a Matrix (E); LC 621 Task Scheduler (M); LC 767 Reorganize String (M); LC 153 Find Minimum in Rotated Sorted Array (M); LC 875 Koko Eating Bananas (M); LC 567 Permutation in String (M); LC 1004 Max Consecutive Ones III (M); LC 424 Longest Repeating Character Replacement (M)

**Behavioral / AI (15-20 phút, tính trong phần Ôn hoặc trong giờ của subtopic bh)**: Ôn miệng 2 story đã viết (STORY #1, #2) trong 10 phút; đo giờ ≤ 2 phút mỗi story.

**Ôn lặp**: D+1: LC 104 Maximum Depth of Binary Tree (ngày 12): viết lại không nhìn lời giải · D+3: LC 225 Implement Stack using Queues (ngày 10): viết lại không nhìn lời giải · D+7: LC 1 Two Sum (ngày 6): viết lại không nhìn lời giải

### Ngày 14 · Chủ Nhật · tuần 2 · 6h: Xung đột và làm việc nhóm; Thất bại, feedback và bài học; Quay lui

**Subtopic**

- `bh.stories.conflict_teamwork` — Xung đột và làm việc nhóm (conflict & teamwork) · 1h
- `bh.stories.failure_feedback` — Thất bại, feedback và bài học (failure & feedback) · 1h
- `dsa.recursion_backtracking.backtracking_core` — Quay lui: tập con, hoán vị, tổ hợp (backtracking) — chia 2 ngày · 0.5h

**Học gì**

- Xung đột và làm việc nhóm: Chọn bất đồng về cách làm (kỹ thuật, quy trình), không phải cãi cá nhân; Lắng nghe, hiểu ý bên kia, rồi dùng bằng chứng (thử cả hai cách, hỏi giảng viên) để cùng chọn; Sinh viên không có manager: thay bằng trưởng nhóm hoặc giảng viên. Ví dụ: bạn cùng nhóm muốn cách A, bạn muốn B; Disagree and commit: không đồng ý nhưng khi nhóm đã chọn vẫn làm hết sức
- Thất bại, feedback và bài học: Chọn thất bại thật, không phải 'điểm yếu là quá cầu toàn'. Ví dụ: nộp trễ bài nhóm, rớt môn, sự kiện CLB tổ chức không như ý; Nhận trách nhiệm phần mình, không đổ lỗi; nói ngay bạn đã sửa gì; Root cause (nguyên nhân gốc) là lý do thật gây lỗi, khác với sửa tạm. Nêu thay đổi cách làm để không lặp lại; Nhận phản hồi tiêu cực không phòng thủ: nghe hết, hỏi lại, rồi sửa
- Quay lui: tập con, hoán vị, tổ hợp: Cây quyết định (decision tree): mỗi tầng là một lựa chọn, mỗi lá là một kết quả; ta đi sâu hết một nhánh bằng đệ quy rồi lùi lại; Khung chọn - khám phá - bỏ chọn (choose-explore-unchoose): path.append(x); gọi đệ quy; path.pop(); Tập con (subsets): n phần tử có 2^n tập con; mỗi phần tử có hai lựa chọn là lấy hoặc không lấy; Hoán vị (permutations): mọi cách xếp thứ tự n phần tử, có n! cách; dùng tập 'đã dùng' để không chọn lại một phần tử

**Thời gian** (tổng 6h/6h): Học 55p · Luyện 95p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p + Mock: I3 - Technical 1 + 2 90p + Chấm mock + sửa lỗi 60p + Quiz cuối tuần + checkpoint 30p

**Bài luyện (không phải bài mock)** · 3 bài

1. LC 34 Find First and Last Position of Element in Sorted Array (M) 🔊 — `dsa.searching_sorting.binary_search_variants`
2. LC 1456 Maximum Number of Vowels in a Substring of Given Length (M) — `dsa.two_pointers_window.sliding_window_fixed`
3. LC 3 Longest Substring Without Repeating Characters (M) — `dsa.two_pointers_window.sliding_window_variable`

**Để dành cho mock (chỉ làm trong giờ mock)**: I3 - Technical 1 + 2

- I3-R1-Q1 Best Time to Buy and Sell Stock (LC 121) — Technical interview 1
- I3-R1-Q2 Kth Largest Element in an Array (LC 215) — Technical interview 1
- I3-R2-Q1 Friends Of Appropriate Ages (LC 825) — Technical interview 2
- I3-R2-Q2 Simplify Path (LC 71) — Technical interview 2

**Behavioral / AI (15-20 phút, tính trong phần Ôn hoặc trong giờ của subtopic bh)**: STORY #2: một lần làm nhóm có bất đồng (conflict_teamwork). Nêu rõ phần việc CỦA BẠN, không nói xấu người khác. STORY #3 và #4: một lần mắc lỗi/thất bại bạn đã sửa thế nào, và một lần nhận phản hồi khó nghe (failure_feedback).

**Ôn lặp**: D+3: LC 70 Climbing Stairs (ngày 11): viết lại không nhìn lời giải · D+7: LC 26 Remove Duplicates from Sorted Array (ngày 7): viết lại không nhìn lời giải · **Ôn mock D+7**: viết lại từ đầu (không xem lời giải) mọi câu của mock ngày 7 (I1 - Technical 1) mà bạn chấm ≤ 1; thay cho bài D+1 của ngày này

**Ôn mock sau buổi này**: D+3 → ngày 17, D+7 → ngày 21; chỉ làm lại câu bạn chấm ≤ 1.

### Ngày 15 · Thứ Hai · tuần 3 · 4h: Quay lui; Đệ quy trên cây, dựng và serialize cây; Duyệt theo tầng, view của cây và cây phân cấp

**Subtopic**

- `dsa.recursion_backtracking.backtracking_core` — Quay lui: tập con, hoán vị, tổ hợp (backtracking) (tiếp) — chia 2 ngày · 1h
- `dsa.trees.tree_recursion` — Đệ quy trên cây, dựng và serialize cây (tree recursion and construction) · 2h
- `dsa.trees.tree_bfs_views_hierarchy` — Duyệt theo tầng, view của cây và cây phân cấp (level-order and hierarchy trees) — chia 2 ngày · 0.5h

**Học gì**

- Đệ quy trên cây, dựng và serialize cây: Từ dưới lên (bottom-up): hàm trả về thông tin của cây con rồi cha ghép lại; Từ trên xuống (top-down): truyền thông tin xuống con bằng tham số, ví dụ độ sâu hoặc tổng đường đi tính đến lúc này; Đường kính (diameter) là đường dài nhất giữa hai node bất kỳ (tính bằng số cạnh): tại mỗi node thử chiều cao trái + phải, cập nhật đáp án chung bằng (xem skill_tree); So sánh cây: same tree, symmetric tree (đối xứng như gương), subtree (cây con) đều là đệ quy trên hai cây cùng lúc
- Duyệt theo tầng, view của cây và cây phân cấp: Duyệt theo tầng với kích thước tầng: mỗi vòng lấy đúng len(queue) node (đúng một tầng), xử lý rồi đẩy con của chúng vào; Zigzag: đếm tầng từ 0; tầng 0, 2, 4... đọc từ trái sang phải, tầng 1, 3, 5... đọc ngược lại (đảo list hoặc dùng deque); Nhìn từ bên phải (right side view): lấy node cuối của mỗi tầng; nhìn từ bên trái thì lấy node đầu; Cây nhiều con (N-ary tree): mỗi node có một list con, như sơ đồ tổ chức công ty; duyệt giống cây nhị phân

**Thời gian** (tổng 4h/4h): Học 75p · Luyện 135p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p

**Bài luyện (không phải bài mock)** · 5 bài

1. LC 112 Path Sum (E) ★ 🔊 — `dsa.trees.tree_recursion`
2. LC 543 Diameter of Binary Tree (E) ★ — `dsa.trees.tree_recursion`
3. LC 122 Best Time to Buy and Sell Stock II (M) ★ — `dsa.arrays_strings.arrays`
4. LC 236 Lowest Common Ancestor of a Binary Tree (M) ★ — `dsa.trees.tree_recursion`
5. LC 129 Sum Root to Leaf Numbers (M) ★ — `dsa.trees.tree_recursion`

**Bài thêm nếu còn giờ (tùy chọn, không tính vào số bài của ngày)**: LC 42 Trapping Rain Water (H); LC 224 Basic Calculator (H); LC 76 Minimum Window Substring (H); LC 22 Generate Parentheses (M); LC 39 Combination Sum (M); LC 77 Combinations (M); LC 110 Balanced Binary Tree (E); LC 111 Minimum Depth of Binary Tree (E); LC 257 Binary Tree Paths (E); LC 572 Subtree of Another Tree (E); LC 1448 Count Good Nodes in Binary Tree (M); LC 113 Path Sum II (M)

**Ôn lặp**: D+1: LC 3 Longest Substring Without Repeating Characters (ngày 14): viết lại không nhìn lời giải · D+3: LC 21 Merge Two Sorted Lists (ngày 12): viết lại không nhìn lời giải · D+7: LC 13 Roman to Integer (ngày 8): viết lại không nhìn lời giải

### Ngày 16 · Thứ Ba · tuần 3 · 4h: Duyệt theo tầng, view của cây và cây phân cấp; Cây nhị phân tìm kiếm; Thiết kế cache

**Subtopic**

- `dsa.trees.tree_bfs_views_hierarchy` — Duyệt theo tầng, view của cây và cây phân cấp (level-order and hierarchy trees) (tiếp) — chia 2 ngày · 0.5h
- `dsa.trees.bst` — Cây nhị phân tìm kiếm (binary search tree) · 1.5h
- `dsa.design_ds.design_cache` — Thiết kế cache: LRU, LFU, TTL (cache design) — chia 2 ngày · 1.5h

**Học gì**

- Cây nhị phân tìm kiếm: Quy tắc BST (invariant): trái < node < phải cho mọi node (giả sử các giá trị khác nhau); duyệt giữa (inorder) ra dãy tăng dần; Tìm và chèn: so với node, nhỏ hơn thì đi trái, lớn hơn thì đi phải; mất O(h) với h là chiều cao; Cây lệch: chèn 1, 2, 3, 4 theo thứ tự tăng thì cây thành một dây dài, h = n nên chậm O(n). Vì vậy cần cây tự cân bằng để giữ h khoảng log n; Xoá node: 0 con thì bỏ; 1 con thì nối con lên; 2 con thì thay bằng node kế tiếp (nhỏ nhất bên phải) rồi xoá node kế tiếp đó
- Thiết kế cache: LRU, LFU, TTL: LRU (least recently used, lâu không dùng nhất bị bỏ trước): get và put đều làm key đó thành "mới dùng"; đầy thì bỏ key cũ nhất; Cách làm O(1): dict tra key -> node, và danh sách liên kết đôi (doubly linked list) giữ thứ tự dùng; dời node lên đầu hoặc cắt node cuối đều O(1); Vì sao cần danh sách liên kết đôi: xoá node ở giữa trong O(1) cần biết node đứng trước nó; dùng node giả ở đầu và cuối (sentinel) để khỏi xét biên; Ca biên: capacity 0 hoặc 1, put key đã tồn tại (cập nhật giá trị và dời lên đầu), get key không có

**Thời gian** (tổng 4h/4h): Học 75p · Luyện 135p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p

**Bài luyện (không phải bài mock)** · 5 bài

1. LC 938 Range Sum of BST (E) ★ 🔊 — `dsa.trees.bst`
2. LC 700 Search in a Binary Search Tree (E) — `dsa.trees.bst`
3. LC 958 Check Completeness of a Binary Tree (M) ★ — `dsa.trees.tree_bfs_views_hierarchy`
4. LC 102 Binary Tree Level Order Traversal (M) — `dsa.trees.tree_bfs_views_hierarchy`
5. LC 173 Binary Search Tree Iterator (M) ★ — `dsa.trees.bst`

**Bài thêm nếu còn giờ (tùy chọn, không tính vào số bài của ngày)**: LC 107 Binary Tree Level Order Traversal II (M); LC 103 Binary Tree Zigzag Level Order Traversal (M); LC 515 Find Largest Value in Each Tree Row (M); LC 98 Validate Binary Search Tree (M); LC 230 Kth Smallest Element in a BST (M); LC 701 Insert into a Binary Search Tree (M); LC 235 Lowest Common Ancestor of a Binary Search Tree (M); LC 270 Closest Binary Search Tree Value (E) (premium); LC 426 Convert Binary Search Tree to Sorted Doubly Linked List (M) (premium)

**Ôn lặp**: D+1: LC 129 Sum Root to Leaf Numbers (ngày 15): viết lại không nhìn lời giải · D+3: LC 1046 Last Stone Weight (ngày 13): viết lại không nhìn lời giải · D+7: LC 232 Implement Queue using Stacks (ngày 9): viết lại không nhìn lời giải

### Ngày 17 · Thứ Tư · tuần 3 · 4h: Thiết kế cache; Cấu trúc O; Khoảng cơ bản ...

**Subtopic**

- `dsa.design_ds.design_cache` — Thiết kế cache: LRU, LFU, TTL (cache design) (tiếp) — chia 2 ngày · 0.5h
- `dsa.design_ds.design_o1_structures` — Cấu trúc O(1): RandomizedSet, stack đặc biệt (O(1) structures) · 1.5h
- `dsa.greedy_intervals.interval_basics` — Khoảng cơ bản: gộp, chèn, chồng lấn (interval fundamentals) · 1h
- `dsa.greedy_intervals.interval_sweep` — Sweep line và bài lịch (sweep line and calendars) — chia 2 ngày · 0.5h

**Học gì**

- Cấu trúc O: Nguyên tắc: với mỗi thao tác đề yêu cầu, hỏi "cấu trúc nào làm việc đó O(1)", rồi ghép các cấu trúc và giữ chúng đồng bộ; RandomizedSet: list lưu giá trị, dict ánh xạ giá trị -> chỉ số. Xoá = đổi chỗ với phần tử cuối rồi pop (swap-delete). getRandom = random.choice(list); Min Stack: thêm một stack phụ lưu giá trị nhỏ nhất tại mỗi mức, nên getMin O(1); Max Frequency Stack: dict đếm tần suất và dict "tần suất -> stack các phần tử"; pop lấy từ stack của tần suất cao nhất
- Khoảng cơ bản: gộp, chèn, chồng lấn: Hai khoảng a, b chồng lấn khi a.start < b.end và b.start < a.end; gộp các đoạn chồng nhau: sắp theo start; nếu start mới <= end hiện tại thì gộp (end = max), không thì mở khoảng mới; Insert Interval: danh sách đã sắp xếp; thêm phần trước, gộp phần chồng lấn, rồi thêm phần sau; Non-overlapping Intervals: sắp theo end, giữ khoảng kết thúc sớm; khoảng nào chồng lên cái đã giữ thì bỏ; số bị bỏ là đáp án
- Sweep line và bài lịch: Sweep line: mỗi khoảng thành hai sự kiện (start, +1), (end, -1); sắp theo thời gian, cộng dồn; giá trị lớn nhất là số khoảng chồng nhau nhiều nhất; Cùng thời điểm thì xử lý "ra" trước "vào": họp 9-10 và 10-11 chỉ cần một phòng; Meeting Rooms II bằng heap xem `dsa.heap.heap_ds`; sweep line (ý trên) cho cùng đáp án mà không cần heap; Mảng hiệu (difference array): cộng +1 tại start, -1 tại end, rồi cộng dồn; hợp với bài đếm theo mốc thời gian như Car Pooling

**Thời gian** (tổng 4h/4h): Học 75p · Luyện 135p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p

**Bài luyện (không phải bài mock)** · 5 bài

1. LC 706 Design HashMap (E) 🔊 — `dsa.design_ds.design_cache`
2. LC 228 Summary Ranges (E) — `dsa.greedy_intervals.interval_basics`
3. LC 380 Insert Delete GetRandom O(1) (M) ★ — `dsa.design_ds.design_o1_structures`
4. LC 1396 Design Underground System (M) — `dsa.design_ds.design_o1_structures`
5. LC 986 Interval List Intersections (M) ★ — `dsa.greedy_intervals.interval_basics`

**Bài thêm nếu còn giờ (tùy chọn, không tính vào số bài của ngày)**: LC 252 Meeting Rooms (E) (premium); LC 163 Missing Ranges (E) (premium)

**Ôn lặp**: D+3: LC 34 Find First and Last Position of Element in Sorted Array (ngày 14): viết lại không nhìn lời giải · D+7: LC 225 Implement Stack using Queues (ngày 10): viết lại không nhìn lời giải · **Ôn mock D+3**: viết lại từ đầu (không xem lời giải) mọi câu của mock ngày 14 (I3 - Technical 1 + 2) mà bạn chấm ≤ 1; thay cho bài D+1 của ngày này

### Ngày 18 · Thứ Năm · tuần 3 · 4h: Sweep line và bài lịch; Thao tác ma trận và lưới 2D; Ownership và lãnh đạo

**Subtopic**

- `dsa.greedy_intervals.interval_sweep` — Sweep line và bài lịch (sweep line and calendars) (tiếp) — chia 2 ngày · 1h
- `dsa.arrays_strings.matrix_traversal` — Thao tác ma trận và lưới 2D (matrix traversal) · 1.5h
- `bh.stories.ownership_leadership` — Ownership và lãnh đạo (ownership & leadership) · 1h

**Học gì**

- Thao tác ma trận và lưới 2D: Chỉ số và biên: grid[r][c] với 0 <= r < số hàng và 0 <= c < số cột; kiểm tra biên trước khi truy cập; Tạo lưới đúng: [[0]*m for _ in range(n)], không phải [[0]*m]*n (các hàng sẽ dùng chung một list); Mảng hướng (direction array): dirs = [(-1,0),(1,0),(0,-1),(0,1)] là 4 hướng lên, xuống, trái, phải, để khỏi viết 4 câu if; Duyệt xoắn ốc (spiral): đi 4 cạnh rồi thu nhỏ biên (trên, dưới, trái, phải) sau mỗi vòng
- Ownership và lãnh đạo: Ownership: nhận việc không ai nhận (làm slide cho nhóm, tổ chức nhóm học) và theo đến hết, không bỏ dở; Bias for action: thấy vấn đề thì bắt tay làm, không ngồi chờ ai bảo; Kết quả đo được: nhóm được 9 điểm, 30 người tham dự sự kiện CLB; Red flag: 'không phải việc của tôi', kể như mình là anh hùng một mình (hero), ép người khác (micromanage)

**Thời gian** (tổng 4h/4h): Học 75p · Luyện 135p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p

**Bài luyện (không phải bài mock)** · 5 bài

1. LC 637 Average of Levels in Binary Tree (E) 🔊 — `dsa.trees.tree_bfs_views_hierarchy`
2. LC 766 Toeplitz Matrix (E) — `dsa.arrays_strings.matrix_traversal`
3. LC 981 Time Based Key-Value Store (M) — `dsa.design_ds.design_cache`
4. LC 435 Non-overlapping Intervals (M) — `dsa.greedy_intervals.interval_basics`
5. LC 1094 Car Pooling (M) — `dsa.greedy_intervals.interval_sweep`

**Bài thêm nếu còn giờ (tùy chọn, không tính vào số bài của ngày)**: LC 48 Rotate Image (M); LC 73 Set Matrix Zeroes (M); LC 498 Diagonal Traverse (M)

**Behavioral / AI (15-20 phút, tính trong phần Ôn hoặc trong giờ của subtopic bh)**: STORY #5: dẫn dắt khi không có chức danh / chủ động làm thêm (ownership_leadership).

**Ôn lặp**: D+1: LC 986 Interval List Intersections (ngày 17): viết lại không nhìn lời giải · D+3: LC 112 Path Sum (ngày 15): viết lại không nhìn lời giải · D+7: LC 70 Climbing Stairs (ngày 11): viết lại không nhìn lời giải

### Ngày 19 · Thứ Sáu · tuần 3 · 4h: Ưu tiên, deadline và yêu cầu mơ hồ; Nhập xuất console và file cơ bản; Bắt lỗi cơ bản với try/except ...

**Subtopic**

- `bh.stories.prioritization_ambiguity` — Ưu tiên, deadline và yêu cầu mơ hồ (prioritization & ambiguity) · 1h
- `py.core.io_input` — Nhập xuất console và file cơ bản (console & file I/O) · 0.5h
- `py.core.try_except_basics` — Bắt lỗi cơ bản với try/except (error handling basics) · 0.5h
- `py.core.regex` — Biểu thức chính quy (regex) · 0.5h
- `py.errors_modules.files_pathlib` — File, pathlib và serialization (JSON, CSV) · 0.5h
- `dsa.practical.file_log_parsing` — Parse file/log, biến đổi dữ liệu và tra cứu (file and log parsing) — chia 2 ngày · 0.5h

**Học gì**

- Ưu tiên, deadline và yêu cầu mơ hồ: Chọn việc quan trọng và đem lại nhiều lợi ích làm trước (impact vs effort: lợi ích so với công sức); Báo sớm cho người liên quan khi biết sẽ trễ, đừng đợi tới hạn; Cắt bớt phần chưa cần để kịp hạn (MVP: bản tối thiểu chạy được); Đề mơ hồ thì hỏi lại, chia nhỏ, nói rõ giả định bạn dùng. Red flag: ngồi chờ chỉ dẫn
- Nhập xuất console và file cơ bản: input() dừng chờ người dùng gõ rồi trả về chữ (str); muốn số phải đổi: n = int(input()); print(a, b, sep=', ', end='') chỉnh dấu ngăn cách và dấu kết thúc dòng; f-string giúp in đẹp; open('ten.txt') mở file; chế độ 'r' đọc, 'w' ghi (xóa nội dung cũ), 'a' ghi thêm vào cuối; with open(...) as f: tự đóng file khi ra khỏi khối, kể cả khi có lỗi, như tự đóng cửa khi rời phòng
- Bắt lỗi cơ bản với try/except: Exception: lỗi lúc chạy (ZeroDivisionError, ValueError, IndexError, KeyError, FileNotFoundError...); không bắt thì chương trình dừng và in traceback; try: thử chạy; except TenLoi: nếu gặp đúng lỗi đó thì chạy khối này và chương trình vẫn đi tiếp; Bắt đúng loại lỗi (except ValueError), không viết except trống vì sẽ nuốt cả lỗi bạn không ngờ tới; else chạy khi không có lỗi; finally luôn chạy dù có lỗi hay không (dùng để dọn dẹp)
- Biểu thức chính quy: Regex: mẫu mô tả dạng chữ cần tìm, như tìm trong Word nhưng linh hoạt hơn; dùng qua module re (import re); Ký tự đặc biệt: \d là một chữ số, \w là chữ, số hoặc gạch dưới, . là ký tự bất kỳ, [abc] là một trong các ký tự a, b, c; Lặp: + một hoặc nhiều, * không hoặc nhiều, ? không hoặc một, {3} đúng 3 lần; ^ và $ là đầu và cuối chuỗi; Ghép lại thành một mẫu: r'0\d{9}' là số 0 rồi đúng 9 chữ số; r'\d{4}-\d{2}-\d{2}' khớp ngày như 2025-03-14
- File, pathlib và serialization: pathlib.Path('thu_muc') / 'a.txt' ghép đường dẫn; .exists(), .read_text() đọc/kiểm tra file; JSON: định dạng chữ giống dict, ví dụ '{"ten": "An", "diem": [8, 9]}'; json.loads(chuoi) và json.load(file) đọc; CSV: bảng ngăn bằng dấu phẩy, mở được bằng Excel; csv.DictReader đọc mỗi dòng thành dict; os và shutil: tạo thư mục, sao chép, di chuyển, xóa file
- Parse file/log, biến đổi dữ liệu và tra cứu: Đọc từng dòng (for line in open(path)) thay vì nạp cả file vào bộ nhớ; hợp với file rất lớn; Cắt dòng: split khi định dạng đơn giản, regex (mẫu tìm chuỗi) khi phức tạp; định dạng CSV, JSON hoặc key=value; Dòng hỏng: có quy tắc rõ (bỏ qua và đếm số dòng hỏng, hoặc báo lỗi kèm số dòng), đừng để chương trình sập; Group-by (gom nhóm): Counter hoặc defaultdict để đếm, cộng; top-N bằng most_common; thời gian đọc bằng datetime.strptime

**Thời gian** (tổng 4h/4h): Học 75p · Luyện 135p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p

**Bài luyện (không phải bài mock)** · 5 bài

1. LC 226 Invert Binary Tree (E) 🔊 — `dsa.trees.tree_basics`
2. LC 703 Kth Largest Element in a Stream (E) — `dsa.heap.heap_ds`
3. LC 1797 Design Authentication Manager (M) — `dsa.design_ds.design_cache`
4. LC 729 My Calendar I (M) — `dsa.greedy_intervals.interval_sweep`
5. LC 54 Spiral Matrix (M) — `dsa.arrays_strings.matrix_traversal`

**Bài thêm nếu còn giờ (tùy chọn, không tính vào số bài của ngày)**: LC 1108 Defanging an IP Address (E); LC 1678 Goal Parser Interpretation (E); LC 8 String to Integer (atoi) (M); LC 7 Reverse Integer (M)

**Behavioral / AI (15-20 phút, tính trong phần Ôn hoặc trong giờ của subtopic bh)**: STORY #6: hạn chót bị dời hoặc yêu cầu chưa rõ (prioritization_ambiguity).

**Ôn lặp**: D+1: LC 1094 Car Pooling (ngày 18): viết lại không nhìn lời giải · D+3: LC 938 Range Sum of BST (ngày 16): viết lại không nhìn lời giải · D+7: LC 21 Merge Two Sorted Lists (ngày 12): viết lại không nhìn lời giải

### Ngày 20 · Thứ Bảy · tuần 3 · 6h: Parse file/log, biến đổi dữ liệu và tra cứu; Biểu diễn đồ thị và thuật ngữ; DFS và BFS trên đồ thị ...

**Subtopic**

- `dsa.practical.file_log_parsing` — Parse file/log, biến đổi dữ liệu và tra cứu (file and log parsing) (tiếp) — chia 2 ngày · 1h
- `dsa.graphs.graph_representation` — Biểu diễn đồ thị và thuật ngữ (graph representation) · 1h
- `dsa.graphs.graph_traversal` — DFS và BFS trên đồ thị (graph traversal) · 1.5h
- `dsa.graphs.grid_graphs` — BFS/DFS trên lưới (grid graphs) · 1.5h
- `dsa.graphs.bfs_shortest_path` — BFS đường đi ngắn nhất và tìm kiếm trạng thái (BFS shortest path) — chia 2 ngày · 0.5h

**Học gì**

- Biểu diễn đồ thị và thuật ngữ: Đồ thị (graph): đỉnh (vertex/node) và cạnh (edge). Bạn bè trên mạng xã hội, bản đồ đường, môn học tiên quyết đều là đồ thị; Có hướng / vô hướng (directed/undirected): cạnh một chiều (A theo dõi B) hay hai chiều (A và B là bạn); Bậc (degree) = số cạnh chạm vào đỉnh. Đường đi (path) = dãy đỉnh nối nhau bằng cạnh. Chu trình (cycle) = đường đi quay về đỉnh xuất phát; Thành phần liên thông (connected component): một cụm đỉnh đi được tới nhau; một đồ thị có thể gồm nhiều cụm rời nhau
- DFS và BFS trên đồ thị: DFS (depth-first search, duyệt chiều sâu): đi hết một nhánh tới cùng, hết đường thì quay lại; viết bằng đệ quy hoặc stack (chồng, vào sau ra trước); BFS (breadth-first search, duyệt chiều rộng): thăm hết đỉnh cách 1 bước, rồi cách 2 bước, ...; dùng queue (hàng đợi, vào trước ra trước); visited (tập đỉnh đã thăm): đồ thị có thể có vòng nên thiếu visited sẽ đi vô tận. Với BFS đánh dấu ngay khi đẩy vào queue; Cả DFS và BFS đều mất O(V+E): mỗi đỉnh và mỗi cạnh được xét một số lần cố định
- BFS/DFS trên lưới: Đi 4 hướng bằng danh sách (dr, dc) như [(1,0),(-1,0),(0,1),(0,-1)]; luôn kiểm tra ô mới còn nằm trong lưới trước khi dùng; đếm thành phần liên thông trên lưới (flood fill): đảo là cụm ô đất dính nhau; Flood fill và max area of island: cùng cách loang, chỉ khác thứ cần đếm (đổi màu hoặc đếm số ô); Đánh dấu đã thăm bằng set toạ độ, hoặc sửa thẳng ô thành "0" cho đỡ tốn bộ nhớ; chỉ sửa input khi đề cho phép
- BFS đường đi ngắn nhất và tìm kiếm trạng thái: BFS cho đường ngắn nhất khi không có trọng số: đỉnh nào được thăm sớm nhất ở vòng nào thì khoảng cách chính là số vòng đó; Đếm khoảng cách theo từng vòng: lấy len(queue) hiện tại làm một vòng, xong vòng thì tăng bước lên một; Trạng thái (state) = gói toàn bộ tình huống hiện tại thành một giá trị so sánh được (tuple), dùng làm đỉnh; ví dụ khoá số "0202" là một đỉnh; Open the Lock và Word Ladder: hàng xóm của trạng thái là các trạng thái sau đúng một thao tác (xem skill_tree)

**Thời gian** (tổng 6h/6h): Học 115p · Luyện 215p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p

**Bài luyện (không phải bài mock)** · 6 bài

1. LC 997 Find the Town Judge (E) 🔊 — `dsa.graphs.graph_representation`
2. LC 733 Flood Fill (E) — `dsa.graphs.grid_graphs`
3. LC 452 Minimum Number of Arrows to Burst Balloons (M) — `dsa.greedy_intervals.interval_sweep`
4. LC 811 Subdomain Visit Count (M) — `dsa.practical.file_log_parsing`
5. LC 785 Is Graph Bipartite? (M) ★ — `dsa.graphs.graph_traversal`
6. LC 547 Number of Provinces (M) — `dsa.graphs.graph_traversal`

**Bài thêm nếu còn giờ (tùy chọn, không tính vào số bài của ngày)**: LC 133 Clone Graph (M); LC 797 All Paths From Source to Target (M); LC 130 Surrounded Regions (M); LC 417 Pacific Atlantic Water Flow (M)

**Behavioral / AI (15-20 phút, tính trong phần Ôn hoặc trong giờ của subtopic bh)**: STORY thêm: lần học một thứ khó và mới (dùng cho câu "học nhanh"). Ôn miệng STORY #1-#4.

**Ôn lặp**: D+1: LC 54 Spiral Matrix (ngày 19): viết lại không nhìn lời giải · D+3: LC 706 Design HashMap (ngày 17): viết lại không nhìn lời giải · D+7: LC 1046 Last Stone Weight (ngày 13): viết lại không nhìn lời giải

### Ngày 21 · Chủ Nhật · tuần 3 · 6h: BFS đường đi ngắn nhất và tìm kiếm trạng thái; Topological sort, phụ thuộc và lập lịch task

**Subtopic**

- `dsa.graphs.bfs_shortest_path` — BFS đường đi ngắn nhất và tìm kiếm trạng thái (BFS shortest path) (tiếp) — chia 2 ngày · 1h
- `dsa.graphs.topological_sort` — Topological sort, phụ thuộc và lập lịch task (topological sort and scheduling) — chia 2 ngày · 1.25h

**Học gì**

- Topological sort, phụ thuộc và lập lịch task: Đồ thị phụ thuộc: vẽ mũi tên A -> B nghĩa là A phải xong trước B. Thứ tự topo chỉ tồn tại khi đồ thị là DAG (có hướng, không có chu trình); Thuật toán Kahn: đếm in-degree (số việc phải làm trước) của mỗi việc, cho các việc in-degree 0 vào queue, lấy ra làm rồi giảm in-degree của việc sau (xem skill_tree); Phát hiện chu trình bằng Kahn: nếu số việc đã lấy ra ít hơn tổng số việc thì còn một vòng phụ thuộc, không có thứ tự hợp lệ; Cách thứ hai bằng DFS: ghi đỉnh khi DFS xong nó (post-order), cuối cùng đảo ngược danh sách

**Thời gian** (tổng 6h/6h): Học 45p · Luyện 90p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p + Mock: N2 - Phone screen + Onsite coding 1 90p + Chấm mock + sửa lỗi 75p + Quiz cuối tuần + checkpoint 30p

**Bài luyện (không phải bài mock)** · 3 bài

1. LC 463 Island Perimeter (E) 🔊 — `dsa.graphs.grid_graphs`
2. LC 1091 Shortest Path in Binary Matrix (M) ★ — `dsa.graphs.bfs_shortest_path`
3. LC 994 Rotting Oranges (M) — `dsa.graphs.bfs_shortest_path`

**Bài thêm nếu còn giờ (tùy chọn, không tính vào số bài của ngày)**: LC 752 Open the Lock (M); LC 490 The Maze (M) (premium); LC 127 Word Ladder (H); LC 489 Robot Room Cleaner (H) (premium)

**Để dành cho mock (chỉ làm trong giờ mock)**: N2 - Phone screen + Onsite coding 1

- N2-R1-Q1 Binary Tree Vertical Order Traversal (LC 314) — Phone screen
- N2-R1-Q2 Find Peak Element (LC 162) — Phone screen
- N2-R2-Q1 Subarray Sum Equals K (LC 560) — Onsite coding 1
- N2-R2-Q2 LRU Cache (LC 146) — Onsite coding 1

**Ôn lặp**: D+3: LC 637 Average of Levels in Binary Tree (ngày 18): viết lại không nhìn lời giải · D+7: LC 34 Find First and Last Position of Element in Sorted Array (ngày 14): viết lại không nhìn lời giải · **Ôn mock D+7**: viết lại từ đầu (không xem lời giải) mọi câu của mock ngày 14 (I3 - Technical 1 + 2) mà bạn chấm ≤ 1; thay cho bài D+1 của ngày này

**Ôn mock sau buổi này**: D+3 → ngày 24, D+7 → ngày 28; chỉ làm lại câu bạn chấm ≤ 1.

### Ngày 22 · Thứ Hai · tuần 4 · 4h: Topological sort, phụ thuộc và lập lịch task; Thao tác bit; Định dạng vòng practical và bài nhiều phần ...

**Subtopic**

- `dsa.graphs.topological_sort` — Topological sort, phụ thuộc và lập lịch task (topological sort and scheduling) (tiếp) — chia 2 ngày · 0.75h
- `dsa.math_bits.bit_basics` — Thao tác bit (bit manipulation) · 1.5h
- `dsa.practical.practical_format` — Định dạng vòng practical và bài nhiều phần (practical round format) · 1h
- `dsa.practical.simulation_state_machines` — Mô phỏng và state machine (simulations and state machines) — chia 2 ngày · 0.25h

**Học gì**

- Thao tác bit: Nhị phân: 1101 là 13, 0110 là 6. Python in bằng bin(13) và viết 0b1101; AND (&): bit ra là 1 khi cả hai bit đều 1. OR (|): ra 1 khi có ít nhất một bit 1. XOR (^): ra 1 khi hai bit khác nhau. NOT (~): đảo bit; Dịch bit: x << 1 nhân đôi x, x >> 1 chia đôi (làm tròn xuống); 1 << i là số chỉ có bit i bật; Kiểm tra / bật / tắt / đảo bit i: x & (1<<i), x | (1<<i), x & ~(1<<i), x ^ (1<<i)
- Định dạng vòng practical và bài nhiều phần: Định dạng nhiều phần: phần sau thêm yêu cầu lên code cũ; ví dụ banking: 1 tạo tài khoản và nạp tiền, 2 chuyển tiền, 3 top chi tiêu, 4 chuyển hẹn giờ; Đọc hết đề, ghi các giả định, hỏi lại khi mơ hồ (thứ tự khi bằng nhau, xử lý lỗi thế nào); Viết code dễ mở rộng: hàm nhỏ, tên rõ, tách dữ liệu và xử lý; đừng tối ưu sớm khi chưa có yêu cầu; Test từng phần: ví dụ trong đề đổi thành assert (assert f(2) == 4, báo lỗi nếu sai)
- Mô phỏng và state machine: Dịch đúng từng luật đề: đọc kỹ, viết lại luật bằng lời mình, kiểm tra từng luật bằng ví dụ nhỏ; State machine (máy trạng thái): liệt kê trạng thái bằng enum và bảng "trạng thái + sự kiện -> trạng thái mới"; Mô phỏng lưới theo bước: mỗi bước tính lưới mới từ bản sao của lưới cũ (double buffer), nếu không ô sau sẽ thấy ô trước đã đổi (xem skill_tree); Robot đi theo lệnh: lưu vị trí và hướng, mỗi lệnh đổi hướng hoặc tiến lên một ô, kiểm tra biên

**Thời gian** (tổng 4h/4h): Học 75p · Luyện 135p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p

**Bài luyện (không phải bài mock)** · 5 bài

1. LC 953 Verifying an Alien Dictionary (E) ★ 🔊 — `dsa.graphs.topological_sort`
2. LC 191 Number of 1 Bits (E) — `dsa.math_bits.bit_basics`
3. LC 207 Course Schedule (M) ★ — `dsa.graphs.topological_sort`
4. LC 210 Course Schedule II (M) ★ — `dsa.graphs.topological_sort`
5. LC 1239 Maximum Length of a Concatenated String with Unique Characters (M) ★ — `dsa.math_bits.bit_basics`

**Bài thêm nếu còn giờ (tùy chọn, không tính vào số bài của ngày)**: LC 987 Vertical Order Traversal of a Binary Tree (H); LC 460 LFU Cache (H); LC 716 Max Stack (H) (premium); LC 310 Minimum Height Trees (M); LC 269 Alien Dictionary (H) (premium)

**Ôn lặp**: D+1: LC 994 Rotting Oranges (ngày 21): viết lại không nhìn lời giải · D+3: LC 226 Invert Binary Tree (ngày 19): viết lại không nhìn lời giải · D+7: LC 112 Path Sum (ngày 15): viết lại không nhìn lời giải

### Ngày 23 · Thứ Ba · tuần 4 · 4h: Mô phỏng và state machine; Refactor, debug và code review; Exception và xử lý lỗi ...

**Subtopic**

- `dsa.practical.simulation_state_machines` — Mô phỏng và state machine (simulations and state machines) (tiếp) — chia 2 ngày · 1.25h
- `dsa.practical.refactor_debug_review` — Refactor, debug và code review (refactoring, debugging and review rounds) · 1h
- `py.errors_modules.exceptions` — Exception và xử lý lỗi (exceptions) · 0.5h
- `py.typing_testing.pytest_testing` — Unit test với pytest, mock và thiết kế test — chia 2 ngày · 0.75h

**Học gì**

- Refactor, debug và code review: Đọc code lạ: chạy thử với ví dụ nhỏ, đọc hàm chính trước rồi mới đọc hàm phụ; Tái hiện rồi khoanh vùng bug: dùng print hoặc debugger để kiểm tra giá trị tại từng bước, thu hẹp dần đến một dòng; Bug hay gặp: lệch một (off-by-one), sửa list khi đang duyệt nó, hai biến cùng trỏ một list (aliasing), tham số mặc định là list; Tối ưu: thay hai vòng for lồng nhau O(n^2) bằng set hoặc dict O(n)
- Exception và xử lý lỗi: Custom exception (lỗi tự định nghĩa): class LoiSoDu(Exception) để lỗi mang đúng tên nghiệp vụ; nên có một class gốc chung rồi các class con; raise không đối số ném lại lỗi đang bắt; raise LoiMoi() from loi_cu đổi sang lỗi khác nhưng giữ nguyên nhân; finally luôn chạy, kể cả khi trong try có return; dùng để dọn dẹp; EAFP ('xin lỗi sau': cứ thử rồi bắt lỗi) và LBYL ('kiểm tra trước'): Python ưa EAFP
- Unit test với pytest, mock và thiết kế test: Test: hàm tên test_... nằm trong file tên test_*.py (pytest chỉ tìm file và hàm theo tên này), gọi code của bạn rồi dùng assert để kiểm tra kết quả; assert cong(1, 2) == 3: nếu sai, pytest in ra giá trị hai bên để dễ tìm lỗi; pytest.raises(ValueError) kiểm tra code báo đúng lỗi khi nhận dữ liệu xấu; Parametrize: chạy cùng một test với nhiều bộ dữ liệu: @pytest.mark.parametrize('n, kq', [(2, True), (9, False)]) rồi def test_nt(n, kq): assert (xem skill_tree)

**Thời gian** (tổng 4h/4h): Học 75p · Luyện 135p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p

**Bài luyện (không phải bài mock)** · 5 bài

1. LC 338 Counting Bits (E) 🔊 — `dsa.math_bits.bit_basics`
2. LC 1275 Find Winner on a Tic Tac Toe Game (E) — `dsa.practical.simulation_state_machines`
3. LC 523 Continuous Subarray Sum (M) ★ — `dsa.arrays_strings.prefix_sum`
4. LC 1020 Number of Enclaves (M) — `dsa.graphs.grid_graphs`
5. LC 542 01 Matrix (M) — `dsa.graphs.bfs_shortest_path`

**Bài thêm nếu còn giờ (tùy chọn, không tính vào số bài của ngày)**: LC 59 Spiral Matrix II (M); LC 289 Game of Life (M)

**Ôn lặp**: D+1: LC 1239 Maximum Length of a Concatenated String with Unique Characters (ngày 22): viết lại không nhìn lời giải · D+3: LC 997 Find the Town Judge (ngày 20): viết lại không nhìn lời giải · D+7: LC 938 Range Sum of BST (ngày 16): viết lại không nhìn lời giải

### Ngày 24 · Thứ Tư · tuần 4 · 4h: Unit test với pytest, mock và thiết kế test; Vòng code có hỗ trợ AI; Deep dive dự án kỹ thuật và bảo vệ quyết định ...

**Subtopic**

- `py.typing_testing.pytest_testing` — Unit test với pytest, mock và thiết kế test (tiếp) — chia 2 ngày · 0.25h
- `dsa.practical.ai_assisted_coding` — Vòng code có hỗ trợ AI (AI-assisted coding round) · 1h
- `bh.stories.project_deep_dive` — Deep dive dự án kỹ thuật và bảo vệ quyết định (project deep dive) · 1.5h
- `bh.motivation.why_company` — Vì sao công ty này và câu chuyện sự nghiệp (motivation & career story) — chia 2 ngày · 0.75h

**Học gì**

- Vòng code có hỗ trợ AI: Đọc luật trước: được dùng AI tới đâu, có phải nói ra khi dùng không; Prompt tốt có ngữ cảnh, ràng buộc và test. Xấu: "viết hàm lọc". Tốt: "Python 3, filter_active(users) trả user có active=True, giữ thứ tự, kèm 3 test"; Chia việc nhỏ trước khi hỏi, hỏi từng bước thay vì cả bài cùng lúc; Kiểm chứng đầu ra: chạy test và tự đọc code; AI hay bịa API không tồn tại (hallucination), hoặc bỏ sót ca biên
- Deep dive dự án kỹ thuật và bảo vệ quyết định: Chọn 1-2 dự án code bạn tự làm, hiểu thật sâu phần của mình (bài tập môn, dự án cá nhân, thực tập đều được); Nói theo thứ tự: dự án giải quyết vấn đề gì, phần bạn làm, cách bạn chọn và vì sao, kết quả, hạn chế; Mức bắt đầu: kể 2 phút một bài code bạn từng làm, nêu một chỗ khó và cách vượt qua; Không biết thì nói 'em chưa biết, em sẽ tìm theo cách...' thay vì đoán bừa
- Vì sao công ty này và câu chuyện sự nghiệp: Xem website, sản phẩm, blog kỹ thuật của công ty; ghi ra 2-3 điểm bạn thật sự thích; Gắn lý do với việc bạn từng làm hoặc muốn học: dự án, CLB, open source (dự án mã nguồn công khai); Vì sao vị trí/team này: nêu việc hằng ngày bạn muốn làm; Tránh 'vì lương cao' hay 'vì công ty nổi tiếng'. Intern nên nói về học hỏi, mentor, sản phẩm

**Thời gian** (tổng 4h/4h): Học 75p · Luyện 135p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p

**Bài luyện (không phải bài mock)** · 5 bài

1. LC 929 Unique Email Addresses (E) 🔊 — `dsa.practical.file_log_parsing`
2. LC 1971 Find if Path Exists in Graph (E) — `dsa.graphs.graph_representation`
3. LC 657 Robot Return to Origin (E) — `dsa.practical.simulation_state_machines`
4. LC 209 Minimum Size Subarray Sum (M) — `dsa.two_pointers_window.sliding_window_variable`
5. LC 78 Subsets (M) — `dsa.recursion_backtracking.backtracking_core`

**Behavioral / AI (15-20 phút, tính trong phần Ôn hoặc trong giờ của subtopic bh)**: Quay video 2 phút nói về dự án tự hào nhất (project_deep_dive): vấn đề, lựa chọn kỹ thuật, kết quả có số; chuẩn bị 3 câu đào sâu. Viết câu trả lời "Vì sao Meta / vì sao SWE" 90 giây (why_company).

**Ôn lặp**: D+3: LC 463 Island Perimeter (ngày 21): viết lại không nhìn lời giải · D+7: LC 706 Design HashMap (ngày 17): viết lại không nhìn lời giải · **Ôn mock D+3**: viết lại từ đầu (không xem lời giải) mọi câu của mock ngày 21 (N2 - Phone screen + Onsite coding 1) mà bạn chấm ≤ 1; thay cho bài D+1 của ngày này

### Ngày 25 · Thứ Năm · tuần 4 · 4h: Vì sao công ty này và câu chuyện sự nghiệp; Quy trình kỹ thuật có AI hỗ trợ; Kiểm chứng và sửa lỗi đầu ra của AI ...

**Subtopic**

- `bh.motivation.why_company` — Vì sao công ty này và câu chuyện sự nghiệp (motivation & career story) (tiếp) — chia 2 ngày · 0.25h
- `bh.ai_fluency.ai_workflow` — Quy trình kỹ thuật có AI hỗ trợ (AI-assisted workflow) · 1h
- `bh.ai_fluency.verify_ai_output` — Kiểm chứng và sửa lỗi đầu ra của AI (verifying AI output) · 1h
- `bh.ai_fluency.ai_safety_values` — An toàn AI và giá trị AI có trách nhiệm (AI safety values) · 1h

**Học gì**

- Quy trình kỹ thuật có AI hỗ trợ: Dùng AI để học: nhờ giải thích, gợi ý sửa lỗi, nhưng bạn phải tự hiểu từng dòng code nhận được; Coding agent là công cụ AI tự viết, sửa code theo yêu cầu. Bạn vẫn phải đọc diff (bản so sánh trước và sau); Không dán secret (mật khẩu, khoá) hay code riêng của công ty vào AI; Biết khi nào KHÔNG nên dùng AI: bài kiểm tra, việc bạn muốn học kỹ, dữ liệu nhạy cảm
- Kiểm chứng và sửa lỗi đầu ra của AI: Hallucination: AI bịa thông tin hoặc hàm không tồn tại nhưng nói như thật. Ví dụ AI nêu một cuốn sách không có; Luôn chạy thử code AI đưa ra và đọc hiểu từng dòng trước khi dùng; Đối chiếu tài liệu chính thức; thay số vào thử khi AI giải toán; Trách nhiệm cuối cùng thuộc về bạn, không phải AI
- An toàn AI và giá trị AI có trách nhiệm: Đọc trang sứ mệnh và quy tắc sử dụng của công ty để hiểu họ coi trọng điều gì; 4 rủi ro cơ bản: bị lạm dụng (misuse), làm sai mục tiêu (misalignment), thiên vị (bias), lộ riêng tư (privacy); Ví dụ: lạm dụng = người xấu nhờ chatbot viết thư lừa đảo; sai mục tiêu = nhờ "cho code chạy nhanh" mà AI xóa luôn test

**Thời gian** (tổng 3.75h/4h): Học 115p · Luyện 80p · Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p

**Bài luyện (không phải bài mock)** · 4 bài

1. LC 94 Binary Tree Inorder Traversal (E) 🔊 — `dsa.trees.tree_basics`
2. LC 33 Search in Rotated Sorted Array (M) — `dsa.searching_sorting.binary_search_variants`
3. LC 46 Permutations (M) — `dsa.recursion_backtracking.backtracking_core`
4. LC 874 Walking Robot Simulation (M) — `dsa.practical.simulation_state_machines`

**Behavioral / AI (15-20 phút, tính trong phần Ôn hoặc trong giờ của subtopic bh)**: STORY #7 [AI]: quy trình bạn dùng AI khi học/làm: công cụ, việc giao cho AI, việc tự làm, cách kiểm chứng. STORY #8 [AI]: một lần AI sai và bạn phát hiện/sửa (verify_ai_output); chuẩn bị 3 dấu hiệu "code AI đáng ngờ". STORY #9 [AI]: trách nhiệm với code do AI viết; khi nào bác bỏ gợi ý (ai_safety_values); 15 phút nhắc lại LLM là gì (hallucination, context).

**Ôn lặp**: D+1: LC 78 Subsets (ngày 24): viết lại không nhìn lời giải · D+3: LC 953 Verifying an Alien Dictionary (ngày 22): viết lại không nhìn lời giải · D+7: LC 637 Average of Levels in Binary Tree (ngày 18): viết lại không nhìn lời giải

### Ngày 26 · Thứ Sáu · tuần 4 · 4h: Buffer

Không có nội dung mới.

**Thời gian** (tổng 2.75h/4h): Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p + Luyện tổng hợp (bài còn thiếu, pattern yếu) 135p

**Luyện tổng hợp: bài còn thiếu theo subtopic và pattern yếu (không phải bài mock)** · 5 bài

1. LC 905 Sort Array By Parity (E) 🔊 — `dsa.arrays_strings.array_techniques`
2. LC 136 Single Number (E) — `dsa.math_bits.bit_basics`
3. LC 451 Sort Characters By Frequency (M) — `dsa.searching_sorting.sorting_applications`
4. LC 658 Find K Closest Elements (M) — `dsa.heap.heap_top_k`
5. LC 17 Letter Combinations of a Phone Number (M) — `dsa.recursion_backtracking.backtracking_core`

**Ôn lặp**: D+1: LC 874 Walking Robot Simulation (ngày 25): viết lại không nhìn lời giải · D+3: LC 338 Counting Bits (ngày 23): viết lại không nhìn lời giải · D+7: LC 226 Invert Binary Tree (ngày 19): viết lại không nhìn lời giải

### Ngày 27 · Thứ Bảy · tuần 4 · 6h: Mock + đánh giá

Không có nội dung mới.

**Thời gian** (tổng 5.25h/6h): Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p + Mock: N1 - Phone screen + Onsite coding 1 + 2 135p + Chấm mock + sửa lỗi 60p + Luyện tổng hợp (bài còn thiếu, pattern yếu) 90p

**Luyện tổng hợp: bài còn thiếu theo subtopic và pattern yếu (không phải bài mock)** · 3 bài

1. LC 190 Reverse Bits (E) 🔊 — `dsa.math_bits.bit_basics`
2. LC 438 Find All Anagrams in a String (M) — `dsa.arrays_strings.string_algorithms`
3. LC 912 Sort an Array (M) — `dsa.searching_sorting.sorting_algorithms`

**Để dành cho mock (chỉ làm trong giờ mock)**: N1 - Phone screen + Onsite coding 1 + 2

- N1-R1-Q1 Valid Palindrome II (LC 680) — Phone screen
- N1-R1-Q2 Top K Frequent Elements (LC 347) — Phone screen
- N1-R2-Q1 Merge Intervals (LC 56) — Onsite coding 1 (truyền thống)
- N1-R2-Q2 Binary Tree Right Side View (LC 199) — Onsite coding 1 (truyền thống)
- N1-R3-Q1 Minimum Remove to Make Valid Parentheses (LC 1249) — Onsite coding 2 (truyền thống)
- N1-R3-Q2 Dot Product of Two Sparse Vectors (LC 1570) — Onsite coding 2 (truyền thống)

**Ôn lặp**: D+1: LC 17 Letter Combinations of a Phone Number (ngày 26): viết lại không nhìn lời giải · D+3: LC 929 Unique Email Addresses (ngày 24): viết lại không nhìn lời giải · D+7: LC 997 Find the Town Judge (ngày 20): viết lại không nhìn lời giải

**Ôn mock sau buổi này**: D+3 → ngày 30; chỉ làm lại câu bạn chấm ≤ 1.

### Ngày 28 · Chủ Nhật · tuần 4 · 6h: Mock + đánh giá

Không có nội dung mới.

**Thời gian** (tổng 5.25h/6h): Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p + Mock: N2 AI-enabled + N2 Behavioral + N1 Behavioral 150p + Chấm mock + sửa lỗi 75p + Quiz cuối tuần + checkpoint 30p + Luyện tổng hợp (bài còn thiếu, pattern yếu) 30p

**Luyện tổng hợp: bài còn thiếu theo subtopic và pattern yếu (không phải bài mock)** · 1 bài

1. LC 108 Convert Sorted Array to Binary Search Tree (E) 🔊 — `dsa.trees.bst`

**Bài thêm nếu còn giờ (tùy chọn, không tính vào số bài của ngày)**: LC 921 Minimum Add to Make Parentheses Valid (M); LC 301 Remove Invalid Parentheses (H); LC 57 Insert Interval (M); LC 253 Meeting Rooms II (M) (premium)

**Để dành cho mock (chỉ làm trong giờ mock)**: N2 AI-enabled + N2 Behavioral + N1 Behavioral

- N2-R4-Q1 AI-enabled: Card game "Pick 15" (sum-fifteen) — AI-enabled coding (tùy chọn: có thể gặp, thay 1 vòng coding)
- N2-R5-Q1 Dự án bạn tự hào nhất — Behavioral
- N2-R5-Q2 Hạn chót bị dời sớm — Behavioral
- N2-R5-Q3 Vì sao Meta? — Behavioral
- N2-R5-Q4 Nhận phản hồi khó — Behavioral
- N2-R5-Q5 [AI] Trách nhiệm với code do AI viết — Behavioral
- N1-R5-Q1 Project bạn tự hào nhất — Behavioral
- N1-R5-Q2 Bất đồng với bạn cùng nhóm — Behavioral
- N1-R5-Q3 Một lần bạn mắc lỗi hoặc thất bại — Behavioral
- N1-R5-Q4 [AI] Bạn dùng AI khi học và làm dự án như thế nào? — Behavioral
- N1-R5-Q5 [AI] Một lần AI trả lời sai — Behavioral

**Behavioral / AI (15-20 phút, tính trong phần Ôn hoặc trong giờ của subtopic bh)**: Ôn miệng toàn bộ 9 story + câu "Vì sao Meta" trước khi vào mock behavioral.

**Ôn lặp**: D+3: LC 94 Binary Tree Inorder Traversal (ngày 25): viết lại không nhìn lời giải · D+7: LC 463 Island Perimeter (ngày 21): viết lại không nhìn lời giải · **Ôn mock D+7**: viết lại từ đầu (không xem lời giải) mọi câu của mock ngày 21 (N2 - Phone screen + Onsite coding 1) mà bạn chấm ≤ 1; thay cho bài D+1 của ngày này

**Ôn mock sau buổi này**: dùng buffer cuối tháng; chỉ làm lại câu bạn chấm ≤ 1.

### Ngày 29 · Thứ Hai · tuần 5 · 4h: Mock + đánh giá

Không có nội dung mới.

**Thời gian** (tổng 2.75h/4h): Ôn lặp (D+1, D+3, D+7) + nhật ký lỗi 30p + Mock: N2 - Onsite coding 2 + N6 OA Level 1-2 (buffer) 90p + Chấm mock + sửa lỗi 45p

**Để dành cho mock (chỉ làm trong giờ mock)**: N2 - Onsite coding 2 + N6 OA Level 1-2 (buffer)

- N2-R3-Q1 Exclusive Time of Functions (LC 636) — Onsite coding 2
- N2-R3-Q2 Number of Islands (LC 200) — Onsite coding 2
- N6-R1-Q1 Level 1 - Tài khoản cơ bản: create / deposit / transfer (LC -) — Phần 1 — OA CodeSignal-style, 4 level (PLAUSIBLE)
- N6-R1-Q2 Level 2 - Top spenders (xếp hạng chi tiêu) (LC -) — Phần 1 — OA CodeSignal-style, 4 level (PLAUSIBLE)

**Ôn lặp**: D+1: LC 108 Convert Sorted Array to Binary Search Tree (ngày 28): viết lại không nhìn lời giải · D+3: LC 905 Sort Array By Parity (ngày 26): viết lại không nhìn lời giải · D+7: LC 953 Verifying an Alien Dictionary (ngày 22): viết lại không nhìn lời giải

**Ôn mock sau buổi này**: dùng buffer cuối tháng; chỉ làm lại câu bạn chấm ≤ 1.

**Buffer**: còn khoảng 1.2h dự phòng: bù bài/subtopic bị nợ trong checkpoint, hoặc quay lại mục 2.4. Nếu đúng tiến độ: làm N2 Onsite coding 2 và N6-R1 Level 1-2 trong giờ mock rồi làm gói AI/ML.

### Ngày 30 · Thứ Ba · tuần 5 · 4h: Buffer

Không có nội dung mới.

**Thời gian** (tổng 3.5h/4h): Chạy lại chẩn đoán đầu vào 120p + Điền bảng sẵn sàng + go/no-go 30p + Bù lỗi lớn nhất + kế hoạch tiếp theo 60p

**Bài thêm nếu còn giờ (tùy chọn, không tính vào số bài của ngày)**: LC 695 Max Area of Island (M)

**Ôn lặp**: D+3: LC 190 Reverse Bits (ngày 27): viết lại không nhìn lời giải · D+7: LC 338 Counting Bits (ngày 23): viết lại không nhìn lời giải · **Ôn mock D+3**: viết lại từ đầu (không xem lời giải) mọi câu của mock ngày 27 (N1 - Phone screen + Onsite coding 1 + 2) mà bạn chấm ≤ 1; thay cho bài D+1 của ngày này

**Buffer + Đánh giá cuối tháng**: chạy lại chẩn đoán đầu vào (2h), điền bảng sẵn sàng, quyết định go/no-go (`assessment.md` mục 3).

## 5. Bài luyện "nói to khi code" (think-aloud)

Từ ngày 6, bài đầu tiên của mỗi ngày (có 🔊) làm theo khung 6 bước, nói thành tiếng và ghi âm 1 lần/tuần để nghe lại:

1. Nhắc lại đề bằng lời của mình + hỏi 2 câu làm rõ (input rỗng? trùng? âm? kích thước?).
2. Đưa 1 ví dụ nhỏ, tự giải bằng tay.
3. Nói cách chậm trước (brute force) + độ phức tạp, rồi cách tối ưu và vì sao.
4. Viết code, vừa viết vừa nói tên biến và ý định từng khối.
5. Chạy thử bằng tay (dry-run) 1 ví dụ thường + 1 ví dụ biên.
6. Nói time/space cuối cùng và 1 cách cải tiến.

Chấm 5 trục (xem `assessment.md` mục 2.3): Correctness, Complexity, Code quality, Communication, Testing.

## 6. Ngân hàng story behavioral và dùng AI (rải trong tháng)

Mỗi story viết theo STAR/CARL (Situation, Task, Action, Result; Result có số hoặc bằng chứng). Lưu vào bảng: tên story, 4 câu, thời lượng nói (≤ 2 phút), câu hỏi mà story trả lời được.

| Ngày | Việc |
|---|---|
| 10 | Viết 60 giây giới thiệu bản thân (bh.method.self_intro), đọc to và đo giờ. Học khung STAR/CARL; viết STORY #1 (dự án ở trường/cá nhân): 5 câu Situation-Task-Action-Result. |
| 13 | Ôn miệng 2 story đã viết (STORY #1, #2) trong 10 phút; đo giờ ≤ 2 phút mỗi story. |
| 14 | STORY #2: một lần làm nhóm có bất đồng (conflict_teamwork). Nêu rõ phần việc CỦA BẠN, không nói xấu người khác. STORY #3 và #4: một lần mắc lỗi/thất bại bạn đã sửa thế nào, và một lần nhận phản hồi khó nghe (failure_feedback). |
| 18 | STORY #5: dẫn dắt khi không có chức danh / chủ động làm thêm (ownership_leadership). |
| 19 | STORY #6: hạn chót bị dời hoặc yêu cầu chưa rõ (prioritization_ambiguity). |
| 20 | STORY thêm: lần học một thứ khó và mới (dùng cho câu "học nhanh"). Ôn miệng STORY #1-#4. |
| 24 | Quay video 2 phút nói về dự án tự hào nhất (project_deep_dive): vấn đề, lựa chọn kỹ thuật, kết quả có số; chuẩn bị 3 câu đào sâu. Viết câu trả lời "Vì sao Meta / vì sao SWE" 90 giây (why_company). |
| 25 | STORY #7 [AI]: quy trình bạn dùng AI khi học/làm: công cụ, việc giao cho AI, việc tự làm, cách kiểm chứng. STORY #8 [AI]: một lần AI sai và bạn phát hiện/sửa (verify_ai_output); chuẩn bị 3 dấu hiệu "code AI đáng ngờ". STORY #9 [AI]: trách nhiệm với code do AI viết; khi nào bác bỏ gợi ý (ai_safety_values); 15 phút nhắc lại LLM là gì (hallucination, context). |
| 28 | Ôn miệng toàn bộ 9 story + câu "Vì sao Meta" trước khi vào mock behavioral. |

Gợi ý ghép story ↔ câu mock: 3 story đủ trả lời hầu hết câu (dự án, bất đồng, thất bại); thêm 1 story "học cái khó", 1 story "mơ hồ/hạn chót", 1 story "dẫn dắt", 3 story AI (quy trình dùng AI, AI sai, trách nhiệm code AI).

**Vòng AI-enabled (60 phút, ngày 22-28)**: tập đọc code có sẵn → chạy test → viết giả thuyết bug → mới nhờ AI → tự đọc lại đề xuất → viết test → nói to lý do tin/bác bỏ. Không dán nguyên đề vào AI.

## 7. Dùng file mock mỗi tuần

File Word `Meta_2026_Intern_NewGrad_Mock.docx` (sinh từ `content_ng/*.json`) có: đề, gợi ý 3 bậc, lời giải, lỗi hay gặp, bảng tự chấm. Quy trình mỗi lần mock:

1. **Chuẩn bị** (5 phút): tắt autocomplete/AI, mở trình soạn thảo trống, bấm giờ đúng như vòng (45 hoặc 60 phút).
2. **Làm**: chỉ xem đề; được xem "gợi ý bậc 1" nếu kẹt 10 phút (trừ 1 điểm Correctness); không xem lời giải.
3. **Chấm** (xem rubric `assessment.md` mục 2.3): chạy lại code, đối chiếu lời giải, chấm 5 trục 0-3.
4. **Ghi lỗi** vào nhật ký (mục 11.1): loại lỗi, subtopic id, cách sửa, ngày ôn lại.
5. **Làm lại** câu sai sau 3 ngày (D+3) và 7 ngày (D+7) bằng cách viết lại từ đầu.
6. **Quy tắc không lộ đề**: chỉ mở mock đúng ngày. Bài luyện hằng ngày đã loại câu của mock trong lịch và các bài follow-up (biến thể) được nêu trong lời giải của chúng, cho đến sau ngày mock đó (kiểm tra V4, V4d). Riêng LC 20 Valid Parentheses được miễn vì là bài nền của stack_problems.

| Tuần | Mock | Ngày | Ghi chú |
|---|---|---|---|
| 1 | I1 - Technical 1 | 7 | I1-R1-Q1; I1-R1-Q2 |
| 2 | I3 - Technical 1 + 2 | 14 | I3-R1-Q1; I3-R1-Q2; I3-R2-Q1; I3-R2-Q2 |
| 3 | N2 - Phone screen + Onsite coding 1 | 21 | N2-R1-Q1; N2-R1-Q2; N2-R2-Q1; N2-R2-Q2 |
| 4 | N1 - Phone screen + Onsite coding 1 + 2 | 27 | N1-R1-Q1; N1-R1-Q2; N1-R2-Q1; N1-R2-Q2; N1-R3-Q1; N1-R3-Q2 |
| 4 | N2 AI-enabled + N2 Behavioral + N1 Behavioral | 28 | N2-R4-Q1; N2-R5-Q1; N2-R5-Q2; N2-R5-Q3; N2-R5-Q4; N2-R5-Q5; N1-R5-Q1; N1-R5-Q2; N1-R5-Q3; N1-R5-Q4; N1-R5-Q5 |
| 5 | N2 - Onsite coding 2 + N6 OA Level 1-2 (buffer) | 29 | N2-R3-Q1; N2-R3-Q2; N6-R1-Q1; N6-R1-Q2 |

### 7.1 Mock đã được "thả" vào kho bài luyện (review M1)

Chỉ các câu của mock **trong lịch** bị khoá. Các bộ I2, I4, N3, N4, N5, N6 không làm trong tháng nên bài LeetCode của chúng được dùng làm bài luyện cho đúng subtopic (nếu không thì các subtopic hot như LCA, Diameter, K Closest, Valid Parentheses sẽ không có bài nào). Hệ quả: khi làm các mock đó sau tháng 1, các câu đã thả sẽ không còn "chưa thấy"; câu chưa dùng vẫn nguyên.

| Câu | LC | Trạng thái trong kế hoạch |
|---|---|---|
| I1-R2-Q1 Product of Array Except Self | 238 | bài luyện ngày 8 |
| I2-R1-Q1 Valid Word Abbreviation | 408 | bài thêm (tùy chọn) ngày 6 |
| I2-R1-Q2 Squares of a Sorted Array | 977 | bài luyện ngày 7 |
| I2-R2-Q1 Basic Calculator II | 227 | bài luyện ngày 10 |
| I2-R2-Q2 Sum Root to Leaf Numbers | 129 | bài luyện ngày 15 |
| I4-R1-Q1 Valid Parentheses | 20 | bài luyện ngày 9 |
| I4-R1-Q2 K Closest Points to Origin | 973 | bài luyện ngày 13 |
| N3-R1-Q1 Lowest Common Ancestor of a Binary Tree | 236 | bài luyện ngày 15 |
| N3-R1-Q2 Meeting Rooms II | 253 | bài thêm (tùy chọn) ngày 28 |
| N3-R2-Q1 Random Pick with Weight | 528 | chưa dùng, để dành cho mock sau tháng 1 |
| N3-R2-Q2 Copy List with Random Pointer | 138 | bài luyện ngày 9 |
| N3-R3-Q1 Maximum Length of a Concatenated String with Unique Characters | 1239 | bài luyện ngày 22 |
| N3-R3-Q2 Binary Search Tree Iterator | 173 | bài luyện ngày 16 |
| N4-R1-Q1 Pow(x, n) | 50 | bài luyện ngày 11 |
| N4-R1-Q2 Nested List Weight Sum | 339 | chưa dùng, để dành cho mock sau tháng 1 |
| N4-R2-Q1 Shortest Path in Binary Matrix | 1091 | bài luyện ngày 21 |
| N4-R2-Q2 Remove All Adjacent Duplicates in String II | 1209 | bài luyện ngày 9 |
| N4-R3-Q1 Verifying an Alien Dictionary | 953 | bài luyện ngày 22 |
| N4-R3-Q2 Insert Delete GetRandom O(1) | 380 | bài luyện ngày 17 |
| N5-R1-Q1 Max Consecutive Ones III | 1004 | bài thêm (tùy chọn) ngày 13 |
| N5-R1-Q2 Buildings With an Ocean View | 1762 | bài thêm (tùy chọn) ngày 9 |
| N5-R2-Q1 Continuous Subarray Sum | 523 | bài luyện ngày 23 |
| N5-R3-Q1 Moving Average from Data Stream | 346 | chưa dùng, để dành cho mock sau tháng 1 |
| N6-R2-Q1 Diameter of Binary Tree | 543 | bài luyện ngày 15 |
| N6-R2-Q2 Interval List Intersections (+ union) | 986 | bài luyện ngày 17 |
| N6-R3-Q1 Next Permutation | 31 | chưa dùng, để dành cho mock sau tháng 1 |
| N6-R3-Q2 Diagonal Traverse | 498 | bài thêm (tùy chọn) ngày 18 |
| N6-R4-Q1 Linked List Random Node (reservoir sampling) | 382 | chưa dùng, để dành cho mock sau tháng 1 |

**Mock dự trữ** (làm sau tháng 1 hoặc nếu dư giờ buffer): I2 (Java), I4 (AI/ML), N3/N4 (Java; làm bằng Python cũng được), N5 (AI/ML), N6 (Level 3-4 và các vòng còn lại). Còn **chưa bị dùng** làm bài luyện: N3-R2-Q1 (LC 528), N4-R1-Q2 (LC 339), N5-R3-Q1 (LC 346), N6-R3-Q1 (LC 31), N6-R4-Q1 (LC 382) cùng toàn bộ câu không có LC (behavioral, ML, AI-enabled, OA).

## 8. Gói AI/ML (cho I4 và N5)

Track AI/ML cần thêm ≈ **22 giờ** (hệ số nén như SWE). Cách lấy giờ: (1) rút bớt các mục SWE không thuộc Top-40: `dsa.two_pointers_window.sliding_window_fixed` −1h (bỏ hẳn; sliding_window_variable dạy luôn cửa sổ cố định); `dsa.arrays_strings.matrix_traversal` −1h (chỉ giữ 0.5h duyệt lưới (cần cho grid_graphs), bỏ spiral/rotate/zero matrix); `dsa.design_ds.design_o1_structures` −0.5h (bỏ phần Insert Delete GetRandom, giữ phần LRU (N2 cần)) = 2.5h; (2) dùng giờ trống ở ngày 26-30 sau khi trừ phần luyện tổng hợp và buffer (≈ 1.5h); (3) còn thiếu ≈ **18.0h**: cần thêm khoảng 54 phút/ngày trong 20 ngày (ngày 8-27), hoặc theo bản 6 giờ/ngày ở mục 1. Mỗi buổi thêm học 1 subtopic bên dưới theo thứ tự.

| Subtopic ML (thứ tự học) | Giờ |
|---|---|
| `ml.fundamentals.ml_overview` — Các dạng học máy và quy trình ML (ML workflow) | 1 |
| `ml.classical.decision_trees` — Cây quyết định (decision trees) | 1 |
| `ml.math.linear_algebra_basics` — Vector, ma trận và phép nhân ma trận (linear algebra) | 1 |
| `ml.math.random_variables_expectation` — Biến ngẫu nhiên, kỳ vọng và phương sai (random variables) | 1 |
| `ml.classical.dimensionality_reduction` — Giảm chiều: PCA, t-SNE, UMAP (dimensionality reduction) | 1 |
| `ml.fundamentals.loss_functions` — Hàm mất mát (loss functions) | 1 |
| `ml.math.derivatives_gradients` — Đạo hàm, gradient và quy tắc chuỗi (derivatives) | 1 |
| `ml.math.gradient_descent` — Gradient descent và tối ưu cơ bản (gradient descent) | 1 |
| `ml.classical.linear_regression` — Hồi quy tuyến tính (linear regression) | 1 |
| `ml.classical.logistic_regression` — Hồi quy logistic (logistic regression) | 1 |
| `ml.classical.knn_nb_svm` — k-NN, Naive Bayes và SVM (k-NN, Naive Bayes, SVM) | 1 |
| `ml.classical.unsupervised` — Phân cụm và giảm chiều (unsupervised learning) | 1.5 |
| `py.ecosystem.numpy_basics` — NumPy và vector hóa (vectorization) | 1.5 |
| `ml.coding.kmeans_knn_trees` — Cài đặt k-means, k-NN, cây quyết định (algorithms from scratch) | 1 |
| `ml.coding.linear_logistic_scratch` — Cài đặt hồi quy tuyến tính/logistic từ đầu (models from scratch) | 1 |
| `ml.fundamentals.bias_variance_overfitting` — Bias-variance, overfitting và regularization (bias-variance) | 1 |
| `ml.fundamentals.validation_tuning` — Validation, cross-validation và tuning (validation) | 1 |
| `py.ecosystem.pandas_basics` — pandas cơ bản: Series, DataFrame, chọn dữ liệu | 1 |
| `ml.data_features.cleaning_missing` — Làm sạch dữ liệu, mã hóa và chuẩn hóa (data cleaning) | 1 |
| `ml.coding.pipeline_debugging` — Pipeline end-to-end và debug (pipeline debugging) | 1 |
| `ml.fundamentals.classification_metrics` — Metric phân loại và calibration (classification metrics) | 1 |

Coi như đã biết: `ml.math.algebra_functions_bridge` (Đại số/hàm số lớp 12; ôn 30 phút nếu quên.); `ml.math.probability_basics` (Xác suất cơ bản năm nhất; chỉ nhắc lại 20 phút trong ngày metrics.)

Câu mock ML được chuẩn bị trong gói này: I4-R2-Q3 Precision, Recall, F1 và vài câu ML cơ bản, N5-R4-Q1 AI-enabled: Fix and extend a spam-classifier evaluation script, I4-R2-Q2 Linear Regression: Derive and Implement (NumPy), N6-R4-Q2 Logistic Regression from scratch (NumPy), N5-R2-Q2 ML coding: Implement k-means from scratch (NumPy).

Chưa đủ giờ (cần thêm transformer/attention, ≈ 10 giờ nữa; làm sau tháng 1 hoặc nếu theo track AI chuyên sâu): I4-R2-Q1 Scaled Dot-Product Attention (NumPy), N5-R3-Q2 ML coding: Multi-head self-attention forward pass (NumPy).

Thứ tự gợi ý: numpy_basics → linear_regression/gradient_descent → logistic → metrics/bias-variance → unsupervised/kNN → ML coding scratch; làm I4 Technical 2 (ML coding) vào ngày 25-26 và N5 vào ngày 29-30. Đánh giá riêng của gói này là cụm C11 trong `assessment.md`.

## 9. Ghi chú biến thể Java

Giữ nguyên thứ tự dsa.*, đổi phần ngôn ngữ:

| Phần Python | Thay bằng (Java) |
|---|---|
| py.core.* (ngày 1-3) | `java.core.platform_basics`, `java.core.types_variables`, `java.core.control_flow`, `java.core.strings` |
| py.datastructs.* (ngày 3-5) | `java.core.arrays`, `java.collections.lists`, `java.collections.hashmap_internals`, `java.collections.sets_maps_variants` |
| heap / deque / sort (tuần 2) | `java.collections.queues_deques`, `java.collections.deque_heap_basic`, `java.collections.interview_idioms_basic` |
| py.oop.classes_basics (ngày 10) | `java.oop.oop_intro`, `java.oop.classes_constructors` |

Mock Java sẵn có: I2, N3, N4. Lưu ý Java: `Integer` overflow (Pow(x, n) với `Integer.MIN_VALUE`), `PriorityQueue` với comparator, `ArrayDeque` thay `deque`, `HashMap.getOrDefault`. Cộng thêm ≈ 8-10 giờ cho cú pháp (chuyển từ buffer và bớt `py.*`).

## 10. Đánh giá kiến thức (layer 2)

Quy trình đầy đủ nằm ở `assessment.md` (và `assessment.json`): (1) chẩn đoán đầu vào Day 0 (2-3h) có luật thích nghi và cách điều chỉnh kế hoạch; (2) quiz cuối mỗi tuần + rubric chấm mock + quy tắc qua/không qua; (3) đánh giá cuối tháng, bảng sẵn sàng và luật go/no-go; (4) bảng theo dõi để điền.

## 11. Nhật ký lỗi, quy tắc điểm, và khi bị chậm tiến độ

### 11.1 Nhật ký lỗi

Mỗi lần sai (bài luyện hoặc mock) ghi 1 dòng:

| Ngày | Bài / câu | Subtopic id | Loại lỗi | Nguyên nhân gốc | Cách sửa (1 câu) | Ôn lại D+3 | Ôn lại D+7 | Xong |
|---|---|---|---|---|---|---|---|---|
| 5 | LC 209 | dsa.two_pointers_window.sliding_window_variable | Biên | quên co cửa sổ khi tổng ≥ target | dùng while thay if | 8 | 12 | ☐ |

Loại lỗi: **Hiểu đề**, **Chọn cấu trúc/pattern**, **Logic**, **Biên (edge case)**, **Cú pháp/API Python**, **Độ phức tạp**, **Giao tiếp**, **Hết giờ**. Cuối tuần đếm loại lỗi nhiều nhất và dành 30 phút buffer cho nó.

### 11.2 Quy tắc điểm 0-3 (tự chấm mỗi subtopic)

- **0**: không nhớ khái niệm. **1**: giải thích được nhưng không tự code được bài easy. **2**: tự code bài easy-medium đúng trong ≤ 25 phút, có thể xem 1 gợi ý. **3**: code đúng bài medium không gợi ý trong ≤ 20 phút, nêu đúng time/space và 2 test biên.

### 11.3 Chưa qua checkpoint / bị chậm

| Tình huống | Làm gì |
|---|---|
| Một subtopic < 2 cuối tuần | Dùng buffer của tuần tới: đọc lại concept 20 phút, làm lại 3 bài đã sai (viết lại, không xem), làm quiz lại. Nếu vẫn < 2: học tiếp nhưng đánh dấu "nợ" và thêm 2 bài mỗi ngày vào phần ôn. |
| Chậm ≤ 1 ngày | Dùng ngày 29 (buffer 1), bỏ phần "Học" của mục ít ưu tiên trong ngày đó (xem thứ tự cắt bên dưới). |
| Chậm 2-3 ngày | Dùng cả 2 buffer, cắt theo thứ tự: `matrix_traversal` → `sliding_window_fixed` → `simulation_state_machines` (giữ phần card game của N2) → phần Insert Delete GetRandom của `design_o1_structures` (giữ LRU, vì N2 cần). Giữ `bit_basics`, `string_algorithms`, `topological_sort` vì thuộc Top-40. Giữ nguyên mock và behavioral. |
| Chậm > 3 ngày | Chuyển sang bản 2h/ngày (mục 1) hoặc kéo dài thêm 1 tuần; không bỏ mock cuối tuần 1-3. |
| Mock điểm Correctness < 2 hai lần liên tiếp | Quay lại mức dễ hơn của chính pattern đó (LC easy cùng chủ đề) trước khi làm mock tiếp. |
| Hiểu nhưng chậm | Giữ bài, nhưng bấm giờ 25 phút/bài; viết lại từ trí nhớ vào D+3, D+7. |
