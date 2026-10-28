# Review: sd.archetypes.cloud_compute

**Verdict: APPROVE (clean).** Independent content review, 2026.

- Technical accuracy: platform for running untrusted code (code judge, online IDE, CI, serverless) correctly framed as a job scheduler whose work is hostile code, shifting focus to isolation + resource limits. Threat model (delete host files, exfiltrate data, outbound attacks, fork bomb, infinite loop, crypto mining) and least-privilege sandbox (no network, read-only FS) — correct.
- Special check: "a plain container is NOT a strong security boundary" stated directly and correctly justified — containers share the host kernel (isolation only via namespaces/cgroups), so a kernel exploit enables container escape + side-channel risk. Stronger isolation: gVisor (user-space kernel intercepting syscalls) and Firecracker/microVM (lightweight hardware virtualization, own kernel, ms boot, how serverless/Lambda runs untrusted code). Defense-in-depth (seccomp, AppArmor/SELinux, dropped capabilities, read-only FS, no network) — all correct.
- Resource limits + timeouts via cgroups (CPU, memory/OOM, pids vs fork bomb, wall-clock vs infinite loop — the "2 s / 256 MB" judge rule) — correct. Warm pool: pre-booted sandboxes to kill cold start, reset/recycle or discard between runs to remove prior tenant traces, background refill/autoscale — correct.
- Quizzes: b06 (container shares kernel → escape; distractors correctly reject "container slower" and "container can't limit RAM/CPU"), b08 (timeout + pids limit stop loop/fork bomb; correctly rejects "warm pool = safety" and "microVM makes loop stop"), b10 fill (cold start / warm) — every `answer` + `explain_md` correct.
- Mastery: S238 diff1 recall (isolation + resource limits), S239 diff2 scenario (rebut "Docker is enough", 3-part), S240 diff3 interview (architecture + why container insufficient + warm pool + fairness) matching Mức-3 bar. Levels/rubrics sensible.
- Reuse: explicitly inherits job scheduler (API→queue→scheduler→worker→result), fairness/quota, autoscale; streaming logs and session persistence reused, not re-taught.
- Language: Vietnamese clear; English terms parenthesized.
