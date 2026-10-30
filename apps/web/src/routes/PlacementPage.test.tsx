import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  answerPlacement,
  normalizePlacementResult,
  normalizePlacementView,
  placementHeartbeat,
  skipPlacement,
  startPlacement,
  type CheckStepResult,
} from "../lib/api";
import { budgetView, gateChips, groupByModule, skillChip } from "../lib/placementFlow";
import { PlacementFinishedView, PlacementResultView, PlacementSessionView } from "./PlacementPage";

const html = (node: React.ReactElement) => renderToStaticMarkup(createElement(MemoryRouter, null, node));
const noop = () => {};

const rawView = (over: Record<string, unknown> = {}) => ({
  placement_id: 7,
  status: "in_progress",
  resumed: false,
  stale: false,
  stop_reason: null,
  message_vi: null,
  active_ms: 14 * 60_000 + 20_000,
  budget: { soft_ms: 45 * 60_000, hard_ms: 60 * 60_000, remaining_ms: 45 * 60_000 },
  progress: { gates_total: 7, gates_done: 2 },
  gates: [
    { code: "C1", subtopic_id: "py.core.strings", name_vi: "Python căn bản", outcome: "passed", l1: null, retry_after: null },
    { code: "C2", subtopic_id: "py.datastructs.dict", name_vi: "Cấu trúc dữ liệu", outcome: "passed_unclean", l1: null, retry_after: null },
    { code: "C3", subtopic_id: "dsa.arrays_strings.hash_tables", name_vi: "Mảng, hash", outcome: null, l1: null, retry_after: null },
    { code: "C4", subtopic_id: "dsa.two_pointers_window.two_pointers", name_vi: "Hai con trỏ", outcome: "unavailable", l1: null, retry_after: null },
  ],
  current: {
    gate: "C3",
    subtopic_id: "dsa.arrays_strings.hash_tables",
    name_vi: "Mảng, hash",
    probing: false,
    check_session_id: 11,
    elapsed_ms: 0,
    step: {
      index: 0,
      count: 2,
      item_id: "Q258-L2",
      level: 2,
      type: "write_code",
      minutes: 6,
      time_limit_ms: 360_000,
      prompt_md: "Viết `first_unique(s)`.",
      problem_id: "chk.first_unique",
    },
  },
  ...over,
});

const view = normalizePlacementView(rawView());

const session = (over: Partial<Parameters<typeof PlacementSessionView>[0]> = {}) =>
  createElement(PlacementSessionView, {
    view,
    step: view.current!.step!,
    activeMs: view.active_ms,
    itemMs: 30_000,
    last: null,
    busy: false,
    confirm: null,
    softOffer: false,
    onConfirm: noop,
    onGiveUp: noop,
    onFinish: noop,
    onExit: noop,
    onNext: noop,
    onKeepGoing: noop,
    commit: async () => true,
    ...over,
  });

