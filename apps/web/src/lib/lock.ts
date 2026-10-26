// Unlock / preview helpers (SPEC 5.3, UI_SPEC S5). The server never enforces locks; the UI does.
import { getMap, type LockReason, type MapSubtopic } from "./api";
import { useAsync } from "./hooks";

export const STATUS_LABEL: Record<string, string> = {
  locked: "Khoá",
  unlocked: "Mở",
  in_progress: "Đang học",
  done: "Xong",
  blocked_missing_content: "Chưa có nội dung",
};

export const statusLabel = (status: string): string => STATUS_LABEL[status] ?? "Mới";

/** Locked = not unlocked yet (including blocked by a prerequisite that has no content). */
export const isLocked = (item: Pick<MapSubtopic, "unlocked">): boolean => !item.unlocked;

export function reasonText(r: LockReason): string {
  const name = r.name_vi ?? r.prerequisite;
  if (r.missing_content) return `${name}: chưa có nội dung`;
  return `cần ${name} ≥ ${r.need} (hiện ${r.score ?? 0})`;
}

export function lockSummary(item: MapSubtopic): string {
  return item.lock_reasons.length
    ? item.lock_reasons.map(reasonText).join("; ")
    : (item.lock_reason ?? "chưa mở");
}

/** Reason shown when the editor / Run / Submit are disabled in preview, or undefined when open. */
export function previewReason(item: MapSubtopic | null | undefined): string | undefined {
  if (!item || !isLocked(item)) return undefined;
  return `Đang xem trước: ${lockSummary(item)}. Soạn code và Submit bị tắt cho đến khi mục này mở.`;
}

/** Map entry of one subtopic; null while loading or when the map is unavailable (never blocks). */
export function useSubtopicLock(subtopicId: string): MapSubtopic | null {
  const map = useAsync(getMap, []);
  return map.data?.find((s) => s.id === subtopicId) ?? null;
}
