# Review: sd.api.api_styles

**Verdict: PASS (clean).** Independent content review, 2026-10-27.

## Technical accuracy & currency (2026)
- REST characterization correct: resource + HTTP verbs, cacheable `GET`, ubiquitous/debuggable, over/under-fetching as the main cost. Accurate.
- gRPC correct: protobuf binary over HTTP/2, multiplexing, server/client/bidirectional streaming, strong `.proto` contract; poor browser support (needs gRPC-Web + proxy), hard to eyeball-debug. Current and right for internal low-latency service-to-service.
- GraphQL correct: single endpoint, client-selected fields, solves over/under-fetch; costs = N+1 (DataLoader), lost URL/HTTP caching (POST single endpoint), server complexity (schema/resolvers, depth limiting). Accurate.
- Boundary rule (public → REST/GraphQL; internal low-latency → gRPC) with explicit trade-off framing is sound interview guidance.

## Schema-compat 3 rules (SPECIAL check)
All three correct: (1) add only optional fields; (2) never remove/rename/retype an existing field, and never reuse a protobuf field number; (3) breaking change → version it (`/v2`, run old+new side by side). Matches industry practice.

## Quizzes
- b04 (internal, low-latency, strong contract → gRPC): answer `b` correct; distractors + explain accurate.
- b06 (true statement about GraphQL): answer `a` correct; `b`/`c` rebuttals accurate (GraphQL is JSON over one POST endpoint, not binary; binary/HTTP2 is gRPC).
- b09 fill (`optional`): correct, accept list reasonable.

## Mastery items vs bar
Bar: "chọn và bảo vệ kiểu API cho public và internal, nêu chi phí mỗi lựa chọn và 3 quy tắc tương thích schema."
- S100 (diff1 recall): name each style's main strength — correct, recall level. `answer_md` + `rubric_md` sound.
- S101 (diff2 score-2 scenario): mobile over/under-fetch → GraphQL + ≥2 costs. Correct, right difficulty; rubric sensible.
- S102 (diff3 interview): choose+defend both boundaries, costs, 3 schema rules — matches the bar exactly. `answer_md` correct; rubric gates on costs + all 3 rules.
- Items only test ideas the lesson teaches (all covered in b02–b08). 

## Language
Vietnamese clear; English terms consistently parenthesized (over/under-fetch, DataLoader, backward compatibility, field number, etc.).

## Minor (non-blocking)
- b02 lists "`GET` là idempotent và có thể cache" — cacheability derives from `GET` being *safe*, not from idempotency (PUT/DELETE are idempotent but not cacheable). Both clauses are individually true, so not an error; could be sharpened in a future pass.
