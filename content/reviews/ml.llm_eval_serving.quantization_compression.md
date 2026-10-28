# Review: ml.llm_eval_serving.quantization_compression

**Reviewer:** independent content reviewer (Opus), 2026-10-27
**Verdict: PASS — clean, không cần sửa.**

## Độ chính xác kỹ thuật (2026)
- Byte/tham số: FP16/BF16 = 2B, INT8 = 1B, INT4 = 0,5B: đúng.
- **Verify 70B** (70×10^9): FP16 = 140 GB, INT8 = 70 GB, INT4 = 35 GB — xác nhận bằng tính toán, đúng cả ba.
- 48 GB VRAM: FP16 (140) và INT8 (70) không vừa, INT4 (35) vừa + còn chỗ KV cache: đúng.
- PTQ (GPTQ/AWQ, chỉ cần calibration data, không train lại, rẻ/nhanh) vs QAT (giữ chất lượng ở bit rất thấp nhưng tốn kém): phân biệt đúng.
- Weight-only vs weight+activation (outlier làm activation khó nén), KV-cache quant: đúng.
- Yêu cầu đo suy giảm chất lượng trên eval set sau nén, INT4 thường tụt nhỏ, 3/2-bit rủi ro tăng nhanh: đúng, cân bằng, đúng thực tế 2026.
- Distillation + pruning/sparsity nêu đúng ở mức tên gọi.

## Quiz
- b04 fill "35 GB" (accept list rộng hợp lý), b06 (a), b08 (a): answer + explain_md đúng; distractor sai được bác đúng ("model tự nén" vô lý; "INT8 luôn tốt hơn" bỏ qua ràng buộc VRAM; "ép bit mù" tụt chất lượng).

## Mastery (khớp mastery_bar_vi "Mức 3: chọn precision+phương pháp theo phần cứng, tính 70B INT4, đo suy giảm")
- S328 (diff1, recall): định nghĩa + lợi ích + byte/tham số — đúng.
- S329 (diff2, scenario score-2): 140/70/35, chọn PTQ, bước đo eval — đúng số, rubric hợp lý.
- S330 (diff3, interview): end-to-end phần cứng → precision/method → 35 GB → đo chất lượng — khớp mastery_bar.
- Mọi item chỉ test ý đã dạy (b01–b10). Không vượt phạm vi.

## Ngôn ngữ
Rõ, thuật ngữ Anh trong ngoặc (quantization, calibration, PTQ/QAT, outlier, distillation, pruning). Dùng dấu phẩy thập phân VN (0,5) nhất quán.

**MUST-FIX: none.**
