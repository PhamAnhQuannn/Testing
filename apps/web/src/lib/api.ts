// The single module that talks to the backend (SPEC 6.4). Response shapes are normalized here
// so that reconciling with the real API (docs/API_M1.md) only touches this file.
import type { ProblemIO, TestCase } from "../runner/Runner";

export class ApiError extends Error {
  constructor(
    readonly status: number,
    readonly code: string,
    message: string,
    /** Extra fields of the error body (e.g. `retry_after`, `level` of check_retry_locked). */
    readonly extra: Record<string, unknown> = {},
  ) {
    super(message);
  }
  get isNetwork(): boolean {
    return this.status === 0;
  }
}

export function newIdempotencyKey(): string {
  return crypto.randomUUID();
}

export interface RequestOptions {
  method?: "GET" | "POST" | "PUT" | "DELETE";
  body?: unknown;
  /** Reuse the key when retrying the same event. Generated for every state-changing request. */
  idempotencyKey?: string;
  /** Survive page unload (pagehide flush). */
  keepalive?: boolean;
  signal?: AbortSignal;
  headers?: Record<string, string>;
}

export const API_BASE = "/api";

export async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const method = options.method ?? "GET";
  const headers: Record<string, string> = { Accept: "application/json", ...options.headers };
  if (options.body !== undefined) headers["Content-Type"] = "application/json";
  if (method !== "GET") headers["Idempotency-Key"] = options.idempotencyKey ?? newIdempotencyKey();

  let response: Response;
  try {
    response = await fetch(`${API_BASE}${path}`, {
      method,
      headers,
      body: options.body === undefined ? undefined : JSON.stringify(options.body),
      keepalive: options.keepalive,
      signal: options.signal,
    });
  } catch {
    throw new ApiError(0, "network", "Không kết nối được server");
  }
  if (!response.ok) {
    let code = `http_${response.status}`;
    let message = response.statusText || "Lỗi server";
    let extra: Record<string, unknown> = {};
    try {
      const data = (await response.json()) as { error?: Record<string, unknown> };
      if (data.error) {
        const { code: c, message: m, ...rest } = data.error;
        code = (c as string | undefined) ?? code;
        message = (m as string | undefined) ?? message;
        extra = rest;
      }
    } catch {
      /* body was not JSON */
    }
    throw new ApiError(response.status, code, message, extra);
  }
  if (response.status === 204) return undefined as T;
  return (await response.json()) as T;
}

const enc = encodeURIComponent;
export const nowIso = () => new Date().toISOString();

// ---------------------------------------------------------------- map

export interface MapSubtopic {
  id: string;
  name_vi: string;
  module: string;
  status: string;
  score: number;
  unlocked: boolean;
  due_cards: number;
  lock_reason?: string | null;
  lock_reasons: LockReason[];
  content_status?: string | null;
  target_intern: number;
}

/** One unmet prerequisite of a locked subtopic (`score` is null when the prerequisite has no content). */
export interface LockReason {
  prerequisite: string;
  name_vi?: string | null;
  score: number | null;
  need: number;
  missing_content?: boolean;
}

type Loose = Record<string, unknown>;
const asArray = (data: unknown, keys: string[]): Loose[] => {
  let arr: unknown[] | null = Array.isArray(data) ? data : null;
  if (!arr) {
    for (const key of keys) {
      const value = (data as Loose | null)?.[key];
      if (Array.isArray(value)) {
        arr = value;
        break;
      }
    }
  }
  // Drop non-object entries so a stray null/primitive in the array can't crash a normalizer.
  return (arr ?? []).filter((x): x is Loose => typeof x === "object" && x !== null);
};

/** `lock_reasons: [{prerequisite, name_vi, score, need}]` -> "cần X ≥ 2". Locks are advisory in M1. */
function lockText(raw: Loose): string | null {
  const reasons = raw.lock_reasons as { prerequisite: string; name_vi?: string; need?: number }[] | undefined;
  if (reasons?.length) {
    return reasons.map((r) => `cần ${r.name_vi ?? r.prerequisite} ≥ ${r.need ?? 2}`).join(", ");
  }
  return (raw.lock_reason as string | null | undefined) ?? null;
}

export function normalizeMap(data: unknown): MapSubtopic[] {
  return asArray(data, ["subtopics", "items", "nodes"]).map((raw) => {
    const id = String(raw.id ?? raw.subtopic_id);
    return {
      id,
      name_vi: String(raw.name_vi ?? raw.title_vi ?? raw.name ?? id),
      module: String(raw.module ?? id.split(".").slice(0, 2).join(".")),
      status: String(raw.status ?? "new"),
      score: Number(raw.score ?? 0),
      unlocked: raw.unlocked !== false,
      due_cards: Number(raw.due_cards ?? 0),
      lock_reason: lockText(raw),
      lock_reasons: ((raw.lock_reasons as LockReason[] | undefined) ?? []).map((r) => ({
        ...r,
        need: r.need ?? 2,
        score: r.score ?? null,
      })),
      target_intern: Number(raw.target_intern ?? 0),
      content_status: (raw.content_status as string | null | undefined) ?? null,
    };
  });
}

/** GET /api/map -> subtopics[] (array or {subtopics|items:[...]}) */
export async function getMap(): Promise<MapSubtopic[]> {
  return normalizeMap(await request<unknown>("/map"));
}

// ---------------------------------------------------------------- diagnosis

export interface DiagnosisStrong {
  subtopic_id: string;
  name_vi: string;
  score: number;
}
export interface DiagnosisImprove extends DiagnosisStrong {
  state: "measured" | "likely_gap";
  firm: boolean;
  concepts: string[];
  has_lesson: boolean;
  target: number;
  gap: number;
  stale: boolean;
}
export interface DiagnosisRoleStats {
  gap: number;
  readiness: number;
  role_relevant: number;
  below_target: number;
  unmeasured_relevant: number;
}
export interface DiagnosisModule extends DiagnosisRoleStats {
  module: string;
  name_vi: string;
  level: string;
  mean: number;
  coverage: number;
  tier: string;
  strong: DiagnosisStrong[];
  improve: DiagnosisImprove[];
  not_assessed_count: number;
}
export interface DiagnosisDomain extends DiagnosisRoleStats {
  section: string;
  name_vi: string;
  track: string;
  level: string;
  mean: number;
  coverage: number;
  tier: string;
  modules: DiagnosisModule[];
}
export interface DiagnosisTrack {
  key: string;
  name_vi: string;
  sections: string[];
}
export interface DiagnosisRole {
  track: string;
  level: string;
  key: string;
  label_vi: string;
}
export interface DiagnosisView {
  tracks: DiagnosisTrack[];
  role: DiagnosisRole;
  readiness_pct: number | null;
  coverage_warning: boolean;
  coverage_message: string | null;
  domains: DiagnosisDomain[];
}

const finite = (v: unknown): number => {
  const n = Number(v ?? 0);
  return Number.isFinite(n) ? n : 0;
};

function normalizeStrong(raw: Loose): DiagnosisStrong {
  const id = String(raw.subtopic_id ?? "");
  return { subtopic_id: id, name_vi: String(raw.name_vi ?? id), score: finite(raw.score) };
}

