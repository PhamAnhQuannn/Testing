// Local grading of lesson quizzes (UI_SPEC S6: graded from the bundle, server confirms).
import type { LessonBlock } from "./api";

type Mcq = Extract<LessonBlock, { type: "quiz_mcq" }>;
type Fill = Extract<LessonBlock, { type: "quiz_fill" }>;
type Predict = Extract<LessonBlock, { type: "predict_output" }>;

export function gradeMcq(block: Mcq, selected: string[]): boolean {
  const want = [...block.answer].sort();
  const got = [...selected].sort();
  return want.length === got.length && want.every((id, i) => id === got[i]);
}

export function gradeFill(block: Fill, values: string[]): boolean {
  return block.blanks.every((blank, i) => {
    const value = (values[i] ?? "").trim();
    if (blank.accept.some((accepted) => accepted === value)) return true;
    if (blank.regex) {
      try {
        return new RegExp(blank.regex).test(value);
      } catch {
        return false;
      }
    }
    return false;
  });
}

export const normalizeOutput = (text: string) =>
  text
    .trimEnd()
    .split("\n")
    .map((line) => line.trimEnd())
    .join("\n");

export function gradePredict(block: Predict, typed: string): boolean {
  return normalizeOutput(typed) === normalizeOutput(block.expected_output);
}

export const isGraded = (block: LessonBlock): boolean =>
  (block.type === "quiz_mcq" || block.type === "quiz_fill" || block.type === "predict_output") &&
  block.graded !== false;

export interface QuizTally {
  graded: number;
  correct: number;
  ratio: number;
  wrong: string[];
}

export function tally(blocks: LessonBlock[], results: Record<string, boolean>): QuizTally {
  const graded = blocks.filter(isGraded);
  const correct = graded.filter((b) => results[b.id] === true).length;
  return {
    graded: graded.length,
    correct,
    ratio: graded.length ? correct / graded.length : 0,
    wrong: graded.filter((b) => results[b.id] !== true).map((b) => b.id),
  };
}