describe("S2 session", () => {
  it("renders the gate step with progress, budget and the give-up / finish actions", () => {
    const out = html(session());
    expect(out).toContain("Cổng 3/7");
    expect(out).toContain("Đã dùng 14:20 / 45:00");
    expect(out).toContain("Không biết");
    expect(out).toContain("Kết thúc");
    expect(out).toContain("Tạm dừng");
    expect(out).toContain("Mảng, hash");
    expect(out).toContain("Mức 2");
    // write_code goes through the shared runner step (problem loads asynchronously)
    expect(out).toContain('aria-busy="true"');
  });

  it("chips: decided gates + the open one, never unavailable ones", () => {
    const chips = gateChips(view);
    expect(chips.map((c) => c.gate.code)).toEqual(["C1", "C2", "C3"]);
    expect(chips[2].current).toBe(true);
    const out = html(session());
    expect(out).toContain("đã đo");
    expect(out).toContain("đúng (chưa tính điểm)");
    expect(out).not.toContain("Hai con trỏ");
  });

  it("hides Không biết and shows a neutral result after an answer; a failed gate leaks no solution", () => {
    const last: CheckStepResult = {
      item_id: "Q258-L2",
      level: 2,
      type: "write_code",
      correct: false,
      passed: false,
      clean: false,
      gave_up: false,
      verdict: "WA",
      tests_passed: 3,
      tests_total: 8,
    };
    const out = html(session({ last }));
    expect(out).toContain("Chưa đúng");
    expect(out).toContain("WA");
    expect(out).toContain("Tiếp tục");
    expect(out).not.toContain(">Không biết<");
    expect(out).not.toMatch(/answer_md|solution.py|reference/i); // the only mention of a solution is the promise there is none
    expect(out).not.toMatch(/streak|chuỗi ngày|phạt/i);
  });

  it("finished sitting: result button + server message", () => {
    const done = normalizePlacementView(
      rawView({ status: "finished", stop_reason: "fail_after_pass", message_vi: "Đã tìm được ranh giới trình độ của bạn." }),
    );
    const last: CheckStepResult = {
      item_id: "Q258-L2",
      level: 2,
      type: "write_code",
      correct: true,
      passed: true,
      clean: false,
      gave_up: false,
      reason: "over_time",
    };
    const out = html(session({ view: done, last }));
    expect(out).toContain("Xem kết quả");
    expect(out).toContain("Đã tìm được ranh giới trình độ của bạn.");
  });

  it("finished view with no current step shows the last result, not the empty state", () => {
    const done = normalizePlacementView(
      rawView({ status: "finished", current: null, stop_reason: "fail_after_pass", message_vi: "Đã tìm được ranh giới trình độ của bạn." }),
    );
    const last: CheckStepResult = {
      item_id: "Q258-L2",
      level: 2,
      type: "write_code",
      correct: false,
      passed: false,
      clean: false,
      gave_up: false,
      verdict: "WA",
      tests_passed: 3,
      tests_total: 8,
    };
    const out = html(createElement(PlacementFinishedView, { view: done, last, onNext: noop }));
    expect(out).toContain("Chưa đúng");
    expect(out).toContain("Đã tìm được ranh giới trình độ của bạn.");
    expect(out).toContain("Xem kết quả");
    expect(out).not.toContain("Chưa có mục");
  });

  it("hides the gate name/level line while a result is shown", () => {
    const last: CheckStepResult = { item_id: "Q258-L2", level: 2, type: "write_code", correct: true, passed: true, clean: true, gave_up: false };
    expect(html(session({ last }))).not.toContain("Mức 2");
  });

  it("budget phases: soft at 45 min, hard at 60 min", () => {
    expect(budgetView(10 * 60_000, 45 * 60_000, 60 * 60_000).phase).toBe("within");
    expect(budgetView(45 * 60_000, 45 * 60_000, 60 * 60_000).phase).toBe("soft");
    expect(budgetView(61 * 60_000, 45 * 60_000, 60 * 60_000)).toMatchObject({ phase: "hard", pct: 100 });
    expect(html(session({ activeMs: 61 * 60_000 }))).toContain("hoàn thành mục đang làm");
    expect(html(session({ softOffer: true }))).toContain("Đã dùng 45 phút");
  });

  it("confirm modals", () => {
    expect(html(session({ confirm: "giveup" }))).toContain("không bị khoá");
    expect(html(session({ confirm: "finish" }))).toContain("Kết thúc và xem kết quả");
    expect(html(session({ confirm: "exit" }))).toContain("được giữ lại");
  });
});

const rawResult = (over: Record<string, unknown> = {}) => ({
  placement_id: 7,
  status: "finished",
  stop_reason: "fail_after_pass",
  message_vi: "Đã tìm được ranh giới trình độ của bạn.",
  active_ms: 41 * 60_000,
  seeded: ["py.core.strings", "py.datastructs.dict"],
  skill_map: [
    { subtopic_id: "py.core.strings", name_vi: "Chuỗi", score: 2, state: "measured", seeded: true, known_basic: true, placement_hint: null },
    { subtopic_id: "py.core.loops", name_vi: "Vòng lặp", score: 0, state: "likely_known", seeded: false, known_basic: false, placement_hint: "likely_known" },
    { subtopic_id: "py.datastructs.dict", name_vi: "Dict", score: 2, state: "measured", seeded: true, known_basic: true, placement_hint: null },
    { subtopic_id: "dsa.arrays_strings.hash_tables", name_vi: "Bảng băm", score: 0, state: "measured", seeded: false, known_basic: false, placement_hint: null },
    { subtopic_id: "dsa.trees.tree_basics", name_vi: "Cây", score: 0, state: "not_assessed", seeded: false, known_basic: false, placement_hint: null },
  ],
  strong_areas: [{ gate: "C1", name_vi: "Python căn bản", subtopic_id: "py.core.strings" }],
  weak_areas: [
    { gate: "C3", name_vi: "Mảng, hash", subtopic_id: "dsa.arrays_strings.hash_tables", outcome: "failed", retry_after: null },
  ],
  start: null,
  content_pending: true,
  test_out_candidates: ["py.core.loops"],
  counts: { measured: 3, likely_known: 1, likely_gap: 0, not_assessed: 1 },
  ...over,
});