function normalizeRoleStats(raw: Loose): DiagnosisRoleStats {
  return {
    gap: finite(raw.gap),
    readiness: finite(raw.readiness),
    role_relevant: finite(raw.role_relevant),
    below_target: finite(raw.below_target),
    unmeasured_relevant: finite(raw.unmeasured_relevant),
  };
}

export function normalizeDiagnosis(data: unknown): DiagnosisView {
  const root = (data ?? {}) as Loose;
  const role = (root.role ?? {}) as Loose;
  const track = String(role.track ?? "swe");
  const level = String(role.level ?? "intern");
  return {
    role: {
      track,
      level,
      key: String(role.key ?? `${track}-${level}`),
      label_vi: String(role.label_vi ?? ""),
    },
    readiness_pct: root.readiness_pct == null ? null : finite(root.readiness_pct),
    coverage_warning: root.coverage_warning === true,
    coverage_message: typeof root.coverage_message === "string" ? root.coverage_message : null,
    tracks: asArray(root, ["tracks"]).map((t) => ({
      key: String(t.key ?? ""),
      name_vi: String(t.name_vi ?? t.key ?? ""),
      sections: ((t.sections as unknown[] | undefined) ?? []).map(String),
    })),
    domains: asArray(root, ["domains"]).map((d) => ({
      section: String(d.section ?? ""),
      name_vi: String(d.name_vi ?? d.section ?? ""),
      track: String(d.track ?? ""),
      level: String(d.level ?? "Chưa đủ dữ liệu"),
      mean: finite(d.mean),
      coverage: finite(d.coverage),
      tier: String(d.tier ?? "chưa đo"),
      ...normalizeRoleStats(d),
      modules: asArray(d, ["modules"]).map((m) => ({
        module: String(m.module ?? ""),
        name_vi: String(m.name_vi ?? m.module ?? ""),
        level: String(m.level ?? "Chưa đủ dữ liệu"),
        mean: finite(m.mean),
        coverage: finite(m.coverage),
        tier: String(m.tier ?? "chưa đo"),
        ...normalizeRoleStats(m),
        strong: asArray(m, ["strong"]).map(normalizeStrong),
        improve: asArray(m, ["improve"]).map((i) => ({
          ...normalizeStrong(i),
          state: i.state === "likely_gap" ? ("likely_gap" as const) : ("measured" as const),
          firm: i.firm === true,
          concepts: ((i.concepts as unknown[] | undefined) ?? []).map(String),
          has_lesson: i.has_lesson === true,
          target: finite(i.target),
          gap: finite(i.gap),
          stale: i.stale === true,
        })),
        not_assessed_count: finite(m.not_assessed_count),
      })),
    })),
  };
}

/** GET /api/diagnosis -> per-domain / per-module skill profile with honest confidence tiers. */
export async function getDiagnosis(role?: string): Promise<DiagnosisView> {
  const qs = role ? `?role=${encodeURIComponent(role)}` : "";
  return normalizeDiagnosis(await request<unknown>(`/diagnosis${qs}`));
}

// ---------------------------------------------------------------- lesson

export type LessonBlock =
  | { id: string; type: "text"; md: string }
  | { id: string; type: "callout"; kind: "tip" | "warning" | "beginner" | "interview"; md: string }
  | {
      id: string;
      type: "code_sample";
      lang: "python" | "java";
      code: string;
      runnable: boolean;
      expected_output?: string;
    }
  | {
      id: string;
      type: "quiz_mcq";
      graded?: boolean;
      prompt_md: string;
      options: { id: string; text_md: string }[];
      /** Not shipped by the server: answer/explain_md come back from POST /quiz/answers. */
      answer?: string[];
      multi?: boolean;
      explain_md?: string;
    }
  | {
      id: string;
      type: "quiz_fill";
      graded?: boolean;
      prompt_md: string;
      blanks: { index?: number }[];
      explain_md?: string;
    }
  | {
      id: string;
      type: "predict_output";
      graded?: boolean;
      code: string;
      expected_output?: string;
      explain_md?: string;
    }
  | {
      id: string;
      type: "code_exercise";
      md: string;
      entry: string;
      starter: string;
      tests: { args: unknown[]; expected: unknown }[];
      hint_md: string;
      solution?: string;
    }
  | { id: string; type: "problem_ref"; problem_id: string }
  | { id: string; type: "summary"; bullets_vi: string[] };

export interface KnownAnswer {
  correct: boolean;
  answer?: unknown;
}

export interface Lesson {
  id: string;
  title_vi: string;
  est_minutes: number;
  objectives_vi: string[];
  blocks: LessonBlock[];
  problems: { practice: string[]; extra: string[] };
  checkpoint: { pass_ratio: number; min_items: number };
  status?: string;
  run_no: number;
  /** From `progress.answers` (current run): first-attempt correctness and last answer. */
  answers: Record<string, KnownAnswer>;
  completed: boolean;
}

export function normalizeLesson(data: unknown): Lesson {
  const root = ((data as Loose).lesson ?? data) as Loose;
  const progress = (root.progress ?? {}) as Loose;
  const raw = (progress.answers ?? {}) as Record<string, Loose>;
  const answers: Lesson["answers"] = {};
  for (const [id, a] of Object.entries(raw)) {
    answers[id] = { correct: Boolean(a.first_correct ?? a.last_correct), answer: a.last_answer };
  }
  return {
    id: String(root.id),
    title_vi: String(root.title_vi ?? root.id),
    est_minutes: Number(root.est_minutes ?? 0),
    objectives_vi: (root.objectives_vi as string[]) ?? [],
    blocks: (root.blocks as LessonBlock[]) ?? [],
    problems: (root.problems as Lesson["problems"]) ?? { practice: [], extra: [] },
    checkpoint: (root.checkpoint as Lesson["checkpoint"]) ?? { pass_ratio: 0.7, min_items: 3 },
    status: root.status as string | undefined,
    run_no: Number(progress.run_no ?? 1),
    answers,
    completed: Boolean(progress.lesson_done ?? false),
  };
}

/** GET /api/lessons/{subtopic_id} -> lesson YAML as JSON (no quiz answers/explanations, no exercise solution) + progress{run_no, answers, lesson_done} */
export async function getLesson(subtopicId: string): Promise<Lesson> {
  return normalizeLesson(await request<unknown>(`/lessons/${enc(subtopicId)}`));
}

export interface QuizAnswerBody {
  /** `<subtopic_id>#<block_id>` */
  quiz_item_id: string;
  run_no: number;
  answer: unknown;
  occurred_at: string;
}
export interface QuizAnswerResult {
  correct: boolean;
  explain_md?: string;
  correct_answer?: unknown;
  first_attempt?: boolean;
  graded?: boolean;
  quiz_best?: number;
}

/** POST /api/quiz/answers {quiz_item_id, run_no, answer, occurred_at} -> {correct, explain_md, correct_answer, first_attempt, quiz_best}. Grading is server-side. */
export function postQuizAnswer(body: QuizAnswerBody, key?: string): Promise<QuizAnswerResult> {
  return request("/quiz/answers", { method: "POST", body, idempotencyKey: key });
}

