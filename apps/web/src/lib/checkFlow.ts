// Pure view logic of the mastery check (UI_SPEC S8, docs/API_M2A.md). No React, no I/O, so it is
// unit-testable. Ruling (option a): the ladder keys on CORRECTNESS; "clean" only decides whether a
// correct answer is evidence for score 2/3 (tested_out). A lock is shown only when the API says so
// (`check_retry_locked`, or `outcome.retry_after` after a real wrong answer).
import { ApiError, type CheckOutcome, type CheckScore, type CheckStepResult } from "./api";

export const LEVEL_TEXT: Record<number, string> = {
  1: "Mức 1 · chẩn đoán",
  2: "Mức 2",
  3: "Mức 3",
};

export type Tone = "ok" | "warn" | "bad" | "neutral";

export interface ResultView {
  tone: Tone;
  title: string;
  detail: string[];
}

const REASON_TEXT: Record<string, string> = {
  hint_limit: "đã dùng quá 1 gợi ý",
  solution_viewed: "đã xem lời giải",
  over_time: "làm quá 1,5 lần thời gian mục tiêu",
};

export function reasonText(reason: string | undefined): string | null {
  if (!reason) return null;
  return REASON_TEXT[reason] ?? reason;
}

export function stepResultView(result: CheckStepResult): ResultView {
  if (result.gave_up) {
    return {
      tone: "neutral",
      title: "Bạn chọn “Không biết”",
      detail: ["Không tính là sai và không bị khoá làm lại."],
    };
  }
  if (result.correct) {
    if (result.clean) {
      return { tone: "ok", title: "Đúng và sạch", detail: ["Kết quả này tính là bằng chứng cho điểm."] };
    }
    const why =
      result.type === "concept"
        ? "câu khái niệm tự chấm nên không dùng làm bằng chứng điểm 2/3"
        : reasonText(result.reason);
    return {
      tone: "warn",
      title: "Đúng, nhưng chưa đạt “sạch” — không tính Test out",
      detail: [
        ...(why ? [`Lý do: ${why}.`] : []),
        "Bạn vẫn đi tiếp, không bị khoá làm lại.",
      ],
    };
  }
  const detail: string[] = [];
  if (result.verdict) {
    const tests =
      result.tests_total !== undefined ? ` · ${result.tests_passed ?? 0}/${result.tests_total} test` : "";
    detail.push(`Kết quả: ${result.verdict}${tests}`);
  }
  detail.push(
    result.level === 1
      ? "Câu chẩn đoán chỉ để biết bạn thiếu gì, không đổi điểm."
      : "Chuyển sang câu chẩn đoán mức 1.",
  );
  return { tone: "bad", title: "Chưa đúng", detail };
}

export interface OutcomeView {
  tone: Tone;
  title: string;
  lines: string[];
  /** Show the 24h lock only for a real fail (API gave retry_after). */
  retryAfter: string | null;
  unlocked: string[];
}

export function outcomeView(outcome: CheckOutcome, score?: CheckScore): OutcomeView {
  const before = score?.before;
  const lines: string[] = [];
  if (before !== undefined) {
    lines.push(`Điểm: ${before} → ${score?.after ?? outcome.score}`);
  } else {
    lines.push(`Điểm: ${outcome.score}`);
  }
  let tone: Tone;
  let title: string;
  if (outcome.tested_out) {
    tone = "ok";
    title = "Test out thành công";
    lines.push("Mục này được mở và tính điểm 2 trở lên.");
  } else if (outcome.need_lesson) {
    tone = "warn";
    title = "Nên học lại bài trước";
    lines.push("Chưa có câu chẩn đoán mức 1 cho mục này; hãy học lesson rồi quay lại.");
  } else if (outcome.level3 === "failed" && outcome.level2 === "passed") {
    tone = "bad";
    title = "Chưa đạt mức 3; điểm mức 2 được giữ";
  } else if (outcome.level2 === "passed" || outcome.level3 === "passed") {
    tone = "warn";
    title = "Đúng nhưng chưa đạt “sạch” — chưa tính Test out";
    lines.push("Bạn đã trả lời đúng nhưng chưa đủ điều kiện sạch (không xem lời giải, tối đa 1 gợi ý, đúng giờ).");
    if (!outcome.retry_after) lines.push("Không bị khoá: bạn có thể làm lại bất cứ lúc nào.");
  } else if (outcome.retry_after) {
    tone = "bad";
    title = "Chưa đạt";
  } else {
    tone = "neutral";
    title = "Chưa đạt";
    lines.push("Bạn đã chọn “Không biết”, không bị khoá làm lại.");
  }
  if (outcome.level3 === "failed" && outcome.level2 === "passed") {
    lines.push("Mức 3 chưa đúng; mức 2 vẫn được giữ.");
  }
  return {
    tone,
    title,
    lines,
    retryAfter: outcome.retry_after,
    unlocked: outcome.newly_unlocked.length ? outcome.newly_unlocked : (score?.newly_unlocked ?? []),
  };
}

export interface Timebox {
  phase: "within" | "past_target" | "over";
  /** What the clock shows: remaining time, then overtime. */
  label: string;
  /** Hard threshold after which the answer can no longer be "clean" (1.5 x target). */
  overAtMs: number;
}

const clock = (ms: number): string => {
  const total = Math.max(0, Math.floor(ms / 1000));
  return `${String(Math.floor(total / 60)).padStart(2, "0")}:${String(total % 60).padStart(2, "0")}`;
};

/** Soft time-box (informational): countdown from the item's minutes, then "quá giờ" at 1.5x. Never submits. */
export function timebox(elapsedMs: number, minutes: number): Timebox {
  const target = minutes * 60_000;
  const overAt = Math.round(target * 1.5);
  if (elapsedMs < target) return { phase: "within", label: `còn ${clock(target - elapsedMs)}`, overAtMs: overAt };
  if (elapsedMs < overAt) {
    return { phase: "past_target", label: `quá mục tiêu · quá giờ lúc ${clock(overAt)}`, overAtMs: overAt };
  }
  return { phase: "over", label: `quá giờ ${clock(elapsedMs - overAt)} (không còn tính sạch)`, overAtMs: overAt };
}

export function formatRetry(iso: string, now: Date = new Date()): string {
  const at = new Date(iso);
  if (Number.isNaN(at.getTime())) return iso;
  const when = at.toLocaleString("vi-VN", { hour: "2-digit", minute: "2-digit", day: "2-digit", month: "2-digit" });
  const mins = Math.ceil((at.getTime() - now.getTime()) / 60_000);
  if (mins <= 0) return when;
  const h = Math.floor(mins / 60);
  return `${when} (còn ${h > 0 ? `${h} giờ ` : ""}${mins % 60} phút)`;
}

/** Retry lock from `POST /checks/{id}/start`; null when the error is something else. */
export function retryLock(error: unknown): { retryAfter: string; level?: number } | null {
  if (!(error instanceof ApiError) || error.code !== "check_retry_locked") return null;
  const retryAfter = error.extra.retry_after;
  if (typeof retryAfter !== "string") return null;
  const level = error.extra.level;
  return { retryAfter, level: typeof level === "number" ? level : undefined };
}
