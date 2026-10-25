# Quy trình đánh giá kiến thức cho kế hoạch Meta 1 tháng

> Sinh bởi `build_assessment.py`. Dữ liệu máy đọc: `assessment.json` (item có `subtopic_id`, `difficulty`, `type`, `prompt`, `answer`, `rubric`). Bảng theo dõi để điền: `tracking.csv` và mục 4. Kế hoạch: `plan.md`. Thang điểm 0-3 theo `interview-prep/README.md`: **0** chưa biết · **1** biết lý thuyết · **2** làm được bài cơ bản · **3** mức phỏng vấn.

## 0. Tóm tắt quy trình

| Thời điểm | Việc | Thời gian | Kết quả |
|---|---|---|---|
| **Day 0** (trước ngày 1) | Chẩn đoán đầu vào, thích nghi theo cụm (mục 1) | 2-3 giờ | Điểm 0-3 từng subtopic → điều chỉnh giờ kế hoạch |
| **Cuối mỗi tuần** (ngày 7, 14, 21, 28) | Quiz 30 phút + chấm mock theo rubric (mục 2) | 30 phút + giờ mock | Qua/không qua; nhật ký lỗi |
| **Ngày 29-30** | Mock đầy đủ chấm bằng rubric + chạy lại chẩn đoán + bảng sẵn sàng (mục 3) | ~3 giờ | Go / Go có điều kiện / No-go |
| **Mỗi ngày** | Ôn lặp D+1/D+3/D+7 + nhật ký lỗi (mục 4) | 30 phút | Điểm tự chấm cập nhật |

Ngân hàng câu hỏi: **254** item (212 chẩn đoán + 42 quiz tuần), phủ **82** subtopic SWE và **21** subtopic gói AI/ML; **175** item code đã được chạy để kiểm chứng output (xem mục 5).

## 1. Đánh giá đầu vào (Day 0, 2-3 giờ)

### 1.1 Cách làm

- Mỗi subtopic có item mức 1 (khái niệm/đọc code), mức 2 (viết bài cơ bản), một số có mức 3 (bài medium/phức tạp hơn). Riêng item behavioral (bh.*) chấm TRỰC TIẾP điểm 0-3 theo rubric của item, không đi theo bậc thang mức 1 → 2 → 3.
- Bắt đầu từ item mức 2. Đúng → nếu có item mức 3 (subtopic hot) thì làm tiếp mức 3: đúng = điểm 3, sai = điểm 2; nếu không có mức 3: điểm 2.
- Sai mức 2 → xuống item mức 1: đúng = điểm 1, sai = điểm 0. Subtopic không có item mức 1 (chỉ có mức 2-3): sai mức 2 thì xem đáp án rồi tự giải thích ý tưởng chính bằng lời trong 2 phút (không nhìn): giải thích được = 1, không = 0. Subtopic chỉ có mức 1: đúng = điểm 1 (cần hands-on), sai = 0.
- Dừng subtopic: tối đa 3 item/subtopic. Dừng cụm: 2 subtopic liên tiếp trong cùng cụm đạt 0 → các subtopic còn lại của cụm ghi 0 mà không kiểm tra.
- Cổng cụm (gate): làm Phần A (10 item cổng, mỗi item time-box 6 phút, behavioral 5 phút, ~1 giờ). Item cổng là item mức 2 ngắn nhất của subtopic cổng, đã được rút gọn để làm được trong 6 phút. Điểm gate ≥ 2: cụm "mạnh"; = 1: "trung bình"; = 0: "yếu". Điểm này là điểm mặc định cho các subtopic của cụm chưa được kiểm tra (mạnh = 2, trung bình = 1, yếu = 0). Bảng điều chỉnh giờ (1.4) áp theo điểm mặc định đó cho từng subtopic chưa kiểm tra; vì Phần B chỉ đủ thời gian kiểm tra một số subtopic mỗi cụm nên độ phân giải là theo cụm. Nếu còn sức, làm tiếp Phần B của cụm trung bình ở buổi tối thứ hai (thêm 60-90 phút), như vậy từng subtopic có điểm riêng.
- Phần B (kiểm tra sâu, time-box theo cụm): cụm mạnh 8 phút (chỉ item mức 3 của các subtopic hot, ưu tiên two_pointers, tree_recursion, heap_top_k, binary_search_variants, grid_graphs...); cụm trung bình 15 phút (item mức 2 từng subtopic theo thứ tự kế hoạch, xuống mức 1 nếu sai); cụm yếu 5 phút (item mức 1 của 2 subtopic đầu).
- Dừng cứng sau 180 phút. Subtopic chưa kiểm tra giữ điểm mặc định của cụm.
- Làm một mình, không tra cứu, không dùng AI, trình soạn thảo trống (có chạy code được). Với item viết code: bấm giờ theo "minutes" của item; xem đáp án chỉ sau khi nộp.

**Thời gian ước tính (script tính từ `minutes` của item):**

| Kịch bản | Phút | Cách tính |
|---|---|---|
| mạnh (10 cụm đều qua gate) | 136 | Phần A + 10 cụm × 8 phút (chỉ item mức 3 của subtopic hot) |
| trung bình (5 cụm qua, 5 cụm điểm 1) | 171 | Phần A + 5 cụm × 8 + 5 cụm × 15 phút (item mức 2 từng subtopic) |
| yếu (10 cụm trượt gate) | 116 | Phần A + 10 cụm × 5 phút (item mức 1 của 2 subtopic đầu) + 10 phút xem đáp án và tự giải thích lời các item sai |
| xấu nhất (10 cụm điểm 1, mỗi cụm dùng hết 15 phút; dừng cứng ở 180) | 180 | Phần A + 10 cụm × 15 phút + 10 phút xem đáp án; nếu vượt thì dừng cứng ở 180 phút |

### 1.2 Cách chấm một subtopic

| Kết quả | Điểm |
|---|---|
| Sai item mức 1 (hoặc subtopic chỉ có mức 1 và sai) | **0** |
| Subtopic behavioral (bh.*): chấm thẳng theo rubric 0-3 của item, không dùng bậc thang | **0-3** |
| Đúng mức 1, sai mức 2 (hoặc subtopic chỉ có mức 1 và đúng) | **1** |
| Đúng mức 2; không có mức 3 hoặc sai mức 3 | **2** |
| Đúng mức 2 và mức 3 trong time-box, không gợi ý | **3** |

Đúng/sai theo `rubric` từng item: với item viết code, đúng = chạy `driver` ra đúng `expected_output`; với item concept, đủ các ý chính trong đáp án; với behavioral, theo rubric 0-3 của item.

### 1.3 Cụm chẩn đoán và item cổng (Phần A, ~1 giờ)

| Cụm | Tên | Item cổng (time-box) | Subtopic cổng | Số subtopic | Tổng phút item mức 2 |
|---|---|---|---|---|---|
| C1 | Python căn bản | `Q012` (6 phút) | `py.core.strings` | 9 | 51 |
| C2 | Cấu trúc dữ liệu Python, hàm, Big-O | `Q023` (6 phút) | `py.datastructs.dict` | 15 | 97 |
| C3 | Mảng, chuỗi, hash, prefix sum | `Q258` (6 phút) | `dsa.arrays_strings.hash_tables` | 8 | 86 |
| C4 | Hai con trỏ, cửa sổ trượt | `Q070` (6 phút) | `dsa.two_pointers_window.two_pointers` | 3 | 26 |
| C5 | Class, linked list, stack/queue | `Q079` (6 phút) | `dsa.linked_list.ll_basics` | 6 | 56 |
| C6 | Recursion, backtracking, binary search, sorting | `Q095` (6 phút) | `dsa.searching_sorting.binary_search_basics` | 6 | 56 |
| C7 | Cây, heap, design, intervals | `Q105` (6 phút) | `dsa.trees.tree_basics` | 10 | 96 |
| C8 | Graph, bit | `Q149` (6 phút) | `dsa.graphs.graph_traversal` | 6 | 66 |
| C9 | Coding thực tế, debug, AI-enabled, công cụ | `Q172` (3 phút) | `py.typing_testing.pytest_testing` | 8 | 43 |
| C10 | Behavioral và dùng AI | `Q091` (5 phút) | `bh.method.star_carl` | 11 | 55 |
| C11 | Gói AI/ML (chỉ khi theo track AI) | `Q253` (6 phút) | `ml.fundamentals.classification_metrics` | 21 | 63 |

### 1.4 Kết quả thay đổi kế hoạch thế nào

| Điểm subtopic | Hệ số giờ kế hoạch | Việc làm |
|---|---|---|
| 3 | ×0 | Bỏ phần "Học"; giữ 1 bài khó nhất của subtopic trong ngày thường (để duy trì). Giải phóng toàn bộ giờ kế hoạch của subtopic. |
| 2 | ×0.5 | Nén: đọc lướt concept 10 phút, làm 2 bài trong pool; giờ còn 50%. |
| 1 | ×1 | Giữ nguyên kế hoạch. |
| 0 | ×1.5 | Tăng 50% giờ; kiểm tra tiền đề (prerequisites trong skill_tree) và lùi về tiền đề nếu chúng < 2; thêm 2 bài easy cùng pattern. |

- Giờ giải phóng được dùng theo thứ tự ưu tiên: (1) subtopic điểm 0-1 ở các cụm sau; (2) kéo thêm subtopic từ bảng "cắt" (plan.md mục 2.4) theo thứ tự: monotonic stack → trie → dp cơ bản → heap nâng cao → git/venv (đã cắt khi nhường chỗ cho N6-R1); (3) mock sớm hơn một tuần.
- Nếu tổng giờ sau điều chỉnh vượt sức chứa: cắt theo thứ tự ở plan.md mục 11.3 (matrix_traversal → sliding_window_fixed → simulation_state_machines → phần GetRandom của design_o1_structures; giữ bit_basics, string_algorithms, topological_sort vì thuộc Top-40).
- Ví dụ tính tay: nếu cụm C1+C2 (py.core, py.datastructs, py.functions) đều đạt 2 thì tiết kiệm ≈ 7.0 giờ; nếu đều đạt 0 thì cần thêm ≈ 7.0 giờ (từ buffer ngày 26-30).
- Quy tắc cụm Python (C1, C2): nếu hơn 30% subtopic của C1 đạt < 2 → thêm 6-8 giờ tiền đề (cs.onramp + py.core) TRƯỚC ngày 1 và đẩy cả kế hoạch lùi tương ứng (hoặc dùng bản 2 giờ/ngày).
- Nếu gate C3 hoặc C4 = 0 (mảng/hash/hai con trỏ): đừng vào tuần 2; dành thêm 2 ngày cho tuần 1 (dùng buffer) vì mọi cụm sau phụ thuộc.

### 1.5 Bộ item chẩn đoán

Quy ước: `[id · mức · loại · ~phút]`. Với item code, "Kết quả đã kiểm chứng" là output khi chạy `python3`.

#### Cụm C1: Python căn bản

##### `py.core.getting_started` — Bắt đầu: chạy Python, cú pháp và quy ước (getting started)

**[Q001 · mức 1 · concept · ~3 phút]** REPL khác script ở điểm nào? Khi chương trình báo lỗi (traceback) bạn đọc từ đâu để biết loại lỗi?

Đáp án / rubric: REPL: gõ từng dòng sau dấu >>> và thấy kết quả ngay; script: file .py chạy cả file bằng `python ten.py`. Traceback: đọc dòng CUỐI cùng (loại lỗi + thông báo), rồi đọc ngược lên để thấy file và số dòng.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q002 · mức 2 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
total = 0
for i in range(1, 4):
    total += i
    print(total)
print("xong")
```
Đáp án (output đã chạy kiểm chứng):

```
1
3
6
xong
```
Giải thích: Dòng print(total) thụt vào nên nằm trong vòng for: in 1, 3, 6. "xong" không thụt nên chỉ in 1 lần.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

##### `py.core.variables_types` — Biến, kiểu dữ liệu và dynamic typing (variables & types)

**[Q003 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
a = 3; b = 2
print(a / b, a // b, type(a / b).__name__)
```
Đáp án (output đã chạy kiểm chứng):

```
1.5 1 float
```
Giải thích: / luôn trả float; // chia lấy phần nguyên.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q004 · mức 2 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
x = "5"
y = int(x) + 2
print(y, x * 2)
```
Đáp án (output đã chạy kiểm chứng):

```
7 55
```
Giải thích: int("5")=5 nên y=7; "5"*2 là lặp chuỗi -> "55".

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

##### `py.core.operators` — Toán tử, biểu thức và số (operators & numbers)

**[Q005 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
print(7 // 2, -7 // 2, 7 % 3, 2 ** 10)
```
Đáp án (output đã chạy kiểm chứng):

```
3 -4 1 1024
```
Giải thích: // làm tròn xuống (về âm vô cực) nên -7 // 2 = -4.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q006 · mức 2 · write_code · ~10 phút]** Viết `digit_sum(n)` trả về tổng các chữ số của số nguyên không âm n, KHÔNG đổi sang chuỗi (dùng // và %).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(digit_sum(123), digit_sum(0), digit_sum(9050))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
6 0 14
```
<details><summary>Code tham khảo</summary>

```python
def digit_sum(n):
    s = 0
    while n > 0:
        s += n % 10
        n //= 10
    return s
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

##### `py.core.conditionals` — Rẽ nhánh và truthiness (conditionals)

**[Q007 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
for v in [0, "", [], None, "0", [0]]:
    print(bool(v), end=" ")
```
Đáp án (output đã chạy kiểm chứng):

```
False False False False True True
```
Giải thích: 0, "", [], None là falsy. "0" (chuỗi có 1 ký tự) và [0] (list có 1 phần tử) là truthy.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q008 · mức 2 · write_code · ~10 phút]** Viết `fizzbuzz(n)` trả list chuỗi từ 1 đến n: bội của 3 -> "Fizz", bội của 5 -> "Buzz", bội của cả hai -> "FizzBuzz", còn lại là số dạng chuỗi.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(fizzbuzz(5)); print(fizzbuzz(15)[-1])
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
['1', '2', 'Fizz', '4', 'Buzz']
FizzBuzz
```
<details><summary>Code tham khảo</summary>

```python
def fizzbuzz(n):
    out = []
    for i in range(1, n + 1):
        if i % 15 == 0: out.append("FizzBuzz")
        elif i % 3 == 0: out.append("Fizz")
        elif i % 5 == 0: out.append("Buzz")
        else: out.append(str(i))
    return out
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

##### `py.core.loops` — Vòng lặp (loops)

**[Q009 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
for i in range(2, 10, 3):
    print(i, end=",")
```
Đáp án (output đã chạy kiểm chứng):

```
2,5,8,
```
Giải thích: range(2, 10, 3) = 2, 5, 8.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q010 · mức 2 · write_code · ~10 phút]** Viết `count_vowels(s)` đếm số nguyên âm (a, e, i, o, u, không phân biệt hoa thường) trong chuỗi s.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(count_vowels("Interview"), count_vowels("xyz"), count_vowels("AEIOU"))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
4 0 5
```
<details><summary>Code tham khảo</summary>

```python
def count_vowels(s):
    c = 0
    for ch in s.lower():
        if ch in "aeiou": c += 1
    return c
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

##### `py.core.strings` — Chuỗi và xử lý văn bản (strings)

**[Q011 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
s = "interview"
print(s[2:5], s[::-1][:3], s.count("e"), s.upper())
```
Đáp án (output đã chạy kiểm chứng):

```
ter wei 2 INTERVIEW
```
Giải thích: s[2:5]="ter"; đảo chuỗi "weivretni" lấy 3 ký tự đầu "wei"; có 2 chữ e.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q012 · mức 2 · write_code · ~6 phút]** Viết `is_pal(s)`: True nếu s là palindrome khi chỉ xét chữ và số, bỏ qua hoa thường.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(is_pal("A man, a plan, a canal: Panama"), is_pal("race a car"), is_pal(""))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
True False True
```
<details><summary>Code tham khảo</summary>

```python
def is_pal(s):
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (6 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q013 · mức 3 · write_code · ~10 phút]** Viết `compress(s)`: "aaabcc" -> "a3b1c2" (mỗi nhóm ký tự liên tiếp thành ký tự + số lần). Chuỗi rỗng trả "".

Driver (chạy sau khi bạn viết hàm/class):

```python
print(compress("aaabcc"), repr(compress("")), compress("z"))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
a3b1c2 '' z1
```
<details><summary>Code tham khảo</summary>

```python
def compress(s):
    out = []
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]: j += 1
        out.append(s[i] + str(j - i)); i = j
    return "".join(out)
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `py.core.io_input` — Nhập xuất console và file cơ bản (console & file I/O)

**[Q014 · mức 1 · concept · ~3 phút]** `input()` trả về kiểu gì? Làm sao đọc một dòng "3 4 5" thành list số nguyên?

Đáp án / rubric: Luôn trả `str`. Dùng `list(map(int, input().split()))`.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q015 · mức 2 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
line = "3 4 5"
nums = list(map(int, line.split()))
print(sum(nums), nums[-1])
```
Đáp án (output đã chạy kiểm chứng):

```
12 5
```
Giải thích: split() tách theo khoảng trắng, map(int) đổi sang số.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

##### `py.core.try_except_basics` — Bắt lỗi cơ bản với try/except (error handling basics)

**[Q016 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
def f(s):
    try:
        return int(s)
    except ValueError:
        return -1
print(f("12"), f("a1"), f(""))
```
Đáp án (output đã chạy kiểm chứng):

```
12 -1 -1
```
Giải thích: int("a1") và int("") đều ném ValueError.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q017 · mức 2 · concept · ~3 phút]** Khi nào nên dùng try/except thay vì if? Cho 1 ví dụ.

Đáp án / rubric: Khi lỗi khó đoán trước hoặc kiểm tra tốn kém (đọc file, đổi chuỗi sang số, truy cập dict thiếu khóa). Không dùng except trần che lỗi; bắt đúng loại lỗi.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

##### `py.core.regex` — Biểu thức chính quy (regex)

