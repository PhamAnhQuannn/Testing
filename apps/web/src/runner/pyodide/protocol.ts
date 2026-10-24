// Messages between the main thread (PyodideRunner) and the Web Worker.
import type { ProblemIO, TestCase, TestResult } from "../Runner";

export type ToWorker = { type: "run"; runId: number; code: string; io: ProblemIO; tests: TestCase[] };

export type FromWorker =
  | { type: "ready" }
  | { type: "init-error"; message: string }
  | { type: "progress"; runId: number; result: TestResult }
  | { type: "done"; runId: number }
  | { type: "error"; runId: number; message: string };

/** The slice of `Worker` the runner needs; lets tests inject a fake. */
export interface WorkerLike {
  postMessage(message: ToWorker): void;
  terminate(): void;
  onmessage: ((event: { data: FromWorker }) => void) | null;
  onerror: ((event: { message?: string }) => void) | null;
}
