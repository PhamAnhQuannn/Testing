# Content Gap Report — Python Fundamentals

So sánh khoá **"30 Days Of Python"** với các bài **Python Fundamentals** hiện có của Prep App.

## 1. Mục đích và ghi chú quy trình

Báo cáo này đối chiếu nội dung khoá *30 Days Of Python* (nguồn: `D:\30-Days-Of-Python\docs\knowledge-index.md` và
`D:\30-Days-Of-Python\docs\exercises-index.md`) với 18 bài lesson Python đang có trong
`D:\preparing\Testing\content\lessons\py\*.yaml`, nhằm chỉ ra:

- **Concept/built-in** mà một `Day` của 30-Days dạy nhưng bài lesson tương ứng của app **chưa nhắc tới**.
- **Exercise gap**: mỗi lesson đang có bao nhiêu bài luyện, và có thể bổ sung bài nào (lấy ý từ exercises-index)
  để mỗi lesson đạt **≥ 3 bài luyện** (code_exercise + problem).

**Lưu ý về pipeline (quan trọng).** App là **content-driven**: mọi bài tập code không được viết tay tuỳ ý mà
phải đi qua **content pipeline**. Theo `CLAUDE.md` mục *"Authoring a problem"*: tạo
`content/problems/<subtopic_id>/<slug>/` với `problem.yaml` + `solution.py` + `brute.py` (bắt buộc cho medium) +
`wrong/*.py` + `tests/gen.py`; chạy `tools/gen_hidden.py` để sinh `tests/hidden.jsonl` (giá trị `expected` **luôn
lấy từ `solution.py`**, không do người/LLM gõ); chạy `tools/run_problem.py`; tham chiếu từ lesson (`problems:` + block),
đặt `status: validated`, `make validate`, review, rồi `status: published`. Mỗi lesson cần **tối thiểu 3 `graded`
block** (SPEC 3.5). Vì vậy báo cáo này **chỉ đề xuất**, không tự thêm bài. Phạm vi *Fundamentals* = **Day 1–19 và Day 21**.

## 2. Bảng ánh xạ 30-Days Day → App subtopic

| 30-Days Day (title) | App subtopic id | Ghi chú |
|---|---|---|
| Day 1 — Introduction | `py.core.getting_started` | App sâu hơn Day 1 (có traceback, PEP 8). |
| Day 2 — Variables & Built-in Functions | `py.core.variables_types` (+ `getting_started` cho `print`/`import`) | Thiếu `input()`, `dir()`, `help()`, `complex`. |
| Day 3 — Operators | `py.core.operators` | App sâu hơn; thiếu `complex`, bitwise dạy đủ. |
| Day 4 — Strings | `py.core.strings` | Thiếu một số method (xem §3). |
| Day 5 — Lists | `py.datastructs.list` | Thiếu vài method list. |
| Day 6 — Tuples | `py.datastructs.tuple_namedtuple` | App là superset (thêm namedtuple, *rest). |
| Day 7 — Sets | `py.datastructs.dict` (phần "Dict và set") | Set gộp chung bài dict; thiếu nhiều set method. |
| Day 8 — Dictionaries | `py.datastructs.dict` | Bao phủ tốt. |
| Day 9 — Conditionals | `py.core.conditionals` | App sâu hơn (truthy/falsy, assert). |
| Day 10 — Loops | `py.core.loops` | Bao phủ đầy đủ (kể cả for-else). |
| Day 11 — Functions | `py.functions.def_args` | Bao phủ tốt + sâu hơn. |
| Day 12 — Modules | **— none yet** | Không có subtopic riêng (os/sys/random/statistics/string). |
| Day 13 — List Comprehension (+ lambda) | `py.datastructs.comprehensions` (+ phần lambda → `py.functions.lambda_hof`) | |
| Day 14 — Higher Order Functions | `py.functions.lambda_hof` (+ closure → `py.functions.scope_closures`) | **Decorator** chưa dạy (xem §3). |
| Day 15 — Python Type Errors | **— none yet** | Chỉ có phần đọc traceback trong `getting_started`. |
| Day 16 — DateTime | **— none yet** | |
| Day 17 — Exception Handling | **— none yet** | `try/except` mới xuất hiện lẻ trong `classes_basics`; packing/unpacking → `tuple_namedtuple`. |
| Day 18 — Regular Expressions | **— none yet** | |
| Day 19 — File Handling | **— none yet** | |
| Day 21 — Classes and Objects | `py.oop.classes_basics` | Thiếu inheritance/super/overriding (xem §3). |

