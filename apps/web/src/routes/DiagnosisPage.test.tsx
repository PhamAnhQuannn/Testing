import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { normalizeDiagnosis } from "../lib/api";
import { DiagnosisContent } from "./DiagnosisPage";

const improve = (over: Record<string, unknown>) => ({
  subtopic_id: "py.core.loops",
  name_vi: "Vòng lặp",
  score: 1,
  state: "measured",
  firm: true,
  concepts: [],
  has_lesson: true,
  ...over,
});

const mod = (over: Record<string, unknown>) => ({
  module: "py.core",
  name_vi: "Python cơ bản",
  level: "Cơ bản",
  mean: 1.5,
  coverage: 0.4,
  tier: "đã đo",
  strong: [{ subtopic_id: "py.core.vars", name_vi: "Biến", score: 3 }],
  improve: [improve({ concepts: ["for", "while"] })],
  not_assessed_count: 2,
  ...over,
});

const view = (modules: unknown[], extra: Record<string, unknown> = {}) =>
  normalizeDiagnosis({
    ...extra,
    tracks: [{ key: "foundation", name_vi: "Nền tảng", sections: ["py"] }],
    domains: [
      { section: "py", name_vi: "Python", track: "foundation", level: "Cơ bản", mean: 1.5, coverage: 0.4, tier: "đã đo", modules },
    ],
  });

const render = (v: ReturnType<typeof view>) =>
  renderToStaticMarkup(createElement(MemoryRouter, null, createElement(DiagnosisContent, { view: v })));

describe("DiagnosisPage", () => {
  it("renders domains, modules, strong skills, coverage percent and not-assessed count", () => {
    const out = render(view([mod({})]));
    expect(out).toContain("Python");
    expect(out).toContain("Python cơ bản");
    expect(out).toContain("đã đo 40%");
    expect(out).toContain("Đã vững");
    expect(out).toContain("Biến");
    expect(out).toContain("Trọng tâm: for, while");
    expect(out).toContain("2 chủ đề chưa đo");
  });

  it("renders a Đo sâu button per module", () => {
    const out = render(view([mod({}), mod({ module: "py.datastructs", name_vi: "Cấu trúc dữ liệu" })]));
    expect(out.match(/Đo sâu</g)).toHaveLength(2);
  });

  it("shows the firm header for a measured gap", () => {
    const out = render(view([mod({})])); // improve item is firm by default
    expect(out).toContain(">Cần cải thiện<");
    expect(out).not.toContain("chưa đủ dữ liệu");
  });

  it("puts inferred gaps under the hedged header, not the firm one", () => {
    const out = render(view([mod({ improve: [improve({ firm: false, state: "likely_gap" })] })]));
    expect(out).toContain("Có thể cần xem lại (chưa đủ dữ liệu)");
    expect(out).not.toContain(">Cần cải thiện<");
  });

  it("splits a mixed module into both headers by per-item firmness", () => {
    const items = [
      improve({ subtopic_id: "a", name_vi: "A", firm: true }),
      improve({ subtopic_id: "b", name_vi: "B", firm: false, state: "likely_gap", has_lesson: false }),
    ];
    const out = render(view([mod({ improve: items })]));
    expect(out).toContain(">Cần cải thiện<");
    expect(out).toContain("Có thể cần xem lại (chưa đủ dữ liệu)");
  });

  it("renders the empty state when there are no domains", () => {
    expect(render(normalizeDiagnosis({ domains: [] }))).toContain("Chưa có dữ liệu hồ sơ.");
  });

  it("links lessons only when available, and always links the check", () => {
    const items = [improve({}), improve({ subtopic_id: "py.core.x", name_vi: "X", has_lesson: false })];
    const out = render(view([mod({ improve: items })]));
    expect(out).toContain('href="/s/py.core.loops"');
    expect(out).not.toContain('href="/s/py.core.x"');
    expect(out).toContain('href="/check/py.core.x?ctx=test_out"');
  });

  it("renders the role readiness headline", () => {
    const out = render(
      view([mod({})], {
        role: { track: "swe", level: "intern", key: "swe-intern", label_vi: "SWE Intern" },
        readiness_pct: 42,
      }),
    );
    expect(out).toContain("Sẵn sàng cho SWE Intern: 42% chuẩn");
    expect(out).not.toContain("coverage-warning");
  });

  it("shows the coverage warning only when flagged", () => {
    const warned = render(
      view([mod({})], { coverage_warning: true, coverage_message: "Phần lớn Python chưa đo — kết quả còn là ước tính" }),
    );
    expect(warned).toContain("Phần lớn Python chưa đo");
  });

  it("shows the gap note and stale hint", () => {
    const out = render(
      view([
        mod({
          role_relevant: 4,
          below_target: 3,
          gap: 5,
          readiness: 0.4,
          unmeasured_relevant: 2,
          improve: [improve({ stale: true })],
        }),
      ]),
    );
    expect(out).toContain("Cần nâng 3/4 mục lên chuẩn");
    expect(out).toContain("sẵn sàng 40%");
    expect(out).toContain("(đã lâu — nên đo lại)");
  });

  it("omits the gap note when nothing is role-relevant", () => {
    expect(render(view([mod({})]))).not.toContain("gap-note");
  });

  it("survives missing fields", () => {
    expect(() => render(normalizeDiagnosis({ domains: [{ section: "py", modules: [{}] }] }))).not.toThrow();
    expect(normalizeDiagnosis(null).domains).toEqual([]);
  });
});