export interface LessonCompleteResult {
  quiz_best?: number;
  quiz_passed?: boolean;
  score?: number;
  review_card?: { box: number; due_on: string } | null;
  [key: string]: unknown;
}

/** POST /api/lessons/{id}/complete {occurred_at} -> {lesson_done, quiz_best, quiz_passed, score, review_card} */
export function completeLesson(
  subtopicId: string,
  body: { occurred_at: string },
  key?: string,
): Promise<LessonCompleteResult> {
  return request(`/lessons/${enc(subtopicId)}/complete`, {
    method: "POST",
    body,
    idempotencyKey: key,
  });
}

/** POST /api/lessons/{id}/runs {} -> {run_no} */
export function newLessonRun(subtopicId: string, key?: string): Promise<{ run_no: number }> {
  return request(`/lessons/${enc(subtopicId)}/runs`, {
    method: "POST",
    body: {},
    idempotencyKey: key,
  });
}

// ---------------------------------------------------------------- problems

export interface DraftPayload {
  code: string;
  updated_at: string;
  cursor?: number;
  elapsed_ms?: number;
}

export interface Problem {
  id: string;
  subtopic_id: string;
  title: string;
  title_vi: string;
  difficulty: "easy" | "medium" | "hard";
  statement_en_md: string;
  statement_vi_md: string;
  constraints: string[];
  examples: { input: string; output: string; explain_vi?: string }[];
  io: ProblemIO;
  starter: string;
  limits: { time_ms: number; memory_mb: number; time_multiplier?: number };
  time_target_min?: number;
  sample_tests: TestCase[];
  hints_opened: string[];
  hints_total: number;
  status?: string;
  solved: boolean;
}

export function normalizeProblem(data: unknown): Problem {
  const root = ((data as Loose).problem ?? data) as Loose;
  const starter = root.starter as string | { python?: string } | undefined;
  const limits = (root.limits as Problem["limits"]) ?? { time_ms: 1000, memory_mb: 256 };
  const tests = root.tests as { sample?: TestCase[] } | undefined;
  const opened = (root.hints as string[] | undefined) ?? [];
  const hintsTotal = Number(root.hint_count ?? 3);
  return {
    id: String(root.id),
    subtopic_id: String(root.subtopic_id ?? ""),
    title: String(root.title ?? root.id),
    title_vi: String(root.title_vi ?? root.title ?? root.id),
    difficulty: (root.difficulty as Problem["difficulty"]) ?? "easy",
    statement_en_md: String(root.statement_en_md ?? ""),
    statement_vi_md: String(root.statement_vi_md ?? ""),
    constraints: (root.constraints as string[]) ?? [],
    examples: (root.examples as Problem["examples"]) ?? [],
    io: root.io as ProblemIO,
    starter: typeof starter === "string" ? starter : (starter?.python ?? ""),
    limits: { time_multiplier: 3, ...limits, ...pyodideMultiplier(limits) },
    time_target_min: root.time_target_min as number | undefined,
    sample_tests: ((root.sample_tests ?? root.samples ?? tests?.sample ?? []) as TestCase[]) ?? [],
    hints_opened: opened,
    hints_total: hintsTotal,
    status: root.status as string | undefined,
    solved: root.status === "solved" || Boolean(root.solved),
  };
}

function pyodideMultiplier(limits: unknown): { time_multiplier?: number } {
  const multiplier = (limits as { time_multiplier?: { pyodide?: number } | number }).time_multiplier;
  if (typeof multiplier === "number") return { time_multiplier: multiplier };
  return multiplier?.pyodide ? { time_multiplier: multiplier.pyodide } : {};
}

/** GET /api/problems/{id} -> public problem + sample_tests, hint_count, hints (opened only), status */
export async function getProblem(id: string): Promise<Problem> {
  return normalizeProblem(await request<unknown>(`/problems/${enc(id)}`));
}

/** POST /api/problems/{id}/start-submit {} -> {token}; GET /api/problems/{id}/tests/hidden (X-Submit-Token) -> {tests[]} */
export async function getHiddenTests(id: string): Promise<TestCase[]> {
  const start = await request<{ token?: string }>(`/problems/${enc(id)}/start-submit`, {
    method: "POST",
    body: {},
  });
  const data = await request<unknown>(`/problems/${enc(id)}/tests/hidden`, {
    headers: start.token ? { "X-Submit-Token": start.token } : undefined,
  });
  return asArray(data, ["tests", "items", "hidden"]) as TestCase[];
}

/** POST /api/problems/{id}/hints {} -> {hints_used, hint|null, hints[], exhausted} */
export async function openHint(
  id: string,
  key?: string,
): Promise<{ level: number; hint: string; hints_used?: number }> {
  const data = await request<Loose>(`/problems/${enc(id)}/hints`, {
    method: "POST",
    body: {},
    idempotencyKey: key,
  });
  return {
    level: Number(data.hints_used ?? 1),
    hint: String(data.hint ?? ""),
    hints_used: data.hints_used as number | undefined,
  };
}

export interface Solution {
  code: string;
  approach_vi?: string;
  complexity?: string;
}

/** GET /api/problems/{id}/solution -> {code|solution, approach_vi, complexity} (sets solution_viewed) */
export async function getSolution(id: string): Promise<Solution> {
  const data = await request<Loose>(`/problems/${enc(id)}/solution`);
  const nested = (data.solution ?? {}) as Loose;
  return {
    code: String(data.code ?? (typeof data.solution === "string" ? data.solution : nested.code ?? "")),
    approach_vi: (data.approach_vi ?? nested.approach_vi) as string | undefined,
    complexity: (data.complexity ?? nested.complexity) as string | undefined,
  };
}

export interface AttemptBody {
  problem_id: string;
  mode: "run" | "submit";
  language: "python";
  code: string;
  verdict: string;
  passed: number;
  total: number;
  elapsed_ms: number;
  runtime_ms?: number;
  occurred_at: string;
}
export interface AttemptResult {
  ac?: boolean;
  clean?: boolean;
  score?: { before: number; after: number } | null;
  [key: string]: unknown;
}

/** POST /api/attempts {problem_id, mode, language, code, verdict, passed, total, elapsed_ms, runtime_ms, occurred_at} -> 201 {attempt_id, ac, clean, score{before,after,...}|null} */
export function postAttempt(body: AttemptBody, key?: string): Promise<AttemptResult> {
  return request("/attempts", { method: "POST", body, idempotencyKey: key });
}

interface WireCursor {
  line: number;
  ch: number;
  offset: number;
}

function toWireCursor(code: string, offset = 0): WireCursor {
  const before = code.slice(0, offset).split("\n");
  return { line: before.length - 1, ch: before[before.length - 1].length, offset };
}

/** PUT /api/drafts/{problem_id} {code, language, updated_at, cursor{line,ch,offset}, elapsed_ms} -> {accepted, draft} (newer updated_at wins) */
export function putDraft(
  problemId: string,
  draft: DraftPayload,
  options: { keepalive?: boolean } = {},
): Promise<unknown> {
  return request(`/drafts/${enc(problemId)}`, {
    method: "PUT",
    body: {
      code: draft.code,
      language: "python",
      updated_at: draft.updated_at,
      cursor: toWireCursor(draft.code, draft.cursor),
      elapsed_ms: draft.elapsed_ms,
    },
    keepalive: options.keepalive,
  });
}

