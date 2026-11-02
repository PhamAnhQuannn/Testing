import { describe, expect, it } from "vitest";
import type { LessonBlock } from "../lib/api";
import { deriveSections, sectionIndexOfBlock } from "./sections";

const text = (id: string): LessonBlock => ({ id, type: "text", md: id });
const ex = (id: string): LessonBlock => ({ id, type: "code_exercise", md: "", entry: "f", starter: "", tests: [] });
const quiz = (id: string): LessonBlock => ({ id, type: "quiz_mcq", prompt_md: "", options: [] });
const sec = (id: string, extra: object = {}): LessonBlock =>
  ({ id, type: "section", title_vi: `T-${id}`, ...extra }) as LessonBlock;

describe("deriveSections", () => {
  it("flat lesson -> one untitled section with all blocks", () => {
    const s = deriveSections([text("a"), ex("e1"), text("b")]);
    expect(s).toHaveLength(1);
    expect(s[0].id).toBe("a");
    expect(s[0].title).toBe("");
    expect(s[0].blocks.map((b) => b.id)).toEqual(["a", "e1", "b"]);
    expect(s[0].kind).toBe("code");
    expect(s[0].exercise?.id).toBe("e1");
  });

  it("empty lesson -> one empty theory section", () => {
    const s = deriveSections([]);
    expect(s).toHaveLength(1);
    expect(s[0].kind).toBe("theory");
  });

  it("dividers split; intro kept only when non-empty", () => {
    const s = deriveSections([text("i"), sec("s1"), text("a"), quiz("q"), sec("s2"), text("b"), ex("e")]);
    expect(s.map((x) => x.id)).toEqual(["i", "s1", "s2"]);
    expect(s.map((x) => x.kind)).toEqual(["theory", "quiz", "code"]);
    expect(s[1].title).toBe("T-s1");
    expect(deriveSections([sec("s1"), text("a")]).map((x) => x.id)).toEqual(["s1"]);
  });

  it("exercise_ref picks the named exercise, else first; bad ref falls back", () => {
    expect(deriveSections([sec("s", { exercise_ref: "e2" }), ex("e1"), ex("e2")])[0].exercise?.id).toBe("e2");
    expect(deriveSections([sec("s", { exercise_ref: "nope" }), ex("e1")])[0].exercise?.id).toBe("e1");
    expect(deriveSections([sec("s"), ex("e1"), ex("e2")])[0].exercise?.id).toBe("e1");
  });

  it("exercise_ref stays inside its section; summary carried; ungraded quiz is theory", () => {
    const s = deriveSections([sec("a", { summary_vi: "sum", exercise_ref: "e2" }), text("x"), sec("b"), ex("e2")]);
    expect(s[0].exercise).toBeUndefined();
    expect(s[0].summary).toBe("sum");
    const ungraded = { ...quiz("q"), graded: false } as LessonBlock;
    expect(deriveSections([sec("a"), ungraded])[0].kind).toBe("theory");
  });

  it("sectionIndexOfBlock", () => {
    const s = deriveSections([text("i"), sec("s1"), text("a"), sec("s2"), text("b")]);
    expect(sectionIndexOfBlock(s, "a")).toBe(1);
    expect(sectionIndexOfBlock(s, "s2")).toBe(2);
    expect(sectionIndexOfBlock(s, "i")).toBe(0);
    expect(sectionIndexOfBlock(s, "zzz")).toBe(-1);
  });
});
