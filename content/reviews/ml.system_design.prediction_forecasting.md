# Review — ml.system_design.prediction_forecasting

**Verdict: PASS (publish-ready).** Accurate, current. No must-fix.

## Reviewed
- `content/lessons/ml/ml.system_design.prediction_forecasting.yaml`
- `content/checks_extra/ml.system_design.prediction_forecasting.yaml` (S343/S344/S345)

## Findings
- All three special-accuracy requirements nailed:
  - **No label leakage / point-in-time**: prediction-time t as the backbone; feature from before t, label from after t; golden rule point-in-time correctness; concrete traps (updated-after columns, post-t table state, global normalization before split); point-in-time snapshot / feature-store join (b01–b03). Correct.
  - **Time-ordered backtest, no random shuffle**: explicit "tuyệt đối không shuffle"; expanding + rolling-origin; gap = horizon between train and test (b05). Correct and complete (the gap detail is a strong, often-omitted point).
  - **Cost-aligned metric**: MAE/RMSE/MAPE with MAPE caveat (blows up near 0, asymmetric) ; asymmetric/quantile loss when over- vs under-forecast costs differ; prediction intervals (p10/p50/p90) (b07). Correct.
- Model section appropriate: baseline (yesterday / seasonal naive) → GBDT on lag/rolling/calendar/external features → deep (DeepAR/TFT) last; global model across many entities; cold start borrows similar group (b09). Current.
- Serving/lifecycle: batch vs real-time by latency need; drift monitoring + retrain; closing-the-loop interventions bias labels → uplift modeling (b10). Correct and nuanced.
- Quizzes correct: b04=b (account-closed flag is future info → leakage; a and c are point-in-time valid), b06=a (shuffle leaks future; use time split), b08 fill=asymmetric, b11=a (three pillars). Explanations sound.
- Mastery: S343 diff1 recall (leakage + point-in-time + example); S344 diff2 scenario (two eval errors + metric fix); S345 diff3 churn end-to-end matching mastery_bar_vi. Rubrics name leak-free / time-backtest / cost-metric as the required pillars — correct.
- Vietnamese clear; English terms parenthesized.

## Minor (non-blocking)
- None material.
