# Review: ml.llm_eval_serving.batching_scheduling

**Reviewer:** independent content reviewer (Opus), 2026-10-27
**Verdict: PASS — clean, không cần sửa.**

## Độ chính xác kỹ thuật (2026)
- Decode memory-bound → batching nạp trọng số một lần amortize cho nhiều request, throughput tăng gần tuyến tính tới khi compute-bound: đúng.
- Continuous / in-flight batching (vLLM, TGI) lập lịch iteration-level, lấp finished slot ngay → thắng throughput lớn nhất: đúng và đúng thực tế 2026.
- PagedAttention = KV cache theo trang như OS virtual memory, giảm phân mảnh, cho phép chia sẻ trang: đúng.
- Prefix caching dùng lại KV của tiền tố chung (system prompt/few-shot) → giảm TTFT, tiết kiệm compute: đúng; liên hệ với PagedAttention (trang chia sẻ) chính xác.
- Latency ↔ throughput tradeoff, knob max batch size / max num batched tokens, chunked prefill chống head-of-line blocking: đúng và cập nhật.
- Autoscale theo queue depth / pending tokens / GPU util, KHÔNG theo CPU (CPU rảnh khi GPU nghẽn → scale muộn): đúng, đúng trọng tâm.

## Quiz
- b03 (a), b05 (a), b10 (a), b08 fill "prefix caching": tất cả answer + explain_md đúng; distractor được bác bỏ chính xác (b03c đúng là quantization; b05b/c sai; b10b/c sai).

## Mastery (khớp mastery_bar_vi "Mức 3: ... continuous batching + prefix caching + trade-off + autoscaling")
- S325 (diff1, recall): decode memory-bound + amortize + giá là latency — đúng, rubric hợp lý.
- S326 (diff2, scenario score-2): 3 phần (static phí / continuous / PagedAttn hoặc prefix) đúng, rubric phân mức rõ.
- S327 (diff3, interview): kiến trúc + knob tradeoff + autoscaling không-CPU — khớp mastery_bar; answer + rubric đủ.
- Mọi item chỉ test ý đã dạy (b01–b09). Không có khái niệm ngoài bài.

## Ngôn ngữ
Tiếng Việt rõ, thuật ngữ Anh đi kèm ngoặc nhất quán (throughput, latency, scheduler, iteration-level, head-of-line blocking...).

**MUST-FIX: none.**
