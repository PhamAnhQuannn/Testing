# Review: sd.archetypes.news_feed

**Verdict: PASS** (independent content review, 2026). No must-fix.

## Technical accuracy
- Push (fan-out on write): copy post id into each follower's feed cache at post time → read = 1 cache read (fast/stable); write = **F writes** (F = followers), pushed to background workers; wasted work for inactive followers. Correct.
- Pull (fan-out on read): post = 1 write; each open ≈ **K reads + 1 merge** (K = followees) → write cheap, read expensive. Correct.
- Numbers: celebrity with **10M followers** posting **1** post = **10M writes** under pure push; 5 posts/day = 50M writes/day for one account → infeasible (queue backlog, minutes of lag, cost). Correct and well-quantified.
- Hybrid: split by follower threshold — normal accounts push, celebrities pull; at read time merge prebuilt inbox (push from normal followees) with fresh posts from the few celebrities followed (pull = few reads). Correctly resolves the celebrity problem.
- Supporting details accurate: feed cache stores ids only (~200), media on CDN, cursor pagination (justified by new posts shifting offsets), chronological vs ranked, eventual consistency.

## Quizzes / mastery
- b04 pull→push = a correct; b06 10M writes = b correct (distractor a=pull, c="only online" false); b08 fill ghi / đọc / follower correct.
- S214 (diff1): push vs pull + which side is expensive — recall, right level.
- S215 (diff2): quantify F writes, 1M→1M writes, propose hybrid. Right level, numbers required by rubric.
- S216 (diff3 interview): architecture + numeric push/pull comparison + hybrid. Matches mastery_bar ("so sánh ... bằng con số ... xử lý người nổi tiếng bằng cách lai"). Rubrics sensible.

## Reuse (no re-teach)
Builds on social graph, sharded post store, distributed cache, task workers, CDN — assembled, not re-taught. Good.

## Language
Clear Vietnamese; English terms parenthesized (fan-out on write/read, celebrity problem, hybrid, cursor pagination, eventual consistency). No issues.
