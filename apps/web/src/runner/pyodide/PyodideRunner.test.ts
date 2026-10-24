import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { PyodideRunner, perTestLimitMs, WATCHDOG_SLACK_MS } from "./PyodideRunner";
import type { FromWorker, ToWorker, WorkerLike } from "./protocol";
import type { TestResult } from "../Runner";

class FakeWorker implements WorkerLike {
  onmessage: WorkerLike["onmessage"] = null;
  onerror: WorkerLike["onerror"] = null;
  terminated = false;
  received: ToWorker[] = [];
  postMessage(message: ToWorker) {
    this.received.push(message);
  }
  terminate() {
    this.terminated = true;
  }
  emit(message: FromWorker) {
    if (!this.terminated) this.onmessage?.({ data: message });
  }
}

const ok = (id: string): TestResult => ({
  id,
  verdict: "AC",
  got: true,
  error: "",
  stdout: "",
  stderr: "",
  elapsed_ms: 1,
});

const io = { mode: "function", entry: "f" } as const;
const limits = { time_ms: 1000, memory_mb: 256, time_multiplier: 3 };
const tests = [{ id: "a", args: [], expected: 1 }, { id: "b", args: [], expected: 2 }, { id: "c", args: [], expected: 3 }];

function setup() {
  const workers: FakeWorker[] = [];
  const runner = new PyodideRunner(() => {
    const worker = new FakeWorker();
    workers.push(worker);
    return worker;
  });
  return { runner, workers };
}

const tick = () => vi.advanceTimersByTimeAsync(0);

describe("PyodideRunner protocol", () => {
  beforeEach(() => vi.useFakeTimers());
  afterEach(() => vi.useRealTimers());

  it("waits for ready, posts the request and reports progress per test", async () => {
    const { runner, workers } = setup();
    const progress: string[] = [];
    const promise = runner.run({ code: "x", io, tests, limits, onProgress: (r) => progress.push(r.id!) });
    await tick();
    expect(workers[0].received).toHaveLength(0); // not ready yet
    workers[0].emit({ type: "ready" });
    await tick();
    const request = workers[0].received[0];
    expect(request).toMatchObject({ type: "run", code: "x", io, tests });
    const runId = (request as Extract<ToWorker, { type: "run" }>).runId;
    for (const t of tests) workers[0].emit({ type: "progress", runId, result: ok(t.id!) });
    workers[0].emit({ type: "done", runId });
    const result = await promise;
    expect(progress).toEqual(["a", "b", "c"]);
    expect(result).toMatchObject({ verdict: "AC", passed: 3, total: 3 });
  });

  it("terminates the worker on timeout, marks TLE, skips the rest and restarts in the background", async () => {
    const { runner, workers } = setup();
    workers[0].emit({ type: "ready" });
    const promise = runner.run({ code: "while True: pass", io, tests, limits });
    await tick();
    const runId = (workers[0].received[0] as Extract<ToWorker, { type: "run" }>).runId;
    workers[0].emit({ type: "progress", runId, result: ok("a") });
    await vi.advanceTimersByTimeAsync(perTestLimitMs({ limits }) + 1);
    const result = await promise;
    expect(workers[0].terminated).toBe(true);
    expect(workers).toHaveLength(2); // fresh worker booting
    expect(runner.restartCount).toBe(1);
    expect(runner.getState()).toBe("loading");
    expect(result.verdict).toBe("TLE");
    expect(result.results.map((r) => [r.id, r.verdict])).toEqual([
      ["a", "AC"],
      ["b", "TLE"],
    ]);
    expect(result.passed).toBe(1);
    expect(result.total).toBe(3);
  });

  it("cuts an infinite loop within 4 s with the default limits", () => {
    expect(perTestLimitMs({ limits })).toBeLessThanOrEqual(4000);
    expect(perTestLimitMs({ limits })).toBe(3000 + WATCHDOG_SLACK_MS);
  });

  it("resets the watchdog after every progress message", async () => {
    const { runner, workers } = setup();
    workers[0].emit({ type: "ready" });
    const promise = runner.run({ code: "x", io, tests, limits });
    await tick();
    const runId = (workers[0].received[0] as Extract<ToWorker, { type: "run" }>).runId;
    const step = perTestLimitMs({ limits }) - 100;
    for (const t of tests) {
      await vi.advanceTimersByTimeAsync(step);
      workers[0].emit({ type: "progress", runId, result: ok(t.id!) });
    }
    workers[0].emit({ type: "done", runId });
    expect((await promise).verdict).toBe("AC");
    expect(workers[0].terminated).toBe(false);
  });

  it("a compile error ends the run with a single CE result", async () => {
    const { runner, workers } = setup();
    workers[0].emit({ type: "ready" });
    const promise = runner.run({ code: "def (", io, tests, limits });
    await tick();
    const runId = (workers[0].received[0] as Extract<ToWorker, { type: "run" }>).runId;
    workers[0].emit({
      type: "progress",
      runId,
      result: { ...ok("x"), id: null, verdict: "CE", error: "SyntaxError: invalid syntax" },
    });
    const result = await promise;
    expect(result.verdict).toBe("CE");
    expect(result.results).toHaveLength(1);
    expect(result.passed).toBe(0);
  });

  it("queues runs one at a time and ignores stale messages", async () => {
    const { runner, workers } = setup();
    workers[0].emit({ type: "ready" });
    const first = runner.run({ code: "1", io, tests: [tests[0]], limits });
    const second = runner.run({ code: "2", io, tests: [tests[1]], limits });
    await tick();
    expect(workers[0].received).toHaveLength(1);
    const id1 = (workers[0].received[0] as Extract<ToWorker, { type: "run" }>).runId;
    workers[0].emit({ type: "progress", runId: id1, result: ok("a") });
    workers[0].emit({ type: "done", runId: id1 });
    await first;
    await tick();
    expect(workers[0].received).toHaveLength(2);
    const id2 = (workers[0].received[1] as Extract<ToWorker, { type: "run" }>).runId;
    expect(id2).not.toBe(id1);
    workers[0].emit({ type: "progress", runId: id1, result: ok("stale") }); // ignored
    workers[0].emit({ type: "progress", runId: id2, result: ok("b") });
    workers[0].emit({ type: "done", runId: id2 });
    const result = await second;
    expect(result.results.map((r) => r.id)).toEqual(["b"]);
  });

  it("restarts the worker and rejects when the worker reports an error", async () => {
    const { runner, workers } = setup();
    workers[0].emit({ type: "ready" });
    const promise = runner.run({ code: "x", io, tests, limits });
    const failure = expect(promise).rejects.toThrow("boom");
    await tick();
    const runId = (workers[0].received[0] as Extract<ToWorker, { type: "run" }>).runId;
    workers[0].emit({ type: "error", runId, message: "boom" });
    await failure;
    expect(workers[0].terminated).toBe(true);
    expect(workers).toHaveLength(2);
  });

  it("rejects runs when Pyodide fails to load", async () => {
    const { runner, workers } = setup();
    const promise = runner.run({ code: "x", io, tests, limits });
    const failure = expect(promise).rejects.toThrow("no wasm");
    workers[0].emit({ type: "init-error", message: "no wasm" });
    await failure;
    expect(runner.getState()).toBe("error");
  });
});
