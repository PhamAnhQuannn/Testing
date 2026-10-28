# Review: sd.fundamentals.scalability (independent reviewer pass)

**Verdict: OK** (no must-fix; 1 nice-to-have)

9 blocks; graded quiz_mcq: b03, b05, b06. mastery_check l1 [S001], l2 [S002], l3 [S003].
mastery_bar_vi: "kể đúng lộ trình 5 bước ... và chỉ ra cái gì nghẽn ở mỗi bước" — S003 matches it exactly.

## Technical accuracy (verified)
- Vertical vs horizontal: vertical = hard ceiling + single point of failure; horizontal = ~no ceiling, better fault tolerance but needs load-splittable workload. Correct and standard.
- Stateless-as-precondition-for-horizontal framing, externalising session to DB/cache, sticky-session caveat for stateful: all correct.
- 5-step roadmap (1 box -> split tiers -> N app servers + LB -> cache + read replica -> sharding/multi-region) and the shifting bottleneck at each step (single machine -> single app/DB -> shared DB -> write load -> shard ops complexity): technically sound; bottleneck-driven progression is exactly what interviewers reward.
- b08 scalability != performance distinction correct.

## Quiz / mastery correctness
- b03 answer [b] correct; distractors (a) "always cheaper" and (c) "no LB needed" correctly refuted.
- b05 answer [b] (shared DB) correct; (a)/(c) correctly refuted.
- b06 answer [a] (stateless) correct; sticky-session (c) correctly framed as a patch.
- S001 (L1 recall): answer + rubric sensible, two-sided gate (miss one side -> max 0).
- S002 (L2, score-2 gate): a genuine scenario application (single machine CPU-bound -> next step). 3-part answer correct; rubric requires stateless + DB-bottleneck to pass. Good gate.
- S003 (L3, interview): full 5-step ordering + per-step bottleneck + why writes are hardest. Answer correct ("writes can't be replica-scaled like reads; funnel to primary; only sharding splits write load"). Matches mastery_bar_vi.

## Coverage discipline
All three mastery items test only ideas the lesson teaches (vertical/horizontal, stateless, 5-step roadmap, write bottleneck). No leakage to untaught concepts.

## Language
Vietnamese clear; English terms in parentheses on first use (scale up/out, load balancer, stateless, sharding, read replica). Good.

## Findings
- **nice-to-have:** S003 says only sharding splits write load; multi-leader/leaderless quorum also can, but that is out of scope for this subtopic — fine to leave as is.
