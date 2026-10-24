import {
  DEFAULT_LIMITS,
  summarize,
  type RunRequest,
  type RunResult,
  type Runner,
  type TestResult,
} from "../Runner";
import type { FromWorker, WorkerLike } from "./protocol";

/** Extra time on top of `time_ms x multiplier` for message passing and the first-call overhead. */
export const WATCHDOG_SLACK_MS = 300;

export type WorkerFactory = () => WorkerLike;

type Timers = {
  setTimeout: (fn: () => void, ms: number) => unknown;
  clearTimeout: (handle: unknown) => void;
  now: () => number;
};

const realTimers: Timers = {
  setTimeout: (fn, ms) => setTimeout(fn, ms),
  clearTimeout: (handle) => clearTimeout(handle as ReturnType<typeof setTimeout>),
  now: () => performance.now(),
};

export function perTestLimitMs(req: Pick<RunRequest, "limits">): number {
  const limits = { ...DEFAULT_LIMITS, ...req.limits };
  return limits.time_ms * (limits.time_multiplier ?? 3) + WATCHDOG_SLACK_MS;
}

/**
 * Runs Python in a Web Worker holding Pyodide. One run at a time (queued). The watchdog lives
 * here, on the main thread: when a test exceeds its budget the worker is terminated, that test
 * is reported TLE, the remaining tests are skipped and a fresh worker boots in the background.
 */
export class PyodideRunner implements Runner {
  language = "python" as const;

  private worker: WorkerLike | null = null;
  private ready: Promise<void> = Promise.resolve();
  private queue: Promise<unknown> = Promise.resolve();
  private runCounter = 0;
  private restarts = 0;
  private initFailed = false;
  private listeners = new Set<(state: RunnerState) => void>();
  private state: RunnerState = "loading";

  constructor(
    private readonly createWorker: WorkerFactory,
    private readonly timers: Timers = realTimers,
  ) {
    this.spawn();
  }

  get restartCount(): number {
    return this.restarts;
  }

  getState(): RunnerState {
    return this.state;
  }

  subscribe(listener: (state: RunnerState) => void): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  run(req: RunRequest): Promise<RunResult> {
    const result = this.queue.then(() => this.execute(req));
    this.queue = result.catch(() => undefined);
    return result;
  }

  private setState(state: RunnerState) {
    this.state = state;
    this.listeners.forEach((listener) => listener(state));
  }

  private spawn() {
    this.setState("loading");
    const worker = this.createWorker();
    this.worker = worker;
    this.ready = new Promise<void>((resolve, reject) => {
      worker.onmessage = (event) => {
        if (event.data.type === "ready") {
          if (this.worker === worker) this.setState("ready");
          resolve();
        } else if (event.data.type === "init-error") {
          if (this.worker === worker) this.setState("error");
          reject(new Error(event.data.message));
        }
      };
      worker.onerror = (event) => {
        if (this.worker === worker) this.setState("error");
        reject(new Error(event.message ?? "worker error"));
      };
    });
    this.ready.catch(() => undefined); // surfaced to whoever awaits it in execute()
  }

  private restart() {
    this.worker?.terminate();
    this.restarts += 1;
    this.spawn();
  }

  private async execute(req: RunRequest): Promise<RunResult> {
    if (this.initFailed) {
      this.initFailed = false;
      this.restart(); // the previous boot failed (e.g. a fetch glitch): try a fresh worker
    }
    try {
      await this.ready;
    } catch (error) {
      this.initFailed = true; // state stays "error" until the next Run retries
      throw error;
    }
    const worker = this.worker!;
    const started = this.timers.now();
    const runId = ++this.runCounter;
    const limitMs = perTestLimitMs(req);
    const results: TestResult[] = [];

    return new Promise<RunResult>((resolve, reject) => {
      let timer: unknown;
      let settled = false;

      const finish = (action: () => void) => {
        if (settled) return;
        settled = true;
        this.timers.clearTimeout(timer);
        action();
      };
      const resolveNow = () =>
        resolve(summarize(results, req.tests.length, Math.round(this.timers.now() - started)));

      const arm = () => {
        this.timers.clearTimeout(timer);
        timer = this.timers.setTimeout(() => {
          finish(() => {
            const test = req.tests[results.length];
            const tle: TestResult = {
              id: test?.id ?? null,
              verdict: "TLE",
              got: null,
              error: `Quá thời gian cho phép (${req.limits.time_ms} ms)`,
              stdout: "",
              stderr: "",
              elapsed_ms: limitMs,
            };
            results.push(tle);
            req.onProgress?.(tle, results.length - 1);
            this.restart();
            resolveNow();
          });
        }, limitMs);
      };

      worker.onmessage = (event: { data: FromWorker }) => {
        const message = event.data;
        if (!("runId" in message) || message.runId !== runId) return;
        if (message.type === "progress") {
          results.push(message.result);
          req.onProgress?.(message.result, results.length - 1);
          if (message.result.verdict === "CE") finish(resolveNow);
          else arm();
        } else if (message.type === "done") {
          finish(resolveNow);
        } else if (message.type === "error") {
          finish(() => {
            this.restart();
            reject(new Error(message.message));
          });
        }
      };
      worker.onerror = (event) => {
        finish(() => {
          this.restart();
          reject(new Error(event.message ?? "worker error"));
        });
      };

      arm();
      worker.postMessage({ type: "run", runId, code: req.code, io: req.io, tests: req.tests });
    });
  }
}

export type RunnerState = "loading" | "ready" | "error";
