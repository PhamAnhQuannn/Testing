# Review: ml.llm.structured_output_tools

**Verdict: OK** (clean — no must-fix)

Independent content review (AI-engineer / LLM concept track, currency target 2026).

## Technical accuracy
- Rationale for structured output (code, not a human, consumes the answer) correct.
- Three escalating levels: prompt-only (no guarantee) → JSON mode (valid JSON, parseable, but NOT schema-adherent) → structured outputs / schema-constrained decoding (valid AND schema-adherent via constrained decoding, i.e. logit masking to -inf on tokens that would break the schema). Correct and current; the "JSON mode = valid; structured outputs = valid *and* schema" distinction is accurate.
- validate + retry loop: parse + validate (JSON Schema / Pydantic) → retry **with the specific validation error fed back** → bounded retries (2-3) → fallback/degrade, never infinite. Correct.
- function/tool calling 4-step loop correct, with the key point that the **model only proposes** a call and **your code runs it** and returns a tool message; loop until final answer with a step limit. Correct.
- tool_choice (auto / required / specific), parallel tool calls, strict mode, enums, clear names/descriptions. Correct.
- failure handling: stop reason = max_tokens (truncation → JSON cut off, raise limit / split / retry), refusal (detect, do NOT parse as JSON, handle separately), tool error/timeout (catch, return an error tool message so the model recovers, never fabricate, always timeout + loop cap). Correct.

## Quiz / mastery correctness
- b03 (→ b), b07 (→ b, model only proposes), b10 (→ b, error tool message + loop cap), b05 fill (validation error / retry limit) — all answers/explanations correct; distractors correctly reject "model runs the function" and "fabricate a result".
- S022 (L1), S023 (L2 score-2: missing `total` field), S024 (L3 interview: JSON pipeline + full tool loop, who-runs-what, refusal, tool error) — correct; L3 matches mastery_bar exactly.

## Coverage discipline
- Mastery items test only taught ideas. Good.

## Language
- Vietnamese clear; English terms in parentheses.

## Nice-to-have
- None material.
