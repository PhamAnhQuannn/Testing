import { describe, expect, it } from "vitest";
import { normalizeReviewQueue, normalizeReviewResult } from "./api";
import {
  assembleSession,
  backlogText,
  dueInText,
  hasMoreThanPreset,
  lessonBlockOf,
  remaining,
  resultView,
  waitingText,
} from "./review";

const rawCard = (i: number, over: Record<string, unknown> = {}) => ({
  subtopic_id: `s${i}`,
  name_vi: `Mục ${i}`,
  box: 1,
  due_on: "2026-10-20",
  overdue_days: 2,
  score: 1,
  lapses: 0,
  item_kind: "recall",
  item: { kind: "recall", ref: `s${i}#q1`, type: "quiz_mcq", subtopic_id: `s${i}` },
  recall_item: { kind: "recall", ref: `s${i}#q1`, type: "quiz_mcq", subtopic_id: `s${i}` },
  ...over,
});
const codeCard = (i: number) =>
  rawCard(i, {
    box: 4,
    item_kind: "code",
    item: { kind: "code", ref: `prob${i}`, type: "write_code", subtopic_id: `s${i}` },
  });

const rawQueue = (cards: unknown[], over: Record<string, unknown> = {}) => ({
  today: "2026-10-25",
  total_due: cards.length,
  backlog_warn: 20,
  backlog: false,
  cards,
  short_session: { enabled: true, size: 2, max_code: 2, cards: [] },
  ...over,
});

describe("assembleSession", () => {
  const cards = [codeCard(1), rawCard(2), codeCard(3), rawCard(4)];
  const queue = normalizeReviewQueue(
    rawQueue(cards, {
      short_session: {
        enabled: true,
        size: 3,
        max_code: 2,
        cards: [
          { subtopic_id: "s1", item_kind: "code" },
          { subtopic_id: "s2", item_kind: "recall" },
          { subtopic_id: "s3", item_kind: "recall" }, // demoted
        ],
      },
    }),
  );

  it("full mode keeps the whole queue in server order", () => {
    expect(assembleSession(queue, "full").map((s) => s.card.subtopic_id)).toEqual(["s1", "s2", "s3", "s4"]);
  });

  it("short mode limits to the hint and demotes code to the recall item, without dropping the queue", () => {
    const short = assembleSession(queue, "short");
    expect(short.map((s) => [s.card.subtopic_id, s.item.kind])).toEqual([
      ["s1", "code"],
      ["s2", "recall"],
      ["s3", "recall"],
    ]);
    expect(queue.cards).toHaveLength(4);
    expect(hasMoreThanPreset(queue)).toBe(true);
  });

  it("falls back to the full queue when the preset is off", () => {
    const off = normalizeReviewQueue(
      rawQueue(cards, { short_session: { enabled: false, size: null, max_code: 2, cards: [] } }),
    );
    expect(assembleSession(off, "short")).toHaveLength(4);
    expect(hasMoreThanPreset(off)).toBe(false);
  });

  it("leaves out cards with no usable item and tracks remaining", () => {
    const q = normalizeReviewQueue(rawQueue([rawCard(1, { item: null, item_kind: null, recall_item: null }), rawCard(2)]));
    const session = assembleSession(q, "full");
    expect(session).toHaveLength(1);
    expect(remaining(session, new Set(["s2"]))).toHaveLength(0);
  });
});

describe("wording and views", () => {
  it("backlog and waiting text are soft", () => {
    const text = [backlogText(25), waitingText(3), waitingText(0)].join(" ").toLowerCase();
    for (const bad of ["trễ", "muộn", "phạt", "streak", "late", "behind", "chậm"]) expect(text).not.toContain(bad);
  });

  it("resultView shows box move, next due and score change only when changed", () => {
    const base = {
      subtopic_id: "s1",
      success: true,
      item_ref: "s1#q1",
      item_kind: "recall",
      box_before: 3,
      box_after: 4,
      due_on: "2026-11-01",
      lapses: 0,
      score: { before: 2, after: 2 },
      newly_unlocked: [],
    };
    const same = resultView(normalizeReviewResult(base), "2026-10-25");
    expect(same.lines[0]).toBe("Hộp 3 → hộp 4");
    expect(same.lines[1]).toContain("+7 ngày");
    expect(same.lines.join()).not.toContain("Điểm mục");
    const up = resultView(normalizeReviewResult({ ...base, score: { before: 2, after: 3 } }), "2026-10-25");
    expect(up.lines.join()).toContain("Điểm mục: 2 → 3");
    const fail = resultView(normalizeReviewResult({ ...base, success: false, box_after: 1, due_on: "2026-10-26" }), "2026-10-25");
    expect(fail.lines[1]).toContain("ngày mai");
    expect(fail.title).not.toMatch(/sai|trượt|thất bại/i);
  });

  it("dueInText and lessonBlockOf", () => {
    expect(dueInText("2026-10-25", "2026-10-25")).toBe("hôm nay");
    expect(dueInText("2026-10-30")).toBe("2026-10-30");
    expect(lessonBlockOf("a.b#q1")).toEqual({ subtopicId: "a.b", blockId: "q1" });
    expect(lessonBlockOf("check:a.b:Q1")).toBeNull();
  });
});
