import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { normalizeDiagnosis } from "../lib/api";
import { DiagnosisContent, RoleSelector, composeRole, splitRole } from "./DiagnosisPage";

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

  it("renders weak and suspected concept status, else the descriptive concepts", () => {
    const withStatus = render(
      view([
        mod({
          improve: [
            improve({
              concepts: ["for", "while"],
              concept_status: [
                { slug: "for-loop", text: "Vòng for", status: "weak", n_hit: 0, n_miss: 2 },
                { slug: "break", text: "break", status: "suspected", n_hit: 1, n_miss: 1 },
              ],
            }),
          ],
        }),
      ]),
    );
    expect(withStatus).toContain("Hổng: Vòng for");
    expect(withStatus).toContain("break (nghi ngờ — cần đo thêm)");
    expect(withStatus).not.toContain("Trọng tâm");
    const empty = render(view([mod({})]));
    expect(empty).toContain("Trọng tâm: for, while");
    expect(empty).not.toContain("concept-status");
  });

  it("renders the practices section with a status chip per practice", () => {
    const practices = [
      { practice: "verify", label_vi: "Kiểm chứng đầu ra", status: "weak", n_hit: 0, n_miss: 2 },
      { practice: "review", label_vi: "Đọc & review code", status: "suspected", n_hit: 0, n_miss: 1 },
      { practice: "measure", label_vi: "Đo lường & eval", status: "untested", n_hit: 0, n_miss: 0 },
    ];
    const out = render(view([mod({})], { practices }));
    expect(out).toContain("Thói quen làm việc");
    expect(out).toContain("Kiểm chứng đầu ra");
    expect(out).toContain(">Hổng<");
    expect(out).toContain(">nghi ngờ<");
    expect(out).toContain(">chưa đo<");
    expect(render(view([mod({})]))).not.toContain("Thói quen làm việc");
    expect(normalizeDiagnosis(null).practices).toEqual([]);
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

  it("renders the 4-level readiness row with the selected level emphasized", () => {
    const out = render(
      view([mod({})], {
        role: { track: "swe", level: "junior", key: "swe-junior", label_vi: "SWE Junior" },
        readiness_pct: 30,
        levels: [
          { level: "intern", readiness_pct: 60, label_vi: "SWE Intern" },
          { level: "fresher", readiness_pct: 45, label_vi: "SWE Fresher" },
          { level: "junior", readiness_pct: 30, label_vi: "SWE Junior" },
          { level: "senior", readiness_pct: null, label_vi: "SWE Senior" },
        ],
      }),
    );
    expect(out).toContain("Sẵn sàng cho SWE Junior: 30% chuẩn");
    expect(out).toContain("Intern 60%");
    expect(out).toContain("Fresher 45%");
    expect(out).toContain("<strong aria-current=\"true\">Junior 30%</strong>");
    expect(out).toContain("<span> · Senior</span>"); // null % hidden
  });

  it("composes role keys from the track toggle and level select", () => {
    expect(composeRole("swe", "junior")).toBe("swe-junior");
    expect(splitRole("ai-senior")).toEqual(["ai", "senior"]);
    expect(splitRole("garbage")).toEqual(["swe", "intern"]);
    const out = renderToStaticMarkup(
      createElement(RoleSelector, { value: "swe-junior", onChange: () => {} }),
    );
    expect(out).toContain('data-testid="track-toggle"');
    expect(out).toMatch(/<option value="junior" selected/);
    expect(out.match(/<option /g)).toHaveLength(4);
  });
});