/** GET /api/drafts/{problem_id}?language=python -> {draft: {code, updated_at, cursor, elapsed_ms, rev} | null} */
export async function getDraft(problemId: string): Promise<DraftPayload | null> {
  const data = await request<{ draft?: Loose | null }>(`/drafts/${enc(problemId)}?language=python`);
  const d = data.draft;
  if (!d) return null;
  const cursor = d.cursor as Partial<WireCursor> | number | null | undefined;
  return {
    code: String(d.code ?? ""),
    updated_at: String(d.updated_at),
    cursor: typeof cursor === "number" ? cursor : cursor?.offset,
    elapsed_ms: d.elapsed_ms as number | undefined,
  };
}

// ---------------------------------------------------------------- resume

export interface ResumeState {
  mode: "lesson" | "problem" | "check" | "placement" | "review" | "other";
  route: string;
  ref: Record<string, unknown>;
  context?: Record<string, unknown>;
  updated_at: string;
}

/** PUT /api/resume {mode, route, ref, context, updated_at} -> {ok:true} (POST same body for sendBeacon) */
export function putResume(state: ResumeState, options: { keepalive?: boolean } = {}): Promise<unknown> {
  return request("/resume", { method: "PUT", body: state, keepalive: options.keepalive });
}

/** GET /api/resume -> {primary, others[], in_progress}; primary: {mode, route, ref, stale?} | null */
export async function getResume(): Promise<ResumeState | null> {
  const data = await request<{ primary?: ResumeState | null }>("/resume");
  return data.primary ?? null;
}

// ---------------------------------------------------------------- mastery check (docs/API_M2A.md)

export type CheckType = "write_code" | "read_code" | "concept" | "mcq";
export type CheckContext = "mastery" | "test_out";

export interface CheckStep {
  index: number;
  count: number;
  item_id: string;
  level: number;
  type: CheckType;
  minutes: number;
  time_limit_ms: number;
  prompt_md: string;
  /** write_code */
  problem_id?: string;
  /** read_code */
  code?: string;
  /** concept: shown only after the learner asks for it */
  answer_md?: string;
  /** mcq: the options (the server never sends the correct index) */
  choices?: string[];
}

export interface CheckStepResult {
  item_id: string;
  level: number;
  type: CheckType;
  correct: boolean;
  passed: boolean;
  clean: boolean;
  gave_up: boolean;
  /** `hint_limit` | `solution_viewed` | `over_time` when correct but not clean. */
  reason?: string;
  verdict?: string;
  tests_passed?: number;
  tests_total?: number;
}

export interface CheckSession {
  session_id: number;
  subtopic_id: string;
  context: CheckContext;
  attempt_no: number;
  status: string;
  resumed: boolean;
  elapsed_ms: number;
  step: CheckStep;
  results: CheckStepResult[];
}

export interface CheckScore {
  before: number;
  after: number;
  tested_out: boolean;
  newly_unlocked: string[];
}

export type LevelLabel = "passed" | "failed" | "gave_up" | null;

export interface CheckOutcome {
  level1: LevelLabel;
  level2: LevelLabel;
  level3: LevelLabel;
  tested_out: boolean;
  score: number;
  need_lesson: boolean;
  /** ISO time; only set after a real wrong answer (never for correct-but-unclean or "Không biết"). */
  retry_after: string | null;
  newly_unlocked: string[];
}

export interface CheckAnswerResponse {
  session_id: number;
  finished: boolean;
  result: CheckStepResult;
  next: CheckStep | null;
  score: CheckScore;
  outcome: CheckOutcome | null;
}

export type CheckAnswerBody =
  | { code: string; language: "python"; verdict: string; passed_tests: number; total: number; runtime_ms?: number }
  | { answer: string }
  | { self_grade: boolean }
  | { choice: number }
  | { gave_up: true };

const ids = (value: unknown): string[] =>
  Array.isArray(value)
    ? value.map((v) => (typeof v === "string" ? v : String((v as Loose).id ?? (v as Loose).subtopic_id ?? "")))
    : [];

export function normalizeCheckStep(raw: Loose): CheckStep {
  const minutes = Number(raw.minutes ?? 10);
  return {
    index: Number(raw.index ?? 0),
    count: Number(raw.count ?? 1),
    item_id: String(raw.item_id),
    level: Number(raw.level ?? 2),
    type: raw.type as CheckType,
    minutes,
    time_limit_ms: Number(raw.time_limit_ms ?? minutes * 60_000),
    prompt_md: String(raw.prompt_md ?? ""),
    problem_id: raw.problem_id as string | undefined,
    code: raw.code as string | undefined,
    answer_md: raw.answer_md as string | undefined,
    choices: Array.isArray(raw.choices) ? (raw.choices as unknown[]).map(String) : undefined,
  };
}

export function normalizeCheckResult(raw: Loose): CheckStepResult {
  const passed = Boolean(raw.passed);
  return {
    item_id: String(raw.item_id),
    level: Number(raw.level ?? 0),
    type: raw.type as CheckType,
    correct: raw.correct === undefined ? passed : Boolean(raw.correct),
    passed,
    clean: Boolean(raw.clean),
    gave_up: Boolean(raw.gave_up),
    reason: (raw.reason as string | null | undefined) ?? undefined,
    verdict: raw.verdict as string | undefined,
    tests_passed: raw.tests_passed as number | undefined,
    tests_total: raw.tests_total as number | undefined,
  };
}

export function normalizeCheckSession(data: unknown): CheckSession {
  const raw = data as Loose;
  return {
    session_id: Number(raw.session_id),
    subtopic_id: String(raw.subtopic_id),
    context: (raw.context as CheckContext) ?? "mastery",
    attempt_no: Number(raw.attempt_no ?? 1),
    status: String(raw.status ?? "in_progress"),
    resumed: Boolean(raw.resumed),
    elapsed_ms: Number(raw.elapsed_ms ?? 0),
    step: normalizeCheckStep(raw.step as Loose),
    results: ((raw.results as Loose[] | undefined) ?? []).map(normalizeCheckResult),
  };
}

export function normalizeCheckAnswer(data: unknown): CheckAnswerResponse {
  const raw = data as Loose;
  const score = (raw.score ?? {}) as Loose;
  const outcome = raw.outcome as Loose | null | undefined;
  return {
    session_id: Number(raw.session_id),
    finished: Boolean(raw.finished),
    result: normalizeCheckResult(raw.result as Loose),
    next: raw.next ? normalizeCheckStep(raw.next as Loose) : null,
    score: {
      before: Number(score.before ?? 0),
      after: Number(score.after ?? 0),
      tested_out: Boolean(score.tested_out),
      newly_unlocked: ids(score.newly_unlocked),
    },
    outcome: outcome
      ? {
          level1: (outcome.level1 as LevelLabel) ?? null,
          level2: (outcome.level2 as LevelLabel) ?? null,
          level3: (outcome.level3 as LevelLabel) ?? null,
          tested_out: Boolean(outcome.tested_out),
          score: Number(outcome.score ?? 0),
          need_lesson: Boolean(outcome.need_lesson),
          retry_after: (outcome.retry_after as string | null | undefined) ?? null,
          newly_unlocked: ids(outcome.newly_unlocked),
        }
      : null,
  };
}

