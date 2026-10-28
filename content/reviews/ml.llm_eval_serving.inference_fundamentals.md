# Review: ml.llm_eval_serving.inference_fundamentals

**Reviewer:** independent content reviewer (AI-engineer track)
**Date:** 2026-10-27
**Verdict: PASS — no must-fix.** Accurate, current (2026); all memory/KV arithmetic verified; quizzes and mastery items correct.

## Technical accuracy & currency (numbers verified)
- Prefill = whole prompt in one pass, **compute-bound**, sets **TTFT**; decode = one token/step, autoregressive, **memory-bandwidth-bound** (re-reads all weights per token), sets **TPOT/ITL + throughput**. Correct, matches SPECIAL check.
- **KV cache**: stores K/V of past tokens → O(1) per step vs recompute O(n); grows with **batch × sequence length**, can exceed weights at long context. Correct, matches SPECIAL check.
- **Weights = params × bytes/param; fp16 = 2 B/param → 7B = 14 GB** ✓; 13B ≈ 26 GB ✓; int8 ≈ 7 GB ✓; int4 ≈ 3.5 GB ✓. Matches SPECIAL check.
- KV formula `2 × layers × kv_head × head_dim × bytes × tokens × batch`: worked example 2×32×8×128×2 = 131,072 B ≈ 0.13 MB/token ✓; ×4000 ≈ 0.5 GB ✓; 32 kv_head variant = 524,288 B/token, ×4000 ≈ 2 GB = 4× ✓ (shows GQA/MQA benefit). head_dim = hidden/heads (4096/32=128) ✓.
- Decode memory-bound → **batching** amortizes one weight-read across many sequences, raises throughput (costs extra KV, may raise per-request latency) — correct. GQA/MQA shrink KV via shared K/V — correct.

## Quizzes
- b04 [a] decode memory-bound / prefill compute-bound — correct; option (c) is the reversed claim, rightly wrong.
- b09 fill "14" (GB) — correct; explain gives the 2×(billions) mnemonic.
- b10 [a] batching exploits spare compute to raise throughput — correct; "read weights twice" / "drop KV cache" rightly rejected.

## Mastery items
- S322 (diff1): prefill vs decode + which latency each sets — right level; rubric penalizes swapping compute/memory-bound.
- S323 (diff2 scenario): 7B fp16, 4000 tokens → weights 14 GB + KV ~0.5 GB, why KV grows — numbers match lesson; rubric sensible.
- S324 (diff3 interview): memory budget (weights + KV formula + example) + TTFT/throughput from prefill/decode + batching + a KV-cutting lever (GQA/MQA) — matches `mastery_bar_vi`. Only tests taught ideas; FlashAttention caveat (speeds attention, not cache size) is accurate.

## Language
Vietnamese clear; English terms parenthesized (prefill, decode, compute-bound, memory-bandwidth-bound, KV cache, TTFT, TPOT/ITL, throughput, GQA/MQA).
