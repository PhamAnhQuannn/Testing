// Shared Run/Submit execution for ProblemPage and CheckPage: sample tests for Run, hidden tests
// (token flow in getHiddenTests) for Submit, live progress into a PanelState.
import type { PanelState } from "../components/TestResultPanel";
import { getRunner } from "../runner";
import type { RunResult, TestCase } from "../runner/Runner";
import { getHiddenTests, type Problem } from "./api";
import { buildPanel, hiddenLabel, sampleLabel } from "./runView";

export async function runProblem(
  kind: "run" | "submit",
  problem: Pick<Problem, "id" | "io" | "limits" | "sample_tests">,
  source: string,
  setPanel: (panel: PanelState | null) => void,
): Promise<RunResult> {
  let tests: TestCase[] = problem.sample_tests;
  if (kind === "submit") {
    setPanel({ kind, rows: [], total: 0, running: true, verdict: null, stdout: "", stderr: "", note: "Đang tải test ẩn…" });
    tests = await getHiddenTests(problem.id);
  }
  const options = { hidden: kind === "submit", label: kind === "submit" ? hiddenLabel : sampleLabel };
  const seen: RunResult["results"] = [];
  const result = await getRunner().run({
    code: source,
    io: problem.io,
    tests,
    limits: problem.limits,
    onProgress: (r) => {
      seen.push(r);
      setPanel(buildPanel(kind, tests, seen, options, true));
    },
  });
  setPanel(buildPanel(kind, tests, result.results, options, false, result));
  return result;
}
