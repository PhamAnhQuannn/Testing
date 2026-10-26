import { createElement, type ReactElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { normalizeReviewQueue, normalizeReviewResult, type LessonBlock } from "../lib/api";
import { assembleSession } from "../lib/review";
import { CardHeader, RecallView, ResultCard, ReviewDone, ReviewTop } from "./ReviewPage";

const html = (node: ReactElement) => renderToStaticMarkup(createElement(MemoryRouter, null, node));
const noop = () => {};

const recallItem = (i: number) => ({ kind: "recall", ref: `s${i}#q1`, type: "quiz_mcq", subtopic_id: `s${i}` });
const card = (i: number, over: Record<string, unknown> = {}) => ({
  subtopic_id: `s${i}`,
  name_vi: `Mục ${i}`,
  box: 1,
  due_on: "2026-10-20",
  overdue_days: 2,
  score: 1,
  lapses: 0,
  item_kind: "recall",
  item: recallItem(i),
  recall_item: recallItem(i),
  ...over,
});
const queueOf = (n: number, over: Record<string, unknown> = {}) =>
  normalizeReviewQueue({
    today: "2026-10-25",
    total_due: n,
    backlog_warn: 20,
    backlog: false,
    cards: Array.from({ length: n }, (_, i) => card(i + 1)),
    short_session: {
      enabled: true,
      size: 6,
      max_code: 2,
      cards: Array.from({ length: Math.min(n, 6) }, (_, i) => ({ subtopic_id: `s${i + 1}`, item_kind: "recall" })),
    },
    ...over,
  });

const top = (queue: ReturnType<typeof queueOf>, mode: "short" | "full" = "full", reviewed = 0) =>
  html(createElement(ReviewTop, { queue, mode, onMode: noop, reviewed, showPreset: reviewed === 0 }));

describe("ReviewTop", () => {
  it("shows the backlog banner only when backlog is true, with soft wording", () => {
    expect(top(queueOf(3))).not.toContain("backlog-banner");
    const out = top(queueOf(25, { backlog: true }));
    expect(out).toContain("backlog-banner");
    expect(out).toContain("25 thẻ");
    for (const bad of ["trễ", "muộn", "phạt", "streak", "late", "behind"]) expect(out.toLowerCase()).not.toContain(bad);
  });

  it("offers the Phiên ngắn preset as a suggestion next to the full queue", () => {
    const out = top(queueOf(10));
    expect(out).toContain("Phiên ngắn");
    expect(out).toContain("Tất cả (10)");
    expect(top(queueOf(10), "short")).toContain("Phiên ngắn: 6 thẻ, tối đa 2 thẻ code");
    expect(top(queueOf(4))).not.toContain("Phiên ngắn"); // nothing to trim
  });
});

describe("steps", () => {
  const q = queueOf(2);
  const sc = assembleSession(q, "full")[0];

  it("recall step shows the prompt and self-grade buttons", () => {
    const block = { id: "q1", type: "quiz_mcq", prompt_md: "O(1) lookup?", options: [{ id: "a", text_md: "dict" }] } as LessonBlock;
    const out = html(createElement(RecallView, { sc, block, busy: false, onResult: noop, onSkip: noop }));
    expect(out).toContain("O(1) lookup?");
    expect(out).toContain("Nhớ rồi");
    expect(out).toContain("Chưa nhớ");
    expect(out).toContain("Bỏ qua");
  });

  it("card header shows box and kind", () => {
    const out = html(createElement(CardHeader, { sc, left: 2 }));
    expect(out).toContain("hộp 1");
    expect(out).toContain("nhớ nhanh");
    expect(out).toContain("còn 2 thẻ");
  });

  it("result card shows box move and score change", () => {
    const result = normalizeReviewResult({
      subtopic_id: "s1", success: true, box_before: 3, box_after: 4, due_on: "2026-11-01", lapses: 0,
      score: { before: 2, after: 3 }, newly_unlocked: [],
    });
    const out = html(createElement(ResultCard, { result, today: "2026-10-25", onNext: noop, hasNext: true }));
    expect(out).toContain("Hộp 3 → hộp 4");
    expect(out).toContain("Điểm mục: 2 → 3");
    expect(out).toContain("Thẻ tiếp");
  });
});

describe("ReviewDone", () => {
  it("empty queue shows the friendly nothing-due state", () => {
    const out = html(createElement(ReviewDone, { queue: queueOf(0), mode: "full", reviewed: 0, skipped: 0, onFull: noop }));
    expect(out).toContain("Hết thẻ đến hạn");
    expect(out).toContain("Học tiếp");
  });

  it("finished preset offers Ôn tiếp while cards remain", () => {
    const out = html(createElement(ReviewDone, { queue: queueOf(10), mode: "short", reviewed: 6, skipped: 0, onFull: noop }));
    expect(out).toContain("Xong phiên ngắn");
    expect(out).toContain("Ôn tiếp");
  });
});
