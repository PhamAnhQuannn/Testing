import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { CodeEditor } from "../components/CodeEditor";
import { Markdown } from "../components/Markdown";
import { useToast } from "../components/Toast";
import { Link } from "react-router-dom";
import { nowIso, postQuizAnswer, type KnownAnswer, type LessonBlock } from "../lib/api";
import { DraftController, type Draft } from "../lib/draftStore";
import { useRunnerState } from "../lib/hooks";
import { idbStore } from "../lib/idb";
import { getRunner } from "../runner";
import { normalizeOutput } from "../lib/grade";

export interface BlockContext {
  subtopicId: string;
  runNo: number;
  /** Server-known answers for the current run (reload keeps them). */
  known: Record<string, KnownAnswer>;
  onAnswered: (blockId: string, correct: boolean) => void;
  activeExercise: string | null;
  doneExercises: Set<string>;
  onOpenExercise: (blockId: string) => void;
  canEdit: boolean;
}

type Of<T extends LessonBlock["type"]> = Extract<LessonBlock, { type: T }>;

const CALLOUT_LABEL: Record<Of<"callout">["kind"], string> = {
  tip: "Mẹo",
  warning: "Lưu ý",
  beginner: "Cho người mới",
  interview: "Mẹo phỏng vấn",
};

export function BlockView({ block, ctx }: { block: LessonBlock; ctx: BlockContext }) {
  switch (block.type) {
    case "text":
      return <Markdown md={block.md} />;
    case "callout":
      return (
        <aside className={`callout ${block.kind}`}>
          <div className="label">{CALLOUT_LABEL[block.kind]}</div>
          <Markdown md={block.md} />
        </aside>
      );
    case "code_sample":
      return <CodeSample block={block} ctx={ctx} />;
    case "quiz_mcq":
      return <QuizMcq key={ctx.runNo} block={block} ctx={ctx} />;
    case "quiz_fill":
      return <QuizFill key={ctx.runNo} block={block} ctx={ctx} />;
    case "predict_output":
      return <PredictOutput key={ctx.runNo} block={block} ctx={ctx} />;
    case "code_exercise":
      return <ExerciseCard block={block} ctx={ctx} />;
    case "problem_ref":
      return (
        <div className="block-card">
          Bài tập đầy đủ: <Link to={`/p/${block.problem_id}`}>{block.problem_id}</Link>
        </div>
      );
    case "summary":
      return (
        <div className="block-card">
          <strong>Tóm tắt</strong>
          <ul>
            {block.bullets_vi.map((bullet, i) => (
              <li key={i}>
                <Markdown md={bullet} />
              </li>
            ))}
          </ul>
        </div>
      );
  }
}

// ------------------------------------------------------------------ code_sample

