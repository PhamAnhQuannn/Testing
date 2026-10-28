# Review: sd.fundamentals.performance_metrics (independent reviewer pass)

**Verdict: OK** (no must-fix; 2 nice-to-have)

11 blocks; graded: b04 (mcq), b06 (fill), b08 (mcq). mastery_check l1 [S004], l2 [S005], l3 [S006].
mastery_bar_vi: "đổi số chín sang phút chết/năm, tính availability chuỗi nối tiếp và cụm song song, giải thích vì sao p99 > trung bình" — S006 covers all three.

## Math (verified independently)
- 1 year = 525,600 min. OK.
- 99.9% -> 525.6 min ~= 8.76 h (lesson "526 min ~= 8.8 giờ"). OK.
- 99.99% -> 52.56 min ~= 53 min. OK.
- 99.999% -> 5.256 min ~= 5 min. OK.
- Fan-out: 0.99^10 = 0.9044 (~90% all-fast, ~10% slow). OK.
- Serial 3x 99.9%: 0.999^3 = 0.99700 ~= 99.7%. OK.
- Parallel 2x 99.9%: 1 - 0.001^2 = 0.999999 = 99.9999%. OK.
- S006: 3 parallel clusters in series 0.999999^3 = 0.999997 ~= 99.9997%. OK.

## Quiz / mastery correctness
- b04 answer [b] correct (mean hides tail). See nice-to-have N1 on the explain text.
- b06 fill: 52.56 ~= 53; accept list reasonable (see N2).
- b08 answer [b] (0.999^3 ~= 99.7%) correct; (c) correctly tagged as the parallel formula.
- S004 (L1): latency vs throughput, units, one-vs-total — correct, rubric two-sided.
- S005 (L2 gate): serial 99.7% + parallel 99.9999% with the two "why" explanations; rubric requires both reasons. Genuine scenario application. Good.
- S006 (L3 interview): all three mastery-bar skills, calculations correct, qualitative redundancy reasoning sound. Matches bar.
- SLI < SLO <= SLA + error budget (b09), durability vs availability (b05): correct.

## Coverage discipline
Mastery items test only taught ideas (latency/throughput, nines->minutes, serial/parallel math, p99 vs mean, fan-out). No leakage.

## Language
Vietnamese clear; English terms parenthesised on first use (latency, throughput, bandwidth, percentile, tail latency, availability, SLI/SLO/SLA, error budget).

## Findings
- **nice-to-have N1:** b04 explain_md says "p99 luôn lớn hơn hoặc bằng mean theo định nghĩa" — not a definitional truth (an extreme tail beyond p99 can pull mean above p99, e.g. 99 values of 0 + one of 1000 -> p99~=0, mean=10). It holds for typical right-skewed latency distributions but is not "theo định nghĩa". Suggest softening to "với phân phối latency thực tế (lệch phải), p99 hầu như luôn >= mean". The answer [b] is unaffected.
- **nice-to-have N2:** b06 accept list includes "52" and "52.6" though the prompt says "làm tròn tới phút" -> 53. Lenient but not harmful; could drop "52".
