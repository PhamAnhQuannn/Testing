// Runner contract (SPEC 6.2). The UI only knows this interface, so a server runner (Java, M5)
// can replace the Pyodide one without touching components or the API.

export type Verdict = "AC" | "WA" | "TLE" | "RE" | "CE";

export interface ProblemParam {
  name?: string;
  type?: string;
}

/** `io` block of problem.yaml; lesson code_exercise uses `{mode: "function", entry}`. */
export interface ProblemIO {
  mode: "function" | "inplace" | "class_ops" | "stdout";
  entry?: string;
  params?: ProblemParam[];
  returns?: string;
  compare?: "exact" | "unordered" | "float_tol" | "custom";
  inplace_arg?: number;
}

export interface TestCase {
  id?: string;
  args?: unknown[];
  ops?: string[];
  stdin?: string;
  expected?: unknown;
  tags?: string[];
}

/** One result per test, exactly as produced by harness.py (plus TLE decided by the watchdog). */
export interface TestResult {
  id: string | null;
  verdict: Verdict;
  got: unknown;
  error: string;
  stdout: string;
  stderr: string;
  elapsed_ms: number;
}

export interface RunLimits {
  time_ms: number;
  memory_mb: number;
  /** `limits.time_multiplier.pyodide` (default 3). */
  time_multiplier?: number;
}

export interface RunRequest {
  code: string;
  io: ProblemIO;
  tests: TestCase[];
  limits: RunLimits;
  onProgress?: (result: TestResult, index: number) => void;
}

export interface RunResult {
  verdict: Verdict;
  results: TestResult[];
  stdout: string;
  stderr: string;
  elapsed_ms: number;
  passed: number;
  total: number;
}

export interface Runner {
  language: "python" | "java";
  run(req: RunRequest): Promise<RunResult>;
}

export const DEFAULT_LIMITS: RunLimits = { time_ms: 1000, memory_mb: 256, time_multiplier: 3 };

const ORDER: Verdict[] = ["CE", "RE", "TLE", "WA"];

/** Run verdict: CE if the code did not compile, else the worst failing test, else AC. */
export function aggregateVerdict(results: TestResult[], total: number): Verdict {
  for (const verdict of ORDER) {
    if (results.some((r) => r.verdict === verdict)) return verdict;
  }
  return results.length < total ? "TLE" : "AC";
}

export function summarize(results: TestResult[], total: number, elapsed_ms: number): RunResult {
  const compileError = results.find((r) => r.verdict === "CE");
  const shown = compileError ? [compileError] : results;
  return {
    verdict: aggregateVerdict(shown, total),
    results: shown,
    stdout: shown.map((r) => r.stdout).join(""),
    stderr: shown.map((r) => r.stderr).join(""),
    elapsed_ms,
    passed: shown.filter((r) => r.verdict === "AC").length,
    total,
  };
}