**[Q139 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
import re
print(re.findall(r"\d+", "a12b345"), re.sub(r"\s+", " ", "x   y\tz"), bool(re.match(r"^[a-z]+$", "abc1")))
```
Đáp án (output đã chạy kiểm chứng):

```
['12', '345'] x y z False
```
Giải thích: \d+ khớp dãy chữ số; \s+ khớp khoảng trắng; "abc1" có chữ số nên không khớp ^[a-z]+$.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q140 · mức 2 · concept · ~3 phút]** Khi nào nên dùng split/str methods thay vì regex trong bài phỏng vấn?

Đáp án / rubric: Khi định dạng đơn giản và cố định (tách theo khoảng trắng/dấu phẩy). Regex dễ sai biên và khó giải thích; chỉ dùng khi mẫu thật sự phức tạp và hỏi interviewer có được dùng không.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

#### Cụm C2: Cấu trúc dữ liệu Python, hàm, Big-O

##### `py.datastructs.list` — Danh sách (list)

**[Q018 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
a = [1, 2, 3, 4, 5]
b = a[1:4]
b[0] = 99
a.append(6); a.pop(0)
print(a, b)
```
Đáp án (output đã chạy kiểm chứng):

```
[2, 3, 4, 5, 6] [99, 3, 4]
```
Giải thích: Slicing tạo list mới nên sửa b không ảnh hưởng a.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q019 · mức 2 · write_code · ~10 phút]** Viết `move_zeroes(nums)` đưa mọi số 0 về cuối, giữ thứ tự các số khác, sửa tại chỗ và trả lại nums.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(move_zeroes([0, 1, 0, 3, 12]), move_zeroes([0]), move_zeroes([1, 2]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[1, 3, 12, 0, 0] [0] [1, 2]
```
<details><summary>Code tham khảo</summary>

```python
def move_zeroes(nums):
    w = 0
    for x in nums:
        if x != 0:
            nums[w] = x; w += 1
    for i in range(w, len(nums)): nums[i] = 0
    return nums
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

##### `py.datastructs.tuple_namedtuple` — Tuple, unpacking và namedtuple

**[Q020 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
p = (3, 4)
x, y = p
x, y = y, x
print(x, y, p)
```
Đáp án (output đã chạy kiểm chứng):

```
4 3 (3, 4)
```
Giải thích: Hoán đổi bằng unpacking; tuple p không đổi.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q021 · mức 2 · concept · ~3 phút]** Vì sao tuple dùng được làm khóa dict còn list thì không? Cho ví dụ dùng tuple làm khóa.

Đáp án / rubric: Tuple bất biến (hashable) nếu các phần tử bất biến; list mutable nên không hash được. Ví dụ `visited[(r, c)] = True` cho ô lưới.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

##### `py.datastructs.dict` — Từ điển và tập hợp (dict & set)

**[Q022 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
d = {}
for w in "a b a c b a".split():
    d[w] = d.get(w, 0) + 1
print(d, sorted(d, key=d.get)[-1])
```
Đáp án (output đã chạy kiểm chứng):

```
{'a': 3, 'b': 2, 'c': 1} a
```
Giải thích: Đếm tần suất; sorted theo giá trị, phần tử cuối là khóa có giá trị lớn nhất.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q023 · mức 2 · write_code · ~6 phút]** Viết `two_sum(nums, target)` trả list 2 chỉ số i < j sao cho nums[i] + nums[j] == target (có đúng 1 đáp án). Mục tiêu O(n).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(two_sum([2, 7, 11, 15], 9), two_sum([3, 2, 4], 6), two_sum([3, 3], 6))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[0, 1] [1, 2] [0, 1]
```
<details><summary>Code tham khảo</summary>

```python
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (6 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q024 · mức 3 · write_code · ~10 phút]** Viết `first_unique(s)` trả chỉ số của ký tự đầu tiên không lặp trong s, hoặc -1. O(n).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(first_unique("leetcode"), first_unique("loveleetcode"), first_unique("aabb"))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
0 2 -1
```
<details><summary>Code tham khảo</summary>

```python
def first_unique(s):
    from collections import Counter
    c = Counter(s)
    for i, ch in enumerate(s):
        if c[ch] == 1: return i
    return -1
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `py.datastructs.comprehensions` — Comprehension và generator expression

**[Q025 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
print([x * x for x in range(6) if x % 2 == 0], {c for c in "hello"} == set("helo"))
```
Đáp án (output đã chạy kiểm chứng):

```
[0, 4, 16] True
```
Giải thích: Lọc số chẵn rồi bình phương; set bỏ trùng.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q026 · mức 2 · write_code · ~10 phút]** Viết `flatten(m)` biến list các list thành 1 list phẳng, dùng list comprehension một dòng.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(flatten([[1, 2], [3], []]), flatten([]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[1, 2, 3] []
```
<details><summary>Code tham khảo</summary>

```python
def flatten(m):
    return [x for row in m for x in row]
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

##### `py.datastructs.collections_module` — Module collections (Counter, deque, defaultdict)

**[Q027 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
from collections import Counter, defaultdict, deque
c = Counter("banana")
dd = defaultdict(list); dd["x"].append(1)
q = deque([1, 2, 3]); q.appendleft(0); q.pop()
print(c.most_common(1), dict(dd), list(q))
```
Đáp án (output đã chạy kiểm chứng):

```
[('a', 3)] {'x': [1]} [0, 1, 2]
```
Giải thích: banana có 3 chữ a; deque: thêm 0 vào đầu rồi bỏ phần tử cuối (3).

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q028 · mức 2 · write_code · ~10 phút]** Viết `top_words(words, k)` trả k từ xuất hiện nhiều nhất; hoà thì từ nhỏ hơn theo thứ tự chữ cái đứng trước.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(top_words(["i", "love", "leetcode", "i", "love", "coding"], 2), top_words(["b", "a"], 1))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
['i', 'love'] ['a']
```
<details><summary>Code tham khảo</summary>

```python
def top_words(words, k):
    from collections import Counter
    c = Counter(words)
    return sorted(c, key=lambda w: (-c[w], w))[:k]
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

##### `py.datastructs.copying_mutability` — Mutability, aliasing và sao chép (copying)

**[Q029 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
a = [[0] * 2] * 2
a[0][0] = 1
b = [[0] * 2 for _ in range(2)]
b[0][0] = 1
print(a, b)
```
Đáp án (output đã chạy kiểm chứng):

```
[[1, 0], [1, 0]] [[1, 0], [0, 0]]
```
Giải thích: `[[0]*2]*2` nhân bản tham chiếu tới CÙNG một list con; comprehension tạo list con mới mỗi hàng.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q030 · mức 2 · concept · ~3 phút]** Phân biệt gán `b = a`, `b = a[:]` và `copy.deepcopy(a)` với a là list các list.

Đáp án / rubric: `b = a`: cùng một đối tượng. `a[:]`: shallow copy (list ngoài mới, list con vẫn chung). deepcopy: sao chép sâu mọi tầng.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

##### `py.datastructs.heapq_bisect` — heapq và bisect

**[Q031 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
import heapq, bisect
h = [5, 1, 4]; heapq.heapify(h); heapq.heappush(h, 0)
print(heapq.heappop(h), heapq.nsmallest(2, h), bisect.bisect_left([1, 3, 3, 5], 3), bisect.bisect_right([1, 3, 3, 5], 3))
```
Đáp án (output đã chạy kiểm chứng):

```
0 [1, 4] 1 3
```
Giải thích: heapq là min-heap; bisect_left trả vị trí chèn bên trái các số 3, bisect_right bên phải.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q032 · mức 2 · write_code · ~10 phút]** Viết `kth_largest(nums, k)` dùng heapq (min-heap kích thước k), O(n log k).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(kth_largest([3, 2, 1, 5, 6, 4], 2), kth_largest([1], 1))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
5 1
```
<details><summary>Code tham khảo</summary>

```python
def kth_largest(nums, k):
    import heapq
    h = []
    for x in nums:
        heapq.heappush(h, x)
        if len(h) > k: heapq.heappop(h)
    return h[0]
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

##### `py.functions.def_args` — Định nghĩa hàm và đối số (functions & arguments)

**[Q033 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
def f(x, acc=[]):
    acc.append(x)
    return acc
print(f(1), f(2))
```
Đáp án (output đã chạy kiểm chứng):

```
[1, 2] [1, 2]
```
Giải thích: Giá trị mặc định mutable được tạo MỘT lần; hai lời gọi dùng chung list. Sửa: acc=None rồi tạo list mới bên trong.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q034 · mức 2 · write_code · ~10 phút]** Viết `fib(n)` trả số Fibonacci thứ n (fib(0)=0, fib(1)=1) bằng vòng lặp, O(n) thời gian, O(1) bộ nhớ.

Driver (chạy sau khi bạn viết hàm/class):

```python
print([fib(i) for i in range(8)], fib(30))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[0, 1, 1, 2, 3, 5, 8, 13] 832040
```
<details><summary>Code tham khảo</summary>

```python
def fib(n):
    a, b = 0, 1
    for _ in range(n): a, b = b, a + b
    return a
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

##### `py.functions.lambda_hof` — Lambda và hàm bậc cao (higher-order functions)

**[Q035 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
print(sorted(["bb", "a", "ccc"], key=lambda s: -len(s)), list(map(lambda x: x + 1, [1, 2])), list(filter(None, [0, 1, 2])))
```
Đáp án (output đã chạy kiểm chứng):

```
['ccc', 'bb', 'a'] [2, 3] [1, 2]
```
Giải thích: key=-len sắp giảm theo độ dài; filter(None, ...) giữ phần tử truthy.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q036 · mức 2 · concept · ~3 phút]** Khi nào nên dùng lambda, khi nào nên dùng def?

Đáp án / rubric: lambda cho hàm rất ngắn một biểu thức (key của sort, map/filter). Nhiều dòng, cần tên, cần docstring/tái sử dụng -> dùng def.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

##### `py.functions.sorting_keys` — Sắp xếp với key và tính ổn định (sorting)

**[Q037 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
data = [("b", 2), ("a", 2), ("c", 1)]
print(sorted(data, key=lambda t: (-t[1], t[0])))
```
Đáp án (output đã chạy kiểm chứng):

```
[('a', 2), ('b', 2), ('c', 1)]
```
Giải thích: Sắp giảm theo số, hoà thì tăng theo chữ: key là tuple (-số, chữ).

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q038 · mức 2 · write_code · ~10 phút]** Viết `sort_words(words)`: sắp xếp danh sách từ theo độ dài tăng dần, hoà thì theo thứ tự chữ cái.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(sort_words(["pear", "fig", "apple", "kiwi", "fig"]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
['fig', 'fig', 'kiwi', 'pear', 'apple']
```
<details><summary>Code tham khảo</summary>

```python
def sort_words(words):
    return sorted(words, key=lambda w: (len(w), w))
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

##### `cs.complexity.big_o` — Ký hiệu tiệm cận Big-O, Theta, Omega (asymptotic notation)

**[Q041 · mức 1 · concept · ~3 phút]** Cho `for i in range(n): for j in range(n): ...` và `for i in range(n): for j in range(i): ...`. Độ phức tạp mỗi đoạn?

Đáp án / rubric: Đoạn 1: O(n^2) (n*n lần). Đoạn 2: 0+1+...+(n-1) = n(n-1)/2 lần, vẫn O(n^2).

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q042 · mức 2 · concept · ~3 phút]** Độ phức tạp của: `x in list`, `x in set`, `list.pop(0)`, `deque.popleft()`, `sorted(list)`, `heapq.heappush`.

Đáp án / rubric: O(n); O(1) trung bình; O(n); O(1); O(n log n); O(log n).

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

**[Q043 · mức 3 · concept · ~3 phút]** Bài cho n = 10^5. Các cách O(n^2), O(n log n), O(n) có chạy kịp ~1 giây trong Python không? Vì sao? Space của đệ quy sâu n là bao nhiêu?

Đáp án / rubric: O(n^2)=10^10 phép: không kịp. O(n log n) ~ 1.7*10^6 và O(n): kịp. Đệ quy sâu n dùng O(n) stack (Python giới hạn ~1000 tầng mặc định).

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 3; sai: tối đa điểm 2.

##### `dsa.foundations.memory_model` — Mô hình bộ nhớ: mảng, tham chiếu, stack và heap (memory model)

**[Q044 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
a = [1, 2]; b = a; b.append(3)
c = a[:]; c.append(4)
print(a, b is a, c is a, id(a) == id(b))
```
Đáp án (output đã chạy kiểm chứng):

```
[1, 2, 3] True False True
```
Giải thích: b và a cùng một đối tượng; c là bản sao.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q045 · mức 2 · concept · ~3 phút]** Python truyền tham số kiểu gì? Vì sao hàm `def f(lst): lst.append(1)` làm thay đổi list ở ngoài còn `lst = [9]` thì không?

Đáp án / rubric: Truyền tham chiếu đối tượng (pass by object reference): append sửa đối tượng chung; `lst = [9]` chỉ gán tên cục bộ sang đối tượng mới.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

##### `dsa.foundations.lib_toolkit` — Chọn đúng cấu trúc dữ liệu và công cụ thư viện (data structure selection)

**[Q046 · mức 1 · concept · ~3 phút]** Ghép công cụ với việc: (a) đếm tần suất, (b) hàng đợi 2 đầu, (c) lấy k lớn nhất, (d) tìm vị trí chèn trong mảng đã sắp, (e) dict có giá trị mặc định list.

Đáp án / rubric: (a) Counter, (b) deque, (c) heapq.nlargest/min-heap, (d) bisect, (e) defaultdict(list).

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q047 · mức 2 · write_code · ~10 phút]** Viết `merge_sorted(a, b)` gộp hai list đã sắp xếp tăng thành một list sắp xếp, O(n+m), không dùng sorted().

Driver (chạy sau khi bạn viết hàm/class):

```python
print(merge_sorted([1, 3, 5], [2, 4]), merge_sorted([], [1]), merge_sorted([1, 1], [1]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[1, 2, 3, 4, 5] [1] [1, 1, 1]
```
<details><summary>Code tham khảo</summary>

```python
def merge_sorted(a, b):
    i = j = 0; out = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]: out.append(a[i]); i += 1
        else: out.append(b[j]); j += 1
    return out + a[i:] + b[j:]
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

##### `py.functions.scope_closures` — Scope, LEGB và closure

**[Q039 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
def make():
    n = 0
    def inc():
        nonlocal n
        n += 1
        return n
    return inc
f = make(); f()
print(f(), f())
```
Đáp án (output đã chạy kiểm chứng):

```
2 3
```
Giải thích: Hàm trong nhớ biến n của hàm ngoài (closure); nonlocal cho phép gán lại.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q040 · mức 2 · concept · ~3 phút]** Vì sao đoạn `x = 0; def f(): x += 1; f()` báo UnboundLocalError? Sửa thế nào?

Đáp án / rubric: Trong f, `x += 1` gán x nên x được coi là biến cục bộ, chưa có giá trị. Sửa: `global x` (hoặc truyền tham số/trả về giá trị).

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

##### `dsa.foundations.interview_method` — Quy trình giải bài phỏng vấn (interview problem-solving method)

**[Q048 · mức 1 · concept · ~3 phút]** Liệt kê 6 bước làm một bài phỏng vấn coding (từ nhận đề đến xong).

Đáp án / rubric: 1) nhắc lại đề + hỏi làm rõ; 2) ví dụ + biên; 3) brute force + độ phức tạp; 4) tối ưu; 5) code; 6) dry-run bằng ví dụ + biên, nói time/space.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q049 · mức 2 · concept · ~3 phút]** Bạn kẹt 10 phút không ra hướng. Nói gì và làm gì với interviewer?

Đáp án / rubric: Nói to điều đã thử, trình bày brute force để có bài chạy được, hỏi gợi ý cụ thể ("em đang nghĩ dùng hash map để ... có hợp lý không ạ?"), không im lặng.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

#### Cụm C3: Mảng, chuỗi, hash, prefix sum

##### `dsa.arrays_strings.arrays` — Mảng và mảng động (array, dynamic array)

**[Q050 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
a = [3, 1, 4, 1, 5]
a.insert(1, 9); del a[0]; a.remove(1)
print(a, len(a), max(a), a.index(5))
```
Đáp án (output đã chạy kiểm chứng):

```
[9, 4, 1, 5] 4 9 3
```
Giải thích: insert(1,9) -> [3,9,1,4,1,5]; xoá đầu -> [9,1,4,1,5]; remove(1) xoá số 1 đầu tiên.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q051 · mức 2 · write_code · ~10 phút]** Viết `rotate(nums, k)` trả list đã xoay phải k bước (k có thể lớn hơn len).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(rotate([1, 2, 3, 4, 5, 6, 7], 3), rotate([1, 2], 5), rotate([], 3))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[5, 6, 7, 1, 2, 3, 4] [2, 1] []
```
<details><summary>Code tham khảo</summary>

```python
def rotate(nums, k):
    if not nums: return nums
    k %= len(nums)
    return nums[-k:] + nums[:-k] if k else nums[:]
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q052 · mức 3 · write_code · ~10 phút]** Viết `max_subarray(nums)` trả tổng lớn nhất của một đoạn con liên tiếp (Kadane), O(n).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]), max_subarray([-3]), max_subarray([5, 4, -1, 7, 8]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
6 -3 23
```
<details><summary>Code tham khảo</summary>

```python
def max_subarray(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.arrays_strings.hash_tables` — Hash table và hash set (hash table internals)

**[Q053 · mức 1 · concept · ~3 phút]** Vì sao tra cứu dict là O(1) trung bình? Điều gì làm nó thành O(n) trong trường hợp xấu? Khóa nào không dùng được?

Đáp án / rubric: Hàm băm đổi khóa thành chỉ số bucket. Nhiều khóa va chạm (collision) vào cùng bucket -> O(n). Khóa phải hashable (không dùng list/dict/set).

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q054 · mức 2 · write_code · ~10 phút]** Viết `group_anagrams(words)` gom các từ là hoán vị của nhau; trả list các nhóm (mỗi nhóm sắp tăng; các nhóm sắp theo từ đầu).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[['ate', 'eat', 'tea'], ['bat'], ['nat', 'tan']]
```
<details><summary>Code tham khảo</summary>

```python
def group_anagrams(words):
    g = {}
    for w in words:
        g.setdefault("".join(sorted(w)), []).append(w)
    return sorted(sorted(v) for v in g.values())
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q258 · mức 2 · write_code · ~6 phút]** Viết `most_common(words)` trả từ xuất hiện nhiều lần nhất; nếu hòa, trả từ nhỏ hơn theo thứ tự chữ cái. Danh sách rỗng trả chuỗi rỗng.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(most_common(["b", "a", "b", "a", "c"]), most_common(["x"]), repr(most_common([])))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
a x ''
```
<details><summary>Code tham khảo</summary>

```python
def most_common(words):
    cnt = {}
    for w in words:
        cnt[w] = cnt.get(w, 0) + 1
    best = ""
    for w, c in cnt.items():
        if best == "" or c > cnt[best] or (c == cnt[best] and w < best):
            best = w
    return best
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (6 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q055 · mức 3 · write_code · ~10 phút]** Viết `longest_consecutive(nums)` trả độ dài dãy số nguyên liên tiếp dài nhất (không cần liền nhau trong mảng), O(n).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(longest_consecutive([100, 4, 200, 1, 3, 2]), longest_consecutive([]), longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
4 0 9
```
<details><summary>Code tham khảo</summary>

```python
def longest_consecutive(nums):
    s = set(nums); best = 0
    for x in s:
        if x - 1 not in s:
            y = x
            while y + 1 in s: y += 1
            best = max(best, y - x + 1)
    return best
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.arrays_strings.hashing_patterns` — Pattern dùng hash: đếm tần suất, bù trừ, nhóm (hashing patterns) (hot)

**[Q056 · mức 2 · write_code · ~10 phút]** Viết `nearby_duplicate(nums, k)`: True nếu có hai chỉ số i != j, |i-j| <= k và nums[i] == nums[j].

Driver (chạy sau khi bạn viết hàm/class):

```python
print(nearby_duplicate([1, 2, 3, 1], 3), nearby_duplicate([1, 0, 1, 1], 1), nearby_duplicate([1, 2, 3, 1, 2, 3], 2))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
True True False
```
<details><summary>Code tham khảo</summary>

```python
def nearby_duplicate(nums, k):
    last = {}
    for i, x in enumerate(nums):
        if x in last and i - last[x] <= k: return True
        last[x] = i
    return False
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q057 · mức 3 · write_code · ~10 phút]** Viết `isomorphic(s, t)`: True nếu có thể thay mỗi ký tự của s bằng một ký tự cố định để thành t (ánh xạ 1-1).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(isomorphic("egg", "add"), isomorphic("foo", "bar"), isomorphic("badc", "baba"))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
True False False
```
<details><summary>Code tham khảo</summary>

```python
def isomorphic(s, t):
    if len(s) != len(t): return False
    a, b = {}, {}
    for x, y in zip(s, t):
        if a.setdefault(x, y) != y or b.setdefault(y, x) != x: return False
    return True
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.arrays_strings.prefix_sum` — Prefix sum và difference array (prefix sums) (hot)

**[Q060 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
from itertools import accumulate
a = [2, 4, 1, 3]
p = [0] + list(accumulate(a))
print(p, p[4] - p[1])
```
Đáp án (output đã chạy kiểm chứng):

```
[0, 2, 6, 7, 10] 8
```
Giải thích: p[j]-p[i] là tổng a[i..j-1]; p[4]-p[1] = 4+1+3.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q061 · mức 2 · write_code · ~10 phút]** Cho nums và danh sách truy vấn (l, r) (chỉ số bao gồm hai đầu). Viết `range_sums(nums, queries)` trả list tổng, mỗi truy vấn O(1) sau khi xử lý trước.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(range_sums([-2, 0, 3, -5, 2, -1], [(0, 2), (2, 5), (0, 5)]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[1, -1, -3]
```
<details><summary>Code tham khảo</summary>

```python
def range_sums(nums, queries):
    p = [0]
    for x in nums: p.append(p[-1] + x)
    return [p[r + 1] - p[l] for l, r in queries]
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q062 · mức 3 · write_code · ~10 phút]** Viết `count_zero_sum(nums)`: đếm số đoạn con liên tiếp có tổng bằng 0 (prefix sum + dict), O(n).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(count_zero_sum([1, -1, 0]), count_zero_sum([1, 2, 3]), count_zero_sum([0, 0, 0]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
3 0 6
```
<details><summary>Code tham khảo</summary>

```python
def count_zero_sum(nums):
    seen = {0: 1}; s = 0; res = 0
    for x in nums:
        s += x
        res += seen.get(s, 0)
        seen[s] = seen.get(s, 0) + 1
    return res
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.arrays_strings.strings_basics` — Chuỗi cơ bản (string fundamentals)

**[Q058 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
s = " Hello, World "
print(s.strip().lower().split(", "), "-".join(["a", "b"]), s.replace("l", "L").count("L"))
```
Đáp án (output đã chạy kiểm chứng):

```
['hello', 'world'] a-b 3
```
Giải thích: strip().lower() = "hello, world"; split(", ") tách thành 2 từ; có 3 chữ l đổi thành L.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q059 · mức 2 · write_code · ~10 phút]** Viết `add_binary(a, b)` cộng hai chuỗi nhị phân, trả chuỗi nhị phân, KHÔNG dùng int(x, 2).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(add_binary("11", "1"), add_binary("1010", "1011"), add_binary("0", "0"))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
100 10101 0
```
<details><summary>Code tham khảo</summary>

```python
def add_binary(a, b):
    i, j, carry, out = len(a) - 1, len(b) - 1, 0, []
    while i >= 0 or j >= 0 or carry:
        t = carry
        if i >= 0: t += int(a[i]); i -= 1
        if j >= 0: t += int(b[j]); j -= 1
        out.append(str(t % 2)); carry = t // 2
    return "".join(reversed(out))
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

##### `dsa.arrays_strings.string_algorithms` — Thuật toán chuỗi: so khớp mẫu và palindrome (string algorithms) (hot)

**[Q063 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
s = "abcabc"
print(s.find("ca"), s.find("z"), s.startswith("abc"), s[::-1] == s)
```
Đáp án (output đã chạy kiểm chứng):

```
2 -1 True False
```
Giải thích: find trả chỉ số đầu hoặc -1.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q064 · mức 2 · write_code · ~10 phút]** Viết `count_pal_substrings(s)` đếm các chuỗi con đối xứng (mở rộng từ tâm), O(n^2).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(count_pal_substrings("abc"), count_pal_substrings("aaa"), count_pal_substrings("abba"))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
3 6 6
```
<details><summary>Code tham khảo</summary>

```python
def count_pal_substrings(s):
    n = len(s); c = 0
    for ctr in range(2 * n - 1):
        l, r = ctr // 2, ctr // 2 + ctr % 2
        while l >= 0 and r < n and s[l] == s[r]:
            c += 1; l -= 1; r += 1
    return c
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q065 · mức 3 · write_code · ~10 phút]** Viết `find_anagrams(s, p)` trả mọi chỉ số bắt đầu của hoán vị của p trong s (cửa sổ + đếm).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(find_anagrams("cbaebabacd", "abc"), find_anagrams("abab", "ab"), find_anagrams("a", "ab"))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[0, 6] [0, 1, 2] []
```
<details><summary>Code tham khảo</summary>

```python
def find_anagrams(s, p):
    from collections import Counter
    need = Counter(p); win = Counter(); res = []
    for i, ch in enumerate(s):
        win[ch] += 1
        if i >= len(p):
            old = s[i - len(p)]
            win[old] -= 1
            if win[old] == 0: del win[old]
        if win == need: res.append(i - len(p) + 1)
    return res
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.arrays_strings.array_techniques` — Kỹ thuật xử lý mảng tại chỗ (in-place array techniques)

**[Q066 · mức 1 · concept · ~3 phút]** "In-place" nghĩa là gì và vì sao nó thường yêu cầu O(1) bộ nhớ phụ? Nêu 2 kỹ thuật in-place.

Đáp án / rubric: Sửa trực tiếp trên mảng gốc, không tạo mảng mới cùng cỡ. Ví dụ: reader/writer pointer, swap hai đầu, đảo ngược từng đoạn (xoay mảng), cờ Hà Lan.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q067 · mức 2 · write_code · ~10 phút]** Viết `sort_colors(nums)` sắp xếp mảng chỉ chứa 0, 1, 2 tại chỗ trong 1 lượt (Dutch national flag), trả nums.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(sort_colors([2, 0, 2, 1, 1, 0]), sort_colors([2, 0, 1]), sort_colors([0]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[0, 0, 1, 1, 2, 2] [0, 1, 2] [0]
```
<details><summary>Code tham khảo</summary>

```python
def sort_colors(nums):
    lo, mid, hi = 0, 0, len(nums) - 1
    while mid <= hi:
        if nums[mid] == 0: nums[lo], nums[mid] = nums[mid], nums[lo]; lo += 1; mid += 1
        elif nums[mid] == 1: mid += 1
        else: nums[mid], nums[hi] = nums[hi], nums[mid]; hi -= 1
    return nums
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q068 · mức 3 · write_code · ~10 phút]** Viết `majority(nums)` trả phần tử xuất hiện > n/2 lần (Boyer-Moore, O(1) bộ nhớ).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(majority([3, 2, 3]), majority([2, 2, 1, 1, 1, 2, 2]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
3 2
```
<details><summary>Code tham khảo</summary>

```python
def majority(nums):
    cand, cnt = None, 0
    for x in nums:
        if cnt == 0: cand = x
        cnt += 1 if x == cand else -1
    return cand
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.arrays_strings.matrix_traversal` — Thao tác ma trận và lưới 2D (matrix traversal)

**[Q136 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
m = [[1, 2, 3], [4, 5, 6]]
print(list(zip(*m)), [row[::-1] for row in m], len(m), len(m[0]))
```
Đáp án (output đã chạy kiểm chứng):

```
[(1, 4), (2, 5), (3, 6)] [[3, 2, 1], [6, 5, 4]] 2 3
```
Giải thích: zip(*m) chuyển vị (transpose).

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q137 · mức 2 · write_code · ~10 phút]** Viết `spiral(matrix)` trả mọi phần tử theo thứ tự xoắn ốc từ ngoài vào trong.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(spiral([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), spiral([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[1, 2, 3, 6, 9, 8, 7, 4, 5] [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
```
<details><summary>Code tham khảo</summary>

```python
def spiral(m):
    res = []
    while m:
        res += m.pop(0)
        m = [list(r) for r in zip(*m)][::-1]
    return res
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q138 · mức 3 · write_code · ~10 phút]** Viết `rotate_image(m)` xoay ma trận vuông 90 độ theo chiều kim đồng hồ TẠI CHỖ (không tạo ma trận mới), trả m.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(rotate_image([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), rotate_image([[1]]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[[7, 4, 1], [8, 5, 2], [9, 6, 3]] [[1]]
```
<details><summary>Code tham khảo</summary>

```python
def rotate_image(m):
    n = len(m)
    for i in range(n):
        for j in range(i + 1, n): m[i][j], m[j][i] = m[j][i], m[i][j]
    for r in m: r.reverse()
    return m
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

#### Cụm C4: Hai con trỏ, cửa sổ trượt

##### `dsa.two_pointers_window.two_pointers` — Hai con trỏ (two pointers) (hot)

**[Q069 · mức 1 · concept · ~3 phút]** Phân biệt hai dạng two pointers: "hai đầu" và "cùng chiều (reader/writer)". Mỗi dạng hợp với bài nào?

Đáp án / rubric: Hai đầu: mảng đã sắp (two sum sorted, container with most water, palindrome). Cùng chiều: lọc/nén tại chỗ (xoá trùng, move zeroes), cửa sổ trượt.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q070 · mức 2 · write_code · ~6 phút]** Viết `two_sum_sorted(nums, target)` trên mảng đã sắp tăng, trả [i, j] (chỉ số bắt đầu từ 1) hoặc [] nếu không có; O(n), O(1) bộ nhớ.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(two_sum_sorted([2, 7, 11, 15], 9), two_sum_sorted([-1, 0], -1), two_sum_sorted([1, 2], 7))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[1, 2] [1, 2] []
```
<details><summary>Code tham khảo</summary>

```python
def two_sum_sorted(nums, target):
    i, j = 0, len(nums) - 1
    while i < j:
        s = nums[i] + nums[j]
        if s == target: return [i + 1, j + 1]
        if s < target: i += 1
        else: j -= 1
    return []
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (6 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q071 · mức 3 · write_code · ~10 phút]** Viết `three_sum(nums)` trả list các bộ ba (sắp tăng) có tổng 0, không trùng bộ; sắp các bộ tăng dần.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(three_sum([-1, 0, 1, 2, -1, -4]), three_sum([0, 0, 0]), three_sum([1, 2]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[[-1, -1, 2], [-1, 0, 1]] [[0, 0, 0]] []
```
<details><summary>Code tham khảo</summary>

```python
def three_sum(nums):
    nums = sorted(nums); res = []
    for i in range(len(nums) - 2):
        if i and nums[i] == nums[i - 1]: continue
        l, r = i + 1, len(nums) - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s < 0: l += 1
            elif s > 0: r -= 1
            else:
                res.append([nums[i], nums[l], nums[r]]); l += 1
                while l < r and nums[l] == nums[l - 1]: l += 1
    return res
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.two_pointers_window.sliding_window_fixed` — Cửa sổ trượt kích thước cố định (fixed sliding window)

**[Q072 · mức 1 · concept · ~3 phút]** Cửa sổ trượt kích thước cố định k: cập nhật tổng khi trượt 1 bước thế nào? Vì sao O(n) thay vì O(nk)?

Đáp án / rubric: Cộng phần tử mới vào cuối, trừ phần tử rời khỏi đầu: mỗi bước O(1). Không tính lại cả cửa sổ.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q073 · mức 2 · write_code · ~10 phút]** Viết `max_avg(nums, k)` trả trung bình lớn nhất của một đoạn con liên tiếp dài đúng k.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(max_avg([1, 12, -5, -6, 50, 3], 4), max_avg([5], 1))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
12.75 5.0
```
<details><summary>Code tham khảo</summary>

```python
def max_avg(nums, k):
    s = sum(nums[:k]); best = s
    for i in range(k, len(nums)):
        s += nums[i] - nums[i - k]
        best = max(best, s)
    return best / k
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

##### `dsa.two_pointers_window.sliding_window_variable` — Cửa sổ trượt kích thước thay đổi (variable sliding window)

**[Q074 · mức 2 · write_code · ~10 phút]** Viết `longest_unique(s)` trả độ dài chuỗi con dài nhất không có ký tự lặp.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(longest_unique("abcabcbb"), longest_unique(""), longest_unique("pwwkew"), longest_unique("bbbb"))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
3 0 3 1
```
<details><summary>Code tham khảo</summary>

```python
def longest_unique(s):
    last = {}; l = best = 0
    for r, ch in enumerate(s):
        if ch in last and last[ch] >= l: l = last[ch] + 1
        last[ch] = r
        best = max(best, r - l + 1)
    return best
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q075 · mức 3 · write_code · ~10 phút]** Viết `min_len(target, nums)` trả độ dài đoạn con liên tiếp ngắn nhất có tổng >= target (số dương), hoặc 0.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(min_len(7, [2, 3, 1, 2, 4, 3]), min_len(4, [1, 4, 4]), min_len(11, [1, 1, 1]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
2 1 0
```
<details><summary>Code tham khảo</summary>

```python
def min_len(target, nums):
    l = s = 0; best = float("inf")
    for r, x in enumerate(nums):
        s += x
        while s >= target:
            best = min(best, r - l + 1); s -= nums[l]; l += 1
    return 0 if best == float("inf") else best
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

#### Cụm C5: Class, linked list, stack/queue

##### `py.oop.classes_basics` — Class, object, self và property (classes)

**[Q076 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
class P:
    def __init__(self, n): self.n = n
    def __repr__(self): return f"P({self.n})"
a = P(1); b = a; b.n = 2
print(a, a is b)
```
Đáp án (output đã chạy kiểm chứng):

```
P(2) True
```
Giải thích: b và a trỏ cùng một object; print dùng __repr__.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q077 · mức 2 · write_code · ~10 phút]** Viết class `Stack` có push(x), pop(), peek(), is_empty(); pop khi rỗng ném IndexError.

Driver (chạy sau khi bạn viết hàm/class):

```python
s = Stack(); s.push(1); s.push(2)
print(s.pop(), s.peek(), s.is_empty())
s.pop()
try:
    s.pop()
except IndexError as e:
    print("lỗi", e)
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
2 1 False
lỗi empty
```
<details><summary>Code tham khảo</summary>

```python
class Stack:
    def __init__(self): self._a = []
    def push(self, x): self._a.append(x)
    def pop(self):
        if not self._a: raise IndexError("empty")
        return self._a.pop()
    def peek(self): return self._a[-1]
    def is_empty(self): return not self._a
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

##### `dsa.linked_list.ll_basics` — Danh sách liên kết đơn và đôi (singly and doubly linked list)

**[Q078 · mức 1 · concept · ~3 phút]** So sánh mảng và linked list: truy cập phần tử thứ i, chèn vào đầu, chèn vào giữa khi đã có con trỏ tới nút trước. Độ phức tạp?

Đáp án / rubric: Truy cập: mảng O(1), linked list O(n). Chèn đầu: mảng O(n), list O(1). Chèn giữa khi đã có con trỏ: list O(1), mảng O(n).

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q079 · mức 2 · write_code · ~6 phút]** Viết `reverse_list(head)` đảo ngược danh sách liên kết đơn, trả đầu mới.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(to_list(reverse_list(build([1, 2, 3, 4]))), to_list(reverse_list(build([]))), to_list(reverse_list(build([7]))))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[4, 3, 2, 1] [] [7]
```
<details><summary>Code tham khảo</summary>

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
def build(vals):
    dummy = cur = ListNode()
    for v in vals:
        cur.next = ListNode(v); cur = cur.next
    return dummy.next
def to_list(h):
    out = []
    while h:
        out.append(h.val); h = h.next
    return out
def reverse_list(head):
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next
    return prev
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (6 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

##### `dsa.linked_list.ll_manipulation` — Đảo, ghép, nối lại con trỏ và sao chép list (list rewiring) (hot)

**[Q080 · mức 2 · write_code · ~10 phút]** Viết `has_cycle(head)` (Floyd) và `middle(head)` trả nút giữa (nếu 2 nút giữa, lấy nút thứ hai).

Driver (chạy sau khi bạn viết hàm/class):

```python
h = build([1, 2, 3, 4, 5])
print(middle(h).val, middle(build([1, 2, 3, 4])).val, has_cycle(h))
t = h
while t.next: t = t.next
t.next = h.next
print(has_cycle(h))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
3 3 False
True
```
<details><summary>Code tham khảo</summary>

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
def build(vals):
    dummy = cur = ListNode()
    for v in vals:
        cur.next = ListNode(v); cur = cur.next
    return dummy.next
def to_list(h):
    out = []
    while h:
        out.append(h.val); h = h.next
    return out
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast: return True
    return False
def middle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    return slow
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q081 · mức 3 · write_code · ~10 phút]** Viết `remove_nth_from_end(head, n)` xoá nút thứ n tính từ cuối trong 1 lượt (dummy + hai con trỏ cách nhau n).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(to_list(remove_nth_from_end(build([1, 2, 3, 4, 5]), 2)), to_list(remove_nth_from_end(build([1]), 1)), to_list(remove_nth_from_end(build([1, 2]), 2)))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[1, 2, 3, 5] [] [2]
```
<details><summary>Code tham khảo</summary>

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
def build(vals):
    dummy = cur = ListNode()
    for v in vals:
        cur.next = ListNode(v); cur = cur.next
    return dummy.next
def to_list(h):
    out = []
    while h:
        out.append(h.val); h = h.next
    return out
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head); fast = slow = dummy
    for _ in range(n): fast = fast.next
    while fast.next:
        fast, slow = fast.next, slow.next
    slow.next = slow.next.next
    return dummy.next
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.stack_queue.stack_queue_ds` — Stack, queue, deque và cách cài đặt (stack, queue, deque) (hot)

**[Q082 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
from collections import deque
q = deque(); q.append(1); q.append(2); q.appendleft(0)
print(q.popleft(), q.pop(), list(q))
```
Đáp án (output đã chạy kiểm chứng):

```
0 2 [1]
```
Giải thích: appendleft(0) đưa 0 lên đầu; popleft lấy 0; pop lấy 2 ở cuối.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q083 · mức 2 · write_code · ~10 phút]** Viết class `MyQueue` dùng hai stack (list) với push(x), pop(), peek(), empty(); amortized O(1).

Driver (chạy sau khi bạn viết hàm/class):

```python
q = MyQueue(); q.push(1); q.push(2)
print(q.peek(), q.pop(), q.empty(), q.pop(), q.empty())
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
1 1 False 2 True
```
<details><summary>Code tham khảo</summary>

```python
class MyQueue:
    def __init__(self): self.a, self.b = [], []
    def push(self, x): self.a.append(x)
    def _move(self):
        if not self.b:
            while self.a: self.b.append(self.a.pop())
    def pop(self):
        self._move(); return self.b.pop()
    def peek(self):
        self._move(); return self.b[-1]
    def empty(self): return not self.a and not self.b
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

##### `dsa.stack_queue.stack_problems` — Bài toán stack: ngoặc, min stack, tính biểu thức (stack problems) (hot)

**[Q084 · mức 2 · write_code · ~10 phút]** Viết `remove_dups(s)`: liên tục xoá hai ký tự giống nhau đứng cạnh nhau, trả chuỗi cuối (dùng stack).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(remove_dups("abbaca"), repr(remove_dups("aa")), remove_dups("azxxzy"))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
ca '' ay
```
<details><summary>Code tham khảo</summary>

```python
def remove_dups(s):
    st = []
    for ch in s:
        if st and st[-1] == ch: st.pop()
        else: st.append(ch)
    return "".join(st)
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q085 · mức 3 · write_code · ~10 phút]** Viết `daily_temps(t)`: với mỗi ngày i, số ngày phải chờ để có nhiệt độ cao hơn (0 nếu không có). Monotonic stack, O(n).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(daily_temps([73, 74, 75, 71, 69, 72, 76, 73]), daily_temps([30, 40, 50, 60]), daily_temps([60, 50]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[1, 1, 4, 2, 1, 1, 0, 0] [1, 1, 1, 0] [0, 0]
```
<details><summary>Code tham khảo</summary>

```python
def daily_temps(t):
    res = [0] * len(t); st = []
    for i, x in enumerate(t):
        while st and t[st[-1]] < x:
            j = st.pop(); res[j] = i - j
        st.append(i)
    return res
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.stack_queue.parsing_strings` — Phân tích chuỗi và tính biểu thức (string parsing) (hot)

**[Q086 · mức 2 · write_code · ~10 phút]** Viết `eval_rpn(tokens)` tính biểu thức Reverse Polish Notation với + - * / (chia lấy phần nguyên hướng về 0).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(eval_rpn(["2", "1", "+", "3", "*"]), eval_rpn(["4", "13", "5", "/", "+"]), eval_rpn(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
9 6 22
```
<details><summary>Code tham khảo</summary>

```python
def eval_rpn(tokens):
    st = []
    for t in tokens:
        if t in "+-*/" and len(t) == 1:
            b, a = st.pop(), st.pop()
            st.append(a + b if t == "+" else a - b if t == "-" else a * b if t == "*" else int(a / b))
        else: st.append(int(t))
    return st[0]
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q087 · mức 3 · write_code · ~10 phút]** Viết `decode(s)`: "3[a2[c]]" -> "accaccacc" (số lặp, ngoặc lồng nhau) bằng stack.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(decode("3[a]2[bc]"), decode("3[a2[c]]"), decode("2[abc]3[cd]ef"))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
aaabcbc accaccacc abcabccdcdcdef
```
<details><summary>Code tham khảo</summary>

```python
def decode(s):
    st = []; cur = ""; num = 0
    for ch in s:
        if ch.isdigit(): num = num * 10 + int(ch)
        elif ch == "[": st.append((cur, num)); cur, num = "", 0
        elif ch == "]":
            prev, k = st.pop(); cur = prev + cur * k
        else: cur += ch
    return cur
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

#### Cụm C6: Recursion, backtracking, binary search, sorting

##### `dsa.recursion_backtracking.recursion_basics` — Đệ quy cơ bản và chia để trị (recursion, divide and conquer)

**[Q092 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
def f(n): return 1 if n <= 1 else n * f(n - 1)
def g(n): return n if n < 2 else g(n - 1) + g(n - 2)
print(f(5), g(7))
```
Đáp án (output đã chạy kiểm chứng):

```
120 13
```
Giải thích: f là giai thừa; g là Fibonacci chậm O(2^n).

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q093 · mức 2 · write_code · ~10 phút]** Viết `climb(n)`: số cách leo n bậc thang, mỗi bước 1 hoặc 2 bậc (đệ quy có memo hoặc lặp).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(climb(2), climb(5), climb(30))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
2 8 1346269
```
<details><summary>Code tham khảo</summary>

```python
def climb(n, memo={}):
    if n <= 2: return n
    if n not in memo: memo[n] = climb(n - 1) + climb(n - 2)
    return memo[n]
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q094 · mức 3 · write_code · ~10 phút]** Viết `kth_symbol(n, k)`: hàng 1 là "0"; mỗi hàng thay 0->01, 1->10. Trả ký hiệu thứ k (k tính từ 1) của hàng n, không dựng cả hàng.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(kth_symbol(1, 1), kth_symbol(2, 1), kth_symbol(2, 2), kth_symbol(4, 5))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
0 0 1 1
```
<details><summary>Code tham khảo</summary>

```python
def kth_symbol(n, k):
    if n == 1: return 0
    p = kth_symbol(n - 1, (k + 1) // 2)
    return p if k % 2 == 1 else 1 - p
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.searching_sorting.binary_search_basics` — Binary search cơ bản (binary search fundamentals)

**[Q096 · mức 1 · concept · ~3 phút]** Với `lo, hi = 0, len(a) - 1` và `while lo <= hi`, vì sao dùng `mid = lo + (hi - lo) // 2`? Điều kiện dừng? Khi nào dùng `lo < hi`?

Đáp án / rubric: Tránh tràn số ở ngôn ngữ có overflow; Python không tràn nhưng giữ thói quen. `<=` khi tìm đúng giá trị và hai đầu đều là ứng viên; `<` kiểu "hi mở" (hi = len) tìm vị trí đầu tiên thoả điều kiện.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q095 · mức 2 · write_code · ~6 phút]** Viết `search_insert(nums, target)` trả chỉ số của target trong mảng đã sắp, hoặc vị trí cần chèn để vẫn sắp xếp. O(log n).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(search_insert([1, 3, 5, 6], 5), search_insert([1, 3, 5, 6], 2), search_insert([1, 3, 5, 6], 7), search_insert([], 1))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
2 1 4 0
```
<details><summary>Code tham khảo</summary>

```python
def search_insert(nums, target):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target: lo = mid + 1
        else: hi = mid
    return lo
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (6 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q097 · mức 3 · write_code · ~10 phút]** Viết `my_sqrt(x)` trả phần nguyên của căn bậc hai x (x >= 0) bằng binary search, không dùng ** 0.5 hay math.sqrt.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(my_sqrt(8), my_sqrt(0), my_sqrt(1), my_sqrt(2147395599))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
2 0 1 46339
```
<details><summary>Code tham khảo</summary>

```python
def my_sqrt(x):
    lo, hi = 0, x
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid * mid <= x: lo = mid
        else: hi = mid - 1
    return lo
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.searching_sorting.sorting_algorithms` — Thuật toán sắp xếp (sorting algorithms)

**[Q100 · mức 1 · concept · ~3 phút]** So sánh merge sort, quick sort, heap sort: time trung bình/xấu nhất, space, ổn định (stable)? `sorted()` của Python dùng gì?

Đáp án / rubric: Merge: O(n log n) mọi trường hợp, O(n) space, stable. Quick: O(n log n) TB, O(n^2) xấu nhất, O(log n) space, không stable. Heap: O(n log n), O(1), không stable. Python: Timsort (stable, O(n log n)).

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q101 · mức 2 · write_code · ~10 phút]** Viết `merge_sort(a)` trả list mới đã sắp (đệ quy chia đôi + gộp).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(merge_sort([5, 2, 4, 6, 1, 3]), merge_sort([]), merge_sort([2, 2, 1]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[1, 2, 3, 4, 5, 6] [] [1, 2, 2]
```
<details><summary>Code tham khảo</summary>

```python
def merge_sort(a):
    if len(a) <= 1: return a
    m = len(a) // 2
    l, r = merge_sort(a[:m]), merge_sort(a[m:])
    out = []; i = j = 0
    while i < len(l) and j < len(r):
        if l[i] <= r[j]: out.append(l[i]); i += 1
        else: out.append(r[j]); j += 1
    return out + l[i:] + r[j:]
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

##### `dsa.searching_sorting.sorting_applications` — Ứng dụng sort và quickselect (sorting applications)

**[Q102 · mức 2 · write_code · ~10 phút]** Viết `can_attend(intervals)`: True nếu không có hai cuộc họp [start, end) nào chồng nhau (sắp theo start rồi so sánh liền kề).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(can_attend([[0, 30], [5, 10], [15, 20]]), can_attend([[7, 10], [2, 4]]), can_attend([]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
False True True
```
<details><summary>Code tham khảo</summary>

```python
def can_attend(intervals):
    iv = sorted(intervals)
    return all(iv[i][1] <= iv[i + 1][0] for i in range(len(iv) - 1))
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q103 · mức 3 · write_code · ~10 phút]** Viết `largest_number(nums)` ghép các số thành số lớn nhất (trả chuỗi). Gợi ý: sắp theo so sánh a+b với b+a.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(largest_number([10, 2]), largest_number([3, 30, 34, 5, 9]), largest_number([0, 0]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
210 9534330 0
```
<details><summary>Code tham khảo</summary>

```python
def largest_number(nums):
    from functools import cmp_to_key
    s = sorted(map(str, nums), key=cmp_to_key(lambda a, b: -1 if a + b > b + a else 1 if a + b < b + a else 0))
    r = "".join(s)
    return "0" if r[0] == "0" else r
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.searching_sorting.binary_search_variants` — Binary search trên mảng xoay, 2D, peak (binary search variants) (hot)

**[Q098 · mức 2 · write_code · ~10 phút]** Viết `search_range(nums, target)` trả [vị trí đầu, vị trí cuối] của target trong mảng sắp tăng, hoặc [-1, -1]. O(log n).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(search_range([5, 7, 7, 8, 8, 10], 8), search_range([5, 7, 7, 8, 8, 10], 6), search_range([], 0))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[3, 4] [-1, -1] [-1, -1]
```
<details><summary>Code tham khảo</summary>

```python
def search_range(nums, target):
    import bisect
    i = bisect.bisect_left(nums, target)
    if i == len(nums) or nums[i] != target: return [-1, -1]
    return [i, bisect.bisect_right(nums, target) - 1]
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q099 · mức 3 · write_code · ~10 phút]** Viết `search_rotated(nums, target)` tìm target trong mảng sắp tăng đã bị xoay (không trùng), trả chỉ số hoặc -1. O(log n).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(search_rotated([4, 5, 6, 7, 0, 1, 2], 0), search_rotated([4, 5, 6, 7, 0, 1, 2], 3), search_rotated([1], 1))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
4 -1 0
```
<details><summary>Code tham khảo</summary>

```python
def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target: return mid
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]: hi = mid - 1
            else: lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]: lo = mid + 1
            else: hi = mid - 1
    return -1
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.recursion_backtracking.backtracking_core` — Quay lui: tập con, hoán vị, tổ hợp (backtracking) (hot)

**[Q118 · mức 1 · concept · ~3 phút]** Mẫu backtracking gồm 3 bước nào? Vì sao cần "undo" (bỏ lựa chọn) sau khi gọi đệ quy?

Đáp án / rubric: Chọn (choose) -> khám phá (explore: gọi đệ quy) -> bỏ chọn (unchoose). Cần undo vì cùng một danh sách/trạng thái được dùng chung cho các nhánh khác.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q119 · mức 2 · write_code · ~10 phút]** Viết `subsets(nums)` trả mọi tập con (không trùng phần tử). Kết quả sắp theo (độ dài, giá trị) để so sánh.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(subsets([1, 2, 3]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]
```
<details><summary>Code tham khảo</summary>

```python
def subsets(nums):
    res = []; cur = []
    def go(i):
        if i == len(nums):
            res.append(cur[:]); return
        go(i + 1)
        cur.append(nums[i]); go(i + 1); cur.pop()
    go(0)
    return sorted(res, key=lambda x: (len(x), x))
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q120 · mức 3 · write_code · ~10 phút]** Viết `gen_paren(n)` trả mọi chuỗi ngoặc hợp lệ gồm n cặp, sắp theo thứ tự chữ cái.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(gen_paren(3)); print(len(gen_paren(4)))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
['((()))', '(()())', '(())()', '()(())', '()()()']
14
```
<details><summary>Code tham khảo</summary>

```python
def gen_paren(n):
    res = []
    def go(s, o, c):
        if len(s) == 2 * n: res.append(s); return
        if o < n: go(s + "(", o + 1, c)
        if c < o: go(s + ")", o, c + 1)
    go("", 0, 0)
    return sorted(res)
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

#### Cụm C7: Cây, heap, design, intervals

##### `dsa.trees.tree_basics` — Cây nhị phân và duyệt cây (binary trees and traversals) (hot)

**[Q104 · mức 1 · concept · ~3 phút]** Cây nhị phân: 1 là gốc, con trái 2, con phải 3; 2 có con phải 4. Viết thứ tự preorder, inorder, postorder.

Đáp án / rubric: Preorder: 1 2 4 3. Inorder: 2 4 1 3. Postorder: 4 2 3 1.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q105 · mức 2 · write_code · ~6 phút]** Viết `max_depth(root)` và `inorder(root)` (list giá trị theo thứ tự giữa).

Driver (chạy sau khi bạn viết hàm/class):

```python
t = tree([3, 9, 20, None, None, 15, 7])
print(max_depth(t), inorder(t), max_depth(None))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
3 [9, 3, 15, 20, 7] 0
```
<details><summary>Code tham khảo</summary>

```python
from collections import deque
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right
def tree(vals):
    if not vals or vals[0] is None: return None
    root = TreeNode(vals[0]); q = deque([root]); i = 1
    while q and i < len(vals):
        n = q.popleft()
        if i < len(vals) and vals[i] is not None:
            n.left = TreeNode(vals[i]); q.append(n.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            n.right = TreeNode(vals[i]); q.append(n.right)
        i += 1
    return root
def max_depth(r):
    return 0 if not r else 1 + max(max_depth(r.left), max_depth(r.right))
def inorder(r):
    return inorder(r.left) + [r.val] + inorder(r.right) if r else []
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (6 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

##### `dsa.heap.heap_ds` — Binary heap và priority queue (binary heap) (hot)

**[Q106 · mức 1 · concept · ~3 phút]** Heap là gì? Chi phí push, pop, peek, heapify? Python có max-heap không?

Đáp án / rubric: Cây nhị phân gần đầy, cha <= con (min-heap). push/pop O(log n), peek O(1), heapify O(n). heapq chỉ có min-heap; max-heap: đẩy số âm.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q107 · mức 2 · write_code · ~10 phút]** Viết `last_stone(stones)`: mỗi lượt lấy hai hòn nặng nhất đập nhau (bằng nhau thì cả hai biến mất, khác nhau thì còn lại hiệu). Trả cân nặng hòn cuối (hoặc 0).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(last_stone([2, 7, 4, 1, 8, 1]), last_stone([1]), last_stone([3, 3]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
1 1 0
```
<details><summary>Code tham khảo</summary>

```python
def last_stone(stones):
    import heapq
    h = [-s for s in stones]; heapq.heapify(h)
    while len(h) > 1:
        a, b = heapq.heappop(h), heapq.heappop(h)
        if a != b: heapq.heappush(h, a - b)
    return -h[0] if h else 0
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

##### `dsa.heap.heap_top_k` — Top-K bằng heap (top-K with heaps) (hot)

**[Q108 · mức 2 · write_code · ~10 phút]** Viết `top_k_words(words, k)` trả k từ phổ biến nhất (hoà thì chữ cái nhỏ trước), dùng heap hoặc sort.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(top_k_words(["i", "love", "leetcode", "i", "love", "coding"], 2), top_k_words(["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], 4))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
['i', 'love'] ['the', 'is', 'sunny', 'day']
```
<details><summary>Code tham khảo</summary>

```python
def top_k_words(words, k):
    import heapq
    from collections import Counter
    c = Counter(words)
    return heapq.nsmallest(k, c, key=lambda w: (-c[w], w))
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q109 · mức 3 · write_code · ~10 phút]** Viết `kth_smallest(matrix, k)` với ma trận n x n, mỗi hàng và cột đã sắp tăng. Trả phần tử nhỏ thứ k bằng heap (O(k log n)).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(kth_smallest([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8), kth_smallest([[-5]], 1))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
13 -5
```
<details><summary>Code tham khảo</summary>

```python
def kth_smallest(matrix, k):
    import heapq
    n = len(matrix); h = [(matrix[i][0], i, 0) for i in range(n)]; heapq.heapify(h)
    for _ in range(k - 1):
        v, i, j = heapq.heappop(h)
        if j + 1 < n: heapq.heappush(h, (matrix[i][j + 1], i, j + 1))
    return h[0][0]
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.trees.tree_recursion` — Đệ quy trên cây, dựng và serialize cây (tree recursion and construction) (hot)

**[Q121 · mức 2 · write_code · ~10 phút]** Viết `has_path_sum(root, target)`: có đường từ gốc tới LÁ có tổng bằng target không?

Driver (chạy sau khi bạn viết hàm/class):

```python
t = tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])
print(has_path_sum(t, 22), has_path_sum(t, 5), has_path_sum(None, 0))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
True False False
```
<details><summary>Code tham khảo</summary>

```python
from collections import deque
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right
def tree(vals):
    if not vals or vals[0] is None: return None
    root = TreeNode(vals[0]); q = deque([root]); i = 1
    while q and i < len(vals):
        n = q.popleft()
        if i < len(vals) and vals[i] is not None:
            n.left = TreeNode(vals[i]); q.append(n.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            n.right = TreeNode(vals[i]); q.append(n.right)
        i += 1
    return root
def has_path_sum(r, t):
    if not r: return False
    if not r.left and not r.right: return r.val == t
    return has_path_sum(r.left, t - r.val) or has_path_sum(r.right, t - r.val)
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q122 · mức 3 · write_code · ~10 phút]** Viết `is_balanced(root)` (chênh lệch chiều cao hai cây con ≤ 1 ở mọi nút) trong O(n), không tính lại chiều cao nhiều lần.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(is_balanced(tree([3, 9, 20, None, None, 15, 7])), is_balanced(tree([1, 2, 2, 3, 3, None, None, 4, 4])), is_balanced(None))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
True False True
```
<details><summary>Code tham khảo</summary>

```python
from collections import deque
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right
def tree(vals):
    if not vals or vals[0] is None: return None
    root = TreeNode(vals[0]); q = deque([root]); i = 1
    while q and i < len(vals):
        n = q.popleft()
        if i < len(vals) and vals[i] is not None:
            n.left = TreeNode(vals[i]); q.append(n.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            n.right = TreeNode(vals[i]); q.append(n.right)
        i += 1
    return root
def is_balanced(r):
    def h(n):
        if not n: return 0
        a = h(n.left)
        if a < 0: return -1
        b = h(n.right)
        if b < 0 or abs(a - b) > 1: return -1
        return 1 + max(a, b)
    return h(r) >= 0
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.trees.tree_bfs_views_hierarchy` — Duyệt theo tầng, view của cây và cây phân cấp (level-order and hierarchy trees) (hot)

**[Q123 · mức 2 · write_code · ~10 phút]** Viết `level_order(root)` trả list các tầng (mỗi tầng là list giá trị từ trái sang phải).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(level_order(tree([3, 9, 20, None, None, 15, 7])), level_order(None))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[[3], [9, 20], [15, 7]] []
```
<details><summary>Code tham khảo</summary>

```python
from collections import deque
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right
def tree(vals):
    if not vals or vals[0] is None: return None
    root = TreeNode(vals[0]); q = deque([root]); i = 1
    while q and i < len(vals):
        n = q.popleft()
        if i < len(vals) and vals[i] is not None:
            n.left = TreeNode(vals[i]); q.append(n.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            n.right = TreeNode(vals[i]); q.append(n.right)
        i += 1
    return root
def level_order(r):
    res = []; q = deque([r] if r else [])
    while q:
        res.append([n.val for n in q])
        for _ in range(len(q)):
            n = q.popleft()
            if n.left: q.append(n.left)
            if n.right: q.append(n.right)
    return res
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q124 · mức 3 · write_code · ~10 phút]** Viết `zigzag(root)`: như level_order nhưng tầng 0 trái->phải, tầng 1 phải->trái, xen kẽ.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(zigzag(tree([3, 9, 20, None, None, 15, 7])), zigzag(tree([1, 2, 3, 4, 5, 6, 7])))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[[3], [20, 9], [15, 7]] [[1], [3, 2], [4, 5, 6, 7]]
```
<details><summary>Code tham khảo</summary>

```python
from collections import deque
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right
def tree(vals):
    if not vals or vals[0] is None: return None
    root = TreeNode(vals[0]); q = deque([root]); i = 1
    while q and i < len(vals):
        n = q.popleft()
        if i < len(vals) and vals[i] is not None:
            n.left = TreeNode(vals[i]); q.append(n.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            n.right = TreeNode(vals[i]); q.append(n.right)
        i += 1
    return root
def zigzag(r):
    res = []; q = deque([r] if r else []); flip = False
    while q:
        row = [n.val for n in q]
        res.append(row[::-1] if flip else row); flip = not flip
        for _ in range(len(q)):
            n = q.popleft()
            if n.left: q.append(n.left)
            if n.right: q.append(n.right)
    return res
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.trees.bst` — Cây nhị phân tìm kiếm (binary search tree) (hot)

**[Q125 · mức 1 · concept · ~3 phút]** Tính chất của BST? Duyệt inorder BST cho kết quả gì? Tìm một giá trị trong BST cân bằng và lệch tốn bao nhiêu?

Đáp án / rubric: Mọi nút trong cây con trái < nút < mọi nút cây con phải. Inorder cho dãy tăng dần. Tìm: O(log n) khi cân bằng, O(n) khi lệch.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q126 · mức 2 · write_code · ~10 phút]** Viết `is_valid_bst(root)` dùng khoảng (lo, hi) cho mỗi nút, không chỉ so với con trực tiếp.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(is_valid_bst(tree([2, 1, 3])), is_valid_bst(tree([5, 1, 4, None, None, 3, 6])), is_valid_bst(tree([5, 4, 6, None, None, 3, 7])))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
True False False
```
<details><summary>Code tham khảo</summary>

```python
from collections import deque
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right
def tree(vals):
    if not vals or vals[0] is None: return None
    root = TreeNode(vals[0]); q = deque([root]); i = 1
    while q and i < len(vals):
        n = q.popleft()
        if i < len(vals) and vals[i] is not None:
            n.left = TreeNode(vals[i]); q.append(n.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            n.right = TreeNode(vals[i]); q.append(n.right)
        i += 1
    return root
def is_valid_bst(r, lo=float("-inf"), hi=float("inf")):
    if not r: return True
    if not lo < r.val < hi: return False
    return is_valid_bst(r.left, lo, r.val) and is_valid_bst(r.right, r.val, hi)
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q127 · mức 3 · write_code · ~10 phút]** Viết `kth_smallest(root, k)` trong BST bằng inorder lặp (stack) và dừng sớm khi tìm được.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(kth_smallest(tree([3, 1, 4, None, 2]), 1), kth_smallest(tree([5, 3, 6, 2, 4, None, None, 1]), 3))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
1 3
```
<details><summary>Code tham khảo</summary>

```python
from collections import deque
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right
def tree(vals):
    if not vals or vals[0] is None: return None
    root = TreeNode(vals[0]); q = deque([root]); i = 1
    while q and i < len(vals):
        n = q.popleft()
        if i < len(vals) and vals[i] is not None:
            n.left = TreeNode(vals[i]); q.append(n.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            n.right = TreeNode(vals[i]); q.append(n.right)
        i += 1
    return root
def kth_smallest(root, k):
    st = []; cur = root
    while st or cur:
        while cur: st.append(cur); cur = cur.left
        cur = st.pop(); k -= 1
        if k == 0: return cur.val
        cur = cur.right
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.design_ds.design_cache` — Thiết kế cache: LRU, LFU, TTL (cache design) (hot)

**[Q128 · mức 2 · write_code · ~10 phút]** Viết class `MyHashMap` (put, get -> -1 nếu thiếu, remove) bằng mảng bucket + list cặp (chaining), không dùng dict.

Driver (chạy sau khi bạn viết hàm/class):

```python
m = MyHashMap(); m.put(1, 1); m.put(98, 2); m.put(1, 3)
print(m.get(1), m.get(98), m.get(2)); m.remove(1); print(m.get(1), m.get(98))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
3 2 -1
-1 2
```
<details><summary>Code tham khảo</summary>

```python
class MyHashMap:
    def __init__(self): self.b = [[] for _ in range(97)]
    def put(self, k, v):
        row = self.b[k % 97]
        for p in row:
            if p[0] == k: p[1] = v; return
        row.append([k, v])
    def get(self, k):
        for a, v in self.b[k % 97]:
            if a == k: return v
        return -1
    def remove(self, k):
        self.b[k % 97] = [p for p in self.b[k % 97] if p[0] != k]
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q129 · mức 3 · write_code · ~10 phút]** Viết class `TimeMap`: set(key, value, t) với t tăng dần theo từng key; get(key, t) trả value có thời điểm lớn nhất <= t, hoặc "". Dùng binary search.

Driver (chạy sau khi bạn viết hàm/class):

```python
tm = TimeMap(); tm.set("foo", "bar", 1); tm.set("foo", "bar2", 4)
print(repr(tm.get("foo", 1)), tm.get("foo", 3), tm.get("foo", 4), repr(tm.get("foo", 0)), repr(tm.get("x", 5)))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
'bar' bar bar2 '' ''
```
<details><summary>Code tham khảo</summary>

```python
class TimeMap:
    def __init__(self): self.d = {}
    def set(self, k, v, t): self.d.setdefault(k, []).append((t, v))
    def get(self, k, t):
        import bisect
        a = self.d.get(k, [])
        i = bisect.bisect_right(a, (t, chr(0x10ffff)))
        return a[i - 1][1] if i else ""
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.design_ds.design_o1_structures` — Cấu trúc O(1): RandomizedSet, stack đặc biệt (O(1) structures)

**[Q130 · mức 2 · write_code · ~10 phút]** Viết class `MinStack` với push, pop, top, get_min đều O(1).

Driver (chạy sau khi bạn viết hàm/class):

```python
m = MinStack(); m.push(-2); m.push(0); m.push(-3)
print(m.get_min()); m.pop(); print(m.top(), m.get_min())
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
-3
0 -2
```
<details><summary>Code tham khảo</summary>

```python
class MinStack:
    def __init__(self): self.s = []
    def push(self, x): self.s.append((x, min(x, self.s[-1][1]) if self.s else x))
    def pop(self): self.s.pop()
    def top(self): return self.s[-1][0]
    def get_min(self): return self.s[-1][1]
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q131 · mức 3 · write_code · ~10 phút]** Viết class `Underground`: check_in(id, station, t), check_out(id, station, t), average(a, b) = thời gian trung bình các chuyến a -> b đã hoàn thành. O(1) mỗi thao tác.

Driver (chạy sau khi bạn viết hàm/class):

```python
u = Underground(); u.check_in(45, "A", 3); u.check_in(32, "A", 8); u.check_out(45, "B", 15); u.check_out(32, "B", 22)
print(u.average("A", "B")); u.check_in(10, "A", 24); u.check_out(10, "B", 38); print(u.average("A", "B"))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
13.0
13.333333333333334
```
<details><summary>Code tham khảo</summary>

```python
class Underground:
    def __init__(self): self.on = {}; self.tot = {}
    def check_in(self, i, s, t): self.on[i] = (s, t)
    def check_out(self, i, s, t):
        a, t0 = self.on.pop(i)
        k = (a, s); x = self.tot.get(k, (0, 0))
        self.tot[k] = (x[0] + t - t0, x[1] + 1)
    def average(self, a, b):
        x = self.tot[(a, b)]; return x[0] / x[1]
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.greedy_intervals.interval_basics` — Khoảng cơ bản: gộp, chèn, chồng lấn (interval fundamentals) (hot)

**[Q132 · mức 2 · write_code · ~10 phút]** Viết `summary_ranges(nums)` cho mảng số nguyên tăng không trùng: gom thành các khoảng, ví dụ [0,1,2,4,5,7] -> ["0->2","4->5","7"].

Driver (chạy sau khi bạn viết hàm/class):

```python
print(summary_ranges([0, 1, 2, 4, 5, 7]), summary_ranges([]), summary_ranges([5]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
['0->2', '4->5', '7'] [] ['5']
```
<details><summary>Code tham khảo</summary>

```python
def summary_ranges(nums):
    res = []; i = 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1: j += 1
        res.append(str(nums[i]) if i == j else f"{nums[i]}->{nums[j]}"); i = j + 1
    return res
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q133 · mức 3 · write_code · ~10 phút]** Viết `insert_interval(intervals, new)`: intervals đã sắp và không chồng; chèn new và gộp nếu chồng. Trả list mới.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(insert_interval([[1, 3], [6, 9]], [2, 5]), insert_interval([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]), insert_interval([], [5, 7]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[[1, 5], [6, 9]] [[1, 2], [3, 10], [12, 16]] [[5, 7]]
```
<details><summary>Code tham khảo</summary>

```python
def insert_interval(iv, new):
    res = []; i = 0
    while i < len(iv) and iv[i][1] < new[0]: res.append(iv[i]); i += 1
    while i < len(iv) and iv[i][0] <= new[1]:
        new = [min(new[0], iv[i][0]), max(new[1], iv[i][1])]; i += 1
    res.append(new)
    return res + iv[i:]
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.greedy_intervals.interval_sweep` — Sweep line và bài lịch (sweep line and calendars) (hot)

**[Q134 · mức 2 · write_code · ~10 phút]** Viết `min_arrows(points)`: các quả bóng là đoạn [x1, x2]; một mũi tên bắn dọc x phá mọi bóng chứa x. Số mũi tên ít nhất? (sắp theo điểm cuối, tham lam)

Driver (chạy sau khi bạn viết hàm/class):

```python
print(min_arrows([[10, 16], [2, 8], [1, 6], [7, 12]]), min_arrows([[1, 2], [3, 4], [5, 6]]), min_arrows([[1, 2], [2, 3]]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
2 3 1
```
<details><summary>Code tham khảo</summary>

```python
def min_arrows(points):
    pts = sorted(points, key=lambda p: p[1]); n = 0; end = float("-inf")
    for a, b in pts:
        if a > end: n += 1; end = b
    return n
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q135 · mức 3 · write_code · ~10 phút]** Viết `car_pooling(trips, capacity)`: mỗi chuyến [người, lên, xuống]; True nếu không lúc nào vượt capacity. (sweep line: +người tại lên, -người tại xuống)

Driver (chạy sau khi bạn viết hàm/class):

```python
print(car_pooling([[2, 1, 5], [3, 3, 7]], 4), car_pooling([[2, 1, 5], [3, 3, 7]], 5), car_pooling([[3, 2, 7], [3, 7, 9], [8, 3, 9]], 11))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
False True True
```
<details><summary>Code tham khảo</summary>

```python
def car_pooling(trips, capacity):
    ev = []
    for n, a, b in trips: ev += [(a, n), (b, -n)]
    cur = 0
    for _, d in sorted(ev):
        cur += d
        if cur > capacity: return False
    return True
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

#### Cụm C8: Graph, bit

##### `dsa.graphs.graph_representation` — Biểu diễn đồ thị và thuật ngữ (graph representation)

**[Q147 · mức 1 · concept · ~3 phút]** So sánh adjacency list và adjacency matrix: bộ nhớ, kiểm tra cạnh (u,v), duyệt hàng xóm. Khi nào chọn cái nào?

Đáp án / rubric: List: O(V+E) bộ nhớ, kiểm tra cạnh O(deg), duyệt hàng xóm O(deg); hợp đồ thị thưa. Matrix: O(V^2), kiểm tra cạnh O(1), duyệt hàng xóm O(V); hợp đồ thị dày hoặc V nhỏ.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q148 · mức 2 · write_code · ~10 phút]** Viết `find_judge(n, trust)`: người phán xét được n-1 người tin và không tin ai; trust là cặp [a, b] (a tin b). Trả nhãn người đó (1..n) hoặc -1.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(find_judge(2, [[1, 2]]), find_judge(3, [[1, 3], [2, 3]]), find_judge(3, [[1, 3], [2, 3], [3, 1]]), find_judge(1, []))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
2 3 -1 1
```
<details><summary>Code tham khảo</summary>

```python
def find_judge(n, trust):
    score = [0] * (n + 1)
    for a, b in trust: score[a] -= 1; score[b] += 1
    for i in range(1, n + 1):
        if score[i] == n - 1: return i
    return -1
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

##### `dsa.graphs.graph_traversal` — DFS và BFS trên đồ thị (graph traversal)

**[Q149 · mức 2 · write_code · ~6 phút]** Viết `count_components(n, edges)` số thành phần liên thông của đồ thị vô hướng n đỉnh (DFS hoặc BFS).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(count_components(5, [[0, 1], [1, 2], [3, 4]]), count_components(3, []), count_components(4, [[0, 1], [1, 2], [2, 3]]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
2 3 1
```
<details><summary>Code tham khảo</summary>

```python
def count_components(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges: adj[a].append(b); adj[b].append(a)
    seen = [False] * n; c = 0
    for s in range(n):
        if seen[s]: continue
        c += 1; st = [s]; seen[s] = True
        while st:
            u = st.pop()
            for v in adj[u]:
                if not seen[v]: seen[v] = True; st.append(v)
    return c
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (6 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q150 · mức 3 · write_code · ~10 phút]** Viết `is_bipartite(graph)` (graph là danh sách kề) bằng BFS tô 2 màu.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(is_bipartite([[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]), is_bipartite([[1, 3], [0, 2], [1, 3], [0, 2]]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
False True
```
<details><summary>Code tham khảo</summary>

```python
def is_bipartite(graph):
    color = {}
    for s in range(len(graph)):
        if s in color: continue
        color[s] = 0; q = [s]
        while q:
            u = q.pop()
            for v in graph[u]:
                if v not in color: color[v] = 1 - color[u]; q.append(v)
                elif color[v] == color[u]: return False
    return True
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.graphs.grid_graphs` — BFS/DFS trên lưới (grid graphs) (hot)

**[Q151 · mức 2 · write_code · ~10 phút]** Viết `flood_fill(img, sr, sc, color)` tô màu mọi ô liên thông cùng màu với ô (sr, sc) (4 hướng), trả img.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(flood_fill([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2), flood_fill([[0, 0, 0], [0, 0, 0]], 0, 0, 0))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[[2, 2, 2], [2, 2, 0], [2, 0, 1]] [[0, 0, 0], [0, 0, 0]]
```
<details><summary>Code tham khảo</summary>

```python
def flood_fill(img, sr, sc, color):
    old = img[sr][sc]
    if old == color: return img
    st = [(sr, sc)]
    while st:
        r, c = st.pop()
        if 0 <= r < len(img) and 0 <= c < len(img[0]) and img[r][c] == old:
            img[r][c] = color
            st += [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
    return img
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q152 · mức 3 · write_code · ~10 phút]** Viết `max_area(grid)` diện tích đảo lớn nhất (ô 1 liên thông 4 hướng), 0 nếu không có.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(max_area([[0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 1, 1]]), max_area([[0, 0]]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
4 0
```
<details><summary>Code tham khảo</summary>

```python
def max_area(grid):
    R, Cc = len(grid), len(grid[0]); best = 0
    for i in range(R):
        for j in range(Cc):
            if grid[i][j] == 1:
                st = [(i, j)]; grid[i][j] = 0; a = 0
                while st:
                    r, c = st.pop(); a += 1
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < R and 0 <= nc < Cc and grid[nr][nc] == 1: grid[nr][nc] = 0; st.append((nr, nc))
                best = max(best, a)
    return best
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.graphs.bfs_shortest_path` — BFS đường đi ngắn nhất và tìm kiếm trạng thái (BFS shortest path) (hot)

**[Q153 · mức 2 · write_code · ~10 phút]** Viết `shortest(n, edges, s, t)` độ dài đường đi ngắn nhất (số cạnh) từ s tới t trong đồ thị vô hướng, hoặc -1.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(shortest(5, [[0, 1], [1, 2], [0, 3], [3, 4], [4, 2]], 0, 2), shortest(4, [[0, 1]], 0, 3), shortest(3, [], 1, 1))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
2 -1 0
```
<details><summary>Code tham khảo</summary>

```python
def shortest(n, edges, s, t):
    from collections import deque
    adj = [[] for _ in range(n)]
    for a, b in edges: adj[a].append(b); adj[b].append(a)
    dist = {s: 0}; q = deque([s])
    while q:
        u = q.popleft()
        if u == t: return dist[u]
        for v in adj[u]:
            if v not in dist: dist[v] = dist[u] + 1; q.append(v)
    return -1
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q154 · mức 3 · write_code · ~10 phút]** Viết `rotting(grid)`: 2 là cam thối, 1 tươi, 0 trống; mỗi phút cam thối làm thối 4 hướng. Trả số phút để hết tươi, hoặc -1. (BFS nhiều nguồn)

Driver (chạy sau khi bạn viết hàm/class):

```python
print(rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]), rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]), rotting([[0, 2]]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
4 -1 0
```
<details><summary>Code tham khảo</summary>

```python
def rotting(grid):
    from collections import deque
    R, Cc = len(grid), len(grid[0]); q = deque(); fresh = 0
    for i in range(R):
        for j in range(Cc):
            if grid[i][j] == 2: q.append((i, j, 0))
            elif grid[i][j] == 1: fresh += 1
    t = 0
    while q:
        r, c, t = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < Cc and grid[nr][nc] == 1:
                grid[nr][nc] = 2; fresh -= 1; q.append((nr, nc, t + 1))
    return t if fresh == 0 else -1
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.graphs.topological_sort` — Topological sort, phụ thuộc và lập lịch task (topological sort and scheduling) (hot)

**[Q155 · mức 2 · write_code · ~10 phút]** Viết `can_finish(n, prereqs)`: prereqs[i] = [a, b] nghĩa là học b trước a. True nếu có thể học hết (đồ thị không có chu trình). Dùng Kahn (đếm bậc vào).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(can_finish(2, [[1, 0]]), can_finish(2, [[1, 0], [0, 1]]), can_finish(3, []))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
True False True
```
<details><summary>Code tham khảo</summary>

```python
def can_finish(n, prereqs):
    from collections import deque
    adj = [[] for _ in range(n)]; deg = [0] * n
    for a, b in prereqs: adj[b].append(a); deg[a] += 1
    q = deque(i for i in range(n) if deg[i] == 0); seen = 0
    while q:
        u = q.popleft(); seen += 1
        for v in adj[u]:
            deg[v] -= 1
            if deg[v] == 0: q.append(v)
    return seen == n
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q156 · mức 3 · write_code · ~10 phút]** Viết `find_order(n, prereqs)` trả MỘT thứ tự học hợp lệ (hoặc []). Driver sẽ kiểm tra tính hợp lệ chứ không so với đáp án cố định.

Driver (chạy sau khi bạn viết hàm/class):

```python
def ok(n, pre, order):
    if len(order) != n: return False
    pos = {c: i for i, c in enumerate(order)}
    return all(pos[b] < pos[a] for a, b in pre)
print(ok(4, [[1, 0], [2, 0], [3, 1], [3, 2]], find_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]])), find_order(2, [[0, 1], [1, 0]]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
True []
```
<details><summary>Code tham khảo</summary>

```python
def find_order(n, prereqs):
    from collections import deque
    adj = [[] for _ in range(n)]; deg = [0] * n
    for a, b in prereqs: adj[b].append(a); deg[a] += 1
    q = deque(i for i in range(n) if deg[i] == 0); out = []
    while q:
        u = q.popleft(); out.append(u)
        for v in adj[u]:
            deg[v] -= 1
            if deg[v] == 0: q.append(v)
    return out if len(out) == n else []
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.math_bits.bit_basics` — Thao tác bit (bit manipulation) (hot)

**[Q157 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
print(5 & 3, 5 | 3, 5 ^ 3, 1 << 4, 13 >> 1, bin(10))
```
Đáp án (output đã chạy kiểm chứng):

```
1 7 6 16 6 0b1010
```
Giải thích: 101 & 011 = 001; | = 111; ^ = 110; 1<<4 = 16; 13>>1 = 6.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q158 · mức 2 · write_code · ~10 phút]** Viết `popcount(n)` đếm số bit 1 của n >= 0 bằng thủ thuật n & (n - 1) (mỗi lần xoá bit 1 thấp nhất).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(popcount(11), popcount(128), popcount(0), popcount(2**31 - 1))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
3 1 0 31
```
<details><summary>Code tham khảo</summary>

```python
def popcount(n):
    c = 0
    while n:
        n &= n - 1; c += 1
    return c
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q159 · mức 2 · write_code · ~10 phút]** Viết `single_number(nums)`: mọi số xuất hiện đúng 2 lần trừ một số xuất hiện 1 lần. Trả số đó, O(n) thời gian, O(1) bộ nhớ (XOR).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(single_number([4, 1, 2, 1, 2]), single_number([7]), single_number([-1, -1, -2]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
4 7 -2
```
<details><summary>Code tham khảo</summary>

```python
def single_number(nums):
    r = 0
    for x in nums: r ^= x
    return r
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q260 · mức 3 · write_code · ~12 phút]** Viết `max_unique_len(arr)`: arr là list chuỗi chữ thường; chọn một tập con (giữ thứ tự) sao cho ghép các chuỗi được chọn không có ký tự trùng. Trả độ dài lớn nhất. Gợi ý duy nhất: mỗi chuỗi có thể biểu diễn bằng một số nguyên (bitmask).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(max_unique_len(["un", "iq", "ue"]), max_unique_len(["cha", "r", "act", "ers"]), max_unique_len(["aa", "bb"]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
4 6 0
```
<details><summary>Code tham khảo</summary>

```python
def max_unique_len(arr):
    masks = []
    for w in arr:
        m = 0
        for ch in w:
            b = 1 << (ord(ch) - 97)
            if m & b:
                m = -1
                break
            m |= b
        if m != -1:
            masks.append((m, len(w)))
    best = 0
    def go(i, used, total):
        nonlocal best
        best = max(best, total)
        for j in range(i, len(masks)):
            m, ln = masks[j]
            if used & m == 0:
                go(j + 1, used | m, total + ln)
    go(0, 0, 0)
    return best
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (12 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

#### Cụm C9: Coding thực tế, debug, AI-enabled, công cụ

##### `py.errors_modules.files_pathlib` — File, pathlib và serialization (JSON, CSV)

**[Q141 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
import io
f = io.StringIO("a 1\nb 2\n")
rows = [ln.split() for ln in f.read().splitlines()]
print(rows, sum(int(v) for _, v in rows))
```
Đáp án (output đã chạy kiểm chứng):

```
[['a', '1'], ['b', '2']] 3
```
Giải thích: StringIO giả lập file; đọc nội dung rồi tách từng dòng.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q142 · mức 2 · concept · ~3 phút]** Vì sao nên mở file bằng `with open(...) as f`? Cách đọc từng dòng cho file rất lớn?

Đáp án / rubric: with tự đóng file kể cả khi có lỗi. Với file lớn: `for line in f:` (đọc từng dòng, không nạp cả file vào bộ nhớ).

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

##### `dsa.practical.file_log_parsing` — Parse file/log, biến đổi dữ liệu và tra cứu (file and log parsing)

**[Q143 · mức 2 · write_code · ~10 phút]** Cho log dạng "GET /a 200". Viết `top_paths(lines, n)` trả n đường dẫn có nhiều request nhất dạng [(path, count)], hoà thì theo thứ tự chữ cái; bỏ qua dòng sai định dạng.

Driver (chạy sau khi bạn viết hàm/class):

```python
log = ["GET /a 200", "GET /b 404", "bad line", "POST /a 201", "GET /c 200", "GET /b 200"]
print(top_paths(log, 2), top_paths([], 3))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[('/a', 2), ('/b', 2)] []
```
<details><summary>Code tham khảo</summary>

```python
def top_paths(lines, n):
    from collections import Counter
    c = Counter()
    for ln in lines:
        p = ln.split()
        if len(p) == 3 and p[2].isdigit(): c[p[1]] += 1
    return sorted(c.items(), key=lambda x: (-x[1], x[0]))[:n]
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[Q144 · mức 3 · write_code · ~10 phút]** Viết `top_n_words(text, n)`: đếm từ trong văn bản (không phân biệt hoa thường, bỏ dấu câu . , ! ?), trả n từ phổ biến nhất, hoà thì chữ cái nhỏ trước.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(top_n_words("The cat. the DOG! The end, cat?", 2))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[('the', 3), ('cat', 2)]
```
<details><summary>Code tham khảo</summary>

```python
def top_n_words(text, n):
    from collections import Counter
    import re
    c = Counter(re.findall(r"[a-z0-9']+", text.lower()))
    return sorted(c.items(), key=lambda x: (-x[1], x[0]))[:n]
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

##### `dsa.practical.practical_format` — Định dạng vòng practical và bài nhiều phần (practical round format)

**[Q160 · mức 1 · concept · ~3 phút]** Đề kiểu "thiết kế class có nhiều level" (ví dụ ngân hàng, in-memory DB): 5 việc đầu tiên bạn làm trước khi code là gì?

Đáp án / rubric: Đọc kỹ input/output format; liệt kê các thao tác; hỏi biên (id trùng, số âm, thiếu khoá); chọn cấu trúc dữ liệu chính (dict); viết khung class + test ví dụ của đề; code level 1 xong chạy thử rồi mới sang level sau (không viết lại).

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q161 · mức 2 · concept · ~3 phút]** Level 2 yêu cầu thêm "top N theo tổng chi tiêu". Làm sao thêm mà không phá level 1? Nêu 2 cách và trade-off.

Đáp án / rubric: Thêm trường tổng chi tiêu vào cấu trúc hiện có rồi sắp khi gọi (đơn giản, O(n log n)/lần) hoặc giữ heap/dict phụ (nhanh hơn nhưng phức tạp, dễ sai khi cập nhật). Nêu rõ mình bắt đầu bằng cách đơn giản rồi tối ưu nếu cần.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

##### `dsa.practical.simulation_state_machines` — Mô phỏng và state machine (simulations and state machines) (hot)

**[Q162 · mức 1 · concept · ~3 phút]** Mô phỏng một trò chơi theo lượt: bạn tách code thành những phần nào để dễ test và dễ sửa luật?

Đáp án / rubric: Trạng thái (state) tách khỏi luật (rule functions) và vòng lặp điều khiển; hàm thuần cho "bước tiếp theo"; seed ngẫu nhiên cố định để test lặp lại.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q163 · mức 2 · write_code · ~10 phút]** Viết `life_step(board)` một bước Game of Life (ô sống có 2-3 hàng xóm sống thì sống tiếp, ô chết có đúng 3 thì sống), trả bảng mới.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(life_step([[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]
```
<details><summary>Code tham khảo</summary>

```python
def life_step(b):
    R, Cc = len(b), len(b[0])
    def cnt(i, j):
        return sum(b[x][y] for x in range(max(0, i - 1), min(R, i + 2)) for y in range(max(0, j - 1), min(Cc, j + 2))) - b[i][j]
    return [[1 if (b[i][j] and cnt(i, j) in (2, 3)) or (not b[i][j] and cnt(i, j) == 3) else 0 for j in range(Cc)] for i in range(R)]
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

##### `dsa.practical.refactor_debug_review` — Refactor, debug và code review (refactoring, debugging and review rounds) (hot)

**[Q165 · mức 1 · concept · ~3 phút]** Quy trình gỡ lỗi 5 bước khi test fail: bạn làm gì theo thứ tự?

Đáp án / rubric: 1) tái hiện lỗi với input nhỏ nhất; 2) đọc thông báo/traceback; 3) đặt giả thuyết về nguyên nhân; 4) kiểm chứng bằng print/debugger/test nhỏ; 5) sửa đúng nguyên nhân + thêm test chống lặp lại; không sửa mò nhiều chỗ một lúc.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q164 · mức 2 · read_code · ~3 phút]** Đoạn code này có bug. (a) In ra gì? (b) Bug ở đâu và sửa thế nào?

```python
def bs(a, t):
    lo, hi = 0, len(a) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] == t: return mid
        if a[mid] < t: lo = mid + 1
        else: hi = mid - 1
    return -1
print(bs([1, 3, 5], 5), bs([7], 7), bs([1, 3, 5], 1))
```
Đáp án (output đã chạy kiểm chứng):

```
-1 -1 -1
```
Giải thích: Đáp án đúng phải là 2 0 0. Lỗi: `while lo < hi` bỏ sót trường hợp lo == hi; sửa thành `lo <= hi`.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

##### `py.errors_modules.exceptions` — Exception và xử lý lỗi (exceptions)

**[Q167 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
def f():
    try:
        return "try"
    finally:
        print("finally")
print(f())
```
Đáp án (output đã chạy kiểm chứng):

```
finally
try
```
Giải thích: finally luôn chạy trước khi hàm thật sự trả về.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q168 · mức 2 · concept · ~3 phút]** Viết class lỗi riêng `InsufficientFunds` và nói khi nào nên raise exception thay vì trả mã lỗi.

Đáp án / rubric: class InsufficientFunds(Exception): pass. Raise khi tình huống bất thường mà người gọi phải xử lý hoặc không thể tiếp tục; không dùng exception cho luồng bình thường.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

##### `py.typing_testing.pytest_testing` — Unit test với pytest, mock và thiết kế test

**[Q171 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
def add(a, b): return a + b
tests = [(1, 2, 3), (0, 0, 0), (-1, 1, 1)]
fails = [t for t in tests if add(t[0], t[1]) != t[2]]
print(len(fails), fails)
```
Đáp án (output đã chạy kiểm chứng):

```
1 [(-1, 1, 1)]
```
Giải thích: -1 + 1 = 0 khác 1 nên test thứ 3 fail (test sai hoặc code sai? hãy xem lại kỳ vọng).

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q172 · mức 2 · concept · ~3 phút]** Viết 1 test pytest cho hàm `is_even(n)` gồm ít nhất 3 trường hợp (thường, biên, âm) và nói cách chạy.

Đáp án / rubric: def test_is_even(): assert is_even(2); assert not is_even(3); assert is_even(0); assert is_even(-4). Chạy: `pytest -q` trong thư mục dự án.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

**[Q259 · mức 2 · read_code · ~5 phút]** (a) Đoạn code in ra gì? (b) Nếu chạy bằng pytest, test_avg báo fail kiểu gì (AssertionError hay lỗi khác) và ở dòng nào? (c) Sửa `avg` để test_avg qua. (d) Viết lệnh chạy riêng đúng một test `test_avg` trong file test_x.py.

```python
def avg(xs):
    return sum(xs) / len(xs)

def test_avg():
    assert avg([2, 4]) == 3
    assert avg([]) == 0

try:
    test_avg()
except AssertionError:
    print("assert")
except ZeroDivisionError as e:
    print("zero:", e)
```
Đáp án (output đã chạy kiểm chứng):

```
zero: division by zero
```
Giải thích: avg([]) chia cho len = 0 nên ZeroDivisionError (không phải AssertionError), ở dòng assert thứ hai. Sửa: `return sum(xs) / len(xs) if xs else 0`. Lệnh: `pytest test_x.py::test_avg`.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

##### `dsa.practical.ai_assisted_coding` — Vòng code có hỗ trợ AI (AI-assisted coding round) (hot)

**[Q173 · mức 1 · concept · ~3 phút]** Vòng AI-enabled 60 phút: bạn mở đầu thế nào (3 việc đầu tiên) trước khi nhờ AI?

Đáp án / rubric: 1) đọc đề và code/test sẵn có, chạy test xem cái nào fail; 2) tự nêu giả thuyết bug và kế hoạch; 3) chia nhỏ yêu cầu rồi mới prompt AI từng bước, nêu ràng buộc. Không dán nguyên đề.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q174 · mức 2 · read_code · ~3 phút]** Hàm do AI sinh. (a) Chạy ra gì? (b) Có đúng yêu cầu không? Vì sao? Sửa.

```python
# AI viết hàm: "trả phần tử xuất hiện nhiều nhất"
def most_common(xs):
    d = {}
    for x in xs: d[x] = d.get(x, 0) + 1
    return max(d)
print(most_common([1, 1, 2, 3]), most_common(["a", "b", "b"]))
```
Đáp án (output đã chạy kiểm chứng):

```
3 b
```
Giải thích: `max(d)` lấy khoá lớn nhất chứ không phải khoá có tần suất lớn nhất: ví dụ đầu in 3 thay vì 1. Sửa: `max(d, key=d.get)`.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

#### Cụm C10: Behavioral và dùng AI

##### `bh.method.self_intro` — Tự giới thiệu 2 phút (self-introduction)

**[Q088 · mức 1 · behavioral · ~5 phút]** Tự giới thiệu trong 60 giây: bạn là ai, học gì, làm gì nổi bật, vì sao ứng tuyển.

Đáp án / rubric: Đạt (điểm 2): 4 phần (hiện tại - quá khứ liên quan - điểm nổi bật có bằng chứng - lý do ứng tuyển), ≤ 75 giây, không kể lể dài. Điểm 3: có 1 con số/kết quả cụ thể và nối được với vai trò.

Chấm: Đạt (điểm 2): 4 phần (hiện tại - quá khứ liên quan - điểm nổi bật có bằng chứng - lý do ứng tuyển), ≤ 75 giây, không kể lể dài. Điểm 3: có 1 con số/kết quả cụ thể và nối được với vai trò. (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

**[Q089 · mức 2 · behavioral · ~5 phút]** Bạn có "30 giây" thay vì 60 giây: phiên bản rút gọn là gì? Và câu mở đầu để interviewer hỏi tiếp về dự án nào?

Đáp án / rubric: Điểm 2: giữ 3 ý chính, có "mồi" (hook) để interviewer hỏi tiếp. Điểm 3: mồi dẫn tới story bạn đã chuẩn bị kỹ.

Chấm: Điểm 2: giữ 3 ý chính, có "mồi" (hook) để interviewer hỏi tiếp. Điểm 3: mồi dẫn tới story bạn đã chuẩn bị kỹ. (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

##### `bh.method.star_carl` — Cấu trúc trả lời STAR / CARL (answer structure)

**[Q090 · mức 1 · behavioral · ~5 phút]** STAR là viết tắt của gì? Phần nào hay bị bỏ quên nhất?

Đáp án / rubric: Situation, Task, Action, Result (CARL: Context, Action, Result, Learning). Hay bỏ quên Result (số liệu) và Learning; hay nói "chúng em" thay vì "em".

Chấm: Situation, Task, Action, Result (CARL: Context, Action, Result, Learning). Hay bỏ quên Result (số liệu) và Learning; hay nói "chúng em" thay vì "em". (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

**[Q091 · mức 2 · behavioral · ~5 phút]** Biến một câu chuyện lộn xộn sau thành STAR 4 câu: "Nhóm em làm đồ án, có bạn không làm, em phải làm hết, cuối cùng cũng xong."

Đáp án / rubric: Điểm 2: đủ 4 phần, hành động của "em" cụ thể (họp nhóm, chia việc, hỗ trợ...). Điểm 3: kết quả có số/đối chiếu trước-sau + bài học.

Chấm: Điểm 2: đủ 4 phần, hành động của "em" cụ thể (họp nhóm, chia việc, hỗ trợ...). Điểm 3: kết quả có số/đối chiếu trước-sau + bài học. (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

##### `bh.stories.conflict_teamwork` — Xung đột và làm việc nhóm (conflict & teamwork) (hot)

**[Q110 · mức 1 · behavioral · ~5 phút]** Kể 1 lần làm nhóm có bất đồng. Nêu rõ: bất đồng về gì, bạn làm gì, kết quả. Dưới 2 phút.

Đáp án / rubric: Điểm 1: kể được nhưng thiếu hành động của bản thân hoặc kết quả. Điểm 2: đủ STAR, hành động của "em" cụ thể, giữ thái độ tôn trọng. Điểm 3: kết quả đo được, có học được gì, và nếu làm lại sẽ khác thế nào.

Chấm: Điểm 1: kể được nhưng thiếu hành động của bản thân hoặc kết quả. Điểm 2: đủ STAR, hành động của "em" cụ thể, giữ thái độ tôn trọng. Điểm 3: kết quả đo được, có học được gì, và nếu làm lại sẽ khác thế nào. (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

**[Q111 · mức 2 · behavioral · ~5 phút]** Follow-up của interviewer: "Nếu người kia vẫn không đồng ý thì sao?" "Lần này bạn có phải là người sai không?"

Đáp án / rubric: Điểm 2: trả lời trung thực, không đổ lỗi. Điểm 3: chỉ ra dữ liệu/tiêu chí chung được dùng để quyết định, thừa nhận phần sai của mình nếu có.

Chấm: Điểm 2: trả lời trung thực, không đổ lỗi. Điểm 3: chỉ ra dữ liệu/tiêu chí chung được dùng để quyết định, thừa nhận phần sai của mình nếu có. (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

##### `bh.stories.failure_feedback` — Thất bại, feedback và bài học (failure & feedback) (hot)

**[Q112 · mức 1 · behavioral · ~5 phút]** Kể một lần bạn mắc lỗi/thất bại, bạn xử lý và học gì? (đừng chọn "điểm yếu là cầu toàn")

Đáp án / rubric: Điểm 2: lỗi thật, nhận trách nhiệm, hành động sửa, bài học. Điểm 3: bài học đã áp dụng lần sau, có bằng chứng.

Chấm: Điểm 2: lỗi thật, nhận trách nhiệm, hành động sửa, bài học. Điểm 3: bài học đã áp dụng lần sau, có bằng chứng. (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

**[Q113 · mức 2 · behavioral · ~5 phút]** Kể một lần nhận phản hồi khó nghe và bạn đã làm gì sau đó.

Đáp án / rubric: Điểm 2: không phòng thủ, nêu phản hồi cụ thể + việc đã thay đổi. Điểm 3: kết quả đo được sau thay đổi.

Chấm: Điểm 2: không phòng thủ, nêu phản hồi cụ thể + việc đã thay đổi. Điểm 3: kết quả đo được sau thay đổi. (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

##### `bh.stories.ownership_leadership` — Ownership và lãnh đạo (ownership & leadership) (hot)

**[Q114 · mức 1 · behavioral · ~5 phút]** Kể một lần bạn chủ động nhận việc không ai giao hoặc dẫn dắt khi không có chức danh.

Đáp án / rubric: Điểm 2: hành động chủ động rõ, ảnh hưởng tới người khác. Điểm 3: kết quả đo được, người khác tiếp tục làm theo.

Chấm: Điểm 2: hành động chủ động rõ, ảnh hưởng tới người khác. Điểm 3: kết quả đo được, người khác tiếp tục làm theo. (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

**[Q115 · mức 2 · behavioral · ~5 phút]** "Bạn làm gì khi thấy cả nhóm đi sai hướng nhưng bạn không phải leader?"

Đáp án / rubric: Điểm 2: nêu quan điểm bằng dữ liệu, hỏi để hiểu, đề xuất thử nhỏ. Điểm 3: biết tôn trọng quyết định cuối và hỗ trợ.

Chấm: Điểm 2: nêu quan điểm bằng dữ liệu, hỏi để hiểu, đề xuất thử nhỏ. Điểm 3: biết tôn trọng quyết định cuối và hỗ trợ. (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

##### `bh.stories.prioritization_ambiguity` — Ưu tiên, deadline và yêu cầu mơ hồ (prioritization & ambiguity)

**[Q116 · mức 1 · behavioral · ~5 phút]** Deadline đồ án bị dời sớm 3 ngày, còn nhiều việc. Bạn làm gì? (hoặc kể chuyện thật)

Đáp án / rubric: Điểm 2: liệt kê việc, ưu tiên theo giá trị/rủi ro, thông báo sớm, cắt phạm vi. Điểm 3: ví dụ thật có kết quả và có hỏi lại yêu cầu.

Chấm: Điểm 2: liệt kê việc, ưu tiên theo giá trị/rủi ro, thông báo sớm, cắt phạm vi. Điểm 3: ví dụ thật có kết quả và có hỏi lại yêu cầu. (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

**[Q117 · mức 2 · behavioral · ~5 phút]** Yêu cầu của đề bài mơ hồ và không có người hỏi được. Bạn làm gì?

Đáp án / rubric: Điểm 2: nêu giả định rõ ràng, làm bản nhỏ nhất chạy được, kiểm tra lại. Điểm 3: biết lấy ví dụ biên để chốt giả định.

Chấm: Điểm 2: nêu giả định rõ ràng, làm bản nhỏ nhất chạy được, kiểm tra lại. Điểm 3: biết lấy ví dụ biên để chốt giả định. (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

##### `bh.stories.project_deep_dive` — Deep dive dự án kỹ thuật và bảo vệ quyết định (project deep dive) (hot)

**[Q145 · mức 1 · behavioral · ~5 phút]** Giới thiệu dự án bạn tự hào nhất trong 2 phút: vấn đề, bạn làm phần nào, 1 quyết định kỹ thuật, kết quả.

Đáp án / rubric: Điểm 2: rõ vấn đề, vai trò cá nhân, 1 lựa chọn kỹ thuật có lý do. Điểm 3: số liệu, trade-off đã cân nhắc, điều làm lại sẽ khác.

Chấm: Điểm 2: rõ vấn đề, vai trò cá nhân, 1 lựa chọn kỹ thuật có lý do. Điểm 3: số liệu, trade-off đã cân nhắc, điều làm lại sẽ khác. (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

**[Q146 · mức 2 · behavioral · ~5 phút]** Đào sâu: "Phần khó nhất là gì? Vì sao chọn công nghệ X mà không phải Y? Nếu có thêm 1 tuần bạn làm gì?"

Đáp án / rubric: Điểm 2: trả lời cụ thể, không vòng vo. Điểm 3: nêu trade-off, giới hạn, hướng cải tiến hợp lý.

Chấm: Điểm 2: trả lời cụ thể, không vòng vo. Điểm 3: nêu trade-off, giới hạn, hướng cải tiến hợp lý. (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

##### `bh.motivation.why_company` — Vì sao công ty này và câu chuyện sự nghiệp (motivation & career story)

**[Q175 · mức 1 · behavioral · ~5 phút]** Vì sao bạn muốn làm software engineer ở Meta? (90 giây)

Đáp án / rubric: Điểm 2: 2-3 lý do cụ thể (sản phẩm/kỹ thuật/quy mô/văn hoá) gắn với trải nghiệm của bạn. Điểm 3: dẫn chứng (dự án, bài viết engineering) và điều bạn muốn đóng góp; không sáo rỗng.

Chấm: Điểm 2: 2-3 lý do cụ thể (sản phẩm/kỹ thuật/quy mô/văn hoá) gắn với trải nghiệm của bạn. Điểm 3: dẫn chứng (dự án, bài viết engineering) và điều bạn muốn đóng góp; không sáo rỗng. (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

**[Q176 · mức 2 · behavioral · ~5 phút]** Follow-up: "Điều gì ở Meta bạn thấy chưa chắc, hoặc muốn hỏi thêm?"

Đáp án / rubric: Điểm 2: câu hỏi chân thành về công việc hằng ngày/mentor. Điểm 3: câu hỏi cho thấy bạn đã tìm hiểu (ví dụ về team, quy trình review).

Chấm: Điểm 2: câu hỏi chân thành về công việc hằng ngày/mentor. Điểm 3: câu hỏi cho thấy bạn đã tìm hiểu (ví dụ về team, quy trình review). (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

##### `bh.ai_fluency.ai_workflow` — Quy trình kỹ thuật có AI hỗ trợ (AI-assisted workflow) (hot)

**[Q177 · mức 1 · behavioral · ~5 phút]** Bạn dùng AI khi học lập trình như thế nào? Việc nào giao cho AI, việc nào tự làm?

Đáp án / rubric: Điểm 2: mô tả quy trình cụ thể (giải thích khái niệm, gợi ý test; tự viết lời giải trước) và cách kiểm chứng. Điểm 3: có nguyên tắc rõ (không chép, tự giải thích được từng dòng) và ví dụ kết quả.

Chấm: Điểm 2: mô tả quy trình cụ thể (giải thích khái niệm, gợi ý test; tự viết lời giải trước) và cách kiểm chứng. Điểm 3: có nguyên tắc rõ (không chép, tự giải thích được từng dòng) và ví dụ kết quả. (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

**[Q178 · mức 2 · behavioral · ~5 phút]** Nếu được dùng AI trong phỏng vấn, bạn dùng thế nào? Nêu 3 hành động cụ thể.

Đáp án / rubric: Điểm 2: đọc code/chạy test trước, prompt từng bước, đọc lại đề xuất. Điểm 3: nói to lý do chấp nhận/bác bỏ, tự viết test và đo hiệu năng.

Chấm: Điểm 2: đọc code/chạy test trước, prompt từng bước, đọc lại đề xuất. Điểm 3: nói to lý do chấp nhận/bác bỏ, tự viết test và đo hiệu năng. (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

##### `bh.ai_fluency.verify_ai_output` — Kiểm chứng và sửa lỗi đầu ra của AI (verifying AI output) (hot)

**[Q179 · mức 1 · behavioral · ~5 phút]** Kể một lần AI trả lời sai (hoặc code AI có bug) và bạn phát hiện thế nào.

Đáp án / rubric: Điểm 2: ví dụ thật, cách phát hiện (chạy test, đối chiếu tài liệu), cách sửa. Điểm 3: rút ra quy trình kiểm chứng áp dụng về sau.

Chấm: Điểm 2: ví dụ thật, cách phát hiện (chạy test, đối chiếu tài liệu), cách sửa. Điểm 3: rút ra quy trình kiểm chứng áp dụng về sau. (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

**[Q180 · mức 2 · behavioral · ~5 phút]** Liệt kê 4 dấu hiệu một đoạn code do AI viết đáng ngờ, và cách kiểm tra từng dấu hiệu.

Đáp án / rubric: Ví dụ: API không tồn tại (tra tài liệu); thiếu xử lý biên (thử input rỗng/lớn); độ phức tạp không tối ưu (đo/tính); logic đúng với ví dụ nhưng sai tổng quát (viết thêm test).

Chấm: Ví dụ: API không tồn tại (tra tài liệu); thiếu xử lý biên (thử input rỗng/lớn); độ phức tạp không tối ưu (đo/tính); logic đúng với ví dụ nhưng sai tổng quát (viết thêm test). (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

##### `bh.ai_fluency.ai_safety_values` — An toàn AI và giá trị AI có trách nhiệm (AI safety values)

**[Q181 · mức 1 · behavioral · ~5 phút]** Bạn chịu trách nhiệm thế nào với code do AI viết ra trong nhóm? Khi nào bạn bác bỏ gợi ý của AI?

Đáp án / rubric: Điểm 2: người ký tên là người chịu trách nhiệm; bác bỏ khi không hiểu, không test được, hoặc vi phạm bảo mật/giấy phép/dữ liệu riêng tư. Điểm 3: có ví dụ cụ thể và quy tắc nhóm.

Chấm: Điểm 2: người ký tên là người chịu trách nhiệm; bác bỏ khi không hiểu, không test được, hoặc vi phạm bảo mật/giấy phép/dữ liệu riêng tư. Điểm 3: có ví dụ cụ thể và quy tắc nhóm. (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

**[Q182 · mức 2 · behavioral · ~5 phút]** Tình huống: AI đề xuất dán dữ liệu khách hàng thật vào công cụ bên ngoài để debug nhanh. Bạn làm gì?

Đáp án / rubric: Điểm 2: không làm; ẩn danh/giả lập dữ liệu; hỏi quy định công ty. Điểm 3: đề xuất cách tái hiện lỗi không dùng dữ liệu thật và báo lại cho nhóm.

Chấm: Điểm 2: không làm; ẩn danh/giả lập dữ liệu; hỏi quy định công ty. Điểm 3: đề xuất cách tái hiện lỗi không dùng dữ liệu thật và báo lại cho nhóm. (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

#### Cụm C11: Gói AI/ML (chỉ khi theo track AI)

##### `ml.fundamentals.ml_overview` — Các dạng học máy và quy trình ML (ML workflow)

**[Q225 · mức 1 · concept · ~3 phút]** Phân biệt supervised, unsupervised, reinforcement learning bằng 1 ví dụ mỗi loại. Vì sao chia train/validation/test?

Đáp án / rubric: Supervised: có nhãn (phân loại thư rác). Unsupervised: không nhãn (gom nhóm khách hàng). RL: học qua thưởng/phạt (chơi game). Train học tham số; validation chọn mô hình/siêu tham số; test chỉ dùng một lần cuối để ước lượng hiệu năng thật.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q226 · mức 2 · concept · ~3 phút]** Data leakage là gì? Cho 2 ví dụ.

Đáp án / rubric: Thông tin từ ngoài tập train lọt vào lúc huấn luyện làm điểm số ảo. Ví dụ: chuẩn hoá (fit scaler) trên toàn bộ dữ liệu trước khi chia; đặc trưng chứa thông tin của nhãn (ví dụ "đã hoàn tiền" khi dự đoán gian lận).

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

##### `ml.classical.decision_trees` — Cây quyết định (decision trees)

**[Q239 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
labels = [0, 0, 1, 1, 1]
p = labels.count(1) / len(labels)
print(round(1 - (p ** 2 + (1 - p) ** 2), 2))
```
Đáp án (output đã chạy kiểm chứng):

```
0.48
```
Giải thích: Gini = 1 - (0.6^2 + 0.4^2) = 0.48.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

##### `ml.math.linear_algebra_basics` — Vector, ma trận và phép nhân ma trận (linear algebra)

**[Q229 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
import numpy as np
A = np.array([[1, 2], [3, 4]]); x = np.array([1, 1])
print((A @ x).tolist(), A.T.tolist(), int((A * A).sum()))
```
Đáp án (output đã chạy kiểm chứng):

```
[3, 7] [[1, 3], [2, 4]] 30
```
Giải thích: A@x là nhân ma trận-vector; A*A là nhân từng phần tử.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

##### `ml.math.random_variables_expectation` — Biến ngẫu nhiên, kỳ vọng và phương sai (random variables)

**[Q230 · mức 1 · concept · ~3 phút]** Kỳ vọng của một con xúc xắc công bằng? Công thức Var(X)? Với X, Y độc lập thì E[XY] và Var(X+Y)?

Đáp án / rubric: E = 3.5. Var(X) = E[X^2] - (E[X])^2 (xúc xắc: 35/12). Độc lập: E[XY] = E[X]E[Y]; Var(X+Y) = Var X + Var Y.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

##### `ml.classical.dimensionality_reduction` — Giảm chiều: PCA, t-SNE, UMAP (dimensionality reduction)

**[Q242 · mức 1 · concept · ~3 phút]** PCA làm gì? Chọn số thành phần thế nào? Vì sao cần chuẩn hoá dữ liệu trước?

Đáp án / rubric: Chiếu dữ liệu lên các hướng có phương sai lớn nhất (vector riêng của ma trận hiệp phương sai). Chọn số thành phần để giữ ~90-95% phương sai (explained variance). Chuẩn hoá vì PCA nhạy với thang đo.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

##### `ml.fundamentals.loss_functions` — Hàm mất mát (loss functions)

**[Q227 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
import numpy as np
y = np.array([1., 2., 3.]); p = np.array([1., 2., 5.])
print(((y - p) ** 2).mean(), np.abs(y - p).mean())
```
Đáp án (output đã chạy kiểm chứng):

```
1.3333333333333333 0.6666666666666666
```
Giải thích: MSE = (0+0+4)/3; MAE = 2/3.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q228 · mức 2 · concept · ~3 phút]** Vì sao phân loại dùng cross-entropy thay vì MSE? Loss và metric khác nhau thế nào?

Đáp án / rubric: Cross-entropy phạt rất nặng dự đoán tự tin nhưng sai và cho gradient tốt với sigmoid/softmax; MSE gradient nhỏ khi bão hoà. Loss là hàm được tối ưu (cần khả vi); metric là thước đo cuối (accuracy, F1) có thể không khả vi.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

##### `ml.math.derivatives_gradients` — Đạo hàm, gradient và quy tắc chuỗi (derivatives)

**[Q231 · mức 1 · concept · ~3 phút]** Đạo hàm của f(x) = x^2 + 3x tại x = 2? Gradient của f(x, y) = x^2 + y^2 tại (1, 2)?

Đáp án / rubric: f'(x) = 2x + 3 = 7. Gradient = (2x, 2y) = (2, 4).

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q232 · mức 2 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
f = lambda x: x ** 3
h = 1e-5
print(round((f(2 + h) - f(2 - h)) / (2 * h), 3))
```
Đáp án (output đã chạy kiểm chứng):

```
12.0
```
Giải thích: Đạo hàm số bằng sai phân trung tâm; f'(2) = 3*2^2 = 12.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

##### `ml.math.gradient_descent` — Gradient descent và tối ưu cơ bản (gradient descent)

**[Q233 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
x = 5.0
for _ in range(3):
    x -= 0.1 * 2 * x
print(round(x, 4))
```
Đáp án (output đã chạy kiểm chứng):

```
2.56
```
Giải thích: Tối thiểu hoá f=x^2 (gradient 2x) với learning rate 0.1: 5 -> 4 -> 3.2 -> 2.56.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q234 · mức 2 · concept · ~3 phút]** Learning rate quá lớn hoặc quá nhỏ gây gì? Phân biệt batch, mini-batch, stochastic gradient descent.

Đáp án / rubric: Quá lớn: dao động/phân kỳ; quá nhỏ: hội tụ chậm. Batch dùng cả dữ liệu mỗi bước; SGD 1 mẫu; mini-batch một lô nhỏ (cân bằng nhiễu và tốc độ).

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

##### `ml.classical.linear_regression` — Hồi quy tuyến tính (linear regression)

**[Q236 · mức 1 · concept · ~3 phút]** Viết công thức dự đoán và loss MSE của hồi quy tuyến tính, và nghiệm đóng. Khi nào nghiệm đóng không dùng được?

Đáp án / rubric: ŷ = Xw (+b); MSE = (1/n)||Xw - y||^2; w = (X^T X)^-1 X^T y. Không dùng khi X^T X không khả nghịch (đa cộng tuyến) hoặc n, d quá lớn -> dùng gradient descent/regularization.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q235 · mức 2 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
import numpy as np
X = np.array([[1, 1], [1, 2], [1, 3]]); y = np.array([2, 3, 4])
w = np.linalg.solve(X.T @ X, X.T @ y)
print(np.round(w, 3).tolist())
```
Đáp án (output đã chạy kiểm chứng):

```
[1.0, 1.0]
```
Giải thích: Nghiệm normal equation w = (X^T X)^-1 X^T y; cột đầu toàn 1 là hệ số chặn (bias). Dữ liệu y = 1 + x.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

##### `ml.classical.logistic_regression` — Hồi quy logistic (logistic regression)

**[Q237 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
import numpy as np
print(round(1 / (1 + np.exp(0)), 2), round(1 / (1 + np.exp(-2)), 3))
```
Đáp án (output đã chạy kiểm chứng):

```
0.5 0.881
```
Giải thích: sigmoid(0)=0.5; sigmoid(2)≈0.881.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q238 · mức 2 · concept · ~3 phút]** Logistic regression ra gì? Đổi ngưỡng 0.5 thành 0.3 ảnh hưởng precision/recall thế nào?

Đáp án / rubric: Ra xác suất P(y=1|x)=sigmoid(w·x+b). Hạ ngưỡng: recall tăng (bắt nhiều hơn), precision thường giảm (nhầm nhiều hơn).

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

##### `ml.classical.knn_nb_svm` — k-NN, Naive Bayes và SVM (k-NN, Naive Bayes, SVM)

**[Q240 · mức 2 · write_code · ~10 phút]** Viết `knn_predict(Xtr, ytr, x, k)` (numpy): nhãn xuất hiện nhiều nhất trong k điểm gần x nhất (khoảng cách Euclid; hoà thì nhãn nhỏ hơn).

Driver (chạy sau khi bạn viết hàm/class):

```python
Xtr = [[0, 0], [0, 1], [5, 5], [6, 5], [5, 6]]; ytr = [0, 0, 1, 1, 1]
print(knn_predict(Xtr, ytr, [1, 1], 3), knn_predict(Xtr, ytr, [5, 4], 3))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
0 1
```
<details><summary>Code tham khảo</summary>

```python
import numpy as np
def knn_predict(Xtr, ytr, x, k):
    d = np.linalg.norm(np.asarray(Xtr, float) - np.asarray(x, float), axis=1)
    idx = np.argsort(d, kind="stable")[:k]
    labels, counts = np.unique(np.asarray(ytr)[idx], return_counts=True)
    return int(labels[np.argmax(counts)])
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

##### `ml.classical.unsupervised` — Phân cụm và giảm chiều (unsupervised learning)

**[Q241 · mức 2 · write_code · ~10 phút]** Viết `assign(points, centroids)` (numpy) trả nhãn cụm gần nhất cho mỗi điểm, và `update(points, labels, k)` trả tâm mới (trung bình mỗi cụm).

Driver (chạy sau khi bạn viết hàm/class):

```python
pts = [[1], [2], [10], [11]]
lab = assign(pts, [[1], [10]])
print(lab, update(pts, lab, 2))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[0, 0, 1, 1] [[1.5], [10.5]]
```
<details><summary>Code tham khảo</summary>

```python
import numpy as np
def assign(points, centroids):
    P = np.asarray(points, float); C = np.asarray(centroids, float)
    return np.argmin(((P[:, None, :] - C[None, :, :]) ** 2).sum(-1), axis=1).tolist()
def update(points, labels, k):
    P = np.asarray(points, float); L = np.asarray(labels)
    return [P[L == j].mean(axis=0).tolist() for j in range(k)]
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

##### `py.ecosystem.numpy_basics` — NumPy và vector hóa (vectorization)

**[Q243 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
import numpy as np
a = np.arange(6).reshape(2, 3)
print(a.shape, a.sum(axis=0).tolist(), (a + np.array([10, 20, 30])).tolist(), a[:, 1].tolist())
```
Đáp án (output đã chạy kiểm chứng):

```
(2, 3) [3, 5, 7] [[10, 21, 32], [13, 24, 35]] [1, 4]
```
Giải thích: sum(axis=0) cộng theo cột; broadcasting cộng vector vào từng hàng.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

##### `ml.coding.kmeans_knn_trees` — Cài đặt k-means, k-NN, cây quyết định (algorithms from scratch)

**[Q244 · mức 1 · concept · ~3 phút]** Mô tả thuật toán k-means (Lloyd) 4 bước và khi nào dừng. Độ phức tạp mỗi vòng?

Đáp án / rubric: Khởi tạo k tâm; gán mỗi điểm vào tâm gần nhất; cập nhật tâm = trung bình cụm; lặp tới khi nhãn không đổi hoặc đủ vòng. Mỗi vòng O(n*k*d).

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

##### `ml.coding.linear_logistic_scratch` — Cài đặt hồi quy tuyến tính/logistic từ đầu (models from scratch)

**[Q245 · mức 2 · write_code · ~10 phút]** Viết `fit_line(x, y, lr, steps)` huấn luyện y = w*x + b bằng gradient descent (MSE), trả (w, b) làm tròn 2 chữ số.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(fit_line([0, 1, 2, 3], [1, 3, 5, 7], 0.05, 5000))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
(2.0, 1.0)
```
<details><summary>Code tham khảo</summary>

```python
import numpy as np
def fit_line(x, y, lr, steps):
    x = np.asarray(x, float); y = np.asarray(y, float); w = b = 0.0
    for _ in range(steps):
        e = w * x + b - y
        w -= lr * 2 * (e * x).mean(); b -= lr * 2 * e.mean()
    return float(round(w, 2)), float(round(b, 2))
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

##### `ml.fundamentals.bias_variance_overfitting` — Bias-variance, overfitting và regularization (bias-variance)

**[Q246 · mức 1 · concept · ~3 phút]** Train error thấp, validation error cao nói lên điều gì? Nêu 3 cách khắc phục.

Đáp án / rubric: Overfitting (phương sai cao). Cách: thêm dữ liệu, regularization (L1/L2, dropout), mô hình đơn giản hơn, early stopping, augmentation.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q247 · mức 2 · concept · ~3 phút]** Cả train và validation error đều cao: vấn đề gì và làm gì? Học đường cong (learning curve) giúp phân biệt thế nào?

Đáp án / rubric: Underfitting (bias cao): mô hình quá đơn giản/đặc trưng yếu -> mô hình mạnh hơn, thêm đặc trưng, giảm regularization. Learning curve: hai đường cao và gần nhau = bias; khoảng cách lớn = variance.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

##### `ml.fundamentals.validation_tuning` — Validation, cross-validation và tuning (validation)

**[Q248 · mức 1 · concept · ~3 phút]** K-fold cross-validation chạy thế nào? Vì sao không tinh chỉnh siêu tham số trên test set? Vì sao phải fit scaler trên train only?

Đáp án / rubric: Chia k phần, lần lượt dùng 1 phần làm validation, trung bình k điểm. Tinh chỉnh trên test làm test thành validation (lạc quan quá mức). Scaler fit trên toàn bộ sẽ rò thống kê của test vào train (leakage).

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

##### `py.ecosystem.pandas_basics` — pandas cơ bản: Series, DataFrame, chọn dữ liệu

**[Q249 · mức 1 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
import pandas as pd
df = pd.DataFrame({"a": [1, 2, 3], "g": ["x", "y", "x"]})
print(df.groupby("g")["a"].sum().to_dict(), df[df.a > 1].shape, df["a"].mean())
```
Đáp án (output đã chạy kiểm chứng):

```
{'x': 4, 'y': 2} (2, 2) 2.0
```
Giải thích: groupby+sum theo nhóm; lọc a>1 còn 2 hàng, 2 cột.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

##### `ml.data_features.cleaning_missing` — Làm sạch dữ liệu, mã hóa và chuẩn hóa (data cleaning)

**[Q251 · mức 1 · concept · ~3 phút]** Nêu 3 cách xử lý dữ liệu thiếu và rủi ro của mỗi cách.

Đáp án / rubric: Xoá hàng (mất dữ liệu, lệch nếu thiếu không ngẫu nhiên); điền mean/median/mode (giảm phương sai, có thể sai lệch); thêm cột cờ "thiếu" + mô hình xử lý được. Luôn tính thống kê trên train only.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q250 · mức 2 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
import pandas as pd
s = pd.Series([1, None, 3, None, 5])
print(s.fillna(s.mean()).tolist(), int(s.isna().sum()))
```
Đáp án (output đã chạy kiểm chứng):

```
[1.0, 3.0, 3.0, 3.0, 5.0] 2
```
Giải thích: Điền giá trị thiếu bằng trung bình (3.0).

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

##### `ml.coding.pipeline_debugging` — Pipeline end-to-end và debug (pipeline debugging)

**[Q252 · mức 2 · read_code · ~3 phút]** Đoạn tiền xử lý này có lỗi gì? In ra gì, và đáng lẽ ra bao nhiêu?

```python
import numpy as np
x = np.array([1., 2., 3., 100.])
train, test = x[:3], x[3:]
mu = x.mean()
print(round((train - mu).mean(), 2))
```
Đáp án (output đã chạy kiểm chứng):

```
-24.5
```
Giải thích: Lỗi data leakage: mu tính cả test (100). Đúng: mu = train.mean() = 2.0 -> kết quả 0.0.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

##### `ml.fundamentals.classification_metrics` — Metric phân loại và calibration (classification metrics)

**[Q254 · mức 1 · concept · ~3 phút]** Khi nào accuracy gây hiểu lầm? Chọn precision hay recall cho bài phát hiện gian lận / lọc thư rác?

Đáp án / rubric: Dữ liệu mất cân bằng (99% lớp âm) -> accuracy cao dù mô hình vô dụng. Gian lận/bệnh: ưu tiên recall (không bỏ sót); lọc thư rác: ưu tiên precision (đừng chặn nhầm thư thật).

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 1; sai: tối đa điểm 0.

**[Q253 · mức 2 · write_code · ~6 phút]** Viết `prf(y_true, y_pred)` trả (precision, recall, f1) làm tròn 2 chữ số, lớp dương là 1; chia cho 0 thì trả 0.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(prf([1, 0, 1, 1, 0, 1], [1, 0, 0, 1, 1, 1]), prf([0, 0], [0, 0]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
(0.75, 0.75, 0.75) (0, 0, 0)
```
<details><summary>Code tham khảo</summary>

```python
def prf(y_true, y_pred):
    tp = sum(1 for a, b in zip(y_true, y_pred) if a == 1 and b == 1)
    fp = sum(1 for a, b in zip(y_true, y_pred) if a == 0 and b == 1)
    fn = sum(1 for a, b in zip(y_true, y_pred) if a == 1 and b == 0)
    p = tp / (tp + fp) if tp + fp else 0
    r = tp / (tp + fn) if tp + fn else 0
    f = 2 * p * r / (p + r) if p + r else 0
    return round(p, 2), round(r, 2), round(f, 2)
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

## 2. Kiểm tra cuối mỗi tuần

### 2.1 Quy tắc qua / không qua

1. **Điểm từng subtopic của tuần** lấy từ (a) quiz tuần nếu subtopic có item trong quiz; (b) nhật ký luyện: ≥ 2 nếu bạn giải được ít nhất 2 bài trong pool của subtopic mà không xem lời giải trong ≤ 25 phút/bài; (c) câu mock liên quan (rubric mục 2.3). Lấy **điểm thấp nhất** trong các nguồn có.
2. **Qua** khi mọi subtopic của tuần ≥ 2 **và** trung bình Q các câu mock tuần ≥ 2.0 **và** không câu coding nào Correctness = 0.
3. **Chưa qua** (subtopic < 2): dùng giờ buffer/đầu tuần sau theo đúng thứ tự: (i) đọc lại concept 20 phút; (ii) viết lại 3 bài đã sai từ đầu; (iii) làm lại item quiz của subtopic (bản "bổ sung" nếu có); (iv) vẫn < 2 thì ghi "nợ" và thêm 2 bài/ngày vào phần ôn; nếu subtopic là tiền đề của nội dung tuần sau, hoãn nội dung phụ thuộc 1 ngày.
4. **Mock điểm thấp**: câu có Q ≤ 1 → đặt lại các subtopic liên kết (trường `subtopics` trong content_ng) về tối đa 1 và làm lại câu đó sau 3 ngày (viết lại từ đầu) và sau 7 ngày.

### 2.2 Quiz từng tuần

Phần **bắt buộc** làm trong ≤ 30 phút (không tra cứu); phần **bổ sung** làm khi có thời gian hoặc khi một subtopic chưa qua.

#### Quiz tuần 1 (~30 phút bắt buộc)

Subtopic của tuần: `py.core.getting_started`, `py.core.variables_types`, `py.core.operators`, `py.core.conditionals`, `py.core.loops`, `py.core.strings`, `py.datastructs.list`, `py.datastructs.tuple_namedtuple`, `py.datastructs.dict`, `py.datastructs.comprehensions`, `py.datastructs.collections_module`, `py.datastructs.copying_mutability`, `py.datastructs.heapq_bisect`, `py.functions.def_args`, `py.functions.lambda_hof`, `py.functions.sorting_keys`, `cs.complexity.big_o`, `dsa.foundations.memory_model`, `dsa.foundations.lib_toolkit`, `dsa.arrays_strings.arrays`, `dsa.arrays_strings.hash_tables`, `dsa.arrays_strings.hashing_patterns`, `dsa.arrays_strings.prefix_sum`, `dsa.arrays_strings.strings_basics`, `dsa.arrays_strings.string_algorithms`, `py.functions.scope_closures`, `dsa.arrays_strings.array_techniques`, `dsa.two_pointers_window.two_pointers`

Subtopic có item bắt buộc: `dsa.arrays_strings.hashing_patterns`, `dsa.arrays_strings.prefix_sum`, `dsa.two_pointers_window.two_pointers`. Các subtopic còn lại lấy điểm theo nhật ký luyện + mock (quy tắc 1 ở trên).

**Bắt buộc**

**[W190 · mức 3 · write_code · ~10 phút]** Viết `equal_01(nums)` độ dài đoạn con liên tiếp dài nhất có số 0 và số 1 bằng nhau (đổi 0 thành -1 rồi tìm tổng 0).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(equal_01([0, 1]), equal_01([0, 1, 0]), equal_01([0, 0, 1, 0, 0, 0, 1, 1]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
2 2 6
```
<details><summary>Code tham khảo</summary>

```python
def equal_01(nums):
    first = {0: -1}; s = best = 0
    for i, x in enumerate(nums):
        s += 1 if x else -1
        if s in first: best = max(best, i - first[s])
        else: first[s] = i
    return best
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 3. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 2. Sai/không chạy: tối đa điểm 2.

**[W189 · mức 2 · write_code · ~10 phút]** Viết `pair_count(nums, k)` đếm số cặp chỉ số i < j với nums[i] + nums[j] == k, O(n).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(pair_count([1, 2, 3, 4, 3], 6), pair_count([1, 1, 1], 2), pair_count([], 1))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
2 3 0
```
<details><summary>Code tham khảo</summary>

```python
def pair_count(nums, k):
    seen = {}; res = 0
    for x in nums:
        res += seen.get(k - x, 0)
        seen[x] = seen.get(x, 0) + 1
    return res
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[W193 · mức 2 · write_code · ~10 phút]** Viết `max_water(h)` diện tích lớn nhất giữa hai thanh (độ rộng x min chiều cao), O(n) hai con trỏ.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(max_water([1, 8, 6, 2, 5, 4, 8, 3, 7]), max_water([1, 1]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
49 1
```
<details><summary>Code tham khảo</summary>

```python
def max_water(h):
    i, j, best = 0, len(h) - 1, 0
    while i < j:
        best = max(best, (j - i) * min(h[i], h[j]))
        if h[i] < h[j]: i += 1
        else: j -= 1
    return best
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**Bổ sung**

**[W183 · mức 2 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
s = {1, 2, 3}; t = {2, 3, 4}
print(s & t, s | t, s - t, sorted(s ^ t))
```
Đáp án (output đã chạy kiểm chứng):

```
{2, 3} {1, 2, 3, 4} {1} [1, 4]
```
Giải thích: Phép giao, hợp, hiệu, hiệu đối xứng của set.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

**[W184 · mức 2 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
a = list(range(10))
print(a[::3], a[-3:], a[2:-2:2])
```
Đáp án (output đã chạy kiểm chứng):

```
[0, 3, 6, 9] [7, 8, 9] [2, 4, 6]
```
Giải thích: Slicing [start:stop:step], chỉ số âm đếm từ cuối.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

**[W185 · mức 2 · write_code · ~10 phút]** Viết `reverse_words(s)`: đảo thứ tự các từ, bỏ khoảng trắng thừa ("  the sky  is blue " -> "blue is sky the").

Driver (chạy sau khi bạn viết hàm/class):

```python
print(repr(reverse_words("  the sky  is blue ")), repr(reverse_words("a")))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
'blue is sky the' 'a'
```
<details><summary>Code tham khảo</summary>

```python
def reverse_words(s):
    return " ".join(s.split()[::-1])
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[W186 · mức 2 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
def f(a, *args, k=1, **kw):
    return a, args, k, kw
print(f(1, 2, 3, k=4, z=5))
```
Đáp án (output đã chạy kiểm chứng):

```
(1, (2, 3), 4, {'z': 5})
```
Giải thích: *args gom đối số vị trí còn lại thành tuple; **kw gom đối số tên còn lại thành dict.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

**[W187 · mức 2 · concept · ~3 phút]** Độ phức tạp của: (a) `while n > 1: n //= 2`, (b) sort rồi hai con trỏ, (c) fib đệ quy ngây thơ, (d) duyệt ma trận m x n.

Đáp án / rubric: (a) O(log n); (b) O(n log n); (c) O(2^n); (d) O(m*n).

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

**[W188 · mức 2 · write_code · ~10 phút]** Viết `valid_anagram(s, t)` bằng dict đếm ký tự (không dùng sorted).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(valid_anagram("anagram", "nagaram"), valid_anagram("rat", "car"), valid_anagram("", ""))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
True False True
```
<details><summary>Code tham khảo</summary>

```python
def valid_anagram(s, t):
    if len(s) != len(t): return False
    c = {}
    for ch in s: c[ch] = c.get(ch, 0) + 1
    for ch in t:
        if c.get(ch, 0) == 0: return False
        c[ch] -= 1
    return True
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[W191 · mức 2 · write_code · ~10 phút]** Viết `lcp(strs)` tiền tố chung dài nhất của danh sách chuỗi ("" nếu không có).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(repr(lcp(["flower", "flow", "flight"])), repr(lcp(["dog", "car"])), repr(lcp(["a"])))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
'fl' '' 'a'
```
<details><summary>Code tham khảo</summary>

```python
def lcp(strs):
    if not strs: return ""
    p = strs[0]
    for s in strs[1:]:
        while not s.startswith(p): p = p[:-1]
    return p
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[W192 · mức 2 · write_code · ~10 phút]** Viết `plus_one(digits)` cộng 1 vào số lớn biểu diễn bằng list chữ số.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(plus_one([1, 2, 9]), plus_one([9, 9]), plus_one([0]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[1, 3, 0] [1, 0, 0] [1]
```
<details><summary>Code tham khảo</summary>

```python
def plus_one(d):
    for i in range(len(d) - 1, -1, -1):
        if d[i] < 9: d[i] += 1; return d
        d[i] = 0
    return [1] + d
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[W194 · mức 2 · write_code · ~10 phút]** Viết `dedupe_sorted(nums)` xoá trùng tại chỗ trong mảng đã sắp, trả độ dài mới (reader/writer).

Driver (chạy sau khi bạn viết hàm/class):

```python
a = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
n = dedupe_sorted(a)
print(n, a[:n])
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
5 [0, 1, 2, 3, 4]
```
<details><summary>Code tham khảo</summary>

```python
def dedupe_sorted(nums):
    w = 0
    for x in nums:
        if w == 0 or x != nums[w - 1]:
            nums[w] = x; w += 1
    return w
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

#### Quiz tuần 2 (~26 phút bắt buộc)

Subtopic của tuần: `py.oop.classes_basics`, `dsa.linked_list.ll_basics`, `dsa.linked_list.ll_manipulation`, `dsa.stack_queue.stack_queue_ds`, `dsa.stack_queue.stack_problems`, `dsa.stack_queue.parsing_strings`, `dsa.foundations.interview_method`, `bh.method.self_intro`, `bh.method.star_carl`, `dsa.recursion_backtracking.recursion_basics`, `dsa.searching_sorting.binary_search_basics`, `dsa.searching_sorting.sorting_algorithms`, `dsa.searching_sorting.sorting_applications`, `dsa.trees.tree_basics`, `dsa.heap.heap_ds`, `dsa.heap.heap_top_k`, `dsa.searching_sorting.binary_search_variants`, `dsa.two_pointers_window.sliding_window_fixed`, `dsa.two_pointers_window.sliding_window_variable`, `bh.stories.conflict_teamwork`, `bh.stories.failure_feedback`

Subtopic có item bắt buộc: `dsa.linked_list.ll_manipulation`, `dsa.searching_sorting.sorting_algorithms`, `dsa.stack_queue.stack_problems`, `dsa.stack_queue.stack_queue_ds`. Các subtopic còn lại lấy điểm theo nhật ký luyện + mock (quy tắc 1 ở trên).

**Bắt buộc**

**[W196 · mức 2 · write_code · ~10 phút]** Viết `is_pal_list(head)` kiểm tra danh sách liên kết có đối xứng không, O(n) thời gian, O(1) bộ nhớ (tìm giữa + đảo nửa sau).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(is_pal_list(build([1, 2, 2, 1])), is_pal_list(build([1, 2])), is_pal_list(build([1, 2, 1])))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
True False True
```
<details><summary>Code tham khảo</summary>

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
def build(vals):
    dummy = cur = ListNode()
    for v in vals:
        cur.next = ListNode(v); cur = cur.next
    return dummy.next
def to_list(h):
    out = []
    while h:
        out.append(h.val); h = h.next
    return out
def is_pal_list(head):
    slow = fast = head
    while fast and fast.next: slow, fast = slow.next, fast.next.next
    prev = None
    while slow: slow.next, prev, slow = prev, slow, slow.next
    a, b = head, prev
    while b:
        if a.val != b.val: return False
        a, b = a.next, b.next
    return True
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[W197 · mức 2 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
from collections import deque
d = deque([1, 2, 3, 4, 5]); d.rotate(2); print(list(d))
d.rotate(-1); print(list(d), d[0], d[-1])
```
Đáp án (output đã chạy kiểm chứng):

```
[4, 5, 1, 2, 3]
[5, 1, 2, 3, 4] 5 4
```
Giải thích: rotate(k) xoay phải k bước; rotate(-1) xoay trái 1.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

**[W198 · mức 2 · write_code · ~10 phút]** Viết `backspace_equal(s, t)`: "#" là phím xoá lùi; True nếu hai chuỗi sau khi gõ bằng nhau.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(backspace_equal("ab#c", "ad#c"), backspace_equal("a#c", "b"), backspace_equal("ab##", "c#d#"))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
True False True
```
<details><summary>Code tham khảo</summary>

```python
def backspace_equal(s, t):
    def f(x):
        st = []
        for ch in x:
            if ch == "#":
                if st: st.pop()
            else: st.append(ch)
        return st
    return f(s) == f(t)
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[W200 · mức 2 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
a = [("x", 2), ("y", 1), ("z", 2), ("w", 1)]
print(sorted(a, key=lambda t: t[1]))
```
Đáp án (output đã chạy kiểm chứng):

```
[('y', 1), ('w', 1), ('x', 2), ('z', 2)]
```
Giải thích: sorted() ổn định (stable): các phần tử bằng khoá giữ thứ tự ban đầu.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

**Bổ sung**

**[W201 · mức 2 · write_code · ~10 phút]** Viết `k_closest(arr, k, x)` trả k số gần x nhất trong mảng đã sắp (hoà thì số nhỏ hơn), kết quả sắp tăng.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(k_closest([1, 2, 3, 4, 5], 4, 3), k_closest([1, 1, 2, 3, 4, 5], 4, -1))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[1, 2, 3, 4] [1, 1, 2, 3]
```
<details><summary>Code tham khảo</summary>

```python
def k_closest(arr, k, x):
    return sorted(sorted(arr, key=lambda v: (abs(v - x), v))[:k])
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[W203 · mức 2 · write_code · ~10 phút]** Viết `invert(root)` đảo trái-phải cây nhị phân; kiểm tra bằng preorder.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(preorder(invert(tree([4, 2, 7, 1, 3, 6, 9]))), invert(None))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[4, 7, 9, 6, 2, 3, 1] None
```
<details><summary>Code tham khảo</summary>

```python
from collections import deque
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right
def tree(vals):
    if not vals or vals[0] is None: return None
    root = TreeNode(vals[0]); q = deque([root]); i = 1
    while q and i < len(vals):
        n = q.popleft()
        if i < len(vals) and vals[i] is not None:
            n.left = TreeNode(vals[i]); q.append(n.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            n.right = TreeNode(vals[i]); q.append(n.right)
        i += 1
    return root
def invert(r):
    if r: r.left, r.right = invert(r.right), invert(r.left)
    return r
def preorder(r):
    return [r.val] + preorder(r.left) + preorder(r.right) if r else []
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[W195 · mức 2 · write_code · ~10 phút]** Viết `merge_two(a, b)` gộp hai danh sách liên kết đã sắp thành một danh sách sắp.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(to_list(merge_two(build([1, 2, 4]), build([1, 3, 4]))), to_list(merge_two(build([]), build([0]))))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[1, 1, 2, 3, 4, 4] [0]
```
<details><summary>Code tham khảo</summary>

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
def build(vals):
    dummy = cur = ListNode()
    for v in vals:
        cur.next = ListNode(v); cur = cur.next
    return dummy.next
def to_list(h):
    out = []
    while h:
        out.append(h.val); h = h.next
    return out
def merge_two(a, b):
    d = cur = ListNode()
    while a and b:
        if a.val <= b.val: cur.next, a = a, a.next
        else: cur.next, b = b, b.next
        cur = cur.next
    cur.next = a or b
    return d.next
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[W199 · mức 2 · write_code · ~10 phút]** Viết `first_bad(n, is_bad)`: phiên bản 1..n, từ một phiên bản nào đó trở đi đều lỗi. Tìm phiên bản lỗi đầu tiên bằng binary search.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(first_bad(5, lambda v: v >= 4), first_bad(1, lambda v: True), first_bad(10, lambda v: v >= 10))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
4 1 10
```
<details><summary>Code tham khảo</summary>

```python
def first_bad(n, is_bad):
    lo, hi = 1, n
    while lo < hi:
        mid = (lo + hi) // 2
        if is_bad(mid): hi = mid
        else: lo = mid + 1
    return lo
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[W202 · mức 2 · write_code · ~10 phút]** Viết `is_pow3(n)` bằng đệ quy: True nếu n là luỹ thừa của 3 (n >= 1).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(is_pow3(27), is_pow3(0), is_pow3(9), is_pow3(45))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
True False True False
```
<details><summary>Code tham khảo</summary>

```python
def is_pow3(n):
    if n < 1: return False
    if n == 1: return True
    return n % 3 == 0 and is_pow3(n // 3)
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[W204 · mức 2 · write_code · ~10 phút]** Viết `char_replacement(s, k)`: thay tối đa k ký tự để có chuỗi con cùng một ký tự dài nhất. Trả độ dài.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(char_replacement("ABAB", 2), char_replacement("AABABBA", 1), char_replacement("A", 0))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
4 4 1
```
<details><summary>Code tham khảo</summary>

```python
def char_replacement(s, k):
    from collections import defaultdict
    c = defaultdict(int); l = best = mx = 0
    for r, ch in enumerate(s):
        c[ch] += 1; mx = max(mx, c[ch])
        while r - l + 1 - mx > k:
            c[s[l]] -= 1; l += 1
        best = max(best, r - l + 1)
    return best
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

#### Quiz tuần 3 (~30 phút bắt buộc)

Subtopic của tuần: `dsa.recursion_backtracking.backtracking_core`, `dsa.trees.tree_recursion`, `dsa.trees.tree_bfs_views_hierarchy`, `dsa.trees.bst`, `dsa.design_ds.design_cache`, `dsa.design_ds.design_o1_structures`, `dsa.greedy_intervals.interval_basics`, `dsa.greedy_intervals.interval_sweep`, `dsa.arrays_strings.matrix_traversal`, `bh.stories.ownership_leadership`, `bh.stories.prioritization_ambiguity`, `py.core.io_input`, `py.core.try_except_basics`, `py.core.regex`, `py.errors_modules.files_pathlib`, `dsa.practical.file_log_parsing`, `dsa.graphs.graph_representation`, `dsa.graphs.graph_traversal`, `dsa.graphs.grid_graphs`, `dsa.graphs.bfs_shortest_path`

Subtopic có item bắt buộc: `dsa.recursion_backtracking.backtracking_core`, `dsa.trees.tree_bfs_views_hierarchy`, `dsa.trees.tree_recursion`. Các subtopic còn lại lấy điểm theo nhật ký luyện + mock (quy tắc 1 ở trên).

**Bắt buộc**

**[W205 · mức 2 · write_code · ~10 phút]** Viết `permutations(nums)` mọi hoán vị (nums khác nhau), trả danh sách sắp tăng.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(permutations([1, 2, 3])); print(len(permutations([1, 2, 3, 4])))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
24
```
<details><summary>Code tham khảo</summary>

```python
def permutations(nums):
    res = []; used = [False] * len(nums); cur = []
    def go():
        if len(cur) == len(nums): res.append(cur[:]); return
        for i, x in enumerate(nums):
            if used[i]: continue
            used[i] = True; cur.append(x); go(); cur.pop(); used[i] = False
    go()
    return sorted(res)
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[W206 · mức 2 · write_code · ~10 phút]** Viết `good_nodes(root)`: số nút X mà trên đường từ gốc đến X không có nút nào lớn hơn X.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(good_nodes(tree([3, 1, 4, 3, None, 1, 5])), good_nodes(tree([3, 3, None, 4, 2])), good_nodes(tree([1])))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
4 3 1
```
<details><summary>Code tham khảo</summary>

```python
from collections import deque
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right
def tree(vals):
    if not vals or vals[0] is None: return None
    root = TreeNode(vals[0]); q = deque([root]); i = 1
    while q and i < len(vals):
        n = q.popleft()
        if i < len(vals) and vals[i] is not None:
            n.left = TreeNode(vals[i]); q.append(n.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            n.right = TreeNode(vals[i]); q.append(n.right)
        i += 1
    return root
def good_nodes(r, mx=float("-inf")):
    if not r: return 0
    return (r.val >= mx) + good_nodes(r.left, max(mx, r.val)) + good_nodes(r.right, max(mx, r.val))
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[W207 · mức 2 · write_code · ~10 phút]** Viết `avg_levels(root)` trung bình giá trị từng tầng.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(avg_levels(tree([3, 9, 20, None, None, 15, 7])), avg_levels(None))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[3.0, 14.5, 11.0] []
```
<details><summary>Code tham khảo</summary>

```python
from collections import deque
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right
def tree(vals):
    if not vals or vals[0] is None: return None
    root = TreeNode(vals[0]); q = deque([root]); i = 1
    while q and i < len(vals):
        n = q.popleft()
        if i < len(vals) and vals[i] is not None:
            n.left = TreeNode(vals[i]); q.append(n.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            n.right = TreeNode(vals[i]); q.append(n.right)
        i += 1
    return root
def avg_levels(r):
    res = []; q = deque([r] if r else [])
    while q:
        n = len(q); s = 0
        for _ in range(n):
            x = q.popleft(); s += x.val
            if x.left: q.append(x.left)
            if x.right: q.append(x.right)
        res.append(s / n)
    return res
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**Bổ sung**

**[W208 · mức 2 · write_code · ~10 phút]** Viết `lca_bst(root, p, q)` (p, q là giá trị) tổ tiên chung thấp nhất trong BST, O(h).

Driver (chạy sau khi bạn viết hàm/class):

```python
t = tree([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
print(lca_bst(t, 2, 8), lca_bst(t, 2, 4), lca_bst(t, 3, 5))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
6 2 4
```
<details><summary>Code tham khảo</summary>

```python
from collections import deque
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right
def tree(vals):
    if not vals or vals[0] is None: return None
    root = TreeNode(vals[0]); q = deque([root]); i = 1
    while q and i < len(vals):
        n = q.popleft()
        if i < len(vals) and vals[i] is not None:
            n.left = TreeNode(vals[i]); q.append(n.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            n.right = TreeNode(vals[i]); q.append(n.right)
        i += 1
    return root
def lca_bst(r, p, q):
    while r:
        if p < r.val and q < r.val: r = r.left
        elif p > r.val and q > r.val: r = r.right
        else: return r.val
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[W209 · mức 2 · write_code · ~10 phút]** Viết class `TTLCache(ttl)`: put(k, v, now), get(k, now) trả v nếu chưa quá hạn (now - thời điểm put < ttl), nếu không trả None và xoá khoá.

Driver (chạy sau khi bạn viết hàm/class):

```python
c = TTLCache(5); c.put("a", 1, 0)
print(c.get("a", 4), c.get("a", 5), c.get("a", 6), "a" in c.d)
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
1 None None False
```
<details><summary>Code tham khảo</summary>

```python
class TTLCache:
    def __init__(self, ttl): self.ttl = ttl; self.d = {}
    def put(self, k, v, now): self.d[k] = (v, now)
    def get(self, k, now):
        if k not in self.d: return None
        v, t = self.d[k]
        if now - t >= self.ttl:
            del self.d[k]; return None
        return v
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[W210 · mức 2 · write_code · ~10 phút]** Viết `erase_overlap(intervals)`: số khoảng ít nhất cần xoá để các khoảng còn lại không chồng nhau (chạm đầu mút không tính là chồng).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(erase_overlap([[1, 2], [2, 3], [3, 4], [1, 3]]), erase_overlap([[1, 2], [1, 2], [1, 2]]), erase_overlap([[1, 2], [2, 3]]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
1 2 0
```
<details><summary>Code tham khảo</summary>

```python
def erase_overlap(iv):
    iv = sorted(iv, key=lambda x: x[1]); end = float("-inf"); keep = 0
    for a, b in iv:
        if a >= end: keep += 1; end = b
    return len(iv) - keep
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[W214 · mức 2 · write_code · ~10 phút]** Viết `island_perimeter(grid)` chu vi của đảo (ô 1) trong lưới (chỉ có một đảo).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(island_perimeter([[0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [1, 1, 0, 0]]), island_perimeter([[1]]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
16 4
```
<details><summary>Code tham khảo</summary>

```python
def island_perimeter(g):
    p = 0
    for i in range(len(g)):
        for j in range(len(g[0])):
            if g[i][j]:
                p += 4
                if i and g[i - 1][j]: p -= 2
                if j and g[i][j - 1]: p -= 2
    return p
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[W215 · mức 2 · write_code · ~10 phút]** Viết `path_cells(grid)`: lưới 0/1 (1 là tường), đi 4 hướng từ góc trên-trái tới góc dưới-phải. Trả số ô trên đường ngắn nhất (tính cả hai đầu) hoặc -1.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(path_cells([[0, 0, 0], [1, 1, 0], [0, 0, 0]]), path_cells([[0, 1], [1, 0]]), path_cells([[0]]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
5 -1 1
```
<details><summary>Code tham khảo</summary>

```python
def path_cells(g):
    from collections import deque
    R, C = len(g), len(g[0])
    if g[0][0] or g[R - 1][C - 1]: return -1
    q = deque([(0, 0, 1)]); seen = {(0, 0)}
    while q:
        r, c, d = q.popleft()
        if (r, c) == (R - 1, C - 1): return d
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and not g[nr][nc] and (nr, nc) not in seen:
                seen.add((nr, nc)); q.append((nr, nc, d + 1))
    return -1
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[W211 · mức 2 · write_code · ~10 phút]** Viết `set_zeroes(m)` nếu ô là 0 thì đặt cả hàng và cột của nó về 0 (tại chỗ), trả m.

Driver (chạy sau khi bạn viết hàm/class):

```python
print(set_zeroes([[1, 1, 1], [1, 0, 1], [1, 1, 1]]), set_zeroes([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
[[1, 0, 1], [0, 0, 0], [1, 0, 1]] [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]
```
<details><summary>Code tham khảo</summary>

```python
def set_zeroes(m):
    rows = {i for i, r in enumerate(m) if 0 in r}
    cols = {j for r in m for j, v in enumerate(r) if v == 0}
    for i in range(len(m)):
        for j in range(len(m[0])):
            if i in rows or j in cols: m[i][j] = 0
    return m
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[W212 · mức 2 · write_code · ~10 phút]** Cho dòng log "2026-01-01T10:15 ERROR msg". Viết `errors_per_hour(lines)` trả dict {giờ: số dòng ERROR}, giờ lấy 2 chữ số sau "T", sắp theo giờ.

Driver (chạy sau khi bạn viết hàm/class):

```python
log = ["2026-01-01T10:15 ERROR a", "2026-01-01T10:45 INFO b", "2026-01-01T11:05 ERROR c", "2026-01-01T10:59 ERROR d"]
print(errors_per_hour(log))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
{'10': 2, '11': 1}
```
<details><summary>Code tham khảo</summary>

```python
def errors_per_hour(lines):
    c = {}
    for ln in lines:
        ts, lvl = ln.split()[:2]
        if lvl == "ERROR":
            h = ts.split("T")[1][:2]; c[h] = c.get(h, 0) + 1
    return dict(sorted(c.items()))
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[W213 · mức 2 · write_code · ~10 phút]** Viết `has_path(n, edges, s, t)` đồ thị vô hướng có đường từ s tới t không? (DFS/BFS)

Driver (chạy sau khi bạn viết hàm/class):

```python
print(has_path(3, [[0, 1], [1, 2], [2, 0]], 0, 2), has_path(6, [[0, 1], [0, 2], [3, 5], [5, 4], [4, 3]], 0, 5))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
True False
```
<details><summary>Code tham khảo</summary>

```python
def has_path(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for a, b in edges: adj[a].append(b); adj[b].append(a)
    seen = {s}; st = [s]
    while st:
        u = st.pop()
        if u == t: return True
        for v in adj[u]:
            if v not in seen: seen.add(v); st.append(v)
    return False
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

#### Quiz tuần 4 (~29 phút bắt buộc)

Subtopic của tuần: `dsa.graphs.topological_sort`, `dsa.math_bits.bit_basics`, `dsa.practical.practical_format`, `dsa.practical.simulation_state_machines`, `dsa.practical.refactor_debug_review`, `py.errors_modules.exceptions`, `py.typing_testing.pytest_testing`, `dsa.practical.ai_assisted_coding`, `bh.stories.project_deep_dive`, `bh.motivation.why_company`, `bh.ai_fluency.ai_workflow`, `bh.ai_fluency.verify_ai_output`, `bh.ai_fluency.ai_safety_values`

Subtopic có item bắt buộc: `bh.ai_fluency.verify_ai_output`, `bh.stories.project_deep_dive`, `dsa.graphs.topological_sort`, `dsa.math_bits.bit_basics`, `dsa.practical.ai_assisted_coding`, `dsa.practical.refactor_debug_review`. Các subtopic còn lại lấy điểm theo nhật ký luyện + mock (quy tắc 1 ở trên).

**Bắt buộc**

**[W223 · mức 3 · behavioral · ~5 phút]** Mock 3 phút: nói về dự án tự hào nhất, sau đó trả lời 3 câu đào sâu liên tiếp (vì sao, trade-off, làm lại).

Đáp án / rubric: Điểm 3: mạch kể rõ trong 2 phút, có số liệu, trả lời đào sâu bằng dữ kiện, thừa nhận giới hạn, không nói chung chung.

Chấm: Điểm 3: mạch kể rõ trong 2 phút, có số liệu, trả lời đào sâu bằng dữ kiện, thừa nhận giới hạn, không nói chung chung. (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

**[W224 · mức 3 · behavioral · ~5 phút]** Mock: interviewer đưa đoạn code do AI viết có bug tinh vi. Bạn nói to cách bạn kiểm chứng trước khi tin nó.

Đáp án / rubric: Điểm 3: đọc hiểu, chạy test biên, nêu giả thuyết, không tin ngay, sửa và giải thích.

Chấm: Điểm 3: đọc hiểu, chạy test biên, nêu giả thuyết, không tin ngay, sửa và giải thích. (Câu behavioral: chấm TRỰC TIẾP điểm 0-3 theo mô tả trên, không đi theo bậc thang mức 1 → 2 → 3.)

**[W216 · mức 2 · concept · ~3 phút]** So sánh Kahn (BFS, đếm bậc vào) và DFS 3 trạng thái (chưa thăm / đang thăm / xong) để phát hiện chu trình. Khi nào gặp chu trình?

Đáp án / rubric: Kahn: nếu số nút lấy ra < n thì còn chu trình. DFS: gặp lại nút "đang thăm" nghĩa là có chu trình; thứ tự topo là thứ tự đảo của lúc "xong".

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

**[W217 · mức 2 · write_code · ~10 phút]** Viết `missing_number(nums)`: nums chứa n số khác nhau trong 0..n, trả số thiếu bằng XOR (O(1) bộ nhớ). Và `is_pow2(n)` bằng n & (n-1).

Driver (chạy sau khi bạn viết hàm/class):

```python
print(missing_number([3, 0, 1]), missing_number([0, 1]), is_pow2(16), is_pow2(18), is_pow2(0))
```
Kết quả mong đợi (đã chạy với code tham khảo):

```
2 2 True False False
```
<details><summary>Code tham khảo</summary>

```python
def missing_number(nums):
    r = len(nums)
    for i, x in enumerate(nums): r ^= i ^ x
    return r
def is_pow2(n):
    return n > 0 and n & (n - 1) == 0
```

</details>

Chấm: Chạy driver của đề: output khớp expected_output. Đúng không gợi ý trong time-box (10 phút) và độ phức tạp hợp lý: bằng chứng điểm 2. Đúng nhưng phải xem 1 gợi ý hoặc quá time-box: điểm 1. Sai/không chạy: tối đa điểm 1.

**[W219 · mức 2 · read_code · ~3 phút]** Hàm này định "bỏ phần tử trùng, giữ thứ tự". (a) In ra gì? (b) Bug và cách sửa.

```python
def dedupe(xs):
    seen = set()
    out = []
    for x in xs:
        if x in seen:
            out.append(x)
        seen.add(x)
    return out
print(dedupe([1, 2, 1, 3, 2, 1]))
```
Đáp án (output đã chạy kiểm chứng):

```
[1, 2, 1]
```
Giải thích: Điều kiện bị ngược: đang thêm phần tử ĐÃ thấy. Sửa: `if x not in seen: out.append(x)`. Kết quả đúng: [1, 2, 3].

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

**[W222 · mức 2 · concept · ~3 phút]** So sánh prompt xấu "viết code giải bài này" với prompt tốt trong vòng AI-enabled. Cho ví dụ prompt tốt cho một test đang fail.

Đáp án / rubric: Prompt tốt: nêu ngữ cảnh, đoạn lỗi, kết quả mong đợi/thực tế, ràng buộc (không đổi API, giữ O(n)), yêu cầu giải thích và đề xuất test. Ví dụ: "Test test_merge fail ở input [] vì IndexError dòng 12; đề xuất sửa nhỏ nhất và 2 test biên."

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

**Bổ sung**

**[W218 · mức 2 · concept · ~3 phút]** Đề practical nói "mọi thao tác đầu vào là list lệnh, ví dụ ["create A 100", "transfer A B 30"]". Bạn thiết kế hàm xử lý lệnh thế nào để thêm lệnh mới ở level sau mà không sửa nhiều chỗ?

Đáp án / rubric: Tách parse (chuỗi -> lệnh) và thi hành; dùng dict {tên lệnh: method}; mỗi level chỉ thêm method; trả kết quả dạng chuỗi/None đúng format đề; viết test từ ví dụ của đề trước.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

**[W220 · mức 2 · read_code · ~3 phút]** Chạy tay (không chạy máy), dòng code in ra gì? Giải thích 1 câu.

```python
def f(x):
    try:
        return 10 / x
    except ZeroDivisionError:
        return "zero"
    except TypeError:
        return "type"
print(f(2), f(0), f("a"))
```
Đáp án (output đã chạy kiểm chứng):

```
5.0 zero type
```
Giải thích: Mỗi loại ngoại lệ vào nhánh except tương ứng.

Chấm: Output khớp từng ký tự (bỏ khoảng trắng cuối dòng) VÀ giải thích đúng 1 câu. Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

**[W221 · mức 2 · concept · ~3 phút]** Test fail với `assert add(2, 3) == 6`. Pytest in gì giúp bạn gỡ lỗi? Bạn chạy chỉ test đó thế nào?

Đáp án / rubric: In giá trị hai vế của assert (assert 5 == 6) và dòng sai. Chạy một test: `pytest file.py::test_name -x -q`.

Chấm: Đúng các ý chính trong đáp án (thiếu ý quan trọng = sai). Đúng: bằng chứng điểm 2; sai: tối đa điểm 1.

### 2.3 Rubric chấm mock

Chấm ngay sau mock, từng câu. Mỗi trục 0-3.

#### Câu coding (5 trục)

| Trục | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| **Correctness** | không chạy được / sai hướng | ý tưởng đúng nhưng sai ở ví dụ thường hoặc nhiều biên; cần gợi ý lớn | đúng ví dụ thường và biên chính sau khi tự dry-run; có thể 1 lỗi nhỏ | đúng mọi ví dụ và biên, không gợi ý |
| **Complexity** | không nêu được độ phức tạp | nêu được nhưng sai hoặc chỉ brute force | nêu đúng time/space của lời giải mình viết | nêu đúng, so sánh với brute force, nói được cách tối ưu thêm / giới hạn |
| **Code quality** | rối, không đọc được | chạy được nhưng tên biến/khối lặp lộn xộn | gọn, tên có nghĩa, tách hàm hợp lý | như code review chấp nhận được: ngắn, rõ, ít trường hợp đặc biệt |
| **Communication** | im lặng | nói rời rạc, ít giải thích | nhắc lại đề, hỏi làm rõ, nói ý tưởng trước khi code | kể mạch rõ (đề -> ví dụ -> brute force -> tối ưu -> code -> test), nghe và dùng gợi ý tốt |
| **Testing** | không thử | chỉ thử ví dụ đề cho | dry-run ví dụ thường + 1 biên | chủ động nêu 3+ biên (rỗng, 1 phần tử, trùng, âm, lớn) và bắt được lỗi của mình |

**Điểm câu:** Q = làm tròn(0.40*Correctness + 0.15*(Complexity + Code quality + Communication + Testing)); nếu Correctness ≤ 1 thì Q ≤ 1.

#### Câu behavioral (STAR, impact, ownership)

| Trục | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| **STAR/CARL** | không có cấu trúc | thiếu 2 phần trở lên (thường thiếu Result) | đủ S-T-A-R, hơi dài/lan man | gọn, ≤ 2 phút, mỗi phần rõ |
| **Impact** | không có kết quả | kết quả chung chung ("ổn", "tốt hơn") | kết quả cụ thể định tính | kết quả có số liệu hoặc bằng chứng so sánh trước-sau + bài học |
| **Ownership** | đổ lỗi / "chúng em" toàn bộ | ít nói phần mình | rõ phần việc và quyết định của bản thân | chủ động, nhận trách nhiệm cả phần sai, dẫn tới thay đổi hành vi |
| **Communication** | khó hiểu | lan man | rõ ý, tốc độ ổn | tự nhiên, nhìn thẳng, có ví dụ cụ thể, trả lời follow-up không né |
| **AI judgement (chỉ câu [AI])** | coi AI là đáp án đúng | dùng AI nhưng không kiểm chứng | có quy trình kiểm chứng (chạy test, đọc code, đối chiếu) | nêu được khi nào tin/bác bỏ, rủi ro bảo mật/quyền riêng tư, trách nhiệm cuối cùng thuộc về mình |

**Điểm câu:** Q = làm tròn(0.35*STAR + 0.25*Impact + 0.25*Ownership + 0.15*Communication). Câu [AI]: Q = làm tròn(0.30*STAR + 0.20*Impact + 0.20*Ownership + 0.30*AI judgement).

#### Phiếu chấm mock (sao chép cho mỗi lần mock)

| Mock | Câu | Correctness | Complexity | Code quality | Communication | Testing | Q | Lỗi chính |
|---|---|---|---|---|---|---|---|---|
| I1 | I1-R1-Q1 |  |  |  |  |  |  |  |

Từ mock sang điểm subtopic: mỗi câu mock có danh sách `subtopics` (trong `content_ng/*.json`); điểm subtopic từ mock = Q của câu đó (nếu nhiều câu cùng subtopic thì lấy trung bình, làm tròn xuống).

## 3. Đánh giá cuối tháng và sẵn sàng

### 3.1 Trình tự ngày 29-30

1. **Ngày 29**: mock còn lại (N2 Onsite coding 2 và OA nhiều level N6-R1 Level 1-2) chấm bằng rubric mục 2.3. Cùng với N1 (ngày 27), N2 phone + coding 1 (ngày 21), N2 AI-enabled và 2 behavioral (ngày 28): đủ dữ liệu cho mục (c), (d) bên dưới.
2. **Ngày 30 sáng (2 giờ)**: chạy lại chẩn đoán đầu vào đúng quy trình mục 1 (cùng item; vì đã làm 30 ngày trước, bạn có thể nhớ đề: ghi chú "lần 2", viết lại từ đầu không nhìn đáp án cũ, và cộng thêm bằng chứng từ 4 quiz tuần).
3. **Ngày 30 chiều**: điền cột `score_day30` trong bảng sẵn sàng (3.2), áp luật go/no-go (3.3).

### 3.2 Bảng sẵn sàng

Cột `Mục tiêu` lấy từ `skill_tree.json` (`target_swe` cho SWE, `target_ai` cho gói AI/ML). Kế hoạch 1 tháng nhắm: **3 ở subtopic hot, 2 ở còn lại**. Điền Day 0 và Day 30; cột Chênh = Day 30 − mục tiêu áp dụng.

| Subtopic | Hot | Mục tiêu intern | Mục tiêu fresher | Mục tiêu kế hoạch | Day 0 | Day 30 | Chênh |
|---|---|---|---|---|---|---|---|
| `py.core.getting_started` |  | 2 | 3 | 2 |  |  |  |
| `py.core.variables_types` |  | 2 | 3 | 2 |  |  |  |
| `py.core.operators` |  | 2 | 3 | 2 |  |  |  |
| `py.core.conditionals` |  | 2 | 3 | 2 |  |  |  |
| `py.core.loops` |  | 2 | 3 | 2 |  |  |  |
| `py.core.strings` |  | 2 | 3 | 2 |  |  |  |
| `py.datastructs.list` |  | 2 | 3 | 2 |  |  |  |
| `py.datastructs.tuple_namedtuple` |  | 2 | 2 | 2 |  |  |  |
| `py.datastructs.dict` |  | 2 | 3 | 2 |  |  |  |
| `py.datastructs.comprehensions` |  | 2 | 3 | 2 |  |  |  |
| `py.datastructs.collections_module` |  | 2 | 3 | 2 |  |  |  |
| `py.datastructs.copying_mutability` |  | 1 | 3 | 2 |  |  |  |
| `py.datastructs.heapq_bisect` |  | 1 | 3 | 2 |  |  |  |
| `py.functions.def_args` |  | 2 | 3 | 2 |  |  |  |
| `py.functions.lambda_hof` |  | 2 | 3 | 2 |  |  |  |
| `py.functions.sorting_keys` |  | 2 | 3 | 2 |  |  |  |
| `cs.complexity.big_o` |  | 2 | 3 | 2 |  |  |  |
| `dsa.foundations.memory_model` |  | 1 | 2 | 2 |  |  |  |
| `dsa.foundations.lib_toolkit` |  | 2 | 3 | 2 |  |  |  |
| `dsa.arrays_strings.arrays` |  | 2 | 3 | 2 |  |  |  |
| `dsa.arrays_strings.hash_tables` |  | 2 | 3 | 2 |  |  |  |
| `dsa.arrays_strings.hashing_patterns` | x | 2 | 3 | 3 |  |  |  |
| `dsa.arrays_strings.prefix_sum` | x | 1 | 2 | 3 |  |  |  |
| `dsa.arrays_strings.strings_basics` |  | 2 | 3 | 2 |  |  |  |
| `dsa.arrays_strings.string_algorithms` | x | 1 | 2 | 3 |  |  |  |
| `py.functions.scope_closures` |  | 0 | 2 | 2 |  |  |  |
| `dsa.arrays_strings.array_techniques` |  | 1 | 2 | 2 |  |  |  |
| `dsa.two_pointers_window.two_pointers` | x | 2 | 3 | 3 |  |  |  |
| `py.oop.classes_basics` |  | 2 | 3 | 2 |  |  |  |
| `dsa.linked_list.ll_basics` |  | 2 | 3 | 2 |  |  |  |
| `dsa.linked_list.ll_manipulation` | x | 2 | 3 | 3 |  |  |  |
| `dsa.stack_queue.stack_queue_ds` | x | 2 | 3 | 3 |  |  |  |
| `dsa.stack_queue.stack_problems` | x | 2 | 3 | 3 |  |  |  |
| `dsa.stack_queue.parsing_strings` | x | 2 | 3 | 3 |  |  |  |
| `dsa.foundations.interview_method` |  | 2 | 3 | 2 |  |  |  |
| `bh.method.self_intro` |  | 3 | 3 | 2 |  |  |  |
| `bh.method.star_carl` |  | 2 | 3 | 2 |  |  |  |
| `dsa.recursion_backtracking.recursion_basics` |  | 2 | 3 | 2 |  |  |  |
| `dsa.searching_sorting.binary_search_basics` |  | 2 | 3 | 2 |  |  |  |
| `dsa.searching_sorting.sorting_algorithms` |  | 2 | 3 | 2 |  |  |  |
| `dsa.searching_sorting.sorting_applications` |  | 1 | 2 | 2 |  |  |  |
| `dsa.trees.tree_basics` | x | 2 | 3 | 3 |  |  |  |
| `dsa.heap.heap_ds` | x | 2 | 3 | 3 |  |  |  |
| `dsa.heap.heap_top_k` | x | 2 | 3 | 3 |  |  |  |
| `dsa.searching_sorting.binary_search_variants` | x | 0 | 2 | 3 |  |  |  |
| `dsa.two_pointers_window.sliding_window_fixed` |  | 1 | 2 | 2 |  |  |  |
| `dsa.two_pointers_window.sliding_window_variable` |  | 2 | 3 | 2 |  |  |  |
| `bh.stories.conflict_teamwork` | x | 2 | 3 | 3 |  |  |  |
| `bh.stories.failure_feedback` | x | 2 | 3 | 3 |  |  |  |
| `dsa.recursion_backtracking.backtracking_core` | x | 0 | 2 | 3 |  |  |  |
| `dsa.trees.tree_recursion` | x | 2 | 3 | 3 |  |  |  |
| `dsa.trees.tree_bfs_views_hierarchy` | x | 2 | 3 | 3 |  |  |  |
| `dsa.trees.bst` | x | 2 | 3 | 3 |  |  |  |
| `dsa.design_ds.design_cache` | x | 2 | 3 | 3 |  |  |  |
| `dsa.design_ds.design_o1_structures` |  | 0 | 1 | 2 |  |  |  |
| `dsa.greedy_intervals.interval_basics` | x | 2 | 3 | 3 |  |  |  |
| `dsa.greedy_intervals.interval_sweep` | x | 0 | 2 | 3 |  |  |  |
| `dsa.arrays_strings.matrix_traversal` |  | 2 | 3 | 2 |  |  |  |
| `bh.stories.ownership_leadership` | x | 1 | 3 | 3 |  |  |  |
| `bh.stories.prioritization_ambiguity` |  | 1 | 3 | 2 |  |  |  |
| `py.core.io_input` |  | 2 | 2 | 2 |  |  |  |
| `py.core.try_except_basics` |  | 2 | 3 | 2 |  |  |  |
| `py.core.regex` |  | 0 | 1 | 2 |  |  |  |
| `py.errors_modules.files_pathlib` |  | 0 | 2 | 2 |  |  |  |
| `dsa.practical.file_log_parsing` |  | 2 | 3 | 2 |  |  |  |
| `dsa.graphs.graph_representation` |  | 1 | 2 | 2 |  |  |  |
| `dsa.graphs.graph_traversal` |  | 2 | 3 | 2 |  |  |  |
| `dsa.graphs.grid_graphs` | x | 2 | 3 | 3 |  |  |  |
| `dsa.graphs.bfs_shortest_path` | x | 0 | 2 | 3 |  |  |  |
| `dsa.graphs.topological_sort` | x | 2 | 3 | 3 |  |  |  |
| `dsa.math_bits.bit_basics` | x | 0 | 2 | 3 |  |  |  |
| `dsa.practical.practical_format` |  | 1 | 3 | 2 |  |  |  |
| `dsa.practical.simulation_state_machines` | x | 0 | 1 | 3 |  |  |  |
| `dsa.practical.refactor_debug_review` | x | 0 | 2 | 3 |  |  |  |
| `py.errors_modules.exceptions` |  | 2 | 3 | 2 |  |  |  |
| `py.typing_testing.pytest_testing` |  | 0 | 2 | 2 |  |  |  |
| `dsa.practical.ai_assisted_coding` | x | 0 | 2 | 3 |  |  |  |
| `bh.stories.project_deep_dive` | x | 2 | 3 | 3 |  |  |  |
| `bh.motivation.why_company` |  | 2 | 3 | 2 |  |  |  |
| `bh.ai_fluency.ai_workflow` | x | 2 | 3 | 3 |  |  |  |
| `bh.ai_fluency.verify_ai_output` | x | 2 | 3 | 3 |  |  |  |
| `bh.ai_fluency.ai_safety_values` |  | 0 | 1 | 2 |  |  |  |
| `ml.fundamentals.ml_overview` (AI) |  | 2 | 2 | 2 |  |  |  |
| `ml.classical.decision_trees` (AI) |  | 2 | 3 | 2 |  |  |  |
| `ml.math.linear_algebra_basics` (AI) |  | 2 | 2 | 2 |  |  |  |
| `ml.math.random_variables_expectation` (AI) |  | 0 | 1 | 2 |  |  |  |
| `ml.classical.dimensionality_reduction` (AI) |  | 0 | 2 | 2 |  |  |  |
| `ml.fundamentals.loss_functions` (AI) |  | 1 | 2 | 2 |  |  |  |
| `ml.math.derivatives_gradients` (AI) |  | 1 | 2 | 2 |  |  |  |
| `ml.math.gradient_descent` (AI) |  | 1 | 2 | 2 |  |  |  |
| `ml.classical.linear_regression` (AI) |  | 2 | 3 | 2 |  |  |  |
| `ml.classical.logistic_regression` (AI) |  | 2 | 3 | 2 |  |  |  |
| `ml.classical.knn_nb_svm` (AI) |  | 0 | 2 | 2 |  |  |  |
| `ml.classical.unsupervised` (AI) |  | 0 | 2 | 2 |  |  |  |
| `py.ecosystem.numpy_basics` (AI) |  | 1 | 3 | 2 |  |  |  |
| `ml.coding.kmeans_knn_trees` (AI) |  | 0 | 0 | 2 |  |  |  |
| `ml.coding.linear_logistic_scratch` (AI) |  | 0 | 1 | 2 |  |  |  |
| `ml.fundamentals.bias_variance_overfitting` (AI) |  | 2 | 3 | 2 |  |  |  |
| `ml.fundamentals.validation_tuning` (AI) |  | 2 | 3 | 2 |  |  |  |
| `py.ecosystem.pandas_basics` (AI) |  | 1 | 3 | 2 |  |  |  |
| `ml.data_features.cleaning_missing` (AI) |  | 2 | 3 | 2 |  |  |  |
| `ml.coding.pipeline_debugging` (AI) |  | 0 | 0 | 1 |  |  |  |
| `ml.fundamentals.classification_metrics` (AI) |  | 2 | 3 | 2 |  |  |  |

Lưu ý: 59/82 subtopic SWE có mục tiêu fresher = 3 trong cây; một tháng không đủ giờ để đạt 3 ở tất cả, nên luật GO dùng min(mục tiêu, 2) cho subtopic không hot.

### 3.3 Luật go / no-go

**Intern**

- (a) ≥ 90% subtopic SWE đạt ≥ min(target_swe.intern, 2) ở ngày 30;
- (b) mọi subtopic "hot" (cột hot) ≥ 2;
- (c) điểm trung bình các câu coding của mock ≥ 2.0 và không câu nào Correctness = 0, tính trên I3 (4 câu: ngày 14) cộng N2 phone screen + coding 1 (4 câu: ngày 21);
- (d) behavioral: ≥ 4/5 story đạt Q ≥ 2 và 2/2 câu [AI] đạt Q ≥ 2.

**New grad (E3)**

- (a) ≥ 90% subtopic SWE đạt ≥ min(target_swe.fresher, 2) ở ngày 30;
- (b) ≥ 40% subtopic hot đạt 3 và không subtopic hot nào < 2 (kế hoạch nhắm 2 cho phần lớn mục; mức 3 đến từ mock và ôn lặp nên rơi vào GO CÓ ĐIỀU KIỆN là bình thường, không phải thất bại);
- (c) 3 mock gần nhất (N1, N2 phone+coding, N2 coding 2): trung bình coding ≥ 2.3, không câu nào Correctness ≤ 1, ≥ 1 câu AI-enabled đạt Q ≥ 2;
- (d) behavioral như intern, thêm ≥ 1 story có số liệu (Impact = 3).

- **Go có điều kiện**: Đạt (a) nhưng trượt (b)/(c)/(d): GO CÓ ĐIỀU KIỆN. Hẹn phỏng vấn sau ≥ 10 ngày; dành 10 ngày chỉ cho các subtopic hot < 3 và các câu mock Q ≤ 1 (làm lại theo D+3/D+7), rồi chạy lại mục 3.2 chỉ cho các subtopic đó.
- **No-go**: Trượt (a): NO-GO. Làm lại kế hoạch với hệ số giờ ×1.5 cho cụm điểm thấp nhất, kéo dài thêm 2 tuần; không đặt lịch phỏng vấn; xem lại giả định Python/CS ở mục 1 của plan.md.

## 4. Bảng theo dõi (điền hằng ngày / hằng tuần)

### 4.1 Lịch sử điểm theo subtopic

File `tracking.csv` có sẵn cột này cho từng subtopic (mở bằng Excel/Google Sheets). Dưới đây là mẫu 3 dòng:

| subtopic_id | hot | mục tiêu intern/fresher | Tuần | Day 0 | Tuần 1 | Tuần 2 | Tuần 3 | Tuần 4 | Day 30 | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|
| `py.core.getting_started` |  | 2/3 | 1 |  |  |  |  |  |  |  |
| `py.core.variables_types` |  | 2/3 | 1 |  |  |  |  |  |  |  |
| `py.core.operators` |  | 2/3 | 1 |  |  |  |  |  |  |  |

### 4.2 Nhật ký lỗi

| Ngày | Bài / câu | subtopic_id | Loại lỗi | Nguyên nhân gốc | Cách sửa | Ôn lại D+3 | Ôn lại D+7 | Xong |
|---|---|---|---|---|---|---|---|---|
| 5 | LC 209 | dsa.two_pointers_window.sliding_window_variable | Biên | quên co cửa sổ khi tổng ≥ target | dùng `while` thay `if` | 8 | 12 | ☐ |
|  |  |  |  |  |  |  |  | ☐ |

Loại lỗi: Hiểu đề, Chọn cấu trúc/pattern, Logic, Biên (edge case), Cú pháp/API Python, Độ phức tạp, Giao tiếp, Hết giờ. Cuối tuần: đếm loại lỗi nhiều nhất → 30 phút buffer cho loại đó.

### 4.3 Lịch ôn lặp theo subtopic (ngày trong kế hoạch)

Mỗi subtopic ôn bằng cách tự giải thích 2 phút + viết lại 1 bài đã sai. Ngày hết hạn tính từ ngày học xong (ngày cuối cùng subtopic xuất hiện trong plan).

| Subtopic | Học xong (ngày) | D+1 | D+3 | D+7 | D+14 | D+28 | Đã ôn |
|---|---|---|---|---|---|---|---|
| `py.core.getting_started` | 1 | 2 | 4 | 8 | 15 | 29 |  |
| `py.core.variables_types` | 1 | 2 | 4 | 8 | 15 | 29 |  |
| `py.core.operators` | 1 | 2 | 4 | 8 | 15 | 29 |  |
| `py.core.conditionals` | 1 | 2 | 4 | 8 | 15 | 29 |  |
| `py.core.loops` | 1 | 2 | 4 | 8 | 15 | 29 |  |
| `py.core.strings` | 1 | 2 | 4 | 8 | 15 | 29 |  |
| `py.datastructs.list` | 2 | 3 | 5 | 9 | 16 | 30 |  |
| `py.datastructs.tuple_namedtuple` | 2 | 3 | 5 | 9 | 16 | 30 |  |
| `py.datastructs.dict` | 2 | 3 | 5 | 9 | 16 | 30 |  |
| `py.datastructs.comprehensions` | 2 | 3 | 5 | 9 | 16 | 30 |  |
| `py.datastructs.collections_module` | 2 | 3 | 5 | 9 | 16 | 30 |  |
| `py.datastructs.copying_mutability` | 3 | 4 | 6 | 10 | 17 | 31 |  |
| `py.datastructs.heapq_bisect` | 3 | 4 | 6 | 10 | 17 | 31 |  |
| `py.functions.def_args` | 3 | 4 | 6 | 10 | 17 | 31 |  |
| `py.functions.lambda_hof` | 3 | 4 | 6 | 10 | 17 | 31 |  |
| `py.functions.sorting_keys` | 4 | 5 | 7 | 11 | 18 | 32 |  |
| `cs.complexity.big_o` | 4 | 5 | 7 | 11 | 18 | 32 |  |
| `dsa.foundations.memory_model` | 4 | 5 | 7 | 11 | 18 | 32 |  |
| `dsa.foundations.lib_toolkit` | 4 | 5 | 7 | 11 | 18 | 32 |  |
| `dsa.arrays_strings.arrays` | 5 | 6 | 8 | 12 | 19 | 33 |  |
| `dsa.arrays_strings.hash_tables` | 5 | 6 | 8 | 12 | 19 | 33 |  |
| `dsa.arrays_strings.hashing_patterns` | 6 | 7 | 9 | 13 | 20 | 34 |  |
| `dsa.arrays_strings.prefix_sum` | 6 | 7 | 9 | 13 | 20 | 34 |  |
| `dsa.arrays_strings.strings_basics` | 6 | 7 | 9 | 13 | 20 | 34 |  |
| `dsa.arrays_strings.string_algorithms` | 6 | 7 | 9 | 13 | 20 | 34 |  |
| `py.functions.scope_closures` | 7 | 8 | 10 | 14 | 21 | 35 |  |
| `dsa.arrays_strings.array_techniques` | 7 | 8 | 10 | 14 | 21 | 35 |  |
| `dsa.two_pointers_window.two_pointers` | 7 | 8 | 10 | 14 | 21 | 35 |  |
| `py.oop.classes_basics` | 8 | 9 | 11 | 15 | 22 | 36 |  |
| `dsa.linked_list.ll_basics` | 8 | 9 | 11 | 15 | 22 | 36 |  |
| `dsa.linked_list.ll_manipulation` | 9 | 10 | 12 | 16 | 23 | 37 |  |
| `dsa.stack_queue.stack_queue_ds` | 9 | 10 | 12 | 16 | 23 | 37 |  |
| `dsa.stack_queue.stack_problems` | 9 | 10 | 12 | 16 | 23 | 37 |  |
| `dsa.stack_queue.parsing_strings` | 10 | 11 | 13 | 17 | 24 | 38 |  |
| `dsa.foundations.interview_method` | 10 | 11 | 13 | 17 | 24 | 38 |  |
| `bh.method.self_intro` | 10 | 11 | 13 | 17 | 24 | 38 |  |
| `bh.method.star_carl` | 11 | 12 | 14 | 18 | 25 | 39 |  |
| `dsa.recursion_backtracking.recursion_basics` | 11 | 12 | 14 | 18 | 25 | 39 |  |
| `dsa.searching_sorting.binary_search_basics` | 11 | 12 | 14 | 18 | 25 | 39 |  |
| `dsa.searching_sorting.sorting_algorithms` | 12 | 13 | 15 | 19 | 26 | 40 |  |
| `dsa.searching_sorting.sorting_applications` | 12 | 13 | 15 | 19 | 26 | 40 |  |
| `dsa.trees.tree_basics` | 12 | 13 | 15 | 19 | 26 | 40 |  |
| `dsa.heap.heap_ds` | 13 | 14 | 16 | 20 | 27 | 41 |  |
| `dsa.heap.heap_top_k` | 13 | 14 | 16 | 20 | 27 | 41 |  |
| `dsa.searching_sorting.binary_search_variants` | 13 | 14 | 16 | 20 | 27 | 41 |  |
| `dsa.two_pointers_window.sliding_window_fixed` | 13 | 14 | 16 | 20 | 27 | 41 |  |
| `dsa.two_pointers_window.sliding_window_variable` | 13 | 14 | 16 | 20 | 27 | 41 |  |
| `bh.stories.conflict_teamwork` | 14 | 15 | 17 | 21 | 28 | 42 |  |
| `bh.stories.failure_feedback` | 14 | 15 | 17 | 21 | 28 | 42 |  |
| `dsa.recursion_backtracking.backtracking_core` | 15 | 16 | 18 | 22 | 29 | 43 |  |
| `dsa.trees.tree_recursion` | 15 | 16 | 18 | 22 | 29 | 43 |  |
| `dsa.trees.tree_bfs_views_hierarchy` | 16 | 17 | 19 | 23 | 30 | 44 |  |
| `dsa.trees.bst` | 16 | 17 | 19 | 23 | 30 | 44 |  |
| `dsa.design_ds.design_cache` | 17 | 18 | 20 | 24 | 31 | 45 |  |
| `dsa.design_ds.design_o1_structures` | 17 | 18 | 20 | 24 | 31 | 45 |  |
| `dsa.greedy_intervals.interval_basics` | 17 | 18 | 20 | 24 | 31 | 45 |  |
| `dsa.greedy_intervals.interval_sweep` | 18 | 19 | 21 | 25 | 32 | 46 |  |
| `dsa.arrays_strings.matrix_traversal` | 18 | 19 | 21 | 25 | 32 | 46 |  |
| `bh.stories.ownership_leadership` | 18 | 19 | 21 | 25 | 32 | 46 |  |
| `bh.stories.prioritization_ambiguity` | 19 | 20 | 22 | 26 | 33 | 47 |  |
| `py.core.io_input` | 19 | 20 | 22 | 26 | 33 | 47 |  |
| `py.core.try_except_basics` | 19 | 20 | 22 | 26 | 33 | 47 |  |
| `py.core.regex` | 19 | 20 | 22 | 26 | 33 | 47 |  |
| `py.errors_modules.files_pathlib` | 19 | 20 | 22 | 26 | 33 | 47 |  |
| `dsa.practical.file_log_parsing` | 20 | 21 | 23 | 27 | 34 | 48 |  |
| `dsa.graphs.graph_representation` | 20 | 21 | 23 | 27 | 34 | 48 |  |
| `dsa.graphs.graph_traversal` | 20 | 21 | 23 | 27 | 34 | 48 |  |
| `dsa.graphs.grid_graphs` | 20 | 21 | 23 | 27 | 34 | 48 |  |
| `dsa.graphs.bfs_shortest_path` | 21 | 22 | 24 | 28 | 35 | 49 |  |
| `dsa.graphs.topological_sort` | 22 | 23 | 25 | 29 | 36 | 50 |  |
| `dsa.math_bits.bit_basics` | 22 | 23 | 25 | 29 | 36 | 50 |  |
| `dsa.practical.practical_format` | 22 | 23 | 25 | 29 | 36 | 50 |  |
| `dsa.practical.simulation_state_machines` | 23 | 24 | 26 | 30 | 37 | 51 |  |
| `dsa.practical.refactor_debug_review` | 23 | 24 | 26 | 30 | 37 | 51 |  |
| `py.errors_modules.exceptions` | 23 | 24 | 26 | 30 | 37 | 51 |  |
| `py.typing_testing.pytest_testing` | 24 | 25 | 27 | 31 | 38 | 52 |  |
| `dsa.practical.ai_assisted_coding` | 24 | 25 | 27 | 31 | 38 | 52 |  |
| `bh.stories.project_deep_dive` | 24 | 25 | 27 | 31 | 38 | 52 |  |
| `bh.motivation.why_company` | 25 | 26 | 28 | 32 | 39 | 53 |  |
| `bh.ai_fluency.ai_workflow` | 25 | 26 | 28 | 32 | 39 | 53 |  |
| `bh.ai_fluency.verify_ai_output` | 25 | 26 | 28 | 32 | 39 | 53 |  |
| `bh.ai_fluency.ai_safety_values` | 25 | 26 | 28 | 32 | 39 | 53 |  |

(Các ngày > 30 nằm ngoài tháng; làm tiếp trong giai đoạn sau nếu còn thời gian.)

## 5. Kiểm tra tự động

| Kiểm tra | Kết quả | Chi tiết |
|---|---|---|
| A1 mọi item code (read_code / write_code) chạy bằng python3 và output khớp expected_output | PASS | 175 item code đã chạy; lỗi: [] |
| A2 mọi subtopic_id của item tồn tại trong skill_tree.json | PASS | 254 item |
| A3 difficulty ∈ {1,2,3} và type hợp lệ | PASS |  |
| A4 id item duy nhất | PASS |  |
| A5 mọi subtopic được xếp lịch (SWE) có ≥ 1 item chẩn đoán và có item mức 2 (hoặc chỉ mức 1); không subtopic nào thiếu cả hai | PASS | 82 subtopic; có đủ 1+2: 63; có 2+3 (không có mức 1): 19; chỉ mức 1: 0 |
| A6 mọi subtopic của gói AI/ML có ≥ 1 item chẩn đoán | PASS | thiếu: [] |
| A7 mọi item nằm trong subtopic được xếp lịch (SWE hoặc AI/ML); item của subtopic đã cắt khỏi kế hoạch bị loại | PASS | ngoài lịch: []; đã loại 6 item của ['eng.workflow.git_basics', 'py.errors_modules.modules_packages', 'py.typing_testing.envs_packaging'] |
| A8 mọi subtopic SWE thuộc đúng 1 cụm chẩn đoán | PASS | 82 subtopic / 10 cụm |
| A9 thời gian Day 0 ước tính ≤ 180 phút ở mọi kịch bản (có time-box; dừng cứng 180 phút) | PASS | mạnh (10 cụm đều qua gate): 136 phút; trung bình (5 cụm qua, 5 cụm điểm 1): 171 phút; yếu (10 cụm trượt gate): 116 phút; xấu nhất (10 cụm điểm 1, mỗi cụm dùng hết 15 phút; dừng cứng ở 180): 180 phút |
| A9b thời gian Day 0 trong khoảng 2-3 giờ ở kịch bản trung bình và xấu nhất | PASS | mạnh (10 cụm đều qua gate): 136 phút; trung bình (5 cụm qua, 5 cụm điểm 1): 171 phút; yếu (10 cụm trượt gate): 116 phút; xấu nhất (10 cụm điểm 1, mỗi cụm dùng hết 15 phút; dừng cứng ở 180): 180 phút |
| A10 mỗi tuần 1-4 có quiz với ≥ 6 item và phần bắt buộc ≤ 30 phút | PASS | tuần 1: 12 item, bắt buộc 30 phút; tuần 2: 10 item, bắt buộc 26 phút; tuần 3: 11 item, bắt buộc 30 phút; tuần 4: 9 item, bắt buộc 29 phút |
| A11 không có hai item trùng nội dung (prompt + code); item quiz tuần khác item chẩn đoán | PASS |  |
| A12 bảng sẵn sàng: mọi subtopic có target_swe/target_ai hợp lệ (0-3) | PASS | 103 dòng |