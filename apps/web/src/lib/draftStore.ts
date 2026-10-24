// Code drafts (UI_SPEC 4.2/4.3, M1): the newest `updated_at` wins between IndexedDB and the
// server. IndexedDB is written 300 ms after the last keystroke, the server 2 s after it (never
// later than 10 s while typing continuously); blur / hidden / pagehide flush both at once.
import type { DraftPayload } from "./api";
import type { KeyValueStore } from "./idb";

export type Draft = DraftPayload;

export interface MergeResult {
  /** The draft to show; null when neither side has one. */
  draft: Draft | null;
  /** Where it came from. */
  source: "local" | "remote" | "none";
  /** Local copy is ahead of the server (or the server has none): push it up. */
  pushRemote: boolean;
  /** Server copy is ahead of IndexedDB: write it down. */
  pushLocal: boolean;
}

const time = (draft: Draft) => {
  const parsed = Date.parse(draft.updated_at);
  return Number.isNaN(parsed) ? 0 : parsed;
};

/** Newest `updated_at` wins. On an exact tie the local copy wins (it has the cursor). */
export function mergeDrafts(local: Draft | null | undefined, remote: Draft | null | undefined): MergeResult {
  if (!local && !remote) return { draft: null, source: "none", pushRemote: false, pushLocal: false };
  if (local && !remote) return { draft: local, source: "local", pushRemote: true, pushLocal: false };
  if (!local && remote) return { draft: remote, source: "remote", pushRemote: false, pushLocal: true };
  const a = local!;
  const b = remote!;
  if (time(b) > time(a)) {
    return { draft: b, source: "remote", pushRemote: false, pushLocal: a.code !== b.code };
  }
  return { draft: a, source: "local", pushRemote: a.code !== b.code, pushLocal: false };
}

export type SaveStatus =
  | { state: "idle" }
  | { state: "saving" }
  | { state: "saved"; at: string }
  | { state: "error"; message: string };

export interface DraftControllerOptions {
  key: string;
  local: KeyValueStore<Draft>;
  /** Omit for local-only drafts (lesson exercises). */
  remote?: (draft: Draft, options: { keepalive: boolean }) => Promise<unknown>;
  localDelayMs?: number;
  remoteDelayMs?: number;
  remoteMaxMs?: number;
  now?: () => Date;
  onStatus?: (status: SaveStatus) => void;
}

export class DraftController {
  private pending: Draft | null = null;
  private localTimer: ReturnType<typeof setTimeout> | null = null;
  private remoteTimer: ReturnType<typeof setTimeout> | null = null;
  private maxTimer: ReturnType<typeof setTimeout> | null = null;
  private remoteDirty = false;
  private readonly o: Required<
    Pick<DraftControllerOptions, "localDelayMs" | "remoteDelayMs" | "remoteMaxMs" | "now">
  > &
    DraftControllerOptions;

  constructor(options: DraftControllerOptions) {
    this.o = {
      localDelayMs: 300,
      remoteDelayMs: 2000,
      remoteMaxMs: 10_000,
      now: () => new Date(),
      ...options,
    };
  }

  /** Load: merge IndexedDB with the server copy and heal whichever side is behind. */
  async load(remote: Draft | null | undefined): Promise<Draft | null> {
    let local: Draft | undefined;
    try {
      local = await this.o.local.get(this.o.key);
    } catch {
      local = undefined;
    }
    const merged = mergeDrafts(local, remote);
    if (merged.draft && merged.pushLocal) await this.safeLocalPut(merged.draft);
    if (merged.draft && merged.pushRemote && this.o.remote) {
      void this.pushRemote(merged.draft, false);
    }
    return merged.draft;
  }

  /** Record a keystroke batch. */
  update(code: string, cursor?: number, elapsed_ms?: number): void {
    this.pending = { code, cursor, elapsed_ms, updated_at: this.o.now().toISOString() };
    this.remoteDirty = true;
    this.o.onStatus?.({ state: "saving" });
    if (this.localTimer) clearTimeout(this.localTimer);
    this.localTimer = setTimeout(() => void this.flushLocal(), this.o.localDelayMs);
    if (this.o.remote) {
      if (this.remoteTimer) clearTimeout(this.remoteTimer);
      this.remoteTimer = setTimeout(() => void this.flushRemote(false), this.o.remoteDelayMs);
      this.maxTimer ??= setTimeout(() => void this.flushRemote(false), this.o.remoteMaxMs);
    }
  }

  /** Immediate flush of both sides (blur, hidden, pagehide, Ctrl+S). */
  flush(keepalive = false): Promise<void> {
    return Promise.all([this.flushLocal(), this.flushRemote(keepalive)]).then(() => undefined);
  }

  dispose(): void {
    void this.flush();
  }

  private async safeLocalPut(draft: Draft) {
    try {
      await this.o.local.put(this.o.key, draft);
    } catch {
      /* IndexedDB blocked: the server copy still exists */
    }
  }

  private async flushLocal(): Promise<void> {
    if (this.localTimer) clearTimeout(this.localTimer);
    this.localTimer = null;
    const draft = this.pending;
    if (!draft) return;
    await this.safeLocalPut(draft);
    if (!this.o.remote) this.o.onStatus?.({ state: "saved", at: draft.updated_at });
  }

  private async flushRemote(keepalive: boolean): Promise<void> {
    if (this.remoteTimer) clearTimeout(this.remoteTimer);
    if (this.maxTimer) clearTimeout(this.maxTimer);
    this.remoteTimer = this.maxTimer = null;
    if (!this.o.remote || !this.pending || !this.remoteDirty) return;
    this.remoteDirty = false;
    await this.pushRemote(this.pending, keepalive);
  }

  private async pushRemote(draft: Draft, keepalive: boolean): Promise<void> {
    if (!this.o.remote) return;
    try {
      await this.o.remote(draft, { keepalive });
      this.o.onStatus?.({ state: "saved", at: draft.updated_at });
    } catch (error) {
      this.remoteDirty = true; // IndexedDB still has it; retried on the next change or flush
      this.o.onStatus?.({ state: "error", message: error instanceof Error ? error.message : "lỗi" });
    }
  }
}
