# Review: sd.framework.requirements (independent reviewer pass)

**Verdict: OK** (no must-fix)

10 blocks; graded: b04 (mcq), b06 (fill), b08 (mcq). mastery_check l1[S028] l2[S029] l3[S030].
mastery_bar_vi: "trong 5 phút hỏi đủ bộ câu hỏi, ghi ra FR/NFR có ưu tiên, chốt phạm vi" — S030 matches.

## Technical accuracy
- FR = what the system does; NFR = how well. NFR axes (scale/DAU/QPS, latency, availability, consistency, durability, security, cost) + read-heavy vs write-heavy question — complete and current.
- Per-feature consistency (balance=strong, like-count=eventual) is the correct nuance, not a system-wide knob.
- Clarifying-question set and lock-scope / MVP-vs-nice-to-have advice are standard and correct.

## Quiz / mastery correctness
- b04 [b] latency+uptime = NFR — correct; (a)/(c) are FRs, correctly refuted.
- b06 fill: strong / eventual — correct.
- b08 [a] lock scope keeps focus — correct; (b) "runtime speed" and (c) "can't change requirements" correctly refuted (explain clarifies lock != frozen).
- S028 (L1): FR vs NFR + ≥3 axes; rubric sensible.
- S029 (L2 gate): Instagram — 3 FR, 3 NFR on different axes, 1 out-of-scope, strong-vs-eventual with reason. Correct; rubric requires distinct axes (not 3 latency variants) — good gate.
- S030 (L3): self-chosen prompt (URL shortener example), full question set + prioritized FR/NFR + scope sentence + why. Matches bar.

## Consistency
Feeds step 1 of the overview pipeline; DAU/QPS/read-heavy framing explicitly handed to the estimation subtopic (step 2). strong/eventual terminology consistent with sd.fundamentals.cap_consistency.

## Language
Vietnamese clear; English terms parenthesized (functional/non-functional, NFR, DAU, QPS, strong/eventual, MVP, lock scope). Good.
