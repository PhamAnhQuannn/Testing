# Review: sd.archetypes.config_experiment

**Verdict: PASS** (independent content review, 2026). No must-fix.

## Technical accuracy
- Feature flag / remote config / kill switch and A/B testing unified as one platform (rule store + distribution + SDK + analytics) — correct framing.
- **Local SDK evaluation**: SDK loads full ruleset into process memory, background stream/poll refresh, evaluates in RAM — no per-check network call. Benefits correct: ~0 latency (no round-trip per request), fail-open on config-service outage (uses last-loaded ruleset), near-unbounded check volume; server only bears (CDN-cacheable) distribution load. Accurate.
- **Stable bucketing**: bucket = hash(user_id + experiment_id) mod 100, compare to percentage threshold. Three properties correct: deterministic/sticky (same user→same variant, no assignment table needed), even split (good hash spreads 0–99), independence across experiments (experiment_id in the hashed key). Correct.
- **Guardrail metrics**: metrics that must-not-regress (error rate, latency, crash); catch a variant that wins the target metric but harms the system → alert/stop. Correct. Plus gradual rollout + exposure logging. Accurate.

## Quizzes / mastery
- b05 local-eval = a correct; b07 fill hash / 100 / stable(sticky) correct; b08 hash-vs-random = b correct; b11 guardrail = a correct. Distractors well-chosen (b: "copy of user DB" false; c: "re-randomize" false).
- S208 (diff1): flag/kill switch/A-B — recall, right level.
- S209 (diff2): spot two flaws (network-per-check, random-per-check) + fixes (local eval, stable hash). Right level.
- S210 (diff3 interview): full platform + justify CDN, local eval, stable hash, guardrails. Matches mastery_bar. Rubrics sensible.

## Reuse (no re-teach)
Leans on CDN (distribution) by name without re-teaching. Good.

## Language
Clear Vietnamese; English terms parenthesized (local evaluation, fail-open, sticky bucketing, guardrail, exposure log). No issues.