**Days KHÔNG có app subtopic tương ứng** (ứng viên subtopic tương lai, *ngoài scope hiện tại*): **Day 12 (Modules),
Day 15 (Type Errors), Day 16 (DateTime), Day 17 (Exception Handling), Day 18 (Regex), Day 19 (File Handling)**. Các Day
20, 22–30 nằm ngoài phạm vi Fundamentals.

**App subtopic KHÔNG bắt nguồn từ 30-Days** (nội dung app-only, sâu hơn khoá — không có "gap" so với khoá):
`py.datastructs.collections_module` (Counter/defaultdict/deque), `py.datastructs.copying_mutability`,
`py.datastructs.heapq_bisect`, phần lớn `py.functions.sorting_keys`. 30-Days không dạy những phần này.

## 3. Phân tích từng app py subtopic

Quy ước đếm: **CE** = số `code_exercise` block trong lesson; **PB** = số thư mục problem *thực* trong
`content/problems/<id>/` (đã loại các slug `check-*`, vốn là mastery-check `kind:check`). Mục tiêu ≥ 3 = **CE + PB ≥ 3**.

### 3.1 `py.core.getting_started` — Day 1
File: `content/lessons/py/py.core.getting_started.yaml`
- **Concept covered vs missing:** App vượt Day 1 (REPL/script, indentation/PEP 8, comment/docstring, `import math`,
  đọc traceback). **Missing (từ Day 2 cạnh bên):** `input()` để đọc dữ liệu người dùng.
- **Exercises:** CE=1 (`circle_area`), PB=1 (`add-two-integers`) → **2, dưới 3**. Day 1 không có exercise nào
  trong exercises-index, nên nguồn yếu; mượn ý Day 2. **Đề xuất +1:** một bài nhỏ dùng `print`/định dạng hoặc
  `math` (ví dụ `greet_line(name)` hay `circle_circumference(r)`).

### 3.2 `py.core.variables_types` — Day 2
File: `content/lessons/py/py.core.variables_types.yaml`
- **Covered:** `type`, `isinstance`, `int/float/str/bool/None`, dynamic vs strong typing, sai số float, gán nhiều
  biến/swap, `int()/float()/str()`. **Missing vs Day 2:** `input()`, kiểu `complex`, `dir()`, `help()`,
  khảo sát built-in rộng (Day 2 liệt kê `min/max/sum/sorted/len/open` như built-in cần biết).
- **Exercises:** CE=2 (`total_cost`, `sum_equals`), PB=1 (`number-of-good-pairs`) → **3, đạt**. Có thể enrich từ Day 2:
  `circle_area_and_circumference(r)`, so sánh độ dài hai chuỗi.

### 3.3 `py.core.operators` — Day 3
File: `content/lessons/py/py.core.operators.yaml`
- **Covered:** `//`, `%`, `**`, `divmod`, số âm, `==` vs `is`, chained comparison, short-circuit, augmented assign,
  precedence, `round` banker, `math.sqrt/isqrt/gcd/floor/ceil`. **Missing vs Day 3:** kiểu **`complex`** (Day 3 dạy
  khai báo & in type), bitwise được *dạy đủ* (app chỉ nhắc), các công thức hình học.
- **Exercises:** CE=1 (`wrap_hour`), PB=1 (`subtract-product-and-sum`) → **2, dưới 3**. Day 3 có **20 exercise**
  (nguồn rất giàu). **Đề xuất +2:** `triangle_area(base, height)`, `euclidean_distance(x1,y1,x2,y2)` hoặc
  `is_even(n)` (modulus), `seconds_in_years(n)`.

### 3.4 `py.core.strings` — Day 4
File: `content/lessons/py/py.core.strings.yaml`
- **Covered:** index/neg index/slicing, immutable, `split/join/strip/replace/find/rfind/count/startswith/endswith/
  lower/upper/title/capitalize/isdigit/isalpha/isalnum`, `in`, f-string + format spec, `str`/`bytes`.
- **Missing (có trong bảng method của Day 4):** `index`/`rindex` (raise error vs `find` trả -1), `swapcase`,
  `isidentifier`, `islower`/`isupper`, `isnumeric`/`isdecimal`, `expandtabs`, và hai kiểu format cũ: **`%`-formatting**
  và **`str.format()`** (app chỉ dạy f-string).
- **Exercises:** CE=2 (`swap_ends`, `initials`), PB=1 (`length-of-last-word`) → **3, đạt**. Enrich từ Day 4:
  acronym cho `"Python For Everyone"`, đảo chuỗi, tìm index của ký tự.

