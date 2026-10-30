import { createElement, type ReactElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { MemoryRouter } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { ApiError, startPlacement } from "../lib/api";
import ReassessButton, { ReassessModal, runReassess } from "./ReassessButton";

vi.mock("../lib/api", async (importOriginal) => ({
  ...(await importOriginal<typeof import("../lib/api")>()),
  startPlacement: vi.fn(),
  newIdempotencyKey: () => "key-1",
}));

const html = (node: ReactElement) => renderToStaticMarkup(createElement(MemoryRouter, null, node));
const noop = () => {};

describe("ReassessButton", () => {
  beforeEach(() => vi.mocked(startPlacement).mockReset());

  it("renders a subtle open button and no modal until clicked", () => {
    const out = html(createElement(ReassessButton, { experience: "some" }));
    expect(out).toContain('data-testid="reassess-open"');
    expect(out).toContain("Đánh giá lại năng lực");
    expect(out).not.toContain("dialog");
  });

  it("modal preselects the given experience and offers a primary start button", () => {
    const out = html(
      createElement(ReassessModal, { value: "solid", busy: false, onChange: noop, onStart: noop, onClose: noop }),
    );
    expect(out).toContain('role="dialog"');
    expect(out).toContain('name="reassess-experience"');
    expect(out.match(/<input[^>]*checked=""[^>]*>/g)).toHaveLength(1);
    expect(out).toMatch(/<input[^>]*checked=""[^>]*value="solid"/);
    expect(out).toContain("Làm lại không xoá tiến độ");
    expect(out).toMatch(/class="btn primary"[^>]*data-testid="reassess-start"/);
    expect(out).not.toContain("danger");
  });

  it("starts a placement with the chosen level and navigates to it", async () => {
    vi.mocked(startPlacement).mockResolvedValue({ placement_id: 42 } as Awaited<ReturnType<typeof startPlacement>>);
    const navigate = vi.fn();
    const notify = vi.fn();
    await expect(runReassess("none", { navigate, notify })).resolves.toBe(true);
    expect(startPlacement).toHaveBeenCalledWith({ experience: "none", restart: true }, "key-1");
    expect(navigate).toHaveBeenCalledWith("/placement/42");
    expect(notify).not.toHaveBeenCalled();
  });

  it("toasts an error and does not navigate when starting fails", async () => {
    vi.mocked(startPlacement).mockRejectedValueOnce(new Error("boom"));
    const navigate = vi.fn();
    const notify = vi.fn();
    await expect(runReassess("some", { navigate, notify })).resolves.toBe(false);
    expect(notify).toHaveBeenCalledWith("boom", { kind: "error" });
    expect(navigate).not.toHaveBeenCalled();
  });

  it("uses the server-not-running text for network errors", async () => {
    const err = Object.create(ApiError.prototype, { isNetwork: { value: true } });
    vi.mocked(startPlacement).mockRejectedValueOnce(err);
    const notify = vi.fn();
    await runReassess("some", { navigate: vi.fn(), notify });
    expect(notify).toHaveBeenCalledWith("Server chưa chạy nên chưa thực hiện được.", { kind: "error" });
  });
});
