import { describe, expect, it } from "vitest";
import type { LessonBlock } from "./api";
import { normalizeOutput, tally } from "./grade";

describe("quiz bookkeeping", () => {
  it("normalizeOutput ignores trailing whitespace", () => {
    expect(normalizeOutput("a  \nb \n\n")).toBe("a\nb");
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