/** POST /api/checks/{subtopic_id}/start {context} -> session + current step. 409 check_retry_locked carries `extra.retry_after`. */
export async function startCheck(
  subtopicId: string,
  context: CheckContext = "mastery",
  key?: string,
): Promise<CheckSession> {
  return normalizeCheckSession(
    await request<unknown>(`/checks/${enc(subtopicId)}/start`, {
      method: "POST",
      body: { context },
      idempotencyKey: key,
    }),
  );
}

/** POST /api/checks/{subtopic_id}/answer {session_id, item_id, elapsed_ms, ...per type}. Reuse `key` when retrying. */
export async function answerCheck(
  subtopicId: string,
  body: { session_id: number; item_id: string; elapsed_ms: number; session_elapsed_ms?: number } & CheckAnswerBody,
  key?: string,
): Promise<CheckAnswerResponse> {
  return normalizeCheckAnswer(
    await request<unknown>(`/checks/${enc(subtopicId)}/answer`, {
      method: "POST",
      body,
      idempotencyKey: key,
    }),
  );
}

/** POST /api/checks/{session_id}/heartbeat {elapsed_ms (absolute)} -> {session_id, status, elapsed_ms, expires_at} */
export function checkHeartbeat(
  sessionId: number,
  elapsedMs: number,
  options: { keepalive?: boolean } = {},
): Promise<{ session_id: number; status: string; elapsed_ms: number; expires_at?: string }> {
  return request(`/checks/${sessionId}/heartbeat`, {
    method: "POST",
    body: { elapsed_ms: Math.round(elapsedMs) },
    keepalive: options.keepalive,
  });
}

// ---------------------------------------------------------------- review (docs/API_M2A.md "Review")

export type ReviewItemKind = "recall" | "code";

export interface ReviewItem {
  kind: ReviewItemKind;
  /** recall: `<sid>#<block>` or `check:<sid>:<item_id>`; code: a problem id. */
  ref: string;
  type: string | null;
  subtopic_id: string;
}

export interface ReviewCard {
  subtopic_id: string;
  name_vi: string;
  box: number;
  due_on: string;
  overdue_days: number;
  score: number;
  lapses: number;
  item_kind: ReviewItemKind | null;
  item: ReviewItem | null;
  recall_item: ReviewItem | null;
}

export interface ShortSession {
  enabled: boolean;
  size: number | null;
  max_code: number;
  cards: { subtopic_id: string; item_kind: ReviewItemKind | null }[];
}

export interface ReviewQueue {
  today: string;
  total_due: number;
  backlog_warn: number;
  backlog: boolean;
  cards: ReviewCard[];
  short_session: ShortSession;
}

export interface ReviewResultBody {
  success: boolean;
  item_ref?: string;
  item_kind?: ReviewItemKind;
}

export interface ReviewResult {
  subtopic_id: string;
  success: boolean;
  item_ref: string | null;
  item_kind: ReviewItemKind | null;
  box_before: number;
  box_after: number;
  due_on: string;
  lapses: number;
  score: { before: number; after: number };
  newly_unlocked: string[];
}

const reviewItem = (raw: unknown, sid: string): ReviewItem | null => {
  if (!raw || typeof raw !== "object") return null;
  const r = raw as Loose;
  if (typeof r.ref !== "string") return null;
  return {
    kind: r.kind === "code" ? "code" : "recall",
    ref: r.ref,
    type: (r.type as string | null | undefined) ?? null,
    subtopic_id: String(r.subtopic_id ?? sid),
  };
};

const itemKind = (value: unknown): ReviewItemKind | null =>
  value === "code" ? "code" : value === "recall" ? "recall" : null;

export function normalizeReviewQueue(data: unknown): ReviewQueue {
  const raw = (data ?? {}) as Loose;
  const short = (raw.short_session ?? {}) as Loose;
  const cards = ((raw.cards as Loose[] | undefined) ?? []).map((c): ReviewCard => {
    const sid = String(c.subtopic_id);
    return {
      subtopic_id: sid,
      name_vi: String(c.name_vi ?? sid),
      box: Number(c.box ?? 1),
      due_on: String(c.due_on ?? ""),
      overdue_days: Math.max(0, Number(c.overdue_days ?? 0)),
      score: Number(c.score ?? 0),
      lapses: Number(c.lapses ?? 0),
      item_kind: itemKind(c.item_kind),
      item: reviewItem(c.item, sid),
      recall_item: reviewItem(c.recall_item, sid),
    };
  });
  return {
    today: String(raw.today ?? ""),
    total_due: Number(raw.total_due ?? cards.length),
    backlog_warn: Number(raw.backlog_warn ?? 20),
    backlog: Boolean(raw.backlog),
    cards,
    short_session: {
      enabled: Boolean(short.enabled),
      size: short.size === null || short.size === undefined ? null : Number(short.size),
      max_code: Number(short.max_code ?? 2),
      cards: ((short.cards as Loose[] | undefined) ?? []).map((c) => ({
        subtopic_id: String(c.subtopic_id),
        item_kind: itemKind(c.item_kind),
      })),
    },
  };
}

export function normalizeReviewResult(data: unknown): ReviewResult {
  const raw = data as Loose;
  const score = (raw.score ?? {}) as Loose;
  return {
    subtopic_id: String(raw.subtopic_id),
    success: Boolean(raw.success),
    item_ref: (raw.item_ref as string | null | undefined) ?? null,
    item_kind: itemKind(raw.item_kind),
    box_before: Number(raw.box_before ?? 1),
    box_after: Number(raw.box_after ?? 1),
    due_on: String(raw.due_on ?? ""),
    lapses: Number(raw.lapses ?? 0),
    score: { before: Number(score.before ?? 0), after: Number(score.after ?? 0) },
    newly_unlocked: ids(raw.newly_unlocked),
  };
}

/** GET /api/review/queue[?editor=false] -> the whole due list (no cap) + soft backlog flag + short-session hint. */
export async function getReviewQueue(editor = true): Promise<ReviewQueue> {
  return normalizeReviewQueue(await request<unknown>(`/review/queue${editor ? "" : "?editor=false"}`));
}

/** POST /api/review/{subtopic_id}/result. Reuse `key` when retrying the same answer. 409 card_not_due = stale queue. */
export async function postReviewResult(
  subtopicId: string,
  body: ReviewResultBody,
  key?: string,
): Promise<ReviewResult> {
  return normalizeReviewResult(
    await request<unknown>(`/review/${enc(subtopicId)}/result`, {
      method: "POST",
      body,
      idempotencyKey: key,
    }),
  );
}

// ---------------------------------------------------------------- "Học tiếp" (SPEC 5.5) + activity ping

export interface SuggestedProblem {
  id: string;
  title: string;
  title_vi: string | null;
  difficulty: string;
  role: "practice" | "extra";
}

