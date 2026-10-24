// Quiz bookkeeping. Grading itself is server-side (POST /quiz/answers): the lesson JSON ships no answers.
import type { LessonBlock } from "./api";

export const normalizeOutput = (text: string) =>
  text
    .trimEnd()
    .split("\n")
    .map((line) => line.trimEnd())
    .join("\n");

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
