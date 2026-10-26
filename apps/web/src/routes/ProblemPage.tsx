import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { ConfirmModal } from "../components/Modal";
import { EditorPanel, formatClock } from "../components/EditorPanel";
import { Markdown } from "../components/Markdown";
import { SplitLayout } from "../components/SplitLayout";
import { TestResultPanel, type PanelState } from "../components/TestResultPanel";
import { useToast } from "../components/Toast";
import {
  ApiError,
  getDraft,
  getProblem,
  getSolution,
  newIdempotencyKey,
  nowIso,
  openHint,
  postAttempt,
  putDraft,
  putResume,
  type Problem,
  type Solution,
} from "../lib/api";
import { DraftController, type Draft, type SaveStatus } from "../lib/draftStore";
import { lsGet, lsSet, useAsync, useOnline, usePageExit, useRunnerState } from "../lib/hooks";
import { PreviewBanner } from "../components/PreviewBanner";
import { isLocked, previewReason, useSubtopicLock } from "../lib/lock";
import { idbStore } from "../lib/idb";
import { ResumeReporter } from "../lib/resumeReporter";
import { runProblem } from "../lib/runProblem";

export default function ProblemPage() {
  const { problemId } = useParams();
  const problem = useAsync(() => getProblem(problemId!), [problemId]);
  if (problem.loading) {
    return (
      <div className="page" aria-busy="true">
        <div className="skeleton" style={{ width: "50%" }} />
        <div className="skeleton" style={{ width: "90%" }} />
        <div className="skeleton" style={{ width: "70%" }} />
      </div>
    );
  }
  if (problem.error || !problem.data) {
    return (
      <div className="page error-block" role="alert">
        <strong>Không tải được bài tập</strong>
        <p>{problem.error?.message}</p>
        <button className="btn" onClick={problem.reload}>
          Thử lại
        </button>
      </div>
    );
  }
  return <ProblemView key={problem.data.id} problem={problem.data} />;
}

const DIFF: Record<string, string> = { easy: "E", medium: "M", hard: "H" };

