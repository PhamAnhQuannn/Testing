// The single module that talks to the backend (SPEC 6.4). Response shapes are normalized here
// so that reconciling with the real API (docs/API_M1.md) only touches this file.
import type { ProblemIO, TestCase } from "../runner/Runner";

export class ApiError extends Error {
  constructor(
    readonly status: number,
    readonly code: string,
    message: string,
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
    try {
      const data = (await response.json()) as { error?: { code?: string; message?: string } };
      if (data.error) {
        code = data.error.code ?? code;
        message = data.error.message ?? message;
      }
    } catch {
      /* body was not JSON */
    }
    throw new ApiError(response.status, code, message);
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
  content_status?: string | null;
}

type Loose = Record<string, unknown>;
const asArray = (data: unknown, keys: string[]): Loose[] => {
  if (Array.isArray(data)) return data as Loose[];
  for (const key of keys) {
    const value = (data as Loose | null)?.[key];
    if (Array.isArray(value)) return value as Loose[];
  }
  return [];
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
      content_status: (raw.content_status as string | null | undefined) ?? null,
    };
  });
}

/** GET /api/map -> subtopics[] (array or {subtopics|items:[...]}) */
export async function getMap(): Promise<MapSubtopic[]> {
  return normalizeMap(await request<unknown>("/map"));
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
