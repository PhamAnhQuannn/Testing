import { show, type PanelState, type ResultRow } from "../components/TestResultPanel";
import type { RunResult, TestCase, TestResult } from "../runner/Runner";

const SMALL = 200;

const inputOf = (test: TestCase): string =>
  test.ops ? show({ ops: test.ops, args: test.args }) : test.args ? test.args.map(show).join(", ") : show(test.stdin ?? "");

export interface RowOptions {
  hidden: boolean;
  label: (test: TestCase | undefined, index: number) => string;
}

/** Turns runner results into rows. Hidden tests reveal detail only for the first failure and only if small. */
export function toRow(
  result: TestResult,
  test: TestCase | undefined,
  index: number,
  options: RowOptions,
  firstFailure: boolean,
): ResultRow {
  const label = result.verdict === "CE" ? "Biên dịch" : options.label(test, index);
  const row: ResultRow = {
    label,
    verdict: result.verdict,
    elapsed_ms: result.elapsed_ms,
    hidden: options.hidden,
  };
  if (result.verdict === "AC") return row;
  const input = test ? inputOf(test) : "";
  const small = input.length <= SMALL && show(test?.expected).length <= SMALL;
  if (options.hidden && !(firstFailure && small)) return row;
  if (result.verdict !== "CE") row.input = input;
  if (test && "expected" in test) row.expected = show(test.expected);
  if (result.verdict === "WA") row.got = show(result.got);
  row.error = result.error || undefined;
  row.stdout = result.stdout || undefined;
  return row;
}

export function buildPanel(
  kind: "run" | "submit",
  tests: TestCase[],
  results: TestResult[],
  options: RowOptions,
  running: boolean,
  final?: RunResult,
): PanelState {
  let seenFailure = false;
  const rows = results.map((result, i) => {
    const first = result.verdict !== "AC" && !seenFailure;
    if (result.verdict !== "AC") seenFailure = true;
    return toRow(result, tests[i], i, options, first);
  });
  return {
    kind,
    rows,
    total: tests.length,
    running,
    verdict: final?.verdict ?? null,
    elapsed_ms: final?.elapsed_ms,
    stdout: results.map((r) => r.stdout).join(""),
    stderr: results.map((r) => r.stderr).join(""),
    note:
      final && final.passed < final.total && final.verdict !== "AC"
        ? `Test sai đầu tiên: ${rows.find((r) => r.verdict !== "AC")?.label ?? "?"}`
        : undefined,
  };
}

export const sampleLabel = (_test: TestCase | undefined, index: number) => `Sample ${index + 1}`;
export const hiddenLabel = (test: TestCase | undefined, index: number) => test?.id ?? `Test ${index + 1}`;
