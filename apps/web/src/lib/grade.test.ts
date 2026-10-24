import { describe, expect, it } from "vitest";
import type { LessonBlock } from "./api";
import { gradeFill, gradeMcq, gradePredict, tally } from "./grade";

describe("quiz grading", () => {
  it("mcq compares answer sets regardless of order", () => {
    const block = { id: "b", type: "quiz_mcq", answer: ["a", "c"], options: [], prompt_md: "", explain_md: "" } as LessonBlock & { type: "quiz_mcq" };
    expect(gradeMcq(block, ["c", "a"])).toBe(true);
    expect(gradeMcq(block, ["a"])).toBe(false);
  });
  it("fill trims and accepts any listed answer or regex", () => {
    const block = { id: "b", type: "quiz_fill", prompt_md: "", explain_md: "", blanks: [{ accept: ["get"] }, { accept: ["x"], regex: "^y+$" }] } as LessonBlock & { type: "quiz_fill" };
    expect(gradeFill(block, [" get ", "yy"])).toBe(true);
    expect(gradeFill(block, ["set", "x"])).toBe(false);
  });
  it("predict ignores trailing whitespace", () => {
    const block = { id: "b", type: "predict_output", code: "", expected_output: "{2, 3} [1, 4]", explain_md: "" } as LessonBlock & { type: "predict_output" };
    expect(gradePredict(block, "{2, 3} [1, 4]  \n")).toBe(true);
    expect(gradePredict(block, "{3, 2} [1, 4]")).toBe(false);
  });
  it("tally counts graded blocks only", () => {
    const blocks = [
      { id: "q1", type: "quiz_mcq" },
      { id: "q2", type: "quiz_fill" },
      { id: "q3", type: "predict_output", graded: false },
      { id: "t", type: "text" },
    ] as LessonBlock[];
    expect(tally(blocks, { q1: true, q2: false })).toMatchObject({ graded: 2, correct: 1, ratio: 0.5, wrong: ["q2"] });
  });
});