function ProblemView({ problem }: { problem: Problem }) {
  const notify = useToast();
  const lock = useSubtopicLock(problem.subtopic_id);
  const preview = lock !== null && isLocked(lock);
  const online = useOnline();
  const runnerState = useRunnerState();
  const [lang, setLang] = useState<"en" | "vi">(() => (lsGet("prep:lang") === "vi" ? "vi" : "en"));
  const [code, setCode] = useState<string | null>(null);
  const [cursor, setCursor] = useState(0);
  const [status, setStatus] = useState<SaveStatus>({ state: "idle" });
  const [panel, setPanel] = useState<PanelState | null>(null);
  const [running, setRunning] = useState(false);
  const [hints, setHints] = useState<string[]>(problem.hints_opened);
  const [solved, setSolved] = useState(problem.solved);
  const [solution, setSolution] = useState<Solution | null>(null);
  const [confirm, setConfirm] = useState<"solution" | "reset" | null>(null);
  const [showTimer, setShowTimer] = useState(true);
  const [elapsed, setElapsed] = useState(0);
  const elapsedRef = useRef(0);
  const codeRef = useRef("");

  const controller = useMemo(
    () =>
      new DraftController({
        key: `problem:${problem.id}`,
        local: idbStore<Draft>("drafts"),
        remote: (draft, options) => putDraft(problem.id, draft, options),
        onStatus: setStatus,
      }),
    [problem.id],
  );
  const reporter = useMemo(
    () => new ResumeReporter(putResume, idbStore("resume")),
    [],
  );

  // Load: IndexedDB vs server, newest updated_at wins.
  useEffect(() => {
    let alive = true;
    getDraft(problem.id)
      .catch(() => null)
      .then((remote) => controller.load(remote))
      .then((draft) => {
      if (!alive) return;
      elapsedRef.current = draft?.elapsed_ms ?? 0;
      setElapsed(elapsedRef.current);
      setCursor(draft?.cursor ?? 0);
      codeRef.current = draft?.code ?? problem.starter;
      setCode(codeRef.current);
    });
    return () => {
      alive = false;
    };
  }, [controller, problem]);

  // Elapsed = time the problem is on screen and the tab is visible (UI_SPEC 4.2).
  useEffect(() => {
    const timer = setInterval(() => {
      if (document.visibilityState !== "visible") return;
      elapsedRef.current += 1000;
      setElapsed(elapsedRef.current);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    reporter.report({
      mode: "problem",
      route: `/p/${problem.id}`,
      ref: { problem_id: problem.id, cursor },
    });
  }, [reporter, problem.id, cursor]);

  const flushAll = useCallback(
    (keepalive: boolean) => {
      void controller.flush(keepalive);
      void reporter.flush(keepalive);
    },
    [controller, reporter],
  );
  usePageExit(flushAll);
  useEffect(() => () => flushAll(false), [flushAll]);

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if ((event.ctrlKey || event.metaKey) && event.shiftKey && event.key.toLowerCase() === "l") {
        event.preventDefault();
        setLang((l) => {
          const next = l === "en" ? "vi" : "en";
          lsSet("prep:lang", next);
          return next;
        });
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  const onChange = useCallback(
    (next: string, at: number) => {
      codeRef.current = next;
      setCursor(at);
      controller.update(next, at, elapsedRef.current);
    },
    [controller],
  );

  const execute = async (kind: "run" | "submit") => {
    if (preview || running) return; // preview mode: keyboard shortcuts must not run/submit either
    setRunning(true);
    const source = codeRef.current;
    await controller.flush();
    try {
      const result = await runProblem(kind, problem, source, setPanel);
      // One submission = one Idempotency-Key: a retry can never record the attempt twice.
      const attemptKey = newIdempotencyKey();
      const attempt = {
        problem_id: problem.id,
        mode: kind,
        language: "python" as const,
        code: source,
        verdict: result.verdict,
        passed: result.passed,
        total: result.total,
        elapsed_ms: elapsedRef.current,
        runtime_ms: result.elapsed_ms,
        occurred_at: nowIso(),
      };
      const send = () =>
        postAttempt(attempt, attemptKey)
          .then(() => {
            if (kind === "submit" && result.verdict === "AC") setSolved(true); // only after a 2xx
          })
          .catch(() =>
            notify("Chưa lưu được kết quả lên server", {
              kind: "error",
              action: { label: "Thử lại", run: () => void send() },
            }),
          );
      void send();
    } catch (error) {
      setPanel(null);
      notify(
        error instanceof ApiError && error.isNetwork
          ? "Cần server để Submit"
          : `Không chạy được: ${(error as Error).message}`,
        { kind: "error" },
      );
    } finally {
      setRunning(false);
    }
  };

  const run = () => void execute("run");
  const submit = () => void execute("submit");

  const takeHint = async () => {
    try {
      const hint = await openHint(problem.id);
      setHints((list) => (list.length >= hint.level ? list : [...list, hint.hint]));
    } catch (error) {
      notify(`Không mở được gợi ý: ${(error as Error).message}`, { kind: "error" });
    }
  };

  const loadSolution = async () => {
    setConfirm(null);
    try {
      setSolution(await getSolution(problem.id));
    } catch (error) {
      notify(`Không tải được lời giải: ${(error as Error).message}`, { kind: "error" });
    }
  };

  const reset = () => {
    setConfirm(null);
    codeRef.current = problem.starter;
    setCode(problem.starter);
    controller.update(problem.starter, 0, elapsedRef.current);
  };

  const left = (
    <article lang={lang}>
      <div className="crumbs">
        <Link to="/">◄ Bài tập</Link>
        <span>›</span>
        <strong>{problem.title}</strong>
        <span className="chip neutral">{DIFF[problem.difficulty] ?? problem.difficulty}</span>
        {solved && <span className="chip AC">✔ Accepted</span>}
        <span style={{ flex: 1 }} />
        <div role="group" aria-label="Ngôn ngữ đề bài">
          <button className="btn sm" aria-pressed={lang === "en"} onClick={() => setLang("en")}>
            EN
          </button>{" "}
          <button className="btn sm" aria-pressed={lang === "vi"} onClick={() => setLang("vi")}>
            VI
          </button>
        </div>
      </div>
      <h1>{lang === "vi" ? problem.title_vi : problem.title}</h1>
      <Markdown md={lang === "vi" ? problem.statement_vi_md : problem.statement_en_md} lang={lang} />
      <h3>Ví dụ</h3>
      {problem.examples.map((ex, i) => (
        <div className="block-card" key={i} style={{ marginBottom: 8 }}>
          <div>
            <strong>Input:</strong> <code>{ex.input}</code>
          </div>
          <div>
            <strong>Output:</strong> <code>{ex.output}</code>
          </div>
          {ex.explain_vi && <div className="muted">{ex.explain_vi}</div>}
        </div>
      ))}
      {problem.constraints.length > 0 && (
        <>
          <h3>Ràng buộc</h3>
          <ul>
            {problem.constraints.map((c, i) => (
              <li key={i}>{c}</li>
            ))}
          </ul>
        </>
      )}
      {hints.length > 0 && (
        <>
          <h3>Gợi ý đã mở</h3>
          <ol>
            {hints.map((h, i) => (
              <li key={i}>
                <Markdown md={h} />
              </li>
            ))}
          </ol>
        </>
      )}
      {solution && (
        <>
          <h3>Lời giải mẫu</h3>
          <pre className="output">{solution.code}</pre>
          {solution.approach_vi && <Markdown md={solution.approach_vi} />}
          {solution.complexity && (
            <p>
              Độ phức tạp: <code>{solution.complexity}</code>
            </p>
          )}
        </>
      )}
    </article>
  );

  const right = (
    <>
      <div className="toolbar">
        <strong>{problem.title}</strong>
        <span className="grow" />
        {showTimer && <span className="status-line">⏱ {formatClock(elapsed)}</span>}
        <button className="btn sm ghost" onClick={() => setShowTimer((v) => !v)}>
          {showTimer ? "Ẩn giờ" : "Hiện giờ"}
        </button>
      </div>
      {preview && lock && <PreviewBanner item={lock} />}
      {code === null ? (
        <div className="skeleton" style={{ height: 240 }} />
      ) : (
        <EditorPanel
          code={code}
          initialCursor={cursor}
          onChange={onChange}
          onRun={run}
          onSubmit={submit}
          onSave={() => {
            void controller.flush();
            notify("Đã lưu");
          }}
          onBlur={() => void controller.flush()}
          onReset={() => setConfirm("reset")}
          running={running}
          runnerLoading={runnerState === "loading"}
          submitDisabledReason={online ? undefined : "Cần server"}
          hintButton={{
            used: hints.length,
            total: problem.hints_total,
            onClick: () => void takeHint(),
            disabled: !online,
          }}
          status={status}
          previewReason={previewReason(lock)}
        />
      )}
      <TestResultPanel state={panel} />
      <div className="toolbar">
        <button
          className="btn sm"
          disabled={!online || preview}
          title={online ? undefined : "Cần server"}
          onClick={() => (solved ? void loadSolution() : setConfirm("solution"))}
        >
          Xem lời giải mẫu ▾
        </button>
        {panel?.verdict === "AC" && panel.kind === "submit" && (
          <span className="chip ok">AC · {panel.elapsed_ms} ms</span>
        )}
      </div>
    </>
  );

  return (
    <>
      <SplitLayout left={left} right={right} leftTab="Đề bài" rightTab="Code" />
      {confirm === "solution" && (
        <ConfirmModal
          title="Xem lời giải mẫu?"
          confirmLabel="Vẫn xem"
          onCancel={() => setConfirm(null)}
          onConfirm={() => void loadSolution()}
        >
          <p>
            Xem lời giải sẽ khiến bài này không còn tính &quot;clean&quot; và không thể làm bằng
            chứng điểm 2/3. Xem?
          </p>
        </ConfirmModal>
      )}
      {confirm === "reset" && (
        <ConfirmModal
          title="Reset về starter?"
          confirmLabel="Reset"
          onCancel={() => setConfirm(null)}
          onConfirm={reset}
        >
          <p>Code hiện tại sẽ bị thay bằng khung code ban đầu.</p>
        </ConfirmModal>
      )}
    </>
  );
}
