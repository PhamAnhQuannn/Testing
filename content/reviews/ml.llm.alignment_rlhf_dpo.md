# Review: ml.llm.alignment_rlhf_dpo

**Verdict: OK** (clean — no must-fix)

Independent content review (AI-engineer / LLM concept track, currency target 2026).

## Technical accuracy
- Alignment placement correct: after pretraining + SFT; make output match human preferences (HHH); preference data = prompt + chosen + rejected; pairwise comparison more reliable than absolute scoring (b01, b02).
- **RLHF correct and matches special-check**: 3 steps — collect preference pairs → train reward model (Bradley-Terry) → optimize policy with PPO + KL penalty vs a frozen SFT reference model. Four models held at train time (policy, reference, reward, critic/value). Accurate (b03, b06).
- Reward hacking / over-optimization correct, with KL penalty and not-over-optimizing as mitigations; sycophancy and length-bias examples correct (b04, b05).
- **DPO correct and matches special-check**: removes the separate reward model AND the RL/PPO loop; trains directly on chosen/rejected with a simple loss; reward is *implicit* in the loss; reference model + beta; simpler/cheaper/more stable. b06/b07 explicitly state DPO has no separately-trained reward model. Accurate.
- **GRPO correct**: RL variant for reasoning models (DeepSeek-R1 lineage); group of samples, group-relative advantage, NO critic/value model; pairs with RLVR (verifiable rewards for math/code). The PPO (critic+RM) vs DPO (no RL/RM) vs GRPO (RL, no critic, group/verifiable reward) contrast is correct (b08, b09 fill).
- RLAIF / constitutional AI correctly described as AI-judge variants producing the same chosen/rejected pairs (b02).

## Quiz / mastery correctness
- b05 (→ a, KL keeps policy near reference / anti reward-hacking), b07 (→ a, DPO drops RM + RL, implicit reward), b09 fill (GRPO) — all correct. Distractors correctly reject "KL replaces the reward model", "DPO = RLHF renamed", "GRPO needs a critic".
- S283 (L1), S284 (L2 score-2: RLHF pipeline + why DPO + reward hacking), S285 (L3 interview: compare SFT/RLHF-PPO/DPO/GRPO across data, objective, RM/critic, stability) — correct, rubrics sensible, levels right. S285 maps exactly to `mastery_bar_vi`.

## Coverage discipline
- Mastery items test only taught ideas (RLVR, constitutional AI, reward hacking all taught). Good.

## Language
- Vietnamese clear; English terms parenthesized (preference pairs, reward model, PPO, KL penalty, reference model, DPO, beta, GRPO, RLVR, reward hacking, sycophancy).

## Nice-to-have
- None material.