function CodeSample({ block, ctx }: { block: Of<"code_sample">; ctx: BlockContext }) {
  const runnerState = useRunnerState();
  const [code, setCode] = useState(block.code);
  const [out, setOut] = useState<{ text: string; ok: boolean; error?: string } | null>(null);
  const [running, setRunning] = useState(false);
  const codeRef = useRef(block.code);

  const controller = useMemo(
    () =>
      new DraftController({
        key: `sample:${ctx.subtopicId}:${block.id}`,
        local: idbStore<Draft>("sample"),
      }),
    [ctx.subtopicId, block.id],
  );
  useEffect(() => {
    let alive = true;
    controller.load(null).then((draft) => {
      if (alive && draft && draft.code !== block.code) {
        codeRef.current = draft.code;
        setCode(draft.code);
      }
    });
    return () => {
      alive = false;
      void controller.flush();
    };
  }, [controller, block.code]);

  const run = useCallback(async () => {
    setRunning(true);
    try {
      const result = await getRunner().run({
        code: codeRef.current,
        io: { mode: "stdout" },
        tests: [{ id: "run" }],
        limits: { time_ms: 1000, memory_mb: 256, time_multiplier: 3 },
      });
      const r = result.results[0];
      const text = r?.stdout ?? "";
      if (r && r.verdict !== "AC") setOut({ text, ok: false, error: r.error });
      else setOut({ text, ok: block.expected_output === undefined || normalizeOutput(text) === normalizeOutput(block.expected_output) });
    } catch (error) {
      setOut({ text: "", ok: false, error: (error as Error).message });
    } finally {
      setRunning(false);
    }
  }, [block.expected_output]);

  if (!block.runnable || block.lang !== "python") {
    return <pre className="output">{block.code}</pre>;
  }
  return (
    <div>
      <CodeEditor
        value={code}
        ariaLabel="Code mẫu, sửa được"
        minHeight={48}
        onChange={(next, cursor) => {
          codeRef.current = next;
          controller.update(next, cursor);
        }}
        onRun={() => void run()}
        onBlur={() => void controller.flush()}
        readOnly={!ctx.canEdit}
      />
      <div className="toolbar" style={{ marginTop: 8 }}>
        <button
          className="btn sm"
          onClick={() => void run()}
          disabled={running || runnerState === "loading" || !ctx.canEdit}
          title={ctx.canEdit ? "Ctrl/Cmd+Enter" : "Mở trên máy tính để chạy code"}
        >
          {runnerState === "loading" ? "Đang chuẩn bị…" : "▶ Chạy"}
        </button>
        {code !== block.code && (
          <button
            className="btn sm ghost"
            onClick={() => {
              codeRef.current = block.code;
              setCode(block.code);
              controller.update(block.code);
            }}
          >
            ⟲ Về bản gốc
          </button>
        )}
      </div>
      {out && (
        <div aria-live="polite">
          <pre className={`output${out.error ? " bad" : ""}`}>
            {out.error ? out.error : out.text || "(không có output)"}
          </pre>
          {!out.error && block.expected_output !== undefined && (
            <div className={`status-line`}>
              {out.ok ? "✔ Khớp output mong đợi" : `✘ Output mong đợi: ${block.expected_output}`}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// ------------------------------------------------------------------ quizzes

interface Answered {
  correct: boolean;
  explain?: string;
  correctAnswer?: unknown;
  known?: boolean;
}

function useQuizInflight<T>(ctx: BlockContext, blockId: string, initial: T) {
  const store = useMemo(() => idbStore<T>("quiz_inflight"), []);
  const key = `${ctx.subtopicId}:${blockId}:${ctx.runNo}`;
  const [value, setValue] = useState<T>(initial);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  useEffect(() => {
    let alive = true;
    store.get(key).then((saved) => alive && saved !== undefined && setValue(saved)).catch(() => undefined);
    return () => {
      alive = false;
    };
  }, [store, key]);
  const update = (next: T) => {
    setValue(next);
    if (timer.current) clearTimeout(timer.current);
    timer.current = setTimeout(() => void store.put(key, next).catch(() => undefined), 300);
  };
  const clear = () => void store.delete(key).catch(() => undefined);
  return [value, update, clear] as const;
}

/** Grading is server-side (the lesson JSON carries no answers): POST /quiz/answers. */
function useQuizSubmit(ctx: BlockContext, blockId: string, clear: () => void) {
  const notify = useToast();
  const [busy, setBusy] = useState(false);
  const [answered, setAnswered] = useState<Answered | null>(() => {
    const known = ctx.known[blockId];
    return known ? { correct: known.correct, known: true } : null;
  });
  const submit = async (answer: unknown) => {
    setBusy(true);
    try {
      const result = await postQuizAnswer({
        quiz_item_id: `${ctx.subtopicId}#${blockId}`,
        run_no: ctx.runNo,
        answer,
        occurred_at: nowIso(),
      });
      setAnswered({
        correct: result.correct,
        explain: result.explain_md,
        correctAnswer: result.correct_answer,
      });
      clear();
      // only the first answer per block per run counts toward quiz_best
      if (result.first_attempt !== false) ctx.onAnswered(blockId, result.correct);
    } catch (error) {
      notify(`Chưa chấm được (cần server): ${(error as Error).message}`, { kind: "error" });
    } finally {
      setBusy(false);
    }
  };
  return { answered, busy, submit };
}

function Feedback({ answered }: { answered: Answered }) {
  return (
    <div className={`feedback ${answered.correct ? "ok" : "bad"}`} role="status">
      <strong>{answered.correct ? "✔ Đúng" : "✘ Chưa đúng"}</strong>
      {answered.explain && <Markdown md={answered.explain} />}
    </div>
  );
}

function QuizMcq({ block, ctx }: { block: Of<"quiz_mcq">; ctx: BlockContext }) {
  const known = ctx.known[block.id]?.answer;
  const [selected, setSelected, clear] = useQuizInflight<string[]>(
    ctx,
    block.id,
    Array.isArray(known) ? (known as string[]) : [],
  );
  const { answered, busy, submit } = useQuizSubmit(ctx, block.id, clear);
  // `multi` is shipped; without it a single choice is assumed
  const multi = Boolean(block.multi);
  const toggle = (id: string) =>
    setSelected(multi ? (selected.includes(id) ? selected.filter((s) => s !== id) : [...selected, id]) : [id]);
  const right = Array.isArray(answered?.correctAnswer) ? (answered.correctAnswer as string[]) : [];
  return (
    <fieldset className="block-card" disabled={Boolean(answered) || busy}>
      <legend>Quiz</legend>
      <Markdown md={block.prompt_md} />
      {block.options.map((option) => {
        const state = answered && right.length ? (right.includes(option.id) ? "right" : selected.includes(option.id) ? "wrong" : "") : "";
        return (
          <label key={option.id} className={`option ${state}`}>
            <input
              type={multi ? "checkbox" : "radio"}
              name={block.id}
              checked={selected.includes(option.id)}
              onChange={() => toggle(option.id)}
            />
            <Markdown md={option.text_md} />
          </label>
        );
      })}
      {!answered && (
        <button className="btn sm primary" disabled={selected.length === 0 || busy} onClick={() => void submit(selected)}>
          {busy ? "Đang chấm…" : "Kiểm tra"}
        </button>
      )}
      {answered && <Feedback answered={answered} />}
    </fieldset>
  );
}

function QuizFill({ block, ctx }: { block: Of<"quiz_fill">; ctx: BlockContext }) {
  const known = ctx.known[block.id]?.answer;
  const [values, setValues, clear] = useQuizInflight<string[]>(
    ctx,
    block.id,
    Array.isArray(known) ? (known as string[]) : block.blanks.map(() => ""),
  );
  const { answered, busy, submit } = useQuizSubmit(ctx, block.id, clear);
  return (
    <fieldset className="block-card" disabled={Boolean(answered) || busy}>
      <legend>Điền vào chỗ trống</legend>
      <Markdown md={block.prompt_md} />
      {block.blanks.map((_, i) => (
        <label key={i} style={{ display: "block", margin: "4px 0" }}>
          <span className="muted">Chỗ trống {i + 1}: </span>
          <input
            className="text-input"
            value={values[i] ?? ""}
            onChange={(e) => setValues(block.blanks.map((_b, j) => (j === i ? e.target.value : (values[j] ?? ""))))}
            onKeyDown={(e) => e.key === "Enter" && !answered && void submit(values)}
            autoComplete="off"
            spellCheck={false}
          />
        </label>
      ))}
      {!answered && (
        <button className="btn sm primary" onClick={() => void submit(values)} disabled={busy || values.every((v) => !v.trim())}>
          {busy ? "Đang chấm…" : "Kiểm tra"}
        </button>
      )}
      {answered && (
        <>
          {Array.isArray(answered.correctAnswer) && (
            <div className="status-line">Đáp án: {(answered.correctAnswer as string[]).join(", ")}</div>
          )}
          <Feedback answered={answered} />
        </>
      )}
    </fieldset>
  );
}

function PredictOutput({ block, ctx }: { block: Of<"predict_output">; ctx: BlockContext }) {
  const known = ctx.known[block.id]?.answer;
  const [typed, setTyped, clear] = useQuizInflight<string>(ctx, block.id, typeof known === "string" ? known : "");
  const { answered, busy, submit } = useQuizSubmit(ctx, block.id, clear);
  return (
    <fieldset className="block-card" disabled={Boolean(answered) || busy}>
      <legend>Đoán output</legend>
      <pre className="output">{block.code}</pre>
      <label>
        <span className="muted">Output của đoạn code trên:</span>
        <textarea className="text-input" value={typed} onChange={(e) => setTyped(e.target.value)} spellCheck={false} />
      </label>
      {!answered && (
        <button className="btn sm primary" onClick={() => void submit(typed)} disabled={!typed.trim() || busy}>
          {busy ? "Đang chấm…" : "Kiểm tra"}
        </button>
      )}
      {answered && (
        <>
          {typeof answered.correctAnswer === "string" && (
            <>
              <div className="status-line">Output thật:</div>
              <pre className="output">{answered.correctAnswer}</pre>
            </>
          )}
          <Feedback answered={answered} />
        </>
      )}
    </fieldset>
  );
}

// ------------------------------------------------------------------ code_exercise (card in the lesson)

function ExerciseCard({ block, ctx }: { block: Of<"code_exercise">; ctx: BlockContext }) {
  const done = ctx.doneExercises.has(block.id);
  const active = ctx.activeExercise === block.id;
  return (
    <div className="block-card">
      <strong>Bài tập nhỏ {done && <span className="chip ok">✔ Xong</span>}</strong>
      <Markdown md={block.md} />
      <button
        className="btn sm primary"
        onClick={() => ctx.onOpenExercise(block.id)}
        disabled={!ctx.canEdit}
        title={ctx.canEdit ? undefined : "Mở trên máy tính để viết code"}
      >
        {active ? "Đang làm ở editor →" : "Làm bài này"}
      </button>
    </div>
  );
}
