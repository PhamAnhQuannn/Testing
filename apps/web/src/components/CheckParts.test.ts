import { createElement, type ReactElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import type { CheckOutcome, CheckStep, CheckStepResult } from "../lib/api";
import { ConceptStep, LockedCard, OutcomeCard, ReadCodeStep, ResultBanner, Stepper } from "./CheckParts";

const html = (node: ReactElement) => renderToStaticMarkup(createElement(MemoryRouter, null, node));

const step = (over: Partial<CheckStep>): CheckStep => ({
  index: 0,
  count: 3,
  item_id: "q1",
  level: 2,
  type: "read_code",
  minutes: 5,
  time_limit_ms: 300000,
  prompt_md: "Dự đoán output",
  ...over,
});
const result = (over: Partial<CheckStepResult>): CheckStepResult => ({
  item_id: "q1",
  level: 2,
  type: "write_code",
  correct: true,
  passed: true,
  clean: true,
  gave_up: false,
  ...over,
});
const outcome = (over: Partial<CheckOutcome>): CheckOutcome => ({
  level1: null,
  level2: "passed",
  level3: null,
  tested_out: false,
  score: 1,
  need_lesson: false,
  retry_after: null,
  newly_unlocked: [],
  ...over,
});

describe("check step rendering", () => {
  it("read_code shows the code read-only plus an answer box", () => {
    const out = html(createElement(ReadCodeStep, { step: step({ code: "print(1+1)" }), busy: false, onAnswer: () => {} }));
    expect(out).toContain("print(1+1)");
    expect(out).toContain("<textarea");
    expect(out).toContain("Nộp đáp án");
  });

  it("concept hides answer_md until revealed", () => {
    const out = html(
      createElement(ConceptStep, {
        step: step({ type: "concept", answer_md: "ANSWER-TEXT" }),
        busy: false,
        onGrade: () => {},
      }),
    );
    expect(out).toContain("Dự đoán output");
    expect(out).toContain("Hiện đáp án");
    expect(out).not.toContain("ANSWER-TEXT");
  });

  it("stepper lists finished steps and the current one", () => {
    const out = html(createElement(Stepper, { step: step({ level: 3 }), results: [result({ clean: false })] }));
    expect(out).toContain("Mức 2 · đúng");
    expect(out).toContain('aria-current="step"');
    expect(out).toContain("Mức 3");
  });
});

describe("check results rendering", () => {
  it("correct-but-unclean banner shows the reason and no lock", () => {
    const out = html(createElement(ResultBanner, { result: result({ clean: false, reason: "over_time" }) }));
    expect(out).toContain("chưa đạt “sạch”");
    expect(out).toContain("1,5 lần");
    expect(out).not.toContain("24 giờ");
    expect(out).not.toContain("Làm lại");
  });

  it("wrong answer shows the diagnostic and the 24h retry lock; no reference leaked", () => {
    const wrong = result({ correct: false, passed: false, clean: false, verdict: "WA" });
    const out = html(
      createElement(OutcomeCard, {
        subtopicId: "py.x",
        last: { ...wrong, reference: "def secret_solution(): pass" } as CheckStepResult,
        outcome: outcome({ level2: "failed", level1: "failed", retry_after: "2026-10-26T10:00:00Z" }),
      }),
    );
    expect(out).toContain("chẩn đoán mức 1");
    expect(out).toContain("Làm lại sau");
    expect(out).toContain("khoá 24 giờ");
    expect(out).not.toContain("secret_solution");
  });

  it("a FAILED write_code result carrying reference/expected_output never renders them", () => {
    const leaky = {
      ...result({ correct: false, passed: false, clean: false, verdict: "WA", tests_passed: 1, tests_total: 4 }),
      reference: "def secret_solution(): pass",
      expected_output: "EXPECTED-LEAK-42",
    } as CheckStepResult;
    const banner = html(createElement(ResultBanner, { result: leaky }));
    // The view does render the real result (so this is not vacuous) ...
    expect(banner).toContain("WA");
    expect(banner).toContain("1/4 test");
    // ... but nothing from the extra fields.
    for (const text of [banner, html(createElement(Stepper, { step: step({ level: 3 }), results: [leaky] }))]) {
      expect(text).not.toContain("secret_solution");
      expect(text).not.toContain("EXPECTED-LEAK-42");
    }
  });

  it("gave_up outcome shows no lock", () => {
    const out = html(
      createElement(OutcomeCard, {
        subtopicId: "py.x",
        last: result({ gave_up: true, correct: false, passed: false, clean: false }),
        outcome: outcome({ level2: "gave_up" }),
      }),
    );
    expect(out).not.toContain("Làm lại sau");
    expect(out).toContain("không bị khoá");
  });

  it("tested_out outcome shows score change and unlocked subtopics", () => {
    const out = html(
      createElement(OutcomeCard, {
        subtopicId: "py.x",
        outcome: outcome({ tested_out: true, score: 2, newly_unlocked: ["py.next"] }),
        score: { before: 0, after: 2, tested_out: true, newly_unlocked: ["py.next"] },
      }),
    );
    expect(out).toContain("Test out thành công");
    expect(out).toContain("Điểm: 0 → 2");
    expect(out).toContain('href="/s/py.next"');
  });

  it("locked start shows the retry time and a way back", () => {
    const out = html(createElement(LockedCard, { subtopicId: "py.x", retryAfter: "2026-10-26T10:00:00Z", level: 2 }));
    expect(out).toContain("Làm lại được sau");
    expect(out).toContain('href="/s/py.x"');
  });
});
