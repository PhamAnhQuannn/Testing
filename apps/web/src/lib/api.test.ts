import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  ApiError,
  getHiddenTests,
  getDraft,
  getLesson,
  getMap,
  getProblem,
  postAttempt,
  postQuizAnswer,
  putDraft,
  putResume,
  request,
  startCheck,
  answerCheck,
  checkHeartbeat,
  getReviewQueue,
  postReviewResult,
} from "./api";

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });

let fetchMock: ReturnType<typeof vi.fn>;
beforeEach(() => {
  fetchMock = vi.fn();
  vi.stubGlobal("fetch", fetchMock);
});
afterEach(() => vi.unstubAllGlobals());

const lastInit = (n = 0) => fetchMock.mock.calls[n][1] as RequestInit & { headers: Record<string, string> };

describe("request", () => {
  it("sends no Idempotency-Key on GET", async () => {
    fetchMock.mockResolvedValue(json({}));
    await request("/map");
    expect(lastInit().headers["Idempotency-Key"]).toBeUndefined();
  });

  it("sends a fresh uuid Idempotency-Key on every state-changing request", async () => {
    fetchMock.mockImplementation(async () => json({}));
    await request("/attempts", { method: "POST", body: { a: 1 } });
    await request("/attempts", { method: "POST", body: { a: 1 } });
    await putDraft("p", { code: "x", updated_at: "t" });
    await putResume({ mode: "lesson", route: "/s/x", ref: {}, updated_at: "t" });
    const keys = [0, 1, 2, 3].map((i) => lastInit(i).headers["Idempotency-Key"]);
    for (const key of keys) expect(key).toMatch(/^[0-9a-f-]{36}$/);
    expect(new Set(keys).size).toBe(4);
  });

  it("reuses a given key so a retry is idempotent", async () => {
    fetchMock.mockImplementation(async () => json({}));
    await request("/x", { method: "POST", body: {}, idempotencyKey: "k-1" });
    await request("/x", { method: "POST", body: {}, idempotencyKey: "k-1" });
    expect(lastInit(0).headers["Idempotency-Key"]).toBe("k-1");
    expect(lastInit(1).headers["Idempotency-Key"]).toBe("k-1");
  });

  it("maps {error:{code,message}} to ApiError", async () => {
    fetchMock.mockResolvedValue(json({ error: { code: "locked", message: "Mục bị khoá" } }, 403));
    const error = await request("/lessons/x").catch((e: unknown) => e);
    expect(error).toBeInstanceOf(ApiError);
    expect(error).toMatchObject({ status: 403, code: "locked", message: "Mục bị khoá" });
  });

  it("maps a network failure to ApiError status 0", async () => {
    fetchMock.mockRejectedValue(new TypeError("Failed to fetch"));
    const error = (await request("/map").catch((e: unknown) => e)) as ApiError;
    expect(error.isNetwork).toBe(true);
  });

  it("passes keepalive through for pagehide flushes", async () => {
    fetchMock.mockResolvedValue(json({}));
    await putDraft("ransom-note", { code: "c", updated_at: "t" }, { keepalive: true });
    expect(lastInit().keepalive).toBe(true);
    expect(fetchMock.mock.calls[0][0]).toBe("/api/drafts/ransom-note");
    expect(JSON.parse(lastInit().body as string)).toMatchObject({ code: "c", language: "python", cursor: { line: 0, ch: 0 } });
  });
});

describe("normalizers", () => {
  it("getMap accepts an array or {subtopics}", async () => {
    const item = { id: "py.datastructs.dict", name_vi: "Dict", score: 1, unlocked: true, due_cards: 2 };
    fetchMock.mockResolvedValueOnce(json([item]));
    fetchMock.mockResolvedValueOnce(json({ subtopics: [item] }));
    const a = await getMap();
    const b = await getMap();
    expect(a).toEqual(b);
    expect(a[0]).toMatchObject({ module: "py.datastructs", score: 1, due_cards: 2 });
  });

  it("getLesson reads blocks, run_no and answers", async () => {
    fetchMock.mockResolvedValue(
      json({ id: "s.x", title_vi: "T", blocks: [{ id: "b01", type: "text", md: "hi" }], progress: { run_no: 2, lesson_done: false, answers: { b04: { first_correct: false, last_correct: true, last_answer: ["b"] } } } }),
    );
    const lesson = await getLesson("s.x");
    expect(lesson).toMatchObject({ run_no: 2, answers: { b04: { correct: false, answer: ["b"] } } });
    expect(lesson.blocks).toHaveLength(1);
  });

  it("getProblem flattens starter.python, pyodide multiplier, opened hints and status", async () => {
    fetchMock.mockResolvedValue(
      json({
        id: "ransom-note",
        title: "Ransom Note",
        starter: { python: "def f(): pass" },
        limits: { time_ms: 1000, memory_mb: 256, time_multiplier: { pyodide: 3 } },
        io: { mode: "function", entry: "can_construct" },
        sample_tests: [{ id: "s1", args: ["a", "b"], expected: false }],
        hint_count: 3,
        hints: ["h1"],
        status: "solved",
      }),
    );
    const p = await getProblem("ransom-note");
    expect(p.starter).toBe("def f(): pass");
    expect(p.limits.time_multiplier).toBe(3);
    expect(p.sample_tests).toHaveLength(1);
    expect(p.hints_opened).toEqual(["h1"]);
    expect(p.solved).toBe(true);
  });
});