### 3.5 `py.core.conditionals` — Day 9
File: `content/lessons/py/py.core.conditionals.yaml`
- **Covered:** `if/elif/else`, thứ tự nhánh, biểu thức điều kiện, truthy/falsy, `is None`, `in`, `assert`, `pass`
  — sâu hơn Day 9.
- **Exercises:** CE=1 (`shipping_fee`), PB=1 (`fizz-buzz`) → **2, dưới 3**. Day 9 L1–L3 có 7 bài. **Đề xuất +2:**
  `grade(score)` (A/B/C/D/F), `compare_numbers(a, b)` (greater/smaller/equal), `years_to_drive(age)`.

### 3.6 `py.core.loops` — Day 10
File: `content/lessons/py/py.core.loops.yaml`
- **Covered:** `for`/`while`, `range` (3 dạng + step âm), accumulator, `break`/`continue`, nested loop, **for-else** —
  đầy đủ Day 10.
- **Exercises:** CE=4 (`count_vowels`, `collatz_steps`, `sum_skip`-fix, `is_prime`), PB=2 (`fix-sum-positives`,
  `ugly-number`) → **6, đạt**. (Day 10 L3 dạng pattern/triangle/data-file có thể enrich nhưng cần data file.)

### 3.7 `py.datastructs.list` — Day 5
File: `content/lessons/py/py.datastructs.list.yaml`
- **Covered:** index/neg, `len/max/min/sum`, `append/pop/remove`, gán `ds[i]`, `sort` vs `sorted`, slicing,
  `append` vs `extend`, `enumerate`, `zip`, copy `a[:]`, hiệu năng `insert(0)/pop(0)/in`.
- **Missing (method có trong Day 5):** `insert(index, item)` (mới nhắc ở callout hiệu năng), `del lst[i]`, `clear()`,
  `count(item)`, `index(item)`, method `reverse()` (app chỉ có `[::-1]`), method `copy()`.
- **Exercises:** CE=1 (`rotate_right`), PB=1 (`concatenation-of-array`) → **2, dưới 3**. Day 5 có 14 exercise.
  **Đề xuất +2:** `list_stats(nums)` → `(min, max, sum)` hoặc median (ages list L2), `middle_element(lst)`,
  `insert_after(lst, target, item)`.

### 3.8 `py.datastructs.tuple_namedtuple` — Day 6
File: `content/lessons/py/py.datastructs.tuple_namedtuple.yaml`
- **Covered:** tuple immutable, `(x,)`, index/slice/`len`/`in`, unpacking + swap + `*rest`, hashable/khoá dict,
  `namedtuple` — **superset của Day 6** (Day 6 không có namedtuple/`*rest`).
- **Missing vs Day 6:** gần như không; có thể làm rõ chuyển đổi `tuple↔list` và join `+`.
- **Exercises:** CE=1 (`split_head`), PB=1 (`flipping-an-image`) → **2, dưới 3**. **Đề xuất +2** (ý từ Day 6 & Day 17
  unpacking): `merge_tuples(a, b)`, `tuple_contains(t, x)`, hoặc `first_middle_last(t)` dùng unpacking/`*rest`.

### 3.9 `py.datastructs.dict` (+ Set) — Day 7 & Day 8
File: `content/lessons/py/py.datastructs.dict.yaml`
- **Covered (dict):** tạo/tra/thêm/sửa, `.get`, `KeyError`, đếm bằng `.get`, nhóm `setdefault`, `.items()`, O(1).
  **Covered (set):** loại trùng, `|`/`&`/`-`/`^`, hashable.
- **Missing vs Day 8:** `pop(key)`, `popitem()`, `del d[k]`, `keys()`/`values()` (có `.items()`), `clear()`, `copy()`,
  `update()`. **Missing vs Day 7 (Sets):** `add`, `update`, `remove` vs `discard`, `pop`, `issubset`/`issuperset`/
  `isdisjoint`, `union/intersection/difference/symmetric_difference` (app chỉ dạy dạng toán tử, không dạy method).
- **Exercises:** CE=1 (`unique_sorted`), PB=4 (`confusion-counts`, `fix-char-count`, `ransom-note`,
  `write-test-char-count`) → **5, đạt**. (Có thể thêm 1 bài thuần *set* để cân bằng với phần set.)