export interface NextItem {
  id: string;
  name_vi: string;
  score: number;
  target_intern: number;
  status: "unlocked" | "in_progress";
  known_basic: boolean;
  lesson_done: boolean;
  has_lesson: boolean;
  /** ISO time the 24 h check retry lock ends (the item is listed after the ones doable now), or null. */
  check_retry_after: string | null;
  due_card: boolean;
  suggested_problem: SuggestedProblem | null;
}

export interface MustRaise {
  prerequisite: { id: string; name_vi: string; score: number; need: number };
  /** The next locked subtopic this prerequisite would open. */
  unlocks: { id: string; name_vi: string };
  sole_blocker: boolean;
  also_blocks: number;
  suggested_problem: SuggestedProblem | null;
  test_out: { available: boolean; retry_after: string | null };
}

export interface LockedPreview {
  id: string;
  name_vi: string;
  lock_reasons: { prerequisite: string; name_vi: string | null; score: number | null; need: number }[];
}

export interface NextData {
  must_raise: MustRaise[];
  up_next: NextItem[];
  locked_preview: LockedPreview[];
  due_count: number;
  backlog: boolean;
  study: { today_s: number; week_s: number };
}

const num = (v: unknown, d = 0) => (typeof v === "number" && Number.isFinite(v) ? v : d);
const strOrNull = (v: unknown) => (typeof v === "string" ? v : null);

function normalizeSuggested(raw: unknown): SuggestedProblem | null {
  if (!raw || typeof raw !== "object") return null;
  const r = raw as Loose;
  if (typeof r.id !== "string") return null;
  return {
    id: r.id,
    title: String(r.title ?? r.id),
    title_vi: strOrNull(r.title_vi),
    difficulty: String(r.difficulty ?? ""),
    role: r.role === "extra" ? "extra" : "practice",
  };
}

export function normalizeNext(data: unknown): NextData {
  const raw = (data ?? {}) as Loose;
  const list = (v: unknown): Loose[] => (Array.isArray(v) ? (v as Loose[]) : []);
  const study = (raw.study ?? {}) as Loose;
  return {
    must_raise: list(raw.must_raise).map((m): MustRaise => {
      const p = (m.prerequisite ?? {}) as Loose;
      const u = (m.unlocks ?? {}) as Loose;
      const t = (m.test_out ?? {}) as Loose;
      return {
        prerequisite: {
          id: String(p.id),
          name_vi: String(p.name_vi ?? p.id),
          score: num(p.score),
          need: num(p.need, 2),
        },
        unlocks: { id: String(u.id), name_vi: String(u.name_vi ?? u.id) },
        sole_blocker: m.sole_blocker === true,
        also_blocks: num(m.also_blocks),
        suggested_problem: normalizeSuggested(m.suggested_problem),
        test_out: { available: t.available === true, retry_after: strOrNull(t.retry_after) },
      };
    }),
    up_next: list(raw.up_next).map(
      (i): NextItem => ({
        id: String(i.id),
        name_vi: String(i.name_vi ?? i.id),
        score: num(i.score),
        target_intern: num(i.target_intern),
        status: i.status === "in_progress" ? "in_progress" : "unlocked",
        known_basic: i.known_basic === true,
        lesson_done: i.lesson_done === true,
        has_lesson: i.has_lesson !== false,
        check_retry_after: strOrNull(i.check_retry_after),
        due_card: i.due_card === true,
        suggested_problem: normalizeSuggested(i.suggested_problem),
      }),
    ),
    locked_preview: list(raw.locked_preview).map(
      (l): LockedPreview => ({
        id: String(l.id),
        name_vi: String(l.name_vi ?? l.id),
        lock_reasons: list(l.lock_reasons).map((r) => ({
          prerequisite: String(r.prerequisite),
          name_vi: strOrNull(r.name_vi),
          score: typeof r.score === "number" ? r.score : null,
          need: num(r.need, 2),
        })),
      }),
    ),
    due_count: num(raw.due_count),
    backlog: raw.backlog === true,
    study: { today_s: num(study.today_s), week_s: num(study.week_s) },
  };
}

/** GET /api/next -> {must_raise[], up_next[], locked_preview[], due_count, backlog, study}. No current day, no schedule. */
export async function getNext(): Promise<NextData> {
  return normalizeNext(await request<unknown>("/next"));
}

export interface PingResult {
  added_s: number;
  today_s: number;
  week_s: number;
}

/** POST /api/activity/ping every ~30 s while the app is focused; the server caps the added time (60 s, gaps > 2 min skipped). */
export async function pingActivity(): Promise<PingResult> {
  const r = (await request<unknown>("/activity/ping", { method: "POST" })) as Loose;
  return { added_s: num(r?.added_s), today_s: num(r?.today_s), week_s: num(r?.week_s) };
}

export interface ResumeView {
  primary: (ResumeState & { stale: boolean }) | null;
  others: { mode: string; route: string; name_vi: string }[];
}

/** GET /api/resume with `stale` and the other in-progress lessons (S12 banner). */
export async function getResumeView(): Promise<ResumeView> {
  const d = (await request<unknown>("/resume")) as Loose;
  const p = d?.primary as Loose | null | undefined;
  const others = Array.isArray(d?.others) ? (d.others as Loose[]) : [];
  return {
    primary: p
      ? {
          mode: p.mode as ResumeState["mode"],
          route: String(p.route),
          ref: (p.ref as Record<string, unknown>) ?? {},
          context: (p.context as Record<string, unknown>) ?? {},
          updated_at: String(p.updated_at ?? ""),
          stale: p.stale === true,
        }
      : null,
    others: others.map((o) => ({
      mode: String(o.mode ?? "lesson"),
      route: String(o.route),
      name_vi: String(o.name_vi ?? o.route),
    })),
  };
}

// ---------------------------------------------------------------- onboarding (S1)

export interface Onboarding {
  profile_done: boolean;
  placement: "none" | "in_progress" | "finished" | "skipped";
}

export interface Profile {
  target_role: "intern" | "new_grad";
  track: "swe" | "ai";
  language: "python";
  experience: "none" | "some" | "solid";
  display_name?: string;
  tz?: string;
  /** "Bắt đầu từ đầu": no placement session; recorded so S1 is not shown again. */
  placement?: "skipped";
}

/** GET /api/me → onboarding (a missing/odd body counts as "not onboarded"). */
export async function getOnboarding(): Promise<Onboarding> {
  const d = (await request<unknown>("/me")) as Loose;
  const o = (d?.onboarding ?? {}) as Loose;
  return {
    profile_done: o.profile_done === true,
    placement: (o.placement as Onboarding["placement"]) ?? "none",
  };
}

/** PUT /api/profile (idempotent; reuse the key when retrying the same submit). */
export function putProfile(profile: Partial<Profile>, idempotencyKey?: string): Promise<{ onboarding: Onboarding }> {
  return request("/profile", { method: "PUT", body: profile, idempotencyKey });
}

// ---------------------------------------------------------------- settings / backups (S11)

export interface BackupInfo {
  name: string;
  size: number;
  created_at: string;
}

