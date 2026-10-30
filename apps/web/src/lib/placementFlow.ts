// Pure view logic of the placement (UI_SPEC S2/S3, docs/API_M2A.md "Placement"). No React, no I/O.
// Tone is neutral on purpose: no streaks, no penalties, no pass/fail drama.
import type { PlacementGate, PlacementSkillNode, PlacementView } from "./api";

const clock = (ms: number): string => {
  const total = Math.max(0, Math.floor(ms / 1000));
  return `${String(Math.floor(total / 60)).padStart(2, "0")}:${String(total % 60).padStart(2, "0")}`;
};

export interface BudgetView {
  /** within -> soft (>= 45 min: offer to wrap up) -> hard (>= 60 min: finish this item, no new gate). */
  phase: "within" | "soft" | "hard";
  label: string;
  /** 0..100, share of the hard budget used. */
  pct: number;
}

export function budgetView(activeMs: number, softMs: number, hardMs: number): BudgetView {
  const phase = activeMs >= hardMs ? "hard" : activeMs >= softMs ? "soft" : "within";
  return {
    phase,
    label: `Đã dùng ${clock(activeMs)} / ${clock(softMs)}`,
    pct: hardMs > 0 ? Math.min(100, Math.round((activeMs / hardMs) * 100)) : 0,
  };
}

export const GATE_TEXT: Record<string, string> = {
  passed: "đã đo",
  passed_unclean: "đúng (chưa tính điểm)",
  known: "đã biết",
  failed: "chưa vững",
  gave_up: "bỏ qua",
  locked: "tạm khoá",
  knowledge_gap: "hổng kiến thức",
  known_basic: "biết kiến thức cơ bản",
};

/** Rung of a gate: 0 knowledge (mcq), 1 read code, 2 write code. */
export const RUNG_TEXT: Record<number, string> = { 0: "Kiến thức", 1: "Đọc code", 2: "Viết code" };

/** Short Vietnamese description of a gate outcome (result screen); "" when there is nothing to add. */
export const OUTCOME_NOTE: Record<string, string> = {
  knowledge_gap: "Chưa nắm kiến thức nền của mục này; nên học lại bài trước khi viết code.",
  known_basic: "Nắm kiến thức cơ bản nhưng chưa chứng minh được bằng code.",
};

/** Rung label of a concept gate: C1 (rung 0) knowledge, C2 (rung 2) application. */
export const CONCEPT_RUNG_TEXT: Record<number, string> = { 0: "Kiến thức", 2: "Vận dụng" };

/** Outcome label for a probed concept module (result screen); text, never colour alone. */
export const CONCEPT_OUTCOME_TEXT: Record<string, string> = {
  passed: "đã nắm",
  known: "đã nắm",
  known_basic: "nắm kiến thức cơ bản",
  knowledge_gap: "cần học thêm",
  failed: "cần học thêm",
  gave_up: "bỏ qua",
};

export const CONCEPT_STOP_TEXT: Record<string, string> = {
  concept_done: "Đã đo xong các module khái niệm bạn chọn.",
  concept_skipped: "Bạn đã bỏ qua phần đo module khái niệm.",
};

/** Header line for the open item: concept gates show module name + Kiến thức/Vận dụng. */
export function currentLabel(cur: PlacementView["current"], fallbackLevel: string): string {
  if (!cur) return "";
  if (cur.kind === "concept") {
    const r = cur.rung != null ? CONCEPT_RUNG_TEXT[cur.rung] : undefined;
    return `${cur.name_vi} · ${r ?? fallbackLevel}`;
  }
  return `${cur.name_vi} · ${cur.rung != null && RUNG_TEXT[cur.rung] ? RUNG_TEXT[cur.rung] : fallbackLevel}`;
}

/** Chips for the gates that were decided plus the open one (gates never reached are not shown). */
export function gateChips(view: PlacementView): { gate: PlacementGate; current: boolean }[] {
  const open = view.current?.gate;
  return view.gates
    .filter((g) => g.outcome !== "unavailable" && (g.outcome !== null || g.code === open))
    .map((gate) => ({ gate, current: gate.code === open }));
}

export function gateProgressText(view: PlacementView): string {
  const total = Math.max(view.progress.gates_total, 1);
  const n = Math.min(view.progress.gates_done + 1, total);
  return `Cổng ${n}/${total}`;
}

/** Group the skill map by module (`py.core.strings` -> `py.core`), keeping plan order. */
export function groupByModule(nodes: PlacementSkillNode[]): { module: string; nodes: PlacementSkillNode[] }[] {
  const out: { module: string; nodes: PlacementSkillNode[] }[] = [];
  for (const node of nodes) {
    const module = node.subtopic_id.split(".").slice(0, -1).join(".") || node.subtopic_id;
    const last = out[out.length - 1];
    if (last && last.module === module) last.nodes.push(node);
    else out.push({ module, nodes: [node] });
  }
  return out;
}

export interface ChipView {
  text: string;
  /** measured | seeded | hint | none: a dashed chip is an inference, not a score. */
  kind: "seeded" | "measured" | "inferred" | "none";
}

/** Chip = the score that was seeded/measured; dashed `?` for an inference or nothing (no score). */
export function skillChip(node: PlacementSkillNode): ChipView {
  if (node.seeded) return { text: `${node.name_vi} ${node.score}`, kind: "seeded" };
  if (node.state === "measured") return { text: `${node.name_vi} ${node.score}`, kind: "measured" };
  if (node.state === "likely_known") return { text: `${node.name_vi} ? (có thể đã biết)`, kind: "inferred" };
  if (node.state === "likely_gap") return { text: `${node.name_vi} ? (cần học)`, kind: "inferred" };
  return { text: `${node.name_vi} ?`, kind: "none" };
}

export function minutesText(activeMs: number): string {
  return `${Math.max(1, Math.round(activeMs / 60_000))} phút`;
}