### 3.10 `py.datastructs.comprehensions` — Day 13
File: `content/lessons/py/py.datastructs.comprehensions.yaml`
- **Covered:** list comp (filter `if` + ternary), flatten/nested, dict comp, set comp, generator expression, giới hạn
  dễ đọc. **Missing vs Day 13:** sinh **list các tuple** `(i, i**0..i**6)` bằng comprehension; phần **lambda** của
  Day 13 (đã chuyển sang `lambda_hof` — hợp lý).
- **Exercises:** CE=2 (`squares_of_odds`, `flatten`), PB=1 (`how-many-numbers-are-smaller-than-the-current-number`)
  → **3, đạt**. Enrich: `powers_table(n)`, `names_to_fullnames(pairs)`, `rows_to_dicts(rows)`.

### 3.11 `py.datastructs.collections_module` — (không có Day tương ứng)
File: `content/lessons/py/py.datastructs.collections_module.yaml`
- 30-Days **không dạy** `Counter/defaultdict/deque/OrderedDict` → **không có gap từ khoá**; đây là nội dung app-only.
- **Exercises:** CE=2 (`top_word`, `group_by_first`), PB=1 (`majority-element`) → **3, đạt**.

### 3.12 `py.datastructs.copying_mutability` — (không có Day tương ứng)
File: `content/lessons/py/py.datastructs.copying_mutability.yaml`
- Không có trong 30-Days (aliasing, shallow/deep copy, bẫy `[[0]*n]*m`, `+=` list vs tuple) → app-only, không gap khoá.
- **Exercises:** CE=2 (`prefix_snapshots`, `grid_with`), PB=2 (`pascals-triangle`, `rotate-array`) → **4, đạt**.

### 3.13 `py.datastructs.heapq_bisect` — (không có Day tương ứng)
File: `content/lessons/py/py.datastructs.heapq_bisect.yaml`
- Không có trong 30-Days → app-only, không gap khoá.
- **Exercises:** CE=2 (`sum_of_k_largest`, `insert_position`), PB=1 (`running-kth-largest`) → **3, đạt**.

### 3.14 `py.functions.def_args` — Day 11
File: `content/lessons/py/py.functions.def_args.yaml`
- **Covered:** `def/return`, trả `None`, trả tuple, đối số vị trí/tên, default, bẫy mutable default, `*args`/`**kwargs`,
  giải nén `*`/`**`, pass-by-object-reference, docstring/annotation — **bao phủ đầy đủ + sâu hơn Day 11**.
- **Exercises:** CE=2 (`append_to`, `sum_of_squares`), PB=4 (`compute-prf`, `create-target-array-in-the-given-order`,
  `fibonacci-number`, `fix-collect-evens`) → **6, đạt**.

### 3.15 `py.functions.lambda_hof` — Day 14 (+ lambda của Day 13)
File: `content/lessons/py/py.functions.lambda_hof.yaml`
- **Covered:** hàm là giá trị, `lambda`, `map`/`filter` (iterator → `list()`), `reduce`, `partial`, `operator`.
- **Missing vs Day 14:** **Decorator** (`@decorator`, xếp chồng bottom-to-top) — **chưa dạy ở bất kỳ bài nào**
  (closure nằm ở `scope_closures`, nhưng decorator thì thiếu hẳn).
- **Exercises:** CE=2 (`evens_squared`, `product`), PB=1 (`height-checker`) → **3, đạt**. Day 14 có 22 exercise;
  enrich: `to_upper(words)` (map), `filter_startswith(words, ch)`, `chain_sum(nums)` (map+filter+reduce).

### 3.16 `py.functions.scope_closures` — Day 14 (closures/decorators)
File: `content/lessons/py/py.functions.scope_closures.yaml`
- **Covered:** scope local/global, LEGB, `global`/`nonlocal`, `UnboundLocalError`, closure, late binding.
  **Missing vs Day 14:** **decorator** (giống §3.15).
- **Exercises:** **CE=0, PB=0 → 0, GAP LỚN NHẤT.** Chưa có thư mục `content/problems/py.functions.scope_closures/`.
  Day 14 exercises phần lớn dựa trên data-file nên phải **tự author** quanh concept closure/decorator. **Đề xuất +3:**
  `make_counter()` (closure giữ trạng thái), `make_multiplier(k)` → hàm nhân, `fix_late_binding()` / một decorator nhỏ
  (`double_result`). Vì closure trả hàm khó kiểm thử kiểu LeetCode, các bài này cần harness gọi hàm trả về — lưu ý khi
  đưa qua pipeline.