describe("drafts and quiz", () => {
  it("getDraft maps the wire cursor to an offset", async () => {
    fetchMock.mockResolvedValue(json({ draft: { code: "ab", updated_at: "t", cursor: { line: 0, ch: 1, offset: 1 }, elapsed_ms: 5 } }));
    expect(await getDraft("p")).toEqual({ code: "ab", updated_at: "t", cursor: 1, elapsed_ms: 5 });
    expect(fetchMock.mock.calls[0][0]).toBe("/api/drafts/p?language=python");
    fetchMock.mockResolvedValue(json({ draft: null }));
    expect(await getDraft("p")).toBeNull();
  });

  it("putDraft sends line/ch computed from the offset", async () => {
    fetchMock.mockResolvedValue(json({ accepted: true }));
    await putDraft("p", { code: "ab\ncd", updated_at: "t", cursor: 4 });
    expect(JSON.parse(lastInit().body as string).cursor).toEqual({ line: 1, ch: 1, offset: 4 });
  });

  it("postQuizAnswer uses quiz_item_id and an idempotency key", async () => {
    fetchMock.mockResolvedValue(json({ correct: true }));
    await postQuizAnswer({ quiz_item_id: "s#b04", run_no: 1, answer: ["b"], occurred_at: "t" });
    expect(lastInit().headers["Idempotency-Key"]).toBeTruthy();
    expect(JSON.parse(lastInit().body as string)).toMatchObject({ quiz_item_id: "s#b04", run_no: 1 });
  });
});

describe("hidden tests flow", () => {
  it("POST start-submit then GET tests/hidden with X-Submit-Token", async () => {
    fetchMock.mockResolvedValueOnce(json({ token: "tok 1" }));
    fetchMock.mockResolvedValueOnce(json({ tests: [{ id: "h01", args: ["a", "a"], expected: true }] }));
    const tests = await getHiddenTests("ransom-note");
    expect(fetchMock.mock.calls[0][0]).toBe("/api/problems/ransom-note/start-submit");
    expect(lastInit(0).method).toBe("POST");
    expect(fetchMock.mock.calls[1][0]).toBe("/api/problems/ransom-note/tests/hidden");
    expect(lastInit(1).headers["X-Submit-Token"]).toBe("tok 1");
    expect(tests[0].id).toBe("h01");
  });

  it("postAttempt posts the result body with a key", async () => {
    fetchMock.mockResolvedValue(json({ clean: true }));
    await postAttempt({
      problem_id: "ransom-note",
      mode: "submit",
      language: "python",
      code: "c",
      verdict: "AC",
      passed: 12,
      total: 12,
      elapsed_ms: 5000,
      occurred_at: "t",
    });
    expect(lastInit().headers["Idempotency-Key"]).toBeTruthy();
    expect(JSON.parse(lastInit().body as string)).toMatchObject({ mode: "submit", passed: 12 });
  });
});

