import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { DraftController, mergeDrafts, type Draft } from "./draftStore";
import { MemoryStore } from "./idb";

const d = (code: string, at: string): Draft => ({ code, updated_at: at });
const T1 = "2026-10-24T10:00:00.000Z";
const T2 = "2026-10-24T10:00:05.000Z";

describe("mergeDrafts (newest updated_at wins)", () => {
  it("nothing on either side", () => {
    expect(mergeDrafts(null, null)).toMatchObject({ draft: null, source: "none" });
  });
  it("only local: use it and push it to the server", () => {
    expect(mergeDrafts(d("a", T1), null)).toMatchObject({ source: "local", pushRemote: true, pushLocal: false });
  });
  it("only remote: use it and heal IndexedDB", () => {
    expect(mergeDrafts(undefined, d("b", T1))).toMatchObject({ source: "remote", pushLocal: true, pushRemote: false });
  });
  it("local newer (server was down): local wins and is pushed", () => {
    const r = mergeDrafts(d("local", T2), d("remote", T1));
    expect(r.draft?.code).toBe("local");
    expect(r.pushRemote).toBe(true);
  });
  it("remote newer: remote wins and overwrites IndexedDB", () => {
    const r = mergeDrafts(d("local", T1), d("remote", T2));
    expect(r.draft?.code).toBe("remote");
    expect(r.pushLocal).toBe(true);
    expect(r.pushRemote).toBe(false);
  });
  it("identical drafts need no sync", () => {
    const r = mergeDrafts(d("same", T1), d("same", T1));
    expect(r).toMatchObject({ pushRemote: false, pushLocal: false });
  });
  it("same timestamp but different code: local wins", () => {
    expect(mergeDrafts(d("l", T1), d("r", T1))).toMatchObject({ source: "local", pushRemote: true });
  });
  it("unparseable timestamps lose against valid ones", () => {
    expect(mergeDrafts(d("bad", "nope"), d("good", T1)).draft?.code).toBe("good");
  });
});

describe("DraftController timing", () => {
  let local: MemoryStore<Draft>;
  let remote: ReturnType<typeof vi.fn>;
  let clock = 0;
  const make = () =>
    new DraftController({
      key: "k",
      local,
      remote: remote as never,
      now: () => new Date(Date.UTC(2026, 9, 24, 10, 0, 0) + clock),
    });

  beforeEach(() => {
    vi.useFakeTimers();
    local = new MemoryStore();
    remote = vi.fn().mockResolvedValue({});
    clock = 0;
  });
  afterEach(() => vi.useRealTimers());

  it("writes IndexedDB after 300 ms and the server after 2 s", async () => {
    const c = make();
    c.update("x = 1");
    await vi.advanceTimersByTimeAsync(299);
    expect(local.data.size).toBe(0);
    await vi.advanceTimersByTimeAsync(2);
    expect(local.data.get("k")?.code).toBe("x = 1");
    expect(remote).not.toHaveBeenCalled();
    await vi.advanceTimersByTimeAsync(1700);
    expect(remote).toHaveBeenCalledTimes(1);
    expect(remote.mock.calls[0][0].code).toBe("x = 1");
  });

  it("accepted:false with a different server draft: re-PUT stamped after the server copy", async () => {
    remote
      .mockResolvedValueOnce({ accepted: false, draft: { code: "old tab", updated_at: "2026-10-24T10:05:00.000Z" } })
      .mockResolvedValue({ accepted: true });
    const c = make();
    c.update("mine");
    await c.flush();
    expect(remote).toHaveBeenCalledTimes(2);
    const retry = remote.mock.calls[1][0] as Draft;
    expect(retry.code).toBe("mine");
    expect(Date.parse(retry.updated_at)).toBe(Date.parse("2026-10-24T10:05:01.000Z"));
    expect(local.data.get("k")).toMatchObject({ code: "mine", updated_at: retry.updated_at });
  });

  it("accepted:false with the same code is not retried", async () => {
    remote.mockResolvedValue({ accepted: false, draft: { code: "same", updated_at: "2099-01-01T00:00:00Z" } });
    const c = make();
    c.update("same");
    await c.flush();
    expect(remote).toHaveBeenCalledTimes(1);
  });

  it("debounces the server but never waits more than 10 s while typing continuously", async () => {
    const c = make();
    for (let i = 0; i < 20; i++) {
      c.update(`v${i}`);
      await vi.advanceTimersByTimeAsync(900); // keystroke gaps under the 2 s debounce
    }
    // 18 s of continuous typing: server got at least one save from the 10 s cap, not 20 saves.
    expect(remote.mock.calls.length).toBeGreaterThanOrEqual(1);
    expect(remote.mock.calls.length).toBeLessThanOrEqual(3);
    expect(remote.mock.calls[0][0].code).toBe("v11");
  });

  it("flush (blur / pagehide) saves both at once, keepalive for pagehide", async () => {
    const c = make();
    c.update("final");
    await c.flush(true);
    expect(local.data.get("k")?.code).toBe("final");
    expect(remote).toHaveBeenCalledWith(expect.objectContaining({ code: "final" }), { keepalive: true });
    await vi.advanceTimersByTimeAsync(20_000);
    expect(remote).toHaveBeenCalledTimes(1); // timers were cleared, nothing sent twice
  });

  it("does not resend an unchanged draft", async () => {
    const c = make();
    c.update("a");
    await c.flush();
    await c.flush();
    expect(remote).toHaveBeenCalledTimes(1);
  });

  it("keeps the draft dirty after a server failure and retries on the next flush", async () => {
    remote.mockRejectedValueOnce(new Error("down"));
    const statuses: string[] = [];
    const c = new DraftController({
      key: "k",
      local,
      remote: remote as never,
      onStatus: (s) => statuses.push(s.state),
    });
    c.update("a");
    await c.flush();
    expect(statuses).toContain("error");
    expect(local.data.get("k")?.code).toBe("a"); // still safe in IndexedDB
    await c.flush();
    expect(remote).toHaveBeenCalledTimes(2);
  });

  it("load heals the side that is behind", async () => {
    await local.put("k", d("old local", T1));
    const c = make();
    const draft = await c.load(d("newer server", T2));
    expect(draft?.code).toBe("newer server");
    expect(local.data.get("k")?.code).toBe("newer server");

    await local.put("k", d("newest local", "2026-10-24T11:00:00.000Z"));
    const again = await make().load(d("newer server", T2));
    expect(again?.code).toBe("newest local");
    expect(remote).toHaveBeenCalledWith(expect.objectContaining({ code: "newest local" }), { keepalive: false });
  });

  it("local-only drafts (lesson exercises) never call a server", async () => {
    const c = new DraftController({ key: "ex", local });
    c.update("code");
    await c.flush();
    expect(local.data.get("ex")?.code).toBe("code");
  });
});
