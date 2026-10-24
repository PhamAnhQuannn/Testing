import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { CodeEditor } from "../components/CodeEditor";
import { Markdown } from "../components/Markdown";
import { useToast } from "../components/Toast";
import { Link } from "react-router-dom";
import { nowIso, postQuizAnswer, type LessonBlock } from "../lib/api";
import { DraftController, type Draft } from "../lib/draftStore";
import { gradeFill, gradeMcq, gradePredict } from "../lib/grade";
import { useRunnerState } from "../lib/hooks";
import { idbStore } from "../lib/idb";
import { getRunner } from "../runner";
import { normalizeOutput } from "../lib/grade";

export interface BlockContext {
  subtopicId: string;
  runNo: number;
  /** Server-known answers for the current run (reload keeps them). */
  known: Record<string, { correct: boolean }>;
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

type Answered = { correct: boolean; known?: boolean };

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

function useAnswerSubmit(ctx: BlockContext, blockId: string) {
  const notify = useToast();
  return useCallback(
    (answer: unknown, correct: boolean) => {
      ctx.onAnswered(blockId, correct);
      const body = {
        subtopic_id: ctx.subtopicId,
        block_id: blockId,
        run_no: ctx.runNo,
        answer,
        correct,
        occurred_at: nowIso(),
      };
      const key = crypto.randomUUID();
      const send = () =>
        postQuizAnswer(body, key).catch(() =>
          notify("Chưa lưu được câu trả lời", { kind: "error", action: { label: "Thử lại", run: () => void send() } }),
        );
      void send();
    },
    [ctx, blockId, notify],
  );
}

function Feedback({ answered, explain }: { answered: Answered; explain: string }) {
  return (
    <div className={`feedback ${answered.correct ? "ok" : "bad"}`} role="status">
      <strong>{answered.correct ? "✔ Đúng" : "✘ Chưa đúng"}</strong>
      <Markdown md={explain} />
    </div>
  );
}

function QuizMcq({ block, ctx }: { block: Of<"quiz_mcq">; ctx: BlockContext }) {
  const submit = useAnswerSubmit(ctx, block.id);
  const known = ctx.known[block.id];
  const [selected, setSelected, clear] = useQuizInflight<string[]>(ctx, block.id, []);
  const [answered, setAnswered] = useState<Answered | null>(known ? { ...known, known: true } : null);
  const multi = block.multi ?? block.answer.length > 1;
  const toggle = (id: string) =>
    setSelected(multi ? (selected.includes(id) ? selected.filter((s) => s !== id) : [...selected, id]) : [id]);
  const check = () => {
    const correct = gradeMcq(block, selected);
    setAnswered({ correct });
    clear();
    submit(selected, correct);
  };
  return (
    <fieldset className="block-card" disabled={Boolean(answered)} style={{ border: undefined }}>
      <legend>Quiz</legend>
      <Markdown md={block.prompt_md} />
      {block.options.map((option) => {
        const state = answered && !answered.known ? (block.answer.includes(option.id) ? "right" : selected.includes(option.id) ? "wrong" : "") : "";
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
        <button className="btn sm primary" disabled={selected.length === 0} onClick={check}>
          Kiểm tra
        </button>
      )}
      {answered && <Feedback answered={answered} explain={block.explain_md} />}
    </fieldset>
  );
}

function QuizFill({ block, ctx }: { block: Of<"quiz_fill">; ctx: BlockContext }) {
  const submit = useAnswerSubmit(ctx, block.id);
  const known = ctx.known[block.id];
  const [values, setValues, clear] = useQuizInflight<string[]>(ctx, block.id, block.blanks.map(() => ""));
  const [answered, setAnswered] = useState<Answered | null>(known ? { ...known, known: true } : null);
  const check = () => {
    const correct = gradeFill(block, values);
    setAnswered({ correct });
    clear();
    submit(values, correct);
  };
  return (
    <fieldset className="block-card" disabled={Boolean(answered)}>
      <legend>Điền vào chỗ trống</legend>
      <Markdown md={block.prompt_md} />
      {block.blanks.map((_, i) => (
        <label key={i} style={{ display: "block", margin: "4px 0" }}>
          <span className="muted">Chỗ trống {i + 1}: </span>
          <input
            className="text-input"
            value={values[i] ?? ""}
            onChange={(e) => setValues(values.map((v, j) => (j === i ? e.target.value : v)))}
            onKeyDown={(e) => e.key === "Enter" && !answered && check()}
            autoComplete="off"
            spellCheck={false}
          />
        </label>
      ))}
      {!answered && (
        <button className="btn sm primary" onClick={check} disabled={values.every((v) => !v.trim())}>
          Kiểm tra
        </button>
      )}
      {answered && <Feedback answered={answered} explain={block.explain_md} />}
    </fieldset>
  );
}

function PredictOutput({ block, ctx }: { block: Of<"predict_output">; ctx: BlockContext }) {
  const submit = useAnswerSubmit(ctx, block.id);
  const known = ctx.known[block.id];
  const [typed, setTyped, clear] = useQuizInflight<string>(ctx, block.id, "");
  const [answered, setAnswered] = useState<Answered | null>(known ? { ...known, known: true } : null);
  const check = () => {
    const correct = gradePredict(block, typed);
    setAnswered({ correct });
    clear();
    submit(typed, correct);
  };
  return (
    <fieldset className="block-card" disabled={Boolean(answered)}>
      <legend>Đoán output</legend>
      <pre className="output">{block.code}</pre>
      <label>
        <span className="muted">Output của đoạn code trên:</span>
        <textarea
          className="text-input"
          value={typed}
          onChange={(e) => setTyped(e.target.value)}
          spellCheck={false}
        />
      </label>
      {!answered && (
        <button className="btn sm primary" onClick={check} disabled={!typed.trim()}>
          Kiểm tra
        </button>
      )}
      {answered && (
        <>
          <div className="status-line">Output thật:</div>
          <pre className="output">{block.expected_output}</pre>
          <Feedback answered={answered} explain={block.explain_md} />
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