export function normalizeBackup(raw: unknown): BackupInfo {
  const o = (raw ?? {}) as Loose;
  return { name: String(o.name ?? ""), size: Number(o.size ?? 0), created_at: String(o.created_at ?? "") };
}

/** GET /api/backups -> {backups:[{name,size,created_at}]} (newest first as the server sorts). */
export async function listBackups(): Promise<BackupInfo[]> {
  return asArray(await request<unknown>("/backups"), ["backups"]).map(normalizeBackup);
}

/** POST /api/backups ("Sao lưu ngay"). Reuse the key when retrying the same click. */
export async function createBackup(idempotencyKey?: string): Promise<BackupInfo> {
  return normalizeBackup(await request<unknown>("/backups", { method: "POST", idempotencyKey }));
}

/** POST /api/backups/{name}/restore: replaces ALL data; the server backs up the current DB first. */
export async function restoreBackup(name: string, idempotencyKey?: string): Promise<BackupInfo> {
  const d = (await request<unknown>(`/backups/${enc(name)}/restore`, { method: "POST", idempotencyKey })) as Loose;
  return normalizeBackup(d?.restored);
}

export interface SettingsView {
  tz: string;
  review_preset: number | null;
  display_name: string;
  experience: "none" | "some" | "solid";
}

/** GET /api/me -> the editable slice of the settings. */
export async function getSettings(): Promise<SettingsView> {
  const s = (((await request<unknown>("/me")) as Loose)?.settings ?? {}) as Loose;
  return {
    tz: String(s.tz ?? ""),
    review_preset: s.review_preset == null ? null : Number(s.review_preset),
    display_name: String(s.display_name ?? ""),
    experience: s.experience === "none" || s.experience === "solid" ? s.experience : "some",
  };
}

/** PUT /api/settings (`review_preset: null` turns the short session off). */
export function putSettings(
  body: { tz?: string; review_preset?: number | null },
  idempotencyKey?: string,
): Promise<unknown> {
  return request("/settings", { method: "PUT", body, idempotencyKey });
}

// ---------------------------------------------------------------- placement, Phase A (docs/API_M2A.md "Placement")

export type PlacementStatus = "in_progress" | "finished" | "skipped" | string;

export interface PlacementGate {
  code: string;
  subtopic_id: string;
  name_vi: string;
  /** null = not decided yet; else passed | passed_unclean | known | failed | gave_up | locked | unavailable. */
  outcome: string | null;
  l1: string | null;
  retry_after: string | null;
  /** rung ("0" | "1" | "2") -> passed | failed | gave_up. Rung 0 = knowledge, 1 = read code, 2 = write code. */
  rung_results?: Record<string, string>;
}

export interface PlacementBudget {
  soft_ms: number;
  hard_ms: number;
  remaining_ms: number;
}

export interface PlacementCurrent {
  gate: string;
  subtopic_id: string;
  name_vi: string;
  probing: boolean;
  /** "code" (default) | "concept" (concept-phase gate, always an mcq step). */
  kind?: string;
  /** Concept gates only: the module id. */
  module?: string | null;
  /** 0 = knowledge (mcq), 1 = read code, 2 = write code; null/undefined when unknown. */
  rung?: number | null;
  check_session_id: number;
  elapsed_ms: number;
  /** Same shape as a check step (no reference / solution). null when the gate has nothing open. */
  step: CheckStep | null;
}

export interface PlacementConceptOffer {
  module: string;
  name_vi: string;
  hub_subtopic_id: string;
}

export interface PlacementConceptRow {
  gate: string;
  module: string | null;
  name_vi: string;
  subtopic_id: string;
  outcome: string | null;
  score: number;
}

export interface PlacementView {
  placement_id: number;
  status: PlacementStatus;
  /** "code" | "concept_offer" | "concept" */
  phase?: string;
  awaiting_modules?: boolean;
  concept_offer?: PlacementConceptOffer[] | null;
  code_stop_reason?: string | null;
  resumed: boolean;
  stale: boolean;
  stop_reason: string | null;
  message_vi: string | null;
  active_ms: number;
  budget: PlacementBudget;
  progress: { gates_total: number; gates_done: number };
  gates: PlacementGate[];
  current: PlacementCurrent | null;
}

export interface PlacementAnswerResponse {
  result: CheckStepResult;
  gate_outcome: string | null;
  placement: PlacementView;
}

export interface PlacementSkillNode {
  subtopic_id: string;
  name_vi: string;
  score: number;
  /** measured | likely_known | likely_gap | not_assessed */
  state: string;
  seeded: boolean;
  known_basic: boolean;
  placement_hint: string | null;
}

export interface PlacementGateRef {
  gate: string;
  name_vi: string;
  subtopic_id: string;
  outcome?: string;
  retry_after?: string | null;
}

export interface PlacementResult {
  placement_id: number;
  status: PlacementStatus;
  stop_reason: string | null;
  message_vi: string | null;
  active_ms: number;
  seeded: string[];
  skill_map: PlacementSkillNode[];
  strong_areas: PlacementGateRef[];
  weak_areas: PlacementGateRef[];
  concept?: PlacementConceptRow[];
  start: { subtopic_id: string; name_vi: string } | null;
  content_pending: boolean;
  test_out_candidates: string[];
  counts: { measured: number; likely_known: number; likely_gap: number; not_assessed: number };
}

export function normalizePlacementView(data: unknown): PlacementView {
  const raw = (data ?? {}) as Loose;
  const budget = (raw.budget ?? {}) as Loose;
  const progress = (raw.progress ?? {}) as Loose;
  const cur = raw.current as Loose | null | undefined;
  return {
    placement_id: Number(raw.placement_id),
    status: String(raw.status ?? "in_progress"),
    phase: String(raw.phase ?? "code"),
    awaiting_modules: Boolean(raw.awaiting_modules),
    concept_offer:
      ((raw.concept_offer as Loose[] | null | undefined) ?? null)?.map((o) => ({
        module: String(o.module),
        name_vi: String(o.name_vi ?? o.module),
        hub_subtopic_id: String(o.hub_subtopic_id ?? ""),
      })) ?? null,
    code_stop_reason: (raw.code_stop_reason as string | null | undefined) ?? null,
    resumed: Boolean(raw.resumed),
    stale: Boolean(raw.stale),
    stop_reason: (raw.stop_reason as string | null | undefined) ?? null,
    message_vi: (raw.message_vi as string | null | undefined) ?? null,
    active_ms: Number(raw.active_ms ?? 0),
    budget: {
      soft_ms: Number(budget.soft_ms ?? 45 * 60_000),
      hard_ms: Number(budget.hard_ms ?? 60 * 60_000),
      remaining_ms: Number(budget.remaining_ms ?? 60 * 60_000),
    },
    progress: { gates_total: Number(progress.gates_total ?? 0), gates_done: Number(progress.gates_done ?? 0) },
    gates: ((raw.gates as Loose[] | undefined) ?? []).map((g) => ({
      code: String(g.code),
      subtopic_id: String(g.subtopic_id),
      name_vi: String(g.name_vi ?? ""),
      outcome: (g.outcome as string | null | undefined) ?? null,
      l1: (g.l1 as string | null | undefined) ?? null,
      retry_after: (g.retry_after as string | null | undefined) ?? null,
      rung_results: (g.rung_results as Record<string, string> | undefined) ?? undefined,
    })),
    current: cur
      ? {
          gate: String(cur.gate),
          subtopic_id: String(cur.subtopic_id),
          name_vi: String(cur.name_vi ?? ""),
          probing: Boolean(cur.probing),
          kind: String(cur.kind ?? "code"),
          module: (cur.module as string | null | undefined) ?? null,
          rung: typeof cur.rung === "number" ? cur.rung : null,
          check_session_id: Number(cur.check_session_id),
          elapsed_ms: Number(cur.elapsed_ms ?? 0),
          step: cur.step ? normalizeCheckStep(cur.step as Loose) : null,
        }
      : null,
  };
}

