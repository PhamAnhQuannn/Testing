# Review: ml.llm.finetuning_peft

**Verdict: OK** (clean — no must-fix)

Independent content review (AI-engineer / LLM concept track, currency target 2026).

## Technical accuracy
- SFT correct: teach an existing model with (input → desired output) pairs to change behavior/tone/format; quality > quantity; loss masking = loss only on the answer tokens, not the prompt. Correct (b01, b04).
- **LoRA correct and matches special-check**: base weight matrix W is FROZEN; trains two small matrices B, A (adapter); runs as W + (alpha/r)·B·A; rank r small (8/16); adapters are swappable. b07 distractors correctly reject "updates all of W" (that's full fine-tune) and "removes layers". Memory math verified: W 4096×4096 = 16,777,216; r=8 → B(4096×8)+A(8×4096) = 65,536 ≈ 0.39% ≈ 0.4%. Correct (b05, b06).
- **QLoRA correct and matches special-check**: 4-bit quantized frozen base + LoRA adapter on top. Memory verified: 7B ≈ 14 GB FP16 → ≈ 3.5 GB at 4-bit (7B × 0.5 B/param), fits one mid-range GPU (b08, b09 fill).
- **"behavior/format, not fresh knowledge → RAG" correct**: b01, b03 — new/changing company policy is a knowledge problem → RAG; fine-tune doesn't inject facts reliably and must retrain on change. Matches special-check.
- Full fine-tune memory (weights + gradients + optimizer state) and catastrophic forgetting, with hold-out eval before/after including old tasks — correct (b05, b10).

## Quiz / mastery correctness
- b03 (→ a, RAG for new policy), b07 (→ a, LoRA freezes W), b09 fill (4-bit / LoRA) — all correct.
- S280 (L1: SFT + LoRA vs full), S281 (L2 score-2: mid-range GPU → QLoRA, with memory reasoning + hold-out proof), S282 (L3 interview) — correct, rubrics sensible, levels right. S282 maps exactly to `mastery_bar_vi` (LoRA/QLoRA + memory calc, SFT data + loss masking, before/after hold-out eval).

## Coverage discipline
- Mastery items test only taught ideas. Good.

## Language
- Vietnamese clear; English terms parenthesized (SFT, PEFT, LoRA, QLoRA, adapter, rank, loss masking, hold-out, catastrophic forgetting, quantize).

## Nice-to-have
- None material.
