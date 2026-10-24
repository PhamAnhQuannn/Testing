// Resume position (UI_SPEC 4.2): PUT /resume 3 s after the last change, IndexedDB copy at once,
// flushed on pagehide.
import { nowIso, type ResumeState } from "./api";
import type { KeyValueStore } from "./idb";

export class ResumeReporter {
  private pending: ResumeState | null = null;
  private timer: ReturnType<typeof setTimeout> | null = null;

  constructor(
    private readonly send: (state: ResumeState, options: { keepalive: boolean }) => Promise<unknown>,
    private readonly local: KeyValueStore<ResumeState>,
    private readonly delayMs = 3000,
  ) {}

  report(state: Omit<ResumeState, "updated_at">): void {
    this.pending = { ...state, updated_at: nowIso() };
    void this.local.put("current", this.pending).catch(() => undefined);
    if (this.timer) clearTimeout(this.timer);
    this.timer = setTimeout(() => void this.flush(false), this.delayMs);
  }

  async flush(keepalive = false): Promise<void> {
    if (this.timer) clearTimeout(this.timer);
    this.timer = null;
    const state = this.pending;
    if (!state) return;
    this.pending = null;
    try {
      await this.send(state, { keepalive });
    } catch {
      this.pending = state; // retry on the next report/flush
    }
  }
}