export function normalizePlacementAnswer(data: unknown): PlacementAnswerResponse {
  const raw = data as Loose;
  return {
    result: normalizeCheckResult(raw.result as Loose),
    gate_outcome: (raw.gate_outcome as string | null | undefined) ?? null,
    placement: normalizePlacementView(raw.placement),
  };
}

const gateRef = (g: Loose): PlacementGateRef => ({
  gate: String(g.gate),
  name_vi: String(g.name_vi ?? ""),
  subtopic_id: String(g.subtopic_id),
  outcome: g.outcome as string | undefined,
  retry_after: (g.retry_after as string | null | undefined) ?? null,
});

export function normalizePlacementResult(data: unknown): PlacementResult {
  const raw = (data ?? {}) as Loose;
  const counts = (raw.counts ?? {}) as Loose;
  const start = raw.start as Loose | null | undefined;
  return {
    placement_id: Number(raw.placement_id),
    status: String(raw.status ?? "finished"),
    stop_reason: (raw.stop_reason as string | null | undefined) ?? null,
    message_vi: (raw.message_vi as string | null | undefined) ?? null,
    active_ms: Number(raw.active_ms ?? 0),
    seeded: ((raw.seeded as unknown[] | undefined) ?? []).map(String),
    skill_map: ((raw.skill_map as Loose[] | undefined) ?? []).map((m) => ({
      subtopic_id: String(m.subtopic_id),
      name_vi: String(m.name_vi ?? ""),
      score: Number(m.score ?? 0),
      state: String(m.state ?? "not_assessed"),
      seeded: Boolean(m.seeded),
      known_basic: Boolean(m.known_basic),
      placement_hint: (m.placement_hint as string | null | undefined) ?? null,
    })),
    strong_areas: ((raw.strong_areas as Loose[] | undefined) ?? []).map(gateRef),
    weak_areas: ((raw.weak_areas as Loose[] | undefined) ?? []).map(gateRef),
    concept: ((raw.concept as Loose[] | undefined) ?? []).map((c) => ({
      gate: String(c.gate),
      module: (c.module as string | null | undefined) ?? null,
      name_vi: String(c.name_vi ?? c.module ?? ""),
      subtopic_id: String(c.subtopic_id),
      outcome: (c.outcome as string | null | undefined) ?? null,
      score: Number(c.score ?? 0),
    })),
    start: start ? { subtopic_id: String(start.subtopic_id), name_vi: String(start.name_vi ?? "") } : null,
    content_pending: Boolean(raw.content_pending),
    test_out_candidates: ((raw.test_out_candidates as unknown[] | undefined) ?? []).map(String),
    counts: {
      measured: Number(counts.measured ?? 0),
      likely_known: Number(counts.likely_known ?? 0),
      likely_gap: Number(counts.likely_gap ?? 0),
      not_assessed: Number(counts.not_assessed ?? 0),
    },
  };
}

/** POST /api/placement: start, or resume the sitting in progress (`resumed`). `skip` writes nothing. */
export async function startPlacement(
  opts: {
    experience?: "none" | "some" | "solid";
    restart?: boolean;
    skip?: boolean;
    kind?: "initial" | "deep_dive";
    module?: string;
  } = {},
  key?: string,
): Promise<PlacementView> {
  return normalizePlacementView(
    await request<unknown>("/placement", { method: "POST", body: opts, idempotencyKey: key }),
  );
}

/** GET /api/placement/current -> the latest sitting, or null. */
export async function getPlacementCurrent(): Promise<PlacementView | null> {
  const d = (await request<unknown>("/placement/current")) as Loose;
  return d?.placement ? normalizePlacementView(d.placement) : null;
}

export async function getPlacement(id: number | string): Promise<PlacementView> {
  return normalizePlacementView(await request<unknown>(`/placement/${enc(String(id))}`));
}

export async function answerPlacement(
  id: number,
  body: { item_id: string; elapsed_ms: number; session_elapsed_ms?: number } & CheckAnswerBody,
  key?: string,
): Promise<PlacementAnswerResponse> {
  return normalizePlacementAnswer(
    await request<unknown>(`/placement/${id}/answer`, { method: "POST", body, idempotencyKey: key }),
  );
}

/** "Không biết": a give-up (no lock, not a pass). */
export async function skipPlacement(
  id: number,
  body: { item_id: string; elapsed_ms: number; session_elapsed_ms?: number },
  key?: string,
): Promise<PlacementAnswerResponse> {
  return normalizePlacementAnswer(
    await request<unknown>(`/placement/${id}/skip`, { method: "POST", body, idempotencyKey: key }),
  );
}

/** POST /api/placement/{id}/modules: the concept-phase self-report (module ids the user says they
 * know). An empty list ends the sitting. Returns the placement view (`current` = first concept gate). */
export async function selectPlacementModules(
  id: number,
  selected: string[],
  key?: string,
  activeMs?: number,
): Promise<PlacementView> {
  return normalizePlacementView(
    await request<unknown>(`/placement/${id}/modules`, {
      method: "POST",
      body: activeMs === undefined ? { selected } : { selected, active_ms: Math.round(activeMs) },
      idempotencyKey: key,
    }),
  );
}

/** Absolute, monotonic active time; safe to resend. */
export function placementHeartbeat(
  id: number,
  activeMs: number,
  itemElapsedMs?: number,
  options: { keepalive?: boolean } = {},
): Promise<{ placement_id: number; status: string; active_ms: number; budget: PlacementBudget }> {
  return request(`/placement/${id}/heartbeat`, {
    method: "POST",
    body: {
      active_ms: Math.round(activeMs),
      ...(itemElapsedMs === undefined ? {} : { item_elapsed_ms: Math.round(itemElapsedMs) }),
    },
    keepalive: options.keepalive,
  });
}

export async function finishPlacement(id: number, activeMs?: number, key?: string): Promise<PlacementView> {
  return normalizePlacementView(
    await request<unknown>(`/placement/${id}/finish`, {
      method: "POST",
      body: activeMs === undefined ? {} : { active_ms: Math.round(activeMs) },
      idempotencyKey: key,
    }),
  );
}

/** 409 placement_skipped when the sitting was skipped (nothing measured). */
export async function getPlacementResult(id: number | string): Promise<PlacementResult> {
  return normalizePlacementResult(await request<unknown>(`/placement/${enc(String(id))}/result`));
}
