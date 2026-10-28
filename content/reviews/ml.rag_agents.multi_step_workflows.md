# Review: ml.rag_agents.multi_step_workflows

**Verdict: PASS (clean, publishable).** Independent content review, 2026-10-27.

## Technical accuracy & currency
- Fixed/orchestrated workflow vs autonomous agent contrast correct; "prefer the simplest thing that works / use fixed workflow when steps are known" is the right current guidance.
- Five patterns match the standard taxonomy exactly and are described correctly:
  - **Prompt chaining** (output → next input, optional gate),
  - **Routing** (classify then specialized branch),
  - **Parallelization** (fan-out + aggregate; sectioning vs voting),
  - **Orchestrator-workers** (dynamic subtask count, synthesize — correctly distinguished from parallelization),
  - **Evaluator-optimizer** (generate/critique/refine loop with a stop condition).
- Multi-agent cost correct: coordination overhead (token/latency) + error propagation; single well-designed agent or workflow usually wins for structured work; multi-agent only when subtasks are parallel, independent, context-heavy (context isolation pays off). Accurate and current.
- Long-running design: state/checkpoint + durable execution + queue, controlled retry (backoff, idempotent, bounded), human-in-the-loop at checkpoints. Correct.

## Quiz / fill items
- b04 (a), b06 (a), b08 (a), b10 (checkpoint): all `answer` + `explain_md` correct. Distractors reject "more agents always more accurate/cheaper" cleanly.

## Mastery items
- S307 diff1 recall: workflow vs agent + why prefer workflow for known steps. Right level.
- S308 diff2: support-ticket routing + chaining + human approval before refund. Matches lesson.
- S309 diff3 interview: matches `mastery_bar_vi` (pick right pattern + design flow with state, checkpoint, retry, human-review step; plus when multi-agent is NOT worth it). Research-assistant prompt fits orchestrator-workers; rubric requires checkpoint/resume + multi-agent tradeoff. Right level.
- Mastery items stay within lesson scope.

## Vietnamese + terms
Clear; terms parenthesized (orchestrated workflow, autonomous agent, prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer, coordination overhead, error propagation, checkpoint, durable execution, idempotent, human-in-the-loop).

No must-fix items.
