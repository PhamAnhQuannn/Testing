// write_test grading (P3d): the learner's test must FAIL against the planted-bug implementation and
// PASS against the correct one. Both runs reuse the normal runner with the fixed driver appended.
import type { PanelState, ResultRow } from "../components/TestResultPanel";
import { getRunner } from "../runner";
import { DEFAULT_LIMITS, type ProblemIO, type RunResult, type TestCase, type TestResult, type Verdict } from "../runner/Runner";
import driverSource from "../runner/pyodide/testdriver.py?raw";
import type { Problem } from "./api";

export const DRIVER_IO: ProblemIO = {
  mode: "function",
  entry: "_prep_run_tests",
  params: [],
  returns: "str",
  compare: "exact",
};

const BUGGY_TESTS: TestCase[] = [{ id: "buggy", args: [], expected: "FAIL" }];
const CORRECT_TESTS: TestCase[] = [{ id: "correct", args: [], expected: "PASS" }];

export const CHECK_LABELS = ["Bắt được bug", "Không báo động giả"] as const;

/** impl + learner test + driver, in that order, as one module (the driver is always last). */
export function assemble(implSrc: string, learnerTest: string): string {
  return `${implSrc}\n${learnerTest}\n${driverSource}`;
}

export interface FailingTestResult {
  verdict: Verdict;
  passed: number;
  total: number;
  elapsed_ms: number;
  results: TestResult[];
}

function row(label: string, result: TestResult | undefined): ResultRow {
  if (!result) return { label, verdict: "WA", elapsed_ms: 0, hidden: true, error: "Chưa chạy" };
  const failing = result.verdict !== "AC";
  return {
    label,
    verdict: result.verdict,
    elapsed_ms: result.elapsed_ms,
    hidden: !failing,
    error: failing ? result.error || undefined : undefined,
    stdout: failing ? result.stdout || undefined : undefined,
  };
}

function panel(
  rows: ResultRow[],
  running: boolean,
  final?: { verdict: Verdict; elapsed_ms: number },
  extra?: Pick<PanelState, "stdout" | "stderr">,
): PanelState {
  const firstBad = rows.find((r) => r.verdict !== "AC");
  return {
    kind: "submit",
    rows,
    total: 2,
    running,
    verdict: final?.verdict ?? null,
    elapsed_ms: final?.elapsed_ms,
    stdout: extra?.stdout ?? "",
    stderr: extra?.stderr ?? "",
    note: final && final.verdict !== "AC" && firstBad ? `Chưa qua: ${firstBad.label}` : undefined,
  };
}

export async function runFailingTest(
  problem: Pick<Problem, "buggy_code" | "reference_code">,
  learnerTest: string,
  setPanel: (panel: PanelState | null) => void,
): Promise<FailingTestResult> {
  const runner = getRunner();
  const limits = DEFAULT_LIMITS;
  const plan: [string, string, TestCase[]][] = [
    [CHECK_LABELS[0], problem.buggy_code ?? "", BUGGY_TESTS],
    [CHECK_LABELS[1], problem.reference_code ?? "", CORRECT_TESTS],
  ];
  const runs: RunResult[] = [];
  const rows: ResultRow[] = [];
  setPanel(panel([], true));
  for (const [label, impl, tests] of plan) {
    const run = await runner.run({ code: assemble(impl, learnerTest), io: DRIVER_IO, tests, limits });
    runs.push(run);
    rows.push(row(label, run.results[0] ?? { id: tests[0].id ?? null, verdict: run.verdict, got: null, error: "", stdout: run.stdout, stderr: run.stderr, elapsed_ms: run.elapsed_ms }));
    setPanel(panel(rows, rows.length < plan.length));
  }
  const passed = runs.filter((r) => r.verdict === "AC").length;
  const elapsed_ms = runs.reduce((sum, r) => sum + r.elapsed_ms, 0);
  const verdict: Verdict = passed === 2 ? "AC" : (runs.find((r) => r.verdict !== "AC")?.verdict ?? "WA");
  setPanel(
    panel(rows, false, { verdict, elapsed_ms }, {
      stdout: runs.map((r) => r.stdout).join(""),
      stderr: runs.map((r) => r.stderr).join(""),
    }),
  );
  return { verdict, passed, total: 2, elapsed_ms, results: runs.flatMap((r) => r.results) };
}
