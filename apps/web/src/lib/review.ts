// Pure view logic for the review screen (UI_SPEC S9, SPEC 5.4). Soft by design: no streaks, no
// "late"/penalty wording, no cap; the short-session preset is a suggestion over the full queue.
import type { ReviewCard, ReviewItem, ReviewQueue, ReviewResult } from "./api";

export type SessionMode = "short" | "full";

/** Days between boxes after a correct review (SPEC 5.4: D+1,3,7,14,28 then 30). */
export function boxLabel(box: number): string {
  return `hộp ${box}`;
}

/** Boxes 1-2 are quick recall; 3-5 are code (unless the device has no editor / no problem exists). */
export function boxKindText(box: number): string {
  return box <= 2 ? "nhớ nhanh" : "bài code";
}

/** Informational only: how long the card has been waiting. Never "late". */
export function waitingText(overdueDays: number): string {
  if (overdueDays <= 0) return "đến hạn hôm nay";
  return `đã đến hạn từ ${overdueDays} ngày trước`;
}

export function backlogText(totalDue: number): string {
  return `Có ${totalDue} thẻ đang chờ ôn. Không sao cả: ôn bao nhiêu tuỳ bạn, thẻ nào chưa ôn vẫn giữ nguyên ở đó.`;
}

export function dueCountText(total: number): string {
  return total === 0 ? "Không có thẻ đến hạn" : `${total} thẻ đến hạn`;
}

/** The item actually shown for a card; `kind` lets the short-session preset demote code to recall. */
export function itemFor(card: ReviewCard, kind: "recall" | "code" | null = card.item_kind): ReviewItem | null {
  if (kind === "recall") return card.item?.kind === "recall" ? card.item : card.recall_item;
  if (kind === "code") return card.item?.kind === "code" ? card.item : null;
  return null;
}

export interface SessionCard {
  card: ReviewCard;
  item: ReviewItem;
}

/**
 * Cards to step through. "full" = the whole queue in server order. "short" = the first `size` cards of
 * the queue with the server's code demotions applied (the preset hint); the rest stay available through
 * `Ôn tiếp`. Cards with no usable item are left out (they stay due).
 */
export function assembleSession(queue: ReviewQueue, mode: SessionMode): SessionCard[] {
  const hint = queue.short_session;
  const kinds = new Map(hint.cards.map((c) => [c.subtopic_id, c.item_kind]));
  const source =
    mode === "short" && hint.enabled ? queue.cards.filter((c) => kinds.has(c.subtopic_id)) : queue.cards;
  const out: SessionCard[] = [];
  for (const card of source) {
    const kind = mode === "short" && hint.enabled ? (kinds.get(card.subtopic_id) ?? null) : card.item_kind;
    const item = itemFor(card, kind);
    if (item) out.push({ card, item });
  }
  return out;
}

/** Cards still to do in this sitting: not answered and not skipped. */
export function remaining(session: SessionCard[], handled: ReadonlySet<string>): SessionCard[] {
  return session.filter((s) => !handled.has(s.card.subtopic_id));
}

export function presetAvailable(queue: ReviewQueue): boolean {
  return queue.short_session.enabled && (queue.short_session.size ?? 0) > 0 && queue.total_due > 0;
}

export function presetLabel(queue: ReviewQueue): string {
  const hint = queue.short_session;
  return `Phiên ngắn: ${Math.min(hint.size ?? 0, queue.total_due)} thẻ, tối đa ${hint.max_code} thẻ code`;
}

/** True when the preset is a strict subset of the full queue (so "Ôn tiếp" has something to offer). */
export function hasMoreThanPreset(queue: ReviewQueue): boolean {
  return presetAvailable(queue) && queue.total_due > queue.short_session.cards.length;
}

export interface ResultView {
  tone: "ok" | "neutral";
  title: string;
  lines: string[];
}

/** "Đúng -> hộp 4, lần sau +7 ngày" feedback: box move, next due, score change if any. Never punitive. */
export function resultView(result: ReviewResult, today?: string): ResultView {
  const lines = [
    result.success
      ? `Hộp ${result.box_before} → hộp ${result.box_after}`
      : `Hộp ${result.box_before} → hộp ${result.box_after}: thẻ này sẽ quay lại sớm để nhớ chắc hơn`,
    `Lần ôn kế tiếp: ${dueInText(result.due_on, today)}`,
  ];
  if (result.score.after !== result.score.before) {
    lines.push(`Điểm mục: ${result.score.before} → ${result.score.after}`);
  }
  if (result.newly_unlocked.length > 0) lines.push(`Mở khoá: ${result.newly_unlocked.join(", ")}`);
  return {
    tone: result.success ? "ok" : "neutral",
    title: result.success ? "Đúng, nhớ tốt" : "Chưa nhớ, không sao",
    lines,
  };
}

export function dueInText(dueOn: string, today?: string): string {
  if (!today) return dueOn;
  const days = Math.round((Date.parse(dueOn) - Date.parse(today)) / 86_400_000);
  if (!Number.isFinite(days)) return dueOn;
  if (days <= 0) return "hôm nay";
  if (days === 1) return "ngày mai";
  return `${dueOn} (+${days} ngày)`;
}

/** Block id of a lesson recall ref (`<sid>#<block>`); null for `check:` refs. */
export function lessonBlockOf(ref: string): { subtopicId: string; blockId: string } | null {
  if (ref.startsWith("check:")) return null;
  const at = ref.indexOf("#");
  if (at < 0) return null;
  return { subtopicId: ref.slice(0, at), blockId: ref.slice(at + 1) };
}
