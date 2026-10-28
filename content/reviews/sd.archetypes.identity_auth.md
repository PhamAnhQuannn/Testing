# Review: sd.archetypes.identity_auth

**Verdict: APPROVE (clean).** Independent content review, 2026.

- Technical accuracy: authn ("bạn là ai", once per session) vs authz ("bạn được làm gì", nearly every request) correctly distinguished and used to motivate the whole design. SSO via OAuth2/OIDC with central IdP, OIDC ID token vs OAuth2 access token, services verify signature only — correct.
- Special check: JWT (stateless, scales, hard to revoke → short-lived access token + refresh token + denylist) vs session (stateful, instant revoke, lookup per request) — captured precisely, including the "signed ticket / cached permission doesn't know it's stale" through-line. RBAC default vs ABAC for context; permission-check cache with short TTL / invalidate on role change — all correct.
- Quizzes: b03 (authn vs authz boundary), b05 (why JWT hard to revoke), b07 fill (short-lived / refresh / denylist), b11 (cache consequence + invalidation) — every `answer` + `explain_md` correct.
- Mastery: S226 diff1 recall, S227 diff2 scenario (fired employee, 3-part), S228 diff3 interview matching Mức-3 bar (login+authz, JWT-vs-session tradeoff, revocation, cache). Levels/rubrics sensible.
- Reuse: builds on Redis/session store, gateway, caching concepts without re-teaching.
- Language: Vietnamese clear; English terms parenthesized.
- Minor (non-blocking): "OAuth2 access token = được phép làm gì" is a reasonable simplification (access token authorizes resource access).
