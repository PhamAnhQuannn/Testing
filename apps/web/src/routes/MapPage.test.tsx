import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { PreviewBanner } from "../components/PreviewBanner";
import { EditorPanel } from "../components/EditorPanel";
import { normalizeMap, type MapSubtopic } from "../lib/api";
import { previewReason } from "../lib/lock";
import { MapView } from "./MapPage";

const raw = (over: Record<string, unknown>) => ({
  id: "dsa.arrays_strings.arrays",
  name_vi: "Mảng",
  module: "dsa.arrays_strings",
  status: "unlocked",
  score: 0,
  unlocked: true,
  due_cards: 0,
  target_intern: 2,
  lock_reasons: [],
  ...over,
});

const items: MapSubtopic[] = normalizeMap({
  subtopics: [
    raw({ status: "done", score: 3 }),
    raw({ id: "dsa.arrays_strings.sliding", name_vi: "Cửa sổ trượt", status: "in_progress", score: 1, due_cards: 2 }),
    raw({
      id: "dsa.arrays_strings.hash_tables",
      name_vi: "Bảng băm",
      status: "locked",
      unlocked: false,
      lock_reasons: [{ prerequisite: "dsa.arrays_strings.arrays", name_vi: "Mảng", score: 1, need: 2 }],
    }),
  ],
});

const html = (node: React.ReactElement) =>
  renderToStaticMarkup(createElement(MemoryRouter, null, node));

describe("MapView", () => {
  const out = html(createElement(MapView, { items }));

  it("shows score as a number plus a status label, not colour alone", () => {
    expect(out).toContain('aria-label="Điểm 3 trên 3"');
    expect(out).toContain("3/3");
    expect(out).toContain("Xong");
    expect(out).toContain("Đang học");
    expect(out).toContain("Khoá");
  });

  it("shows the due-review count", () => {
    expect(out).toContain("● 2 ôn");
  });

  it("explains a locked item, stays clickable, and offers test-out", () => {
    expect(out).toContain("cần Mảng ≥ 2 (hiện 1)");
    expect(out).toContain('href="/s/dsa.arrays_strings.hash_tables"');
    expect(out).toContain("xem trước");
    expect(out).toContain('href="/check/dsa.arrays_strings.hash_tables?ctx=test_out"');
  });

  it("does not show lock reasons on unlocked items", () => {
    expect(out.match(/lock-reasons/g)?.length).toBe(1);
  });
});

describe("preview mode", () => {
  const locked = items[2];
  it("previewReason is set only for locked subtopics", () => {
    expect(previewReason(locked)).toContain("cần Mảng ≥ 2");
    expect(previewReason(items[0])).toBeUndefined();
    expect(previewReason(null)).toBeUndefined();
  });

  it("banner links to test-out", () => {
    expect(html(createElement(PreviewBanner, { item: locked }))).toContain("ctx=test_out");
  });

  const panel = (previewReason?: string) =>
    html(
      createElement(EditorPanel, {
        code: "x = 1",
        onChange: () => undefined,
        onRun: () => undefined,
        onSubmit: () => undefined,
        onReset: () => undefined,
        running: false,
        runnerLoading: false,
        status: { state: "idle" },
        previewReason,
      }),
    );

  it("disables Run and Submit when previewing", () => {
    const out = panel("Đang xem trước");
    expect(out).toMatch(/<button[^>]*disabled[^>]*>▶ Run/);
    expect(out).toMatch(/<button[^>]*disabled[^>]*>✔ Submit/);
  });

  it("leaves Run and Submit enabled when unlocked", () => {
    const out = panel(undefined);
    expect(out).not.toMatch(/<button[^>]*disabled[^>]*>▶ Run/);
    expect(out).not.toMatch(/<button[^>]*disabled[^>]*>✔ Submit/);
  });
});
