# Review: sd.archetypes.productivity_apps

**Verdict: PASS (clean, publishable).** Independent content review, 2026.

## Technical accuracy & currency
- Recurring events correct: store an RRULE (start + "weekly on Monday") as one row, not materialized rows; **expand-on-read** generates only occurrences inside the queried window. Unbounded series → one row. Accurate.
- Exceptions correct: per-occurrence override record (reschedule/cancel one instance) applied on top during expansion; base rule untouched. Standard iCalendar RRULE + EXDATE/override model.
- Free/busy correct: = merge-intervals. Union everyone's busy intervals, merge overlapping into solid busy blocks, gaps ≥ meeting length = common free slots. Privacy point (busy/free only, not content) correct. b06 correctly rejects intersection-of-busy (a) and single-person (c).
- Reminder correct: a one-shot scheduled job at event_time − lead, reusing job_scheduler (indexed run_at, at-least-once ⇒ dedupe at send; reschedule/cancel on event move). Accurate.
- Timezone/DST trap correct: "9am every Monday" is local wall-clock, not fixed UTC; storing UTC only drifts an hour after a DST transition; fix = store origin timezone with the rule and resolve to absolute instant per occurrence under that zone's DST rules. (One-off events can store the absolute instant.) Accurate.
- Email section correct and appropriately secondary: mailbox storage sharded by user_id, inverted index (reusing search_indexing) scoped to the user's mailbox, threading via reference headers, labels as many-to-many tags, SMTP + retry-with-backoff queue → bounce. Reuses job_scheduler + search_indexing by reference — no re-teach.

## Quizzes
- b04 (why RRULE + expand-on-read) ans=a ✓; distractors (b DB can't store dup titles, c no exceptions needed) correctly false.
- b06 (free/busy for 5 people) ans=a ✓.
- b08 fill (lead / timezone / DST) accept-lists sensible ✓.

## Mastery items
- S268 diff1 recall (why RRULE, and what expand-on-read requires): correct, right level.
- S269 diff2 score-2 (find a slot for 5 people): 3-part answer correct, reduces to merge-intervals; rubric catches the intersection mistake. Right level.
- S270 diff3 interview: RRULE+expand+override / free-busy / reminder via job_scheduler / timezone+DST — matches `mastery_bar_vi` (recurring, free/busy, reminder). Rubric sensible.

## Language
Vietnamese clear; English terms parenthesized (RRULE, expand on read, override/exception, merge intervals, free/busy, lead, time zone, DST, inverted index, SMTP).

No must-fix items.
