import { beforeEach, describe, expect, it, vi } from "vitest";
import type { PanelState } from "../components/TestResultPanel";
import type { RunRequest, RunResult, Verdict } from "../runner/Runner";
import driverSource from "../runner/pyodide/testdriver.py?raw";
import { runFailingTest } from "./runTest";

const calls: RunRequest[] = [];
let impl: (req: RunRequest) => Promise<RunResult> = async () => {
  throw new Error("unset");
};
vi.mock("../runner", () => ({ getRunner: () => ({ run: (req: RunRequest) => {
      calls.push(req);
      return impl(req);
    }, getState: () => "ready", subscribe: () => () => {} }) }));

const result = (verdict: Verdict, id: string): RunResult => ({
  verdict,
  results: [{ id, verdict, got: null, error: "", stdout: "", stderr: "", elapsed_ms: 5 }],
  stdout: "",
  stderr: "",
  elapsed_ms: 5,
  passed: verdict === "AC" ? 1 : 0,
  total: 1,
});

const problem = { buggy_code: "def f(x):\n    return x + 2\n", reference_code: "def f(x):\n    return x + 1\n" };
const test = "def test_f():\n    assert f(1) == 2\n";

describe("runFailingTest", () => {
  beforeEach(() => {
    calls.length = 0;
  });

  it("is AC with passed 2 when both runs are AC, and appends the driver to impl + test", async () => {
    impl = async (req) => result("AC", req.tests[0].id!);
    const panels: (PanelState | null)[] = [];
    const out = await runFailingTest(problem, test, (p) => panels.push(p));
    expect(out).toMatchObject({ verdict: "AC", passed: 2, total: 2, elapsed_ms: 10 });
    expect(calls).toHaveLength(2);
    const [buggy, correct] = calls;
    for (const req of [buggy, correct]) {
      expect(req.io).toMatchObject({ mode: "function", entry: "_prep_run_tests", params: [], returns: "str", compare: "exact" });
      expect(req.tests).toHaveLength(1);
      expect(req.tests[0].args).toEqual([]);
      expect(req.code.endsWith(driverSource)).toBe(true);
      expect(req.code).toContain(test);
    }
    expect(buggy.tests[0]).toEqual({ id: "buggy", args: [], expected: "FAIL" });
    expect(correct.tests[0]).toEqual({ id: "correct", args: [], expected: "PASS" });
    expect(buggy.code).toContain(problem.buggy_code);
    expect(correct.code).toContain(problem.reference_code);
    const last = panels[panels.length - 1]!;
    expect(last.running).toBe(false);
    expect(last.rows.map((r) => r.label)).toEqual(["Bắt được bug", "Không báo động giả"]);
  });

  it("is WA when the buggy run does not fail the test", async () => {
    impl = async (req) => result(req.tests[0].id === "buggy" ? "WA" : "AC", req.tests[0].id!);
    const out = await runFailingTest(problem, test, () => {});
    expect(out).toMatchObject({ verdict: "WA", passed: 1, total: 2 });
  });

  it("surfaces the failing run verdict (false alarm on the correct code)", async () => {
    impl = async (req) => result(req.tests[0].id === "correct" ? "RE" : "AC", req.tests[0].id!);
    const out = await runFailingTest(problem, test, () => {});
    expect(out).toMatchObject({ verdict: "RE", passed: 1, total: 2 });
  });
});
