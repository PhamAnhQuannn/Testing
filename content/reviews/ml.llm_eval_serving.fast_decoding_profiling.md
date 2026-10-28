# Review: ml.llm_eval_serving.fast_decoding_profiling

**Reviewer:** independent content reviewer (Opus), 2026-10-27
**Verdict: PASS — clean, không cần sửa.**

## Độ chính xác kỹ thuật (2026)
- Speculative decoding: draft model nhỏ đề xuất k token; target model verify cả cụm trong **một parallel forward pass**, nhận prefix đúng dài nhất, sửa token sai đầu tiên → nhiều token/lượt: đúng cơ chế.
- **Lossless / output distribution unchanged** (yêu cầu trọng tâm): phát biểu CHÍNH XÁC — luật accept/reject khiến token giữ lại được lấy mẫu theo phân phối của **target**; token bị loại thì target lấy mẫu lại từ phân phối đã hiệu chỉnh; chuỗi ra cùng phân phối với target chạy một mình. Nêu đúng rằng tính lossless KHÔNG phụ thuộc acceptance rate (chỉ ảnh hưởng tốc độ), và greedy thì từng token giống hệt. Trade-off là tính toán thừa khi reject, không phải chất lượng: đúng.
- Tăng tốc 2–3× hợp lý; biến thể Medusa/EAGLE (draft heads), n-gram/prompt lookup, lookahead nêu đúng ở mức tên gọi, đều lossless theo cùng nguyên lý verify.
- Memory-bound vs compute-bound qua roofline / arithmetic intensity (FLOPs/byte so với đỉnh FLOPs/đỉnh băng thông): đúng. Dấu hiệu: memory-bound = GPU util thấp + băng thông gần đỉnh (decode batch nhỏ); compute-bound = util gần đỉnh FLOPs (prefill/batch lớn): đúng.
- Kê đơn theo nút thắt: memory → batch/quantize/spec-decode; compute → fused kernel/CUDA graphs/torch.compile/TensorRT-LLM: đúng, cập nhật 2026.

## Quiz
- b04 (a), b06 fill "acceptance rate", b09 (a), b10 (a): answer + explain_md đúng; distractor bác đúng — đặc biệt b04c ("chỉ lossless khi acceptance 100%") bị bác chính xác, b10b ("spec-decode luôn tăng tốc mọi workload") bị bác đúng (prefill compute-bound lợi ích ít).

## Mastery (khớp mastery_bar_vi "Mức 3: giải thích spec-decode + vì sao không đổi phân phối + profiling memory/compute-bound")
- S331 (diff1, recall): vai trò draft/target + vì sao verify rẻ (một lần đọc trọng số, memory-bound) — đúng.
- S332 (diff2, scenario score-2): (a) lossless, (b) acceptance rate, (c) cách tăng acceptance — đúng, rubric hợp lý.
- S333 (diff3, interview): profiling phân loại + fix + spec-decode lossless gắn vào memory-bound — khớp mastery_bar đầy đủ.
- Mọi item chỉ test ý đã dạy (b01–b10).

## Ngôn ngữ
Rõ, thuật ngữ Anh trong ngoặc (draft/target model, accept/reject, acceptance rate, roofline, arithmetic intensity, memory-bandwidth-bound).

**MUST-FIX: none.**