### 3.17 `py.functions.sorting_keys` — (một phần Day 14 L3 / Day 5)
File: `content/lessons/py/py.functions.sorting_keys.yaml`
- **Covered:** `sorted` vs `list.sort` (trả `None`), `reverse`, `key` (`len/abs/str.lower`/lambda), stable (Timsort),
  key là tuple + đổi dấu, sort dict theo value, `itemgetter` — **đầy đủ, sâu hơn khoá**.
- **Exercises:** CE=2 (`sort_by_abs`, `top_words`), PB=1 (`rank-students`) → **3, đạt**.

### 3.18 `py.oop.classes_basics` — Day 21
File: `content/lessons/py/py.oop.classes_basics.yaml`
- **Covered:** `class`/`__init__`/`self`, instance attribute & method, bẫy class attribute dùng chung, `@property` +
  setter (`@property` không có trong Day 21 — app thêm). **Missing vs Day 21:** **inheritance** (`class Child(Parent)`),
  **`super().__init__()`**, **method overriding**, và default param trong constructor.
- **Exercises:** CE=4 (`make_student`, `final_balance`, `two_baskets`, `try_scores`), PB=0 → **4, đạt về số lượng**
  nhưng **không có problem độc lập nào** (chỉ `check-q077`). Day 21 cho 2 bài class giàu: **`Statistics`**
  (count/sum/min/max/range/mean/median/mode/std/var/freq_dist/describe) và **`PersonAccount`** (incomes/expenses/
  total/balance). **Đề xuất:** thêm 1 problem kiểu `Statistics`/`PersonAccount`, và 1 bài **inheritance** (`Student(Person)`
  + `super`) để đóng concept gap.

## 4. Top-up backlog (ưu tiên)

| Subtopic | #exercises cần thêm | Nguồn (Day) | Effort | Ghi chú |
|---|---:|---|:---:|---|
| `py.functions.scope_closures` | 3 | Day 14 | **M** | Đang 0 bài; closure/decorator trả hàm → cần harness gọi hàm trả về. |
| `py.core.operators` | 2 | Day 3 | **S** | Nguồn 20 exercise, dễ (hình học/modulus). |
| `py.core.conditionals` | 2 | Day 9 | **S** | `grade`, `compare_numbers`. |
| `py.datastructs.list` | 2 | Day 5 | **S** | list stats, middle, insert_after. |
| `py.datastructs.tuple_namedtuple` | 2 | Day 6 / Day 17 | **S** | merge/contains, unpacking. |
| `py.core.getting_started` | 1–2 | Day 1 / Day 2 | **S** | Day 1 không có exercise; mượn ý Day 2. |
| `py.oop.classes_basics` | 1–2 | Day 21 | **L** | Thêm problem `Statistics`/`PersonAccount` + concept inheritance/super. |
| `py.functions.lambda_hof` | 1 (enrich) | Day 14 | **S** | Đã đạt 3; + concept **decorator**. |
| `py.core.strings` | 0 (enrich) | Day 4 | **S** | Đã đạt 3; bổ sung concept `index/rindex/swapcase/%-format/.format`. |

**Concept gaps (không phải thiếu số lượng bài, mà thiếu nội dung):** decorator (`lambda_hof`/`scope_closures`),
inheritance + `super()` + overriding (`classes_basics`), `input()` (`getting_started`/`variables_types`),
nhóm string method của Day 4, set method của Day 7 (`dict` lesson), dict method của Day 8.

---

## 5. Tóm tắt 5 gap lớn nhất

1. **`py.functions.scope_closures` không có bài luyện nào (0 code_exercise, 0 problem)** — gap nghiêm trọng nhất; cần ≥ 3 bài (make_counter, make_multiplier, fix late-binding / decorator nhỏ).
2. **Decorator (Day 14) chưa được dạy** ở bất kỳ bài nào, dù closure và map/filter/reduce đã có — thiếu một concept cốt lõi của higher-order functions.
3. **Inheritance / `super()` / method overriding (Day 21) vắng mặt** trong `classes_basics`, và subtopic này chưa có problem độc lập (chỉ có check item).
4. **Bốn lesson core dưới ngưỡng 3 bài:** `getting_started` (2), `operators` (2), `conditionals` (2), `list` (2), cộng `tuple_namedtuple` (2) — trong khi Day 3/5/9 của khoá có nguồn exercise rất dồi dào để bổ sung.
5. **Sáu Day của khoá chưa có subtopic nào** (Day 12 Modules, 15 Type Errors, 16 DateTime, 17 Exception Handling, 18 Regex, 19 File Handling) và một loạt built-in/string/set/dict method bị thiếu — nằm ngoài scope hiện tại nhưng là ứng viên rõ ràng cho subtopic/nội dung tương lai.
