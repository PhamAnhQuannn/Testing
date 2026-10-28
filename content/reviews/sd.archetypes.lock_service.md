# Review: sd.archetypes.lock_service

**Verdict: PASS (clean, publishable).** Independent content review, 2026.

## Technical accuracy & currency
- API correct: `acquire(name, lease_ttl)` → monotonic fencing token (or reject); `renew`/heartbeat (client renews at ~1/3 of TTL); `release`. Lease semantics correct: miss a renew → lock auto-releases, so a hung/dead client cannot hold forever.
- Fencing token correct: monotonic; resource accepts writes with token ≥ max-seen and rejects a woken-up old holder's smaller token (b03). Standard Kleppmann fencing — accurate.
- Consensus cluster correct: odd 3 or 5 nodes (Raft/Paxos), writes via leader + majority quorum; odd size avoids 2-2 split. Fault tolerance "3 tolerate 1, 5 tolerate 2" correct.
- **Quorum = ⌊n/2⌋+1 verified.** b07: n=5 ⇒ ⌊5/2⌋+1 = 3; tolerate 2 (lose 2 → 3 ≥ quorum survives; lose 3 → 2 < 3 stops). General ⌊(n-1)/2⌋ also correct. S264 repeats correctly.
- Sizing arithmetic verified: 1M keys renewed every 10s ⇒ 100,000 renew/s (1,000,000 / 10 = 100,000) ✓; RAM 1M × ~100 B ≈ 100 MB ✓. Write throughput "few k–few tens of k/s, doesn't scale by adding nodes" accurate for 2026 consensus stores. Mitigations (shard keys across clusters, raise lease_ttl) correct.
- Client-on-disconnect correct: cannot renew → assume lock may be lost → **stop acting on the protected resource**; fencing token is last-resort backstop. b06/b09 both reject "keep going" and the client-side self-renew fallacy (TTL is the service's clock).
- Leader election correctly framed as an application of the same API.
- Reuses distributed_locks + consensus by reference — no re-teach.

## Quizzes
- b03 (fencing token role) ans=b ✓.
- b05 (why consensus cluster not single strong box) ans=b ✓; explain correctly notes quorum writes are *slower* than a single box (safety+fault-tolerance is the point).
- b07 fill (quorum=3, tolerate=2) ✓.
- b09 (disconnect behaviour) ans=b ✓.

## Mastery items
- S262 diff1 recall (three API calls + token property): correct, right level.
- S263 diff2 score-2 scenario (A GC-pauses 15s > 10s lease, token 7 vs B's 8): correct — lease expires, B acquires with larger token, storage rejects A's stale token-7 writes. Rubric keyed to the 3 ideas. Right level.
- S264 diff3 interview: API / cluster / sizing (quorum formula + renew estimate + shard) / disconnect — matches `mastery_bar_vi`. Rubric correctly fails a wrong quorum computation.

## Language
Vietnamese clear; English terms parenthesized (fencing token/số chặn, lease, quorum, consensus, leader election, heartbeat).

No must-fix items.
