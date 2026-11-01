import { createElement, type ReactNode } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { MemoryRouter } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import type { CheckStep, Problem } from "../lib/api";
import { runFailingTest } from "../lib/runTest";
import { attemptWriteTest, WriteTestView } from "./CheckPage";

vi.mock("../lib/hooks", async (importOriginal) => ({
  ...(await importOriginal<typeof import("../lib/hooks")>()),
  useRunnerState: () => "ready",
}));
vi.mock("../components/SplitLayout", () => ({
  SplitLayout: (p: { left: ReactNode; right: ReactNode }) => createElement("div", null, p.left, p.right),
}));
vi.mock("../lib/runTest", () => ({ runFailingTest: vi.fn() }));

const SECRET = "def f(x):\n    return REFERENCE_SECRET\n";
const problem = {
  id: "wt-1",
  title: "T",
  title_vi: "Viết test",
  statement_en_md: "Spec text",
  statement_vi_md: "",
  starter: "",
  buggy_code: "def f(x):\n    return BUGGY_MARKER\n",
  reference_code: SECRET,
  starter_test: "# STARTER_TEST\n",
  item_kind: "write_test",
} as unknown as Problem;
const step = { item_id: "i1", type: "write_test", prompt_md: "Prompt", problem_id: "wt-1" } as unknown as CheckStep;

describe("WriteTestView", () => {
  beforeEach(() => vi.mocked(runFailingTest).mockReset());

  it("shows the buggy code and never renders reference_code", () => {
    const out = renderToStaticMarkup(
      createElement(
        MemoryRouter,
        null,
        createElement(WriteTestView, { session: { session_id: 1 }, step, problem, busy: false, commit: async () => true }),
      ),
    );
    expect(out).toContain("BUGGY_MARKER");
    expect(out).not.toContain("REFERENCE_SECRET");
    expect(out).toContain("FAIL");
  });

  it("builds a write_code-shaped body with total 2 from an AC run", async () => {
    vi.mocked(runFailingTest).mockResolvedValue({ verdict: "AC", passed: 2, total: 2, elapsed_ms: 12, results: [] });
    const body = await attemptWriteTest(problem, "assert True", () => {});
    expect(runFailingTest).toHaveBeenCalledWith(problem, "assert True", expect.any(Function));
    expect(body).toEqual({ code: "assert True", language: "python", verdict: "AC", passed_tests: 2, total: 2, runtime_ms: 12 });
  });
});
