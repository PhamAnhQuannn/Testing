# Review: ml.fundamentals.reinforcement_learning_basics

**Verdict: PASS — no must-fix. Technically accurate, Q-update arithmetic verified, ready to publish.**

Reviewer: independent content review (AI-engineer concept track). Date: 2026-10-27.

## Technical accuracy & currency
- RL loop: agent / environment / state / action / reward / policy; objective = discounted cumulative reward (γ). Correct.
- Exploration vs exploitation + ε-greedy. Correct.
- Bellman update stated correctly: Q(s,a) ← Q(s,a) + α·[r + γ·max Q(s',·) − Q(s,a)]; terms (TD error, learning rate α, discount γ) explained correctly.
- RLHF reuses reward/punishment idea: reward model = environment/scorer, policy = the LLM, RL pushes LLM toward higher reward. Correct, matches checklist.

## Hand-worked Q-updates (recomputed — all correct)
- b02 value intuition: 1 + 0.9×10 = 10. Correct.
- Step 1 (2→3): Q(2,right) ← 0 + 0.5×[10 + 0.9×0 − 0] = **5**. Correct.
- Step 2 (1→2): Q(1,right) ← 0 + 0.5×[−1 + 0.9×5 − 0] = 0.5×[−1+4.5] = 0.5×3.5 = **1.75**. Correct.
- Fill b07 (1.75) and quiz b08 (role of α) correct; value back-propagation explanation sound.

## Quizzes
- b04 (delivery agent only exploiting → add exploration/ε-greedy, ans a), b08 (α = step size, ans a): correct; distractors sound (γ≠α confusion explicitly corrected).

## Mastery items
- S370 diff1 recall (name 6 components + objective): right level.
- S371 diff2 (hand-compute Q(2) then Q(1) + explain back-prop): right level, both numbers correct in answer and rubric.
- S372 diff3 interview (2-step Q by hand + Bellman/policy in words + why RLHF uses reward): matches mastery_bar_vi ("tính tay 2 bước cập nhật Q... giải thích Bellman và policy bằng lời... vì sao alignment dùng ý tưởng thưởng/phạt"). Rubric aligns.

## Prior-concept reuse & language
- Builds toward alignment_rlhf_dpo (explicitly defers PPO/DPO detail). Dog-training analogy is intuitive. Vietnamese clear; English terms parenthesized (reward, policy, discount, Bellman, ε-greedy, reward model, RLHF).
