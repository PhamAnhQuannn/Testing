# Review: sd.distributed.failures_model (independent reviewer pass)

**Verdict: OK** (no must-fix; clean)

11 blocks; graded: b03 (mcq), b06 (fill), b09 (mcq). mastery_check l1 [S130], l2 [S131], l3 [S132].
mastery_bar_vi: "nêu các kiểu lỗi, giải thích vì sao timeout và heartbeat không tuyệt đối đúng và cách fencing token chặn hậu quả." — S132 covers all three pillars.

## Technical accuracy (verified)
- Failure types correctly named/distinguished: crash-stop, crash-recovery, omission, network partition, Byzantine. Byzantine correctly flagged as usually out-of-scope for internal/trusted datacenters (relevant to blockchain / mutually-distrusting parties). Correct.
- Partial failure framing (some nodes/network down, rest alive; live node cannot know peer's state) correct and well-motivated vs single machine.
- Timeout/heartbeat-as-guess argument correct: cannot distinguish dead / slow (GC pause) / dropped reply in an asynchronous network with no upper bound; heartbeat is "the same timeout guess repackaged", false-positive on GC pause / network blip. Accurate.
- Fencing token: monotonic increasing number issued per grant (A=33, B=34); **resource itself** checks and rejects any token lower than the max it has seen. Explicitly stops the stale actor without needing to know whether A really died — "blocks the consequence, not the wrong guess." Correct and precisely stated.
- Split-brain scenario (GC-paused leader/lock-holder wakes and writes) correct.

## Quiz / mastery correctness
- b03 [c] Byzantine out-of-scope internally: correct; a/b/d (crash-recovery, partition, omission) correctly framed as normal failures to handle.
- b06 fill: "timeout" + "heartbeat": correct; accept lists cover EN variants.
- b09 [b] resource compares token vs max-seen (34) and rejects 33: correct. Distractors refuted precisely — (a) no one knows A is dead, (c) A does not know it was replaced, (d) fencing does not fix the network.
- S130 (L1 recall): partial failure definition + why harder than single machine. Sensible, rubric sound.
- S131 (L2 score-2 scenario): 3+ alternatives to "B dead", timeout/heartbeat as guess, split-brain consequence. Good score-2 item; answer correct.
- S132 (L3 interview): all three pillars incl. who checks the token and what it checks. Matches mastery_bar; correct.

## Coverage discipline
Mastery items test only taught ideas (failure types, timeout/heartbeat guess, split brain, fencing). No leakage.

## Language
Vietnamese clear; English terms parenthesised (partial failure, crash-stop/recovery, omission, network partition, Byzantine, timeout, heartbeat, failure detector, GC pause, network blip, split brain, fencing token, monotonic, stale, resource, liveness/safety). Good.

## Findings
None blocking. Accurate and interview-correct.
