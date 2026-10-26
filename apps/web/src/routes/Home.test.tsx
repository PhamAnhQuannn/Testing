import { createElement, type ReactElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { isActive } from "../lib/activity";
import { normalizeNext } from "../lib/api";
import { clock, formatStudy, HomeView } from "./Home";

const html = (node: ReactElement) => renderToStaticMarkup(createElement(MemoryRouter, null, node));
const noop = () => {};

const item = (id: string, over: Record<string, unknown> = {}) => ({
  id,
  name_vi: `Mục ${id}`,
  score: 0,
  target_intern: 2,
  status: "unlocked",
  known_basic: false,
  lesson_done: false,
  has_lesson: true,
  check_retry_after: null,
  due_card: false,
  suggested_problem: null,
  ...over,
});

const nextOf = (over: Record<string, unknown> = {}) =>
  normalizeNext({
    must_raise: [],
    up_next: [item("py.datastructs.dict"), item("py.core.loops")],
    locked_preview: [],
    due_count: 0,
    backlog: false,
    study: { today_s: 4800, week_s: 21900 },
    ...over,
  });

const view = (next = nextOf(), resume: Parameters<typeof HomeView>[0]["resume"] = null) =>
  html(createElement(HomeView, { next, resume, onGo: noop }));

const resumeOf = (over: Record<string, unknown> = {}) => ({
  primary: {
    mode: "lesson" as const,
    route: "/s/py.datastructs.dict",
    ref: { subtopic_id: "py.datastructs.dict" },
    context: {},
    updated_at: "2026-10-25T01:00:00Z",
    stale: false,
    ...over,
  },
  others: [],
});

describe("Home (S4)", () => {
  it("lists up_next with exactly one /s/:id link per subtopic and a score badge first", () => {
    const out = view();
    expect(out.match(/href="\/s\/py\.datastructs\.dict"/g)).toHaveLength(1);
    expect(out).toMatch(/<a [^>]*href="\/s\/py\.datastructs\.dict"[^>]*><span class="badge s0"/);
    expect(out).toContain("Học tiếp ▶"); // first item carries the continue CTA
    expect(out.indexOf("py.datastructs.dict")).toBeLessThan(out.indexOf("py.core.loops"));
  });

  it("keeps a single /s/:id link even with a resume banner and a must_raise row for that item", () => {
    const next = nextOf({
      must_raise: [
        {
          prerequisite: { id: "py.datastructs.dict", name_vi: "dict", score: 1, need: 2 },
          unlocks: { id: "py.datastructs.comprehensions", name_vi: "comprehensions" },
          sole_blocker: true,
          also_blocks: 0,
          suggested_problem: { id: "ransom-note", title: "Ransom Note", title_vi: null, difficulty: "easy", role: "practice" },
          test_out: { available: true, retry_after: null },
        },
      ],
    });
    const out = view(next, resumeOf());
    expect(out.match(/href="\/s\/py\.datastructs\.dict"/g)).toHaveLength(1);
    expect(out).toContain("Cần lên điểm 2 để mở mục sau");
    expect(out).toContain('href="/check/py.datastructs.dict?ctx=test_out"');
    expect(out).toContain('href="/p/ransom-note"');
  });

  it("shows the resume banner only when /resume has something", () => {
    expect(view()).not.toContain("resume-banner");
    const out = view(nextOf(), resumeOf());
    expect(out).toContain("Tiếp tục nơi bạn dừng");
    expect(out).toContain("bài học");
    expect(out).toContain("Mục py.datastructs.dict");
    expect(out).toContain(">Tiếp tục<");
    expect(view(nextOf(), resumeOf({ stale: true }))).toContain(">Mở lại<");
  });

  it("has a due-review entry, and a soft backlog note only when backlog is true", () => {
    const none = view();
    expect(none).toContain("Không có thẻ đến hạn");
    expect(none).not.toContain("backlog-banner");
    const out = view(nextOf({ due_count: 24, backlog: true }));
    expect(out).toContain('href="/review"');
    expect(out).toContain("Ôn 24 thẻ");
    expect(out).toContain("backlog-banner");
  });

  it("puts a check_retry_locked item after, labelled with the time instead of the CTA", () => {
    const next = nextOf({
      up_next: [item("a", { check_retry_after: "2026-10-25T07:30:00Z" }), item("b")],
    });
    const out = view(next);
    expect(out).toContain("chờ đến");
    expect(out).not.toContain("Học tiếp ▶"); // the first row is the waiting one
  });

  it("never shows schedule, quota, streak or penalty wording", () => {
    const out = view(
      nextOf({
        must_raise: [],
        locked_preview: [{ id: "x", name_vi: "X", lock_reasons: [{ prerequisite: "y", name_vi: "Y", score: 1, need: 2 }] }],
        due_count: 30,
        backlog: true,
      }),
      resumeOf(),
    ).toLowerCase();
    for (const w of ["trễ", "late", "quota", "định mức", "streak", "chuỗi", "hôm nay phải", "mục tiêu", "phạt", "bỏ lỡ"]) {
      expect(out).not.toContain(w);
    }
    expect(out).toContain("chỉ để xem");
  });

  it("formats study time neutrally", () => {
    expect(formatStudy(4800)).toBe("1h20");
    expect(formatStudy(25 * 60 + 10)).toBe("25 phút");
    expect(formatStudy(0)).toBe("0 phút");
    expect(clock("2026-10-25T07:30:00Z")).toMatch(/^\d\d:\d\d$/);
  });
});

describe("activity ping gate", () => {
  it("pings only while the page is visible and focused", () => {
    expect(isActive("visible", true)).toBe(true);
    expect(isActive("hidden", true)).toBe(false);
    expect(isActive("visible", false)).toBe(false);
  });
});

describe("normalizeNext", () => {
  it("tolerates a missing body", () => {
    const n = normalizeNext(undefined);
    expect(n.up_next).toEqual([]);
    expect(n.study).toEqual({ today_s: 0, week_s: 0 });
  });
});
