# Review: sd.archetypes.ecommerce_inventory

**Verdict: APPROVE (clean).** Independent content review, 2026.

- Technical accuracy: catalog (read-heavy, cache + search index), cart (best-effort, Redis/KV) vs inventory+order (source of truth) correctly separated. Oversell traced to the read-then-write / check-then-act race with a clear interleaving diagram.
- Special check: conditional atomic decrement `UPDATE items SET stock = stock - :q WHERE id = :id AND stock >= :q` + rows-affected check (1 = ok, 0 = sold out, clean fail) — correct, and correctly explained as eliminating the read/write gap under row lock. reserve → confirm with reservation TTL and release-on-failure/expiry — correct. Order saga + state machine placed → paid → shipping → delivered; compensation on payment failure = restock + refund (not cross-service ACID rollback) — correct. Idempotency-Key on order creation to stop double-submit — correct.
- Quizzes: b04 (why atomic decrement beats read-then-write), b06 (reserve→confirm vs decrement-on-order, rejects "oversell when busy" trap), b09 fill (`stock >= :q`, rows-affected = 1), b10 (compensation = restock + refund) — every `answer` + `explain_md` correct.
- Mastery: S232 diff1 recall, S233 diff2 scenario (1 unit, 2 buyers, 3-part), S234 diff3 interview (write the SQL, draw saga + compensation, reserve + idempotency, hot SKU) matching Mức-3 bar. Levels/rubrics sensible.
- Reuse: builds on idempotency, saga, Redis, cache, search index from earlier; hot-SKU sharded counter / queue callout is appropriately "mention, don't re-teach".
- Language: Vietnamese clear; English terms parenthesized.
