# Review: sd.archetypes.video_streaming

**Verdict: APPROVE (clean).** Independent content review, 2026.

- Technical accuracy: pipeline upload → transcode → segment → deliver is correct and current. Chunked upload + presigned URL, object storage for raw, transcode as async worker-pool job, segment 2–10 s + manifest, CDN delivery — all standard 2026 practice.
- Special check (archetype): HLS (Apple) / DASH (open) over HTTP, static cacheable segments, adaptive bitrate decided client-side per next segment, multiple renditions — all present and correct. ABR correctly framed as "lower quality beats rebuffering".
- Math sanity: "10-min 720p → ~150 segments of 4 s" (600/4 = 150) is correct.
- Quizzes: b04 (transcode via queue/worker), b06 fill (manifest / rendition), b08 (ABR client per-segment), b10 (CDN role) — every `answer` + `explain_md` correct; distractors are good misconceptions, not throwaways.
- Mastery: S223 diff1 recall (segment/manifest/rendition), S224 diff2 scenario (rebuffering, 3-part), S225 diff3 interview "Design YouTube" matching Mức-3 bar (upload→phát, segment/manifest, ABR, CDN, + VOD/live). Levels and rubrics sensible.
- Reuse: explicitly leans on object storage, task workers, CDN (taught earlier) without re-teaching. Good.
- Language: Vietnamese clear; English terms parenthesized consistently (rendition, manifest, adaptive bitrate, etc.).
- Minor (non-blocking): manifest and playlist are treated as synonyms; in strict HLS/DASH terms DASH uses an MPD "manifest" and HLS an .m3u8 "playlist". The simplification is acceptable at this level.
