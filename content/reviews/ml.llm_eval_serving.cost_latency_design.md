# Review: ml.llm_eval_serving.cost_latency_design

**Reviewer:** independent content reviewer (Opus), 2026-10-27
**Verdict: PASS — clean, mọi số học đã kiểm lại, không cần sửa.**

## Độ chính xác số học (đã tính lại độc lập — tất cả đúng)
- b02 capacity: 1.000 × 2/phút × 300 = 10.000 token/s cần; 10.000 ÷ 2.500 = 4 GPU @100%; 10.000 ÷ (2.500×0,70) = 5,71 → 6 GPU. ✓
- b04 quiz: 100 × 500 = 50.000 token/s ÷ 5.000 = 10 GPU. ✓
- b07 chi phí: 2.000 token/s × 3.600 = 7,2 triệu token/giờ; 2 ÷ 7,2 = 0,28 USD/1M @100%; @30% = 2 ÷ 2,16 = 0,93 USD/1M; tháng = 2 × 730 = 1.460 USD. ✓
- b08 break-even: 0,28 ÷ u = 0,60 → u ≈ 0,47 (47%). ✓
- S335: 10.000 token/s, 4→6 GPU; chi phí 2.000×3.600=7,2M → 0,28 USD/1M (dùng throughput thực 2.000, capacity dùng 2.500 — phân biệt "throughput ở ngưỡng độ trễ" vs "throughput thực tế", nhất quán, hợp lý). ✓
- S336: 50.000 token/s; 10 GPU @100%, ÷(5.000×0,70)=14,3 → ~14–15 GPU; chi phí 5.000×3.600=18M → 2÷18 = 0,11 USD/1M; break-even 0,11 ÷ u = 0,60 → u ≈ 0,18 (18%). ✓

## Độ chính xác khái niệm (2026)
- Đếm tokens/s thay vì QPS vì request dài ngắn khác nhau: đúng.
- prefill (compute-bound, quyết định TTFT) vs decode (memory-bound, per-token); context dài → prefill lâu + KV cache phình → tụt dung lượng: đúng.
- Thế căng latency ↔ throughput ↔ batch size, streaming + TTFT thấp: đúng.
- Break-even self-host vs API lập luận bằng ngưỡng mức bận (0,28/u = giá API): đúng cách tư duy, đúng số.
- Cost levers (model nhỏ/quantize ~2–4×, prompt cache ~50–90% input, cap max token, routing/cascade ~30–70%, batch offline ~50%, response/semantic cache, autoscale-to-0): đúng, ước lượng hợp lý; nhấn "output token đắt hơn input" chính xác.

## Quiz
- b04 (a), b06 (a), b09 (a), b11 fill "prompt cache": answer + explain_md đúng; distractor bác đúng (1 GPU/request sai; "vừa rẻ vừa nhanh mọi mặt" sai; self-host/API "luôn rẻ hơn" bị bác bằng ngưỡng mức bận).

## Mastery (khớp mastery_bar_vi "Mức 3: capacity (token/s, QPS, GPU) + chi phí + giảm chi phí + break-even self-host")
- S334 (diff1, recall): vì sao token/s + công thức token/s cần & số GPU — đúng.
- S335 (diff2, scenario score-2): capacity + chi phí + 2 levers — đúng số, rubric hợp lý.
- S336 (diff3, interview): capacity có dự phòng + break-even bằng số + ≥3 levers — khớp mastery_bar đầy đủ.
- Mọi item chỉ test ý đã dạy (b01–b10).

## Ngôn ngữ
Rõ, thuật ngữ Anh trong ngoặc (throughput, TTFT, break-even, headroom, prompt cache, routing/cascade). Dấu phẩy thập phân + chấm hàng nghìn kiểu VN nhất quán.

**MUST-FIX: none.**
