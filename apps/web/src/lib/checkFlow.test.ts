import { describe, expect, it } from "vitest";
import { ApiError, normalizeCheckAnswer, type CheckStepResult } from "./api";
import { formatRetry, outcomeView, retryLock, stepResultView, timebox } from "./checkFlow";

const res = (over: Partial<CheckStepResult>): CheckStepResult => ({
  item_id: "q1",
  level: 2,
  type: "write_code",
  correct: true,
  passed: true,
  clean: true,
  gave_up: false,
  ...over,
});

describe("stepResultView (option a: ladder keys on correctness)", () => {
  it("correct and clean is ok", () => {
    expect(stepResultView(res({})).tone).toBe("ok");
  });

  it("correct but unclean warns with the reason, says it continues, and implies no lock", () => {
    const view = stepResultView(res({ clean: false, reason: "hint_limit" }));
    const text = [view.title, ...view.detail].join(" ");
    expect(view.tone).toBe("warn");
    expect(text).toContain("chưa đạt “sạch”");
    expect(text).toContain("không tính Test out");
    expect(text).toContain("gợi ý");
    expect(text).toContain("không bị khoá");
    expect(text).not.toMatch(/24 giờ/);
  });

  it("maps every reason", () => {
    for (const reason of ["solution_viewed", "over_time"]) {
      expect(stepResultView(res({ clean: false, reason })).detail.join(" ")).toContain("Lý do");
    }
  });

  it("wrong answer drops to the level-1 diagnostic and shows the verdict", () => {
    const view = stepResultView(
      res({ correct: false, passed: false, clean: false, verdict: "WA", tests_passed: 3, tests_total: 6 }),
    );
    expect(view.tone).toBe("bad");
    expect(view.detail.join(" ")).toContain("3/6");
    expect(view.detail.join(" ")).toContain("chẩn đoán mức 1");
  });

  it("gave_up is neutral and not a lock", () => {
    const view = stepResultView(res({ gave_up: true, correct: false, passed: false, clean: false }));
    expect(view.tone).toBe("neutral");
    expect(view.detail.join(" ")).toContain("không bị khoá");
  });
});

describe("outcomeView", () => {
  const base = {
    level1: null,
    level2: "passed" as const,
    level3: null,
    tested_out: false,
    score: 1,
    need_lesson: false,
    retry_after: null,
    newly_unlocked: [],
  };

  it("tested_out shows score before -> after and unlocked items", () => {
    const view = outcomeView(
      { ...base, tested_out: true, score: 2, newly_unlocked: ["py.next"] },
      { before: 0, after: 2, tested_out: true, newly_unlocked: ["py.next"] },
    );
    expect(view.tone).toBe("ok");
    expect(view.title).toBe("Test out thành công");
    expect(view.lines[0]).toBe("Điểm: 0 → 2");
    expect(view.unlocked).toEqual(["py.next"]);
    expect(view.retryAfter).toBeNull();
  });

  it("correct-but-unclean finish: warning, no lock", () => {
    const view = outcomeView(base);
    expect(view.tone).toBe("warn");
    expect(view.retryAfter).toBeNull();
    expect(view.lines.join(" ")).toContain("Không bị khoá");
  });

  it("real fail carries the retry time", () => {
    const view = outcomeView({ ...base, level2: "failed", level1: "failed", retry_after: "2026-10-26T10:00:00Z" });
    expect(view.tone).toBe("bad");
    expect(view.retryAfter).toBe("2026-10-26T10:00:00Z");
  });

  it("level 3 failed after level 2 passed: distinct title, keeps the retry lock", () => {
    const view = outcomeView({ ...base, level3: "failed", retry_after: "2026-10-26T10:00:00Z" });
    expect(view.title).toBe("Chưa đạt mức 3; điểm mức 2 được giữ");
    expect(view.title).not.toContain("sạch");
    expect(view.retryAfter).toBe("2026-10-26T10:00:00Z");
    expect(view.lines.join(" ")).toContain("mức 2 vẫn được giữ");
  });

  it("gave up: no lock", () => {
    const view = outcomeView({ ...base, level2: "gave_up" });
    expect(view.retryAfter).toBeNull();
    expect(view.lines.join(" ")).toContain("không bị khoá");
  });

  it("need_lesson", () => {
    expect(outcomeView({ ...base, level2: "failed", need_lesson: true }).title).toContain("học lại");
  });
});

describe("timebox", () => {
  it("counts down, then flags past target and over time (soft, 1.5x)", () => {
    expect(timebox(0, 6)).toMatchObject({ phase: "within", label: "còn 06:00", overAtMs: 540_000 });
    expect(timebox(6 * 60_000, 6).phase).toBe("past_target");
    expect(timebox(9 * 60_000, 6).phase).toBe("over");
  });
});

describe("retry helpers", () => {
  it("retryLock reads extra fields of check_retry_locked", () => {
    const err = new ApiError(409, "check_retry_locked", "x", { retry_after: "2026-10-26T00:00:00Z", level: 2 });
    expect(retryLock(err)).toEqual({ retryAfter: "2026-10-26T00:00:00Z", level: 2 });
    expect(retryLock(new ApiError(409, "check_already_passed", "x"))).toBeNull();
    expect(retryLock(new Error("x"))).toBeNull();
  });

  it("formatRetry shows the remaining time", () => {
    const now = new Date("2026-10-25T00:00:00Z");
    expect(formatRetry("2026-10-25T14:30:00Z", now)).toContain("còn 14 giờ 30 phút");
  });
});

describe("normalizeCheckAnswer", () => {
  it("accepts newly_unlocked as ids or objects and never invents a reference", () => {
    const out = normalizeCheckAnswer({
      session_id: 1,
      finished: true,
      result: { item_id: "q", level: 2, type: "write_code", passed: false, correct: false, reference: "SECRET" },
      next: null,
      score: { before: 0, after: 0, tested_out: false, newly_unlocked: [{ id: "a" }, "b"] },
      outcome: { level2: "failed", retry_after: "2026-10-26T00:00:00Z", newly_unlocked: [] },
    });
    expect(out.score.newly_unlocked).toEqual(["a", "b"]);
    expect(JSON.stringify(out)).not.toContain("SECRET");
  });
});
