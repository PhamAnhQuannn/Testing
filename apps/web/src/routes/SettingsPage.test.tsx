import { createElement, type ReactElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { createBackup, listBackups, restoreBackup } from "../lib/api";
import { BackupList, RestoreDialog, SettingsForm, formatSize, restoreAllowed } from "./SettingsPage";

const html = (node: ReactElement) => renderToStaticMarkup(createElement(MemoryRouter, null, node));
const noop = () => {};
const b1 = { name: "app-20261025-080200.db", size: 2516582, created_at: "2026-10-25T08:02:00+00:00" };

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });
let fetchMock: ReturnType<typeof vi.fn>;
beforeEach(() => {
  fetchMock = vi.fn();
  vi.stubGlobal("fetch", fetchMock);
});
afterEach(() => vi.unstubAllGlobals());

describe("S11 backup UI", () => {
  it("lists backups with name, time, size and a restore button each", () => {
    const out = html(createElement(BackupList, { backups: [b1], busy: false, onRestore: noop }));
    expect(out).toContain(b1.name);
    expect(out).toContain("2,4 MB");
    expect(out).toContain("Khôi phục");
  });

  it("empty state explains the first backup", () => {
    expect(html(createElement(BackupList, { backups: [], busy: false, onRestore: noop }))).toContain(
      "Chưa có bản sao lưu",
    );
  });

  it("formatSize", () => {
    expect(formatSize(512)).toBe("512 B");
    expect(formatSize(2048)).toBe("2,0 KB");
  });

  it("restore dialog is explicit and gated by the typed phrase", () => {
    const out = html(
      createElement(RestoreDialog, { backup: b1, typed: "", onTyped: noop, onConfirm: noop, onCancel: noop }),
    );
    expect(out).toContain('role="dialog"');
    expect(out).toContain("thay toàn bộ dữ liệu");
    expect(out).toContain("KHOI PHUC");
    expect(restoreAllowed("")).toBe(false);
    expect(restoreAllowed("khoi")).toBe(false);
    expect(restoreAllowed(" khoi phuc ")).toBe(true);
  });

  it("GET /backups is normalized", async () => {
    fetchMock.mockResolvedValue(json({ backups: [b1] }));
    expect(await listBackups()).toEqual([b1]);
    expect(fetchMock.mock.calls[0][0]).toBe("/api/backups");
  });

  it("Sao lưu ngay posts /backups with an Idempotency-Key", async () => {
    fetchMock.mockResolvedValue(json(b1, 201));
    expect((await createBackup()).name).toBe(b1.name);
    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toBe("/api/backups");
    expect(init.method).toBe("POST");
    expect(init.headers["Idempotency-Key"]).toBeTruthy();
  });

  it("restore posts to /backups/{name}/restore and returns the restored backup", async () => {
    fetchMock.mockResolvedValue(json({ restored: b1, status: "ok" }));
    expect((await restoreBackup(b1.name, "k1")).name).toBe(b1.name);
    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toBe(`/api/backups/${b1.name}/restore`);
    expect(init.method).toBe("POST");
    expect(init.headers["Idempotency-Key"]).toBe("k1");
  });
});

describe("S11 general settings", () => {
  it("shows profile, timezone, theme and review preset controls", () => {
    const out = html(
      createElement(SettingsForm, {
        value: { display_name: "Quan", tz: "Asia/Ho_Chi_Minh", review_preset: "6" },
        theme: "dark",
        busy: false,
        onChange: noop,
        onTheme: noop,
        onSave: noop,
      }),
    );
    expect(out).toContain('value="Quan"');
    expect(out).toContain('value="Asia/Ho_Chi_Minh"');
    expect(out).toContain("Giao diện");
    expect(out).toMatch(/<option value="dark" selected/);
    expect(out).toContain('value="6"');
    expect(out).toContain("Lưu cài đặt");
  });
});
