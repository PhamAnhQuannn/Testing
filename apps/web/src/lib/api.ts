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
}

export const API_BASE = "/api";

export async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const method = options.method ?? "GET";
  const headers: Record<string, string> = { Accept: "application/json" };
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
      lock_reason: (raw.lock_reason as string | null | undefined) ?? null,
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
      answer: string[];
      multi?: boolean;
      explain_md: string;
    }
  | {
      id: string;
      type: "quiz_fill";
      graded?: boolean;
      prompt_md: string;
      blanks: { accept: string[]; regex?: string }[];
      explain_md: string;
    }
  | {
      id: string;
      type: "predict_output";
      graded?: boolean;
      code: string;
      expected_output: string;
      explain_md: string;
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
  /** Optional server-side state: answers already given in the current run. */
  answers: Record<string, { correct: boolean; answer?: unknown }>;
  completed: boolean;
}

export function normalizeLesson(data: unknown): Lesson {
  const root = ((data as Loose).lesson ?? data) as Loose;
  const state = (root.state ?? data) as Loose;
  return {
    id: String(root.id),
    title_vi: String(root.title_vi ?? root.id),
    est_minutes: Number(root.est_minutes ?? 0),
    objectives_vi: (root.objectives_vi as string[]) ?? [],
    blocks: (root.blocks as LessonBlock[]) ?? [],
    problems: (root.problems as Lesson["problems"]) ?? { practice: [], extra: [] },
    checkpoint: (root.checkpoint as Lesson["checkpoint"]) ?? { pass_ratio: 0.7, min_items: 3 },
    status: root.status as string | undefined,
    run_no: Number(state.run_no ?? root.run_no ?? 1),
    answers: (state.answers as Lesson["answers"]) ?? {},
    completed: Boolean(state.completed ?? root.completed ?? false),
  };
}

/** GET /api/lessons/{subtopic_id} -> lesson (blocks without code_exercise.solution) [+ run_no, answers, completed] */
export async function getLesson(subtopicId: string): Promise<Lesson> {
  return normalizeLesson(await request<unknown>(`/lessons/${enc(subtopicId)}`));
}

export interface QuizAnswerBody {
  subtopic_id: string;
  block_id: string;
  run_no: number;
  answer: unknown;
  correct: boolean;
  occurred_at: string;
}
export interface QuizAnswerResult {
  correct?: boolean;
  explain_md?: string;
}

/** POST /api/quiz/answers {subtopic_id, block_id, run_no, answer, correct, occurred_at} -> {correct, explain_md} */
export function postQuizAnswer(body: QuizAnswerBody, key?: string): Promise<QuizAnswerResult> {
  return request("/quiz/answers", { method: "POST", body, idempotencyKey: key });
}

export interface LessonCompleteResult {
  quiz_best?: number;
  passed?: boolean;
  score?: number;
  wrong_blocks?: string[];
  review_card_created?: boolean;
  [key: string]: unknown;
}

/** POST /api/lessons/{id}/complete {run_no, occurred_at} -> {quiz_best, score, passed?, wrong_blocks?} */
export function completeLesson(
  subtopicId: string,
  body: { run_no: number; occurred_at: string },
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
  draft: DraftPayload | null;
  status?: string;
  solved: boolean;
}

export function normalizeProblem(data: unknown): Problem {
  const root = ((data as Loose).problem ?? data) as Loose;
  const starter = root.starter as string | { python?: string } | undefined;
  const limits = (root.limits as Problem["limits"]) ?? { time_ms: 1000, memory_mb: 256 };
  const tests = root.tests as { sample?: TestCase[] } | undefined;
  const opened = (root.hints_opened ?? root.hints_shown ?? []) as string[];
  const hintsTotal = Number(root.hints_total ?? (root.hints as unknown[] | undefined)?.length ?? 3);
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
    draft: (root.draft as DraftPayload | null | undefined) ?? null,
    status: root.status as string | undefined,
    solved: Boolean(root.solved ?? root.accepted ?? false),
  };
}

function pyodideMultiplier(limits: unknown): { time_multiplier?: number } {
  const multiplier = (limits as { time_multiplier?: { pyodide?: number } | number }).time_multiplier;
  if (typeof multiplier === "number") return { time_multiplier: multiplier };
  return multiplier?.pyodide ? { time_multiplier: multiplier.pyodide } : {};
}

/** GET /api/problems/{id} -> problem (statement, io, starter, sample_tests, limits, hints_opened[], draft?) */
export async function getProblem(id: string): Promise<Problem> {
  return normalizeProblem(await request<unknown>(`/problems/${enc(id)}`));
}

/** POST /api/problems/{id}/start-submit {} -> {token} ; GET /api/problems/{id}/tests/hidden?token= -> tests[] */
export async function getHiddenTests(id: string): Promise<TestCase[]> {
  const start = await request<{ token?: string }>(`/problems/${enc(id)}/start-submit`, {
    method: "POST",
    body: {},
  });
  const query = start.token ? `?token=${enc(start.token)}` : "";
  const data = await request<unknown>(`/problems/${enc(id)}/tests/hidden${query}`);
  return asArray(data, ["tests", "items", "hidden"]) as TestCase[];
}

/** POST /api/problems/{id}/hints {} -> {level, hint, hints_used} */
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
    level: Number(data.level ?? data.hints_used ?? 1),
    hint: String(data.hint ?? data.text ?? ""),
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
  code: string;
  verdict: string;
  passed: number;
  total: number;
  first_failed?: string | null;
  elapsed_ms: number;
  run_ms?: number;
  occurred_at: string;
}
export interface AttemptResult {
  clean?: boolean;
  score?: number;
  accepted?: boolean;
  [key: string]: unknown;
}

/** POST /api/attempts {problem_id, mode, code, verdict, passed, total, first_failed, elapsed_ms, run_ms, occurred_at} -> {clean?, score?, ...} */
export function postAttempt(body: AttemptBody, key?: string): Promise<AttemptResult> {
  return request("/attempts", { method: "POST", body, idempotencyKey: key });
}

/** PUT /api/drafts/{problem_id} {code, base_rev: null, updated_at, cursor, elapsed_ms} -> {rev?, updated_at?} */
export function putDraft(
  problemId: string,
  draft: DraftPayload,
  options: { keepalive?: boolean } = {},
): Promise<unknown> {
  return request(`/drafts/${enc(problemId)}`, {
    method: "PUT",
    body: { ...draft, base_rev: null },
    keepalive: options.keepalive,
  });
}

// ---------------------------------------------------------------- resume

export interface ResumeState {
  mode: "lesson" | "problem" | "check" | "placement" | "review" | "other";
  route: string;
  ref: Record<string, unknown>;
  context?: Record<string, unknown>;
  updated_at: string;
}

/** PUT /api/resume {mode, route, ref, context, updated_at} -> 204/{} */
export function putResume(state: ResumeState, options: { keepalive?: boolean } = {}): Promise<unknown> {
  return request("/resume", { method: "PUT", body: state, keepalive: options.keepalive });
}

/** GET /api/resume -> {primary, others[], in_progress}; primary: {mode, route, ref, stale?} | null */
export async function getResume(): Promise<ResumeState | null> {
  const data = await request<{ primary?: ResumeState | null }>("/resume");
  return data.primary ?? null;
}
