import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import type { LessonBlock } from "../lib/api";
import type { BlockContext } from "./Blocks";
import { SectionPane } from "./SectionPane";
import { allLessonInteractive, deriveSections, type InteractiveBlock } from "./sections";

const text = (id: string): LessonBlock => ({ id, type: "text", md: id });
const quiz = (id: string): LessonBlock => ({ id, type: "quiz_mcq", prompt_md: `P-${id}`, options: [{ id: "a", text_md: "A" }] });
const sec = (id: string): LessonBlock => ({ id, type: "section", title_vi: `T-${id}` }) as LessonBlock;

const ctx: BlockContext = {
  subtopicId: "x",
  runNo: 1,
  known: {},
  onAnswered: () => undefined,
  doneExercises: new Set(),
  canEdit: true,
};

function render(blocks: LessonBlock[], { preview = false, current }: { preview?: boolean; current?: InteractiveBlock } = {}) {
  const [section] = deriveSections(blocks);
  const all = allLessonInteractive(deriveSections(blocks));
  const cur = current ?? section.interactive[0];
  return renderToStaticMarkup(
    createElement(
      MemoryRouter,
      null,
      createElement(SectionPane, {
        subtopicId: "x",
        section,
        current: cur,
        ctx,
        preview,
        canEdit: !preview,
        results: {},
        done: new Set<string>(),
        practice: [],
        interactive: section.interactive,
        index: cur ? section.interactive.findIndex((b) => b.id === cur.id) : -1,
        allInteractive: all,
        onPrev: () => undefined,
        onNext: () => undefined,
        onJump: () => undefined,
        onPassed: () => undefined,
        onNextSection: () => undefined,
        isLast: true,
      }),
    ),
  );
}

describe("SectionPane", () => {
  it("renders a quiz (right pane) with the Câu i/N counter", () => {
    const out = render([sec("s"), quiz("q1")]);
    expect(out).toContain("Câu 1/1");
    expect(out).toContain("P-q1"); // the quiz prompt is rendered in the right pane
  });

  it("theory-only section is never blank — shows a Ghi nhớ card", () => {
    const out = render([sec("s"), text("a")]);
    expect(out).toContain("Ghi nhớ");
  });

  it("preview mode disables the interactive fieldset and shows a lock note", () => {
    const out = render([sec("s"), quiz("q1")], { preview: true });
    expect(out).toContain("Mục đang khoá");
    expect(out).toMatch(/<fieldset[^>]*disabled/);
  });
});