describe("S3 reduced result", () => {
  const result = normalizePlacementResult(rawResult());

  it("shows the seeded map, strong / weak areas, test-out and the content-pending note", () => {
    const out = html(createElement(PlacementResultView, { result }));
    expect(out).toContain("Kết quả đánh giá");
    expect(out).toContain("41 phút");
    expect(out).toContain("Chuỗi 2"); // seeded chip carries its score
    expect(out).toContain("Dict 2");
    expect(out).toContain("Vòng lặp ? (có thể đã biết)"); // inference: no score
    expect(out).toContain("Cây ?");
    expect(out).toContain("Làm tốt:");
    expect(out).toContain("Python căn bản");
    expect(out).toContain("Cần củng cố:");
    expect(out).toContain("Mảng, hash");
    expect(out).toContain('data-testid="content-pending"');
    expect(out).toContain("đang soạn");
    expect(out).toContain('href="/check/py.core.loops?ctx=test_out"');
    expect(out).toContain('href="/"'); // Bắt đầu học CTA
    expect(out).toContain("Đã tìm được ranh giới trình độ của bạn.");
  });

  it("offers a start lesson when the API has one, and no pending note", () => {
    const out = html(
      createElement(PlacementResultView, {
        result: normalizePlacementResult(
          rawResult({ start: { subtopic_id: "py.core.loops", name_vi: "Vòng lặp" }, content_pending: false }),
        ),
      }),
    );
    expect(out).toContain('href="/s/py.core.loops"');
    expect(out).not.toContain("content-pending");
  });

  it("groups by module and chips seeded vs inferred", () => {
    const groups = groupByModule(result.skill_map);
    expect(groups.map((g) => g.module)).toEqual(["py.core", "py.datastructs", "dsa.arrays_strings", "dsa.trees"]);
    expect(skillChip(result.skill_map[0]).kind).toBe("seeded");
    expect(skillChip(result.skill_map[1]).kind).toBe("inferred");
    expect(skillChip(result.skill_map[3]).kind).toBe("measured");
  });
});

describe("placement api", () => {
  let fetchMock: ReturnType<typeof vi.fn>;
  beforeEach(() => {
    fetchMock = vi.fn().mockImplementation(
      async () =>
        new Response(JSON.stringify({ ...rawView(), result: { item_id: "Q258-L2", passed: true }, placement: rawView() }), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }),
    );
    vi.stubGlobal("fetch", fetchMock);
  });
  afterEach(() => vi.unstubAllGlobals());
  const init = (n: number) => fetchMock.mock.calls[n][1] as RequestInit & { headers: Record<string, string> };
  const url = (n: number) => fetchMock.mock.calls[n][0] as string;

  it("posts the right paths with Idempotency-Key", async () => {
    await startPlacement({ restart: true }, "k-1");
    expect(url(0)).toBe("/api/placement");
    expect(init(0).headers["Idempotency-Key"]).toBe("k-1");
    expect(JSON.parse(init(0).body as string)).toEqual({ restart: true });

    const res = await answerPlacement(7, { item_id: "Q258-L2", elapsed_ms: 1, answer: "x" }, "k-2");
    expect(url(1)).toBe("/api/placement/7/answer");
    expect(init(1).headers["Idempotency-Key"]).toBe("k-2");
    expect(res.placement.current?.step?.item_id).toBe("Q258-L2");

    await skipPlacement(7, { item_id: "Q258-L2", elapsed_ms: 1 });
    expect(url(2)).toBe("/api/placement/7/skip");
    expect(init(2).headers["Idempotency-Key"]).toBeTruthy();

    await placementHeartbeat(7, 15_400.6, 3000);
    expect(url(3)).toBe("/api/placement/7/heartbeat");
    expect(JSON.parse(init(3).body as string)).toEqual({ active_ms: 15401, item_elapsed_ms: 3000 });
  });
});

describe("placement mcq step", () => {
  it("renders an mcq step with rung label and knowledge_gap gate without crashing", () => {
    const v = normalizePlacementView(
      rawView({
        gates: [
          { code: "C1", subtopic_id: "a", name_vi: "Gate A", outcome: "knowledge_gap", l1: null, retry_after: null, rung_results: { "0": "failed" } },
          { code: "C3", subtopic_id: "b", name_vi: "Gate B", outcome: null, l1: null, retry_after: null },
        ],
        current: {
          gate: "C3", subtopic_id: "b", name_vi: "Gate B", probing: false, rung: 0, check_session_id: 12, elapsed_ms: 0,
          step: { index: 0, count: 1, item_id: "m1", level: 1, type: "mcq", minutes: 1, time_limit_ms: 60000, prompt_md: "Chọn đúng?", choices: ["A1", "B1"] },
        },
      }),
    );
    expect(v.current!.rung).toBe(0);
    expect(v.current!.step!.choices).toEqual(["A1", "B1"]);
    const out = html(createElement(PlacementSessionView, {
      view: v, step: v.current!.step!, activeMs: 0, itemMs: 0, last: null, busy: false, confirm: null, softOffer: false,
      onConfirm: noop, onGiveUp: noop, onFinish: noop, onExit: noop, onNext: noop, onKeepGoing: noop, commit: async () => true,
    }));
    expect(out).toContain("Kiến thức");
    expect(out).toContain("A1");
    expect(out).toContain("hổng kiến thức");
  });
});
