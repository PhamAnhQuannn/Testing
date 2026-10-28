# Review: ml.rag_agents.chunking

**Verdict: PASS (clean, publishable).** Independent content review, 2026-10-27.

## Technical accuracy & currency
- Chunk-size tradeoff correct: too big → embedding diluted / wastes context / lowers precision; too small → loses context + fact split across chunks. Accurate and well framed.
- Overlap (10-20%) explained correctly as stitching context across boundaries.
- Parent-document / small-to-big retrieval described correctly (embed small for precision, return larger parent for context) as the stronger fix for fact-spanning beyond overlap.
- Three strategies (fixed+overlap, recursive/structural, semantic) and selection by doc type + embedding token limit are current and correct.
- Parsing/preprocessing (PDF/HTML cleanup, tables, OCR, multimodal), metadata filtering + citation, contextual header all accurate.

## Quiz / fill items
- b03 (answer a), b06 (answer a), b10 (parent-document/small-to-big), b11 (answer a): all `answer` + `explain_md` correct. Distractors are good (b03 c correctly labels "fact split" as a small-chunk error, not big).

## Mastery items
- S292 diff1 recall: correctly tests the size tradeoff, both directions required by rubric. Right level.
- S293 diff2 score-2 scenario: structured PDF manual with tables — strategy + fact-split + table parsing. Matches lesson content; sensible rubric.
- S294 diff3 interview: matches `mastery_bar_vi` (choose strategy by doc type + prove with recall@k/MRR vs fixed baseline). Rubric correctly requires the recall@k/MRR proof. Right level.
- All mastery items test only ideas the lesson teaches.

## Vietnamese + terms
Clear Vietnamese; English terms consistently parenthesized (chunk size, overlap, recursive/structural, semantic, parent-document, recall@k, MRR, silent truncation, OCR).

No must-fix items.
