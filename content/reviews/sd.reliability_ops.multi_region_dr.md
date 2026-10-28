# Review: sd.reliability_ops.multi_region_dr

**Verdict: PASS (clean, ready to publish).** Independent content review, 2026-10-27.

## Technical accuracy & currency
- Failure-domain framing (AZ vs region) correct; multi-region is for surviving a region loss, not for speed. Correct.
- Active-passive (primary + warm/cold standby, failover) vs active-active (all regions serve + write, hardest for consistency, write conflicts) — correct.
- DR ladder (backup-restore → pilot light → warm standby → active-active) ordered correctly by cost↑ / RPO,RTO↓; "untested backup/failover = no backup" is sound.

## RPO / RTO — VERIFIED NOT SWAPPED
- **RPO = max data loss** (how much *data*, measured in time): "RPO = 5 phút ⇒ mất tối đa 5 phút dữ liệu"; lowered by denser replication/backup. Correct.
- **RTO = max downtime** (how long until back up): "RTO = 30 phút ⇒ phục hồi trong 30 phút"; lowered by faster failover. Correct.
- Consistently correct in b03, b04, summary, and checks S163/S164/S165. b04 answer `a` correct; `b` is the swapped-definition trap, correctly marked wrong.

## Sync vs async tradeoff — correct
- Synchronous cross-region replication → **RPO = 0** but higher write latency + reduced availability if the other region stalls. Correct.
- Asynchronous → low latency but a lag window; data in that window is lost on primary failure = **RPO > 0**. Correct; framed as CAP/PACELC. b08 fill (0 / latency / RPO) correct.

## Mastery items
- S163 diff1 recall (define RPO/RTO + how to lower each) — right level; rubric explicitly fails the swapped definition.
- S164 diff2 scenario (RPO 5m / RTO 30m → async + pilot light/warm standby) — score-2, rubric sensible.
- S165 diff3 interview (RPO 0 / RTO ~1m → active-active/warm-hot + sync + name consistency tradeoff + failover drill) — matches mastery_bar_vi.
- Items test only taught ideas; Vietnamese clear, English parenthesized.

No must-fix items.
