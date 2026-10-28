# Review: ml.rag_agents.agent_fundamentals

**Verdict: PASS (clean, publishable).** Independent content review, 2026-10-27.

## Technical accuracy & currency
- Agent = LLM in a loop (observe → decide tool → act → read result → repeat), contrasted correctly with one-shot prompt. Model proposes tool calls; program executes. Correct.
- Tools via function-calling with JSON-schema signatures — correct, and correctly framed as reuse of structured-output/function-calling.
- Agent loop = ReAct (reason → act → observe); memory/context short-term (in context) vs long-term (external store); stop condition + step budget. All correct.
- **MCP** described correctly as an open standard (2024-25) to connect models to tools/data via a uniform interface ("USB-C for tools"), reusable across apps/clients, sitting on top of function-calling. Accurate and current (MCP introduced late 2024).
- Agent vs fixed workflow/RAG decision correct: use agent for open, multi-step, external-action tasks; fixed workflow when steps are predictable (RAG = fixed pipeline). "Simplest thing that works" principle correct.

## Quiz / fill items
- b04 (a), b07 (a), b09 (a), b10 (step budget): all `answer` + `explain_md` correct. Distractors target real misconceptions (agent = fine-tuned model — false; agent cheaper — false; MCP = new model / compression — false).

## Mastery items
- S301 diff1 recall: agent vs one-shot + three pillars; rubric allows 2 of 3 pillars. Right level.
- S302 diff2: CSV date reformat (workflow) vs travel booking (agent) + a risk of over-using agents. Matches lesson.
- S303 diff3 interview: matches `mastery_bar_vi` (build small bounded agent loop, design tools with descriptions + useful errors, say when fixed workflow beats agent). Rubric requires loop + step budget + MCP + agent-vs-workflow criteria. Right level; bonus for human confirmation on side-effecting tools.
- Mastery items stay within lesson scope.

## Vietnamese + terms
Clear; terms parenthesized (loop, one-shot, ReAct, JSON-schema, function calling, MCP, step budget/max_steps, human-in-the-loop).

No must-fix items.
