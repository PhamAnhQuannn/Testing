# Review: sd.archetypes.trading_brokerage

**Verdict: PASS (clean, publishable).** Independent content review, 2026.

## Technical accuracy & currency
- Order book correct: bids high→low, asks low→high, same price = first-in-first-out = price-time priority. Spread defined correctly.
- Match rule correct and emphasized: trade executes at the **resting order's price** (maker price), when buy ≥ ask; large order sweeps several resting orders from best outward; remainder rests = partial fill. Order lifecycle as a small state machine. Accurate.
- Order path correct: app/gateway → pre-trade risk check (funds/limits; **expired orders rejected here, never forwarded**) → single-threaded sequencer (total order + append to event log) → matching engine → fills fan-out to market-data + settlement via ledger.
- Single-threaded in-memory sequencer rationale correct: micro-second latency (RAM, lock-free), deterministic total order (replay → identical result), and crash-safe via replay of the ordered event log (event sourcing; standby consumes same log). Scale = shard by symbol. Accurate.

## Partial-fill arithmetic — VERIFIED
- **b04/b05 worked example.** Asks 51(50cp), 52(30cp); bids 50(100), 49(80). Buy 100cp @max 52:
  1. 52 ≥ 51 → 50cp @51 (resting price), ask-51 clears, buy 50cp left. ✓
  2. 52 ≥ 52 → 30cp @52, ask-52 clears, buy 20cp left. ✓
  3. no asks in range → 20cp rests at 52 as new best bid. ✓ Partial fill across two asks. Correct.
  - b05 option (a) "all 100 @52" is doubly wrong (only 80cp available; wrong price); (c) "needs exact price match" wrong. ans=b ✓.
- **S266 diff2.** Asks 51(40cp), 52(50cp); bids 50(100),49(80). Buy 70cp @max 51: 51 ≥ 51 → 40cp @51, ask-51 clears, buy 30cp left; next ask 52 but 51 < 52 → no further match; 30cp rests at 51 (new best bid). Final: asks 52(50cp); bids 51(30),50(100),49(80). Partial 40/70. ✓ Correct.
- **S267 diff3** = same numbers as b04 (asks 51(50),52(30); bid 50(100); buy 100 @max52): 50@51 + 30@52, 20 rests @52, partial fill across two asks. ✓ Correct.

## Quizzes
- b05 (match outcome) ans=b ✓.
- b08 fill (event sourcing, two words) accept-list ✓.
- b09 (why single-threaded in-memory sequencer) ans=b ✓; explain correctly rejects "cost" (a) and "one user at a time" (c).

## Mastery items
- S265 diff1 recall (book ordering + match price = resting order): correct, right level.
- S266 diff2 score-2 (hand-match with partial fill): correct arithmetic, rubric sensible. Right level.
- S267 diff3 interview: hand-match + order path + single-thread/replay — matches `mastery_bar_vi`. Rubric sensible.

## Language
Vietnamese clear; English terms parenthesized (order book, bids/asks, price-time priority, partial fill, sequencer, matching engine, event sourcing, settlement).

No must-fix items.
