import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  ApiError,
  getHiddenTests,
  getLesson,
  getMap,
  getProblem,
  postAttempt,
  putDraft,
  putResume,
  request,
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
    expect(JSON.parse(lastInit().body as string)).toMatchObject({ code: "c", base_rev: null });
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
      json({ id: "s.x", title_vi: "T", blocks: [{ id: "b01", type: "text", md: "hi" }], run_no: 2, answers: { b04: { correct: true } } }),
    );
    const lesson = await getLesson("s.x");
    expect(lesson).toMatchObject({ run_no: 2, answers: { b04: { correct: true } } });
    expect(lesson.blocks).toHaveLength(1);
  });

  it("getProblem flattens starter.python, pyodide multiplier and the draft", async () => {
    fetchMock.mockResolvedValue(
      json({
        id: "ransom-note",
        title: "Ransom Note",
        starter: { python: "def f(): pass" },
        limits: { time_ms: 1000, memory_mb: 256, time_multiplier: { pyodide: 3 } },
        io: { mode: "function", entry: "can_construct" },
        sample_tests: [{ id: "s1", args: ["a", "b"], expected: false }],
        draft: { code: "x", updated_at: "t" },
      }),
    );
    const p = await getProblem("ransom-note");
    expect(p.starter).toBe("def f(): pass");
    expect(p.limits.time_multiplier).toBe(3);
    expect(p.sample_tests).toHaveLength(1);
    expect(p.draft?.code).toBe("x");
  });
});

describe("hidden tests flow", () => {
  it("POST start-submit then GET tests/hidden with the token", async () => {
    fetchMock.mockResolvedValueOnce(json({ token: "tok 1" }));
    fetchMock.mockResolvedValueOnce(json({ tests: [{ id: "h01", args: ["a", "a"], expected: true }] }));
    const tests = await getHiddenTests("ransom-note");
    expect(fetchMock.mock.calls[0][0]).toBe("/api/problems/ransom-note/start-submit");
    expect(lastInit(0).method).toBe("POST");
    expect(fetchMock.mock.calls[1][0]).toBe("/api/problems/ransom-note/tests/hidden?token=tok%201");
    expect(tests[0].id).toBe("h01");
  });

  it("postAttempt posts the result body with a key", async () => {
    fetchMock.mockResolvedValue(json({ clean: true }));
    await postAttempt({
      problem_id: "ransom-note",
      mode: "submit",
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
