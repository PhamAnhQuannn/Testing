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

export type SecStatus = "done" | "ready" | "todo";

/**
 * Pure: how far along a section is. "done" = finished; "ready" = may advance without finishing
 * (code section the user chose to skip); "todo" = still needs the user's action.
 */
export function sectionStatus(
  s: Section,
  p: {
    visited: Set<string>;
    done: Set<string>;
    results: Record<string, boolean>;
    skipped: Set<string>;
  },
): SecStatus {
  if (s.kind === "code") {
    if (s.exercise && p.done.has(s.exercise.id)) return "done";
    return p.skipped.has(s.id) ? "ready" : "todo";
  }
  if (s.kind === "quiz") {
    const graded = s.blocks.filter(isGraded);
    return graded.length > 0 && graded.every((b) => b.id in p.results) ? "done" : "todo";
  }
  return p.visited.has(s.id) ? "done" : "todo";
}

/** Pure: whether the "next section" button may unlock for a status. */
export function canAdvance(status: SecStatus): boolean {
  return status !== "todo";
}

/** Index of the section containing a block id (or whose own id it is); -1 if none. */
export function sectionIndexOfBlock(sections: Section[], blockId: string | undefined): number {
  if (!blockId) return -1;
  return sections.findIndex((s) => s.id === blockId || s.blocks.some((b) => b.id === blockId));
}

/** One entry in the whole-lesson exercise list (used by the right-pane exercise switcher). */
export interface LessonExerciseEntry {
  /** Index of the section the exercise lives in. */
  sectionIdx: number;
  /** The section's title ("" for the implicit intro). */
  sectionTitle: string;
  exercise: CodeExerciseBlock;
}

/**
 * Pure: every `code_exercise` across the whole lesson, in document order, tagged with its section.
 * Feeds the "danh sách bài tập" rail so the learner can jump to any exercise from the right pane.
 */
export function allLessonExercises(sections: Section[]): LessonExerciseEntry[] {
  const out: LessonExerciseEntry[] = [];
  sections.forEach((s, sectionIdx) => {
    for (const b of s.blocks) {
      if (b.type === "code_exercise") {
        out.push({ sectionIdx, sectionTitle: s.title, exercise: b });
      }
    }
  });
  return out;
}
