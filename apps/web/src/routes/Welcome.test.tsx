import { createElement, type ReactElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { putProfile } from "../lib/api";
import { needsWelcome, profilePayload, showResumeStrip, type ProfileDraft } from "../lib/onboarding";
import { IntroStep, ProfileStep, StartStep } from "./Welcome";

const html = (node: ReactElement) => renderToStaticMarkup(createElement(MemoryRouter, null, node));
const noop = () => {};
const draft: ProfileDraft = {
  target_role: "intern",
  track: "swe",
  language: "python",
  experience: "some",
  display_name: " Quan ",
  tz: "Asia/Ho_Chi_Minh",
};

describe("S1 screens", () => {
  it("profile step has the 4 questions", () => {
    const out = html(
      createElement(ProfileStep, { draft, onChange: noop, onBack: noop, onSubmit: noop, busy: false, error: null }),
    );
    for (const name of ["target_role", "track", "language", "experience"]) expect(out).toContain(`name="${name}"`);
    for (const v of ["intern", "fresher", "junior", "senior"]) expect(out).toContain(`value="${v}"`);
    expect(out).not.toContain("New-grad");
    expect(out).toMatch(/name="target_role" checked="" value="intern"/); // default level
    expect(out).toContain("AI engineer");
    expect(out).toContain("Khá (đã giải bài LeetCode easy)");
  });

  it("submit is disabled until experience is answered", () => {
    const out = html(
      createElement(ProfileStep, {
        draft: { ...draft, experience: "" },
        onChange: noop,
        onBack: noop,
        onSubmit: noop,
        busy: false,
        error: null,
      }),
    );
    expect(out).toMatch(/type="submit"[^>]*disabled/);
  });

  it("start step: placement enabled, skip kept", () => {
    const out = html(createElement(StartStep, { experience: "none", onSkip: noop, onPlacement: noop, busy: false, error: null }));
    expect(out).toMatch(/<button class="btn"[^>]*>Đánh giá trình độ<\/button>/);
    expect(out).not.toMatch(/<button[^>]*disabled[^>]*>Đánh giá/);
    expect(out).not.toContain("sắp có");
    expect(out).toMatch(/<button class="btn primary">Bắt đầu từ đầu/);
  });

  it("start step: a sitting in progress is offered to resume (or restart)", () => {
    const out = html(
      createElement(StartStep, {
        experience: "some",
        onSkip: noop,
        onPlacement: noop,
        onRestart: noop,
        resume: true,
        busy: false,
        error: null,
      }),
    );
    expect(out).toContain("Tiếp tục đánh giá");
    expect(out).toContain("Làm lại từ đầu");
  });

  it("intro shows the Pyodide state", () => {
    expect(html(createElement(IntroStep, { runner: "loading", onNext: noop }))).toContain("Đang chuẩn bị");
    expect(html(createElement(IntroStep, { runner: "ready", onNext: noop }))).toContain("sẵn sàng");
    expect(html(createElement(IntroStep, { runner: "error", onNext: noop }))).toContain("Không tải được");
  });
});

describe("onboarding logic", () => {
  it("routes only a known not-onboarded user to /welcome", () => {
    expect(needsWelcome(null)).toBe(false);
    expect(needsWelcome({ profile_done: false, placement: "none" })).toBe(true);
    expect(needsWelcome({ profile_done: true, placement: "none" })).toBe(false);
  });

  it("builds the PUT /profile payload", () => {
    expect(profilePayload({ ...draft, experience: "" })).toBeNull();
    expect(profilePayload(draft)).toEqual({
      target_role: "intern",
      track: "swe",
      language: "python",
      experience: "some",
      display_name: "Quan",
      tz: "Asia/Ho_Chi_Minh",
    });
  });

  it("payload carries the chosen level", () => {
    for (const level of ["fresher", "junior", "senior"] as const) {
      expect(profilePayload({ ...draft, target_role: level })?.target_role).toBe(level);
    }
  });

  it("resume strip hides on Home, focus screens and its own target", () => {
    expect(showResumeStrip("/", "/s/a")).toBe(false);
    expect(showResumeStrip("/welcome", "/s/a")).toBe(false);
    expect(showResumeStrip("/check/a", "/s/a")).toBe(false);
    expect(showResumeStrip("/s/a", "/s/a?block=b2")).toBe(false);
    expect(showResumeStrip("/map", "/s/a")).toBe(true);
  });
});

describe("putProfile", () => {
  let fetchMock: ReturnType<typeof vi.fn>;
  beforeEach(() => {
    fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ onboarding: { profile_done: true, placement: "none" } }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );
    vi.stubGlobal("fetch", fetchMock);
  });
  afterEach(() => vi.unstubAllGlobals());

  it("PUTs /api/profile with the body and the given Idempotency-Key", async () => {
    await putProfile({ experience: "none" }, "k-1");
    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit & { headers: Record<string, string> }];
    expect(url).toBe("/api/profile");
    expect(init.method).toBe("PUT");
    expect(init.headers["Idempotency-Key"]).toBe("k-1");
    expect(JSON.parse(init.body as string)).toEqual({ experience: "none" });
  });
});