describe("mastery check api", () => {
  it("startCheck POSTs context with an Idempotency-Key and normalizes the session", async () => {
    fetchMock.mockResolvedValue(
      json({
        session_id: 7,
        subtopic_id: "py.x",
        context: "test_out",
        attempt_no: 1,
        status: "in_progress",
        resumed: true,
        elapsed_ms: 1000,
        step: { index: 0, count: 2, item_id: "q1", level: 2, type: "write_code", minutes: 6, time_limit_ms: 360000, prompt_md: "p", problem_id: "check-q1" },
        results: [],
      }),
    );
    const s = await startCheck("py.x", "test_out");
    expect(fetchMock.mock.calls[0][0]).toBe("/api/checks/py.x/start");
    expect(JSON.parse(lastInit().body as string)).toEqual({ context: "test_out" });
    expect(lastInit().headers["Idempotency-Key"]).toMatch(/[0-9a-f-]{36}/);
    expect(s.session_id).toBe(7);
    expect(s.step.problem_id).toBe("check-q1");
    expect(s.resumed).toBe(true);
  });

  it("check_retry_locked keeps retry_after in ApiError.extra", async () => {
    fetchMock.mockResolvedValue(
      json({ error: { code: "check_retry_locked", message: "locked", retry_after: "2026-10-26T00:00:00Z", level: 2 } }, 409),
    );
    const err = (await startCheck("py.x").catch((e: unknown) => e)) as ApiError;
    expect(err.code).toBe("check_retry_locked");
    expect(err.status).toBe(409);
    expect(err.extra.retry_after).toBe("2026-10-26T00:00:00Z");
  });

  it("answerCheck reuses a supplied key and sends the body as is", async () => {
    fetchMock.mockResolvedValue(
      json({
        session_id: 7,
        finished: false,
        result: { item_id: "q1", level: 2, type: "read_code", passed: true, correct: true, clean: false, reason: "over_time" },
        next: { index: 1, count: 2, item_id: "q2", level: 3, type: "concept", minutes: 3, prompt_md: "c", answer_md: "a" },
        score: { before: 0, after: 0 },
        outcome: null,
      }),
    );
    const out = await answerCheck("py.x", { session_id: 7, item_id: "q1", elapsed_ms: 5, answer: "2" }, "key-1");
    expect(lastInit().headers["Idempotency-Key"]).toBe("key-1");
    expect(JSON.parse(lastInit().body as string)).toMatchObject({ session_id: 7, item_id: "q1", answer: "2" });
    expect(out.result.reason).toBe("over_time");
    expect(out.next?.type).toBe("concept");
  });

  it("checkHeartbeat posts the absolute elapsed_ms to the session path", async () => {
    fetchMock.mockResolvedValue(json({ session_id: 7, status: "in_progress", elapsed_ms: 1235 }));
    await checkHeartbeat(7, 1234.6);
    expect(fetchMock.mock.calls[0][0]).toBe("/api/checks/7/heartbeat");
    expect(JSON.parse(lastInit().body as string)).toEqual({ elapsed_ms: 1235 });
  });
});

describe("review api", () => {
  it("getReviewQueue adds editor=false only when asked and normalizes", async () => {
    const body = {
      today: "2026-10-25",
      total_due: 1,
      backlog_warn: 20,
      backlog: false,
      cards: [{ subtopic_id: "s1", name_vi: "S", box: 3, due_on: "2026-10-24", overdue_days: 1, item_kind: "code",
        item: { kind: "code", ref: "p1", type: "write_code", subtopic_id: "s1" }, recall_item: null }],
      short_session: { enabled: true, size: 6, max_code: 2, cards: [{ subtopic_id: "s1", item_kind: "code" }] },
    };
    fetchMock.mockImplementation(async () => json(body));
    const q = await getReviewQueue();
    expect(fetchMock.mock.calls[0][0]).toBe("/api/review/queue");
    expect(q.cards[0].item?.ref).toBe("p1");
    expect(q.short_session.size).toBe(6);
    await getReviewQueue(false);
    expect(fetchMock.mock.calls[1][0]).toBe("/api/review/queue?editor=false");
  });

  it("postReviewResult posts with an Idempotency-Key and surfaces card_not_due", async () => {
    fetchMock.mockResolvedValueOnce(
      json({ subtopic_id: "a.b", success: true, box_before: 1, box_after: 2, due_on: "2026-10-28", lapses: 0, score: { before: 1, after: 1 }, newly_unlocked: [] }),
    );
    const res = await postReviewResult("a.b", { success: true, item_ref: "a.b#q1", item_kind: "recall" }, "k1");
    expect(fetchMock.mock.calls[0][0]).toBe("/api/review/a.b/result");
    expect(lastInit().headers["Idempotency-Key"]).toBe("k1");
    expect(res.box_after).toBe(2);
    fetchMock.mockResolvedValueOnce(json({ error: { code: "card_not_due", message: "x" } }, 409));
    await expect(postReviewResult("a.b", { success: false })).rejects.toMatchObject({ code: "card_not_due", status: 409 });
  });
});
