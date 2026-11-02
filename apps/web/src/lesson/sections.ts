import type { LessonBlock } from "../lib/api";
import { isGraded } from "../lib/grade";

export type CodeExerciseBlock = Extract<LessonBlock, { type: "code_exercise" }>;
export type SectionBlock = Extract<LessonBlock, { type: "section" }>;
export type ContentBlock = Exclude<LessonBlock, SectionBlock>;

export interface Section {
  /** The `section` block's id; the implicit intro uses its first block's id (or a sentinel). */
  id: string;
  /** "" for the implicit intro / a lesson with no `section` block. */
  title: string;
  summary?: string;
  /** The section's non-section blocks, in order. */
  blocks: ContentBlock[];
  exercise?: CodeExerciseBlock;
  kind: "code" | "quiz" | "theory";
}

export const INTRO_SENTINEL = "__intro__";

function build(
  id: string,
  title: string,
  summary: string | undefined,
  ref: string | undefined,
  blocks: ContentBlock[],
): Section {
  const exercises = blocks.filter((b): b is CodeExerciseBlock => b.type === "code_exercise");
  const exercise = (ref ? exercises.find((e) => e.id === ref) : undefined) ?? exercises[0];
  const kind: Section["kind"] = exercise ? "code" : blocks.some(isGraded) ? "quiz" : "theory";
  return { id, title, summary, blocks, exercise, kind };
}

/**
 * Pure: split the flat `blocks` array at `section` blocks. Blocks before the first `section` form an
 * implicit intro (omitted when empty). No `section` block at all = one section holding everything.
 */
export function deriveSections(blocks: LessonBlock[]): Section[] {
  const sections: Section[] = [];
  let head: { id: string; title: string; summary?: string; ref?: string } | null = null;
  let buf: ContentBlock[] = [];
  const flush = () => {
    if (head) sections.push(build(head.id, head.title, head.summary, head.ref, buf));
    else if (buf.length) sections.push(build(buf[0].id, "", undefined, undefined, buf));
    buf = [];
  };
  for (const b of blocks) {
    if (b.type === "section") {
      flush();
      head = { id: b.id, title: b.title_vi, summary: b.summary_vi, ref: b.exercise_ref };
    } else buf.push(b);
  }
  flush();
  if (sections.length === 0) sections.push(build(INTRO_SENTINEL, "", undefined, undefined, []));
  return sections;
}

/** Index of the section containing a block id (or whose own id it is); -1 if none. */
export function sectionIndexOfBlock(sections: Section[], blockId: string | undefined): number {
  if (!blockId) return -1;
  return sections.findIndex((s) => s.id === blockId || s.blocks.some((b) => b.id === blockId));
}
