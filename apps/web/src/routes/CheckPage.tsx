// Mastery check / Test out (UI_SPEC S8, docs/API_M2A.md). Focus mode: no top nav (see App.tsx).
// The session lives on the server, so reloading `/check/:id` resumes it (POST start -> resumed).
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Link, useNavigate, useParams, useSearchParams } from "react-router-dom";
import { ConceptStep, LockedCard, OutcomeCard, ReadCodeStep, ResultBanner, Stepper } from "../components/CheckParts";
import { EditorPanel, formatClock } from "../components/EditorPanel";
import { Markdown } from "../components/Markdown";
import { ConfirmModal } from "../components/Modal";
import { SplitLayout } from "../components/SplitLayout";
import { TestResultPanel, type PanelState } from "../components/TestResultPanel";
import { useToast } from "../components/Toast";
import {
  answerCheck,
  ApiError,
  checkHeartbeat,
  getProblem,
  newIdempotencyKey,
  openHint,
  putResume,
  startCheck,
  type CheckAnswerBody,
  type CheckContext,
  type CheckOutcome,
  type CheckScore,
  type CheckSession,
  type CheckStep,
  type CheckStepResult,
  type Problem,
} from "../lib/api";
import { LEVEL_TEXT, retryLock, timebox } from "../lib/checkFlow";
import { lsGet, lsSet, useAsync, useOnline, usePageExit, useRunnerState } from "../lib/hooks";
import { idbStore } from "../lib/idb";
import { ResumeReporter } from "../lib/resumeReporter";
import { runProblem } from "../lib/runProblem";

const HEARTBEAT_MS = 30_000;

type Phase =
  | { kind: "loading" }
  | { kind: "error"; error: Error }
  | { kind: "locked"; retryAfter: string; level?: number }
  | { kind: "passed" }
  | { kind: "expired" }
  | { kind: "running" };

export default function CheckPage() {
  const { subtopicId } = useParams();
  const [search] = useSearchParams();
  const context: CheckContext = search.get("ctx") === "test_out" ? "test_out" : "mastery";
  return <CheckRunner key={`${subtopicId}:${context}`} subtopicId={subtopicId!} context={context} />;
}

function CheckRunner({ subtopicId, context }: { subtopicId: string; context: CheckContext }) {
  const notify = useToast();
  const navigate = useNavigate();
  const [phase, setPhase] = useState<Phase>({ kind: "loading" });
  const [session, setSession] = useState<CheckSession | null>(null);
  const [step, setStep] = useState<CheckStep | null>(null);
  const [results, setResults] = useState<CheckStepResult[]>([]);
  const [last, setLast] = useState<CheckStepResult | null>(null);
  const [pendingNext, setPendingNext] = useState<CheckStep | null>(null);
  const [outcome, setOutcome] = useState<CheckOutcome | null>(null);
  const [score, setScore] = useState<CheckScore | undefined>();
  const [busy, setBusy] = useState(false);
  const [confirm, setConfirm] = useState<"exit" | "giveup" | null>(null);
  const [reload, setReload] = useState(0);
  const [itemElapsed, setItemElapsed] = useState(0);
  const itemRef = useRef(0);
  const sessionRef = useRef(0);
  const committing = useRef(false);
  const reporter = useMemo(() => new ResumeReporter(putResume, idbStore("resume")), []);

  // Start, or resume the in-progress session (the server decides).
  useEffect(() => {
    let alive = true;
    startCheck(subtopicId, context)
      .then((s) => {
        if (!alive) return;
        setSession(s);
        setStep(s.step);
        setResults(s.results);
        setLast(null);
        setPendingNext(null);
        // Per-item elapsed restarts on reload: the API returns only session-level time. Client time is
        // advisory (the server trusts body.elapsed_ms today; authoritative timing is deferred to M3
        // offline work), so a reload can reset the 1.5x "clean" clock.
        itemRef.current = 0;
        sessionRef.current = s.elapsed_ms;
        setItemElapsed(0);
        setPhase({ kind: "running" });
      })
      .catch((error: Error) => {
        if (!alive) return;
        const lock = retryLock(error);
        if (lock) setPhase({ kind: "locked", retryAfter: lock.retryAfter, level: lock.level });
        else if (error instanceof ApiError && error.code === "check_already_passed") setPhase({ kind: "passed" });
        else setPhase({ kind: "error", error });
      });
    return () => {
      alive = false;
    };
  }, [subtopicId, context, reload]);

  const finished = outcome !== null;
  const active = phase.kind === "running" && step !== null && last === null && !finished;

  // Active time on the item / session: only while the item is on screen and the tab visible.
  useEffect(() => {
    if (!active) return;
    const timer = setInterval(() => {
      if (document.visibilityState !== "visible") return;
      itemRef.current += 1000;
      sessionRef.current += 1000;
      setItemElapsed(itemRef.current);
    }, 1000);
    return () => clearInterval(timer);
  }, [active]);

  // Keep the session alive (24 h idle clock) and store the absolute elapsed time.
  const sessionId = session?.session_id;
  useEffect(() => {
    if (sessionId === undefined || phase.kind !== "running" || finished) return;
    const beat = () =>
      void checkHeartbeat(sessionId, sessionRef.current).catch((error: unknown) => {
        if (error instanceof ApiError && error.code === "check_session_expired") setPhase({ kind: "expired" });
      });
    const timer = setInterval(beat, HEARTBEAT_MS);
    return () => clearInterval(timer);
  }, [sessionId, phase.kind, finished]);

  // Resume pointer (mode "check"): the server resumes from the session, the route is enough.
  useEffect(() => {
    if (!step || finished) return;
    reporter.report({
      mode: "check",
      route: `/check/${subtopicId}${context === "test_out" ? "?ctx=test_out" : ""}`,
      ref: { subtopic_id: subtopicId, session_id: sessionId, item_id: step.item_id },
    });
  }, [reporter, step, finished, subtopicId, context, sessionId]);
  const flush = useCallback((keepalive: boolean) => void reporter.flush(keepalive), [reporter]);
  usePageExit(flush);
  useEffect(() => () => flush(false), [flush]);

  const commit = async (body: CheckAnswerBody): Promise<boolean> => {
    if (!session || !step || committing.current) return false;
    committing.current = true;
    setBusy(true);
    const key = newIdempotencyKey(); // one answer = one key
    try {
      const res = await answerCheck(
        subtopicId,
        {
          session_id: session.session_id,
          item_id: step.item_id,
          elapsed_ms: itemRef.current,
          session_elapsed_ms: sessionRef.current,
          ...body,
        },
        key,
      );
      setLast(res.result);
      setScore(res.score);
      if (res.finished) setOutcome(res.outcome);
      else setPendingNext(res.next);
      return true;
    } catch (error) {
      const code = error instanceof ApiError ? error.code : "";
      if (code === "check_session_expired") setPhase({ kind: "expired" });
      else if (["check_item_answered", "check_wrong_item", "check_session_done"].includes(code)) {
        notify("Phiên đã thay đổi ở nơi khác, đang tải lại…", { kind: "error" });
        setReload((n) => n + 1);
      } else {
        notify(`Chưa gửi được kết quả: ${(error as Error).message}`, { kind: "error" });
      }
      return false;
    } finally {
      committing.current = false;
      setBusy(false);
    }
  };

  const next = () => {
    if (!pendingNext || !last) return;
    setResults((list) => [...list, last]);
    setStep(pendingNext);
    setPendingNext(null);
    setLast(null);
    itemRef.current = 0;
    setItemElapsed(0);
  };

  if (phase.kind === "loading") {
    return (
      <div className="page" aria-busy="true">
        <div className="skeleton" style={{ width: "50%" }} />
        <div className="skeleton" style={{ width: "90%" }} />
      </div>
    );
  }
  if (phase.kind === "locked") {
    return (
      <div className="page check-page">
        <LockedCard subtopicId={subtopicId} retryAfter={phase.retryAfter} level={phase.level} />
      </div>
    );
  }
  if (phase.kind === "passed") {
    return (
      <div className="page check-page">
        <section className="card" role="status">
          <h1>Đã hoàn thành kiểm tra</h1>
          <p>Bạn đã vượt qua toàn bộ các mức kiểm tra của mục này.</p>
          <Link className="btn primary" to={`/s/${subtopicId}`}>
            Về bài học
          </Link>
        </section>
      </div>
    );
  }
  if (phase.kind === "expired") {
    return (
      <div className="page check-page">
        <section className="card" role="alert">
          <h1>Phiên kiểm tra đã hết hạn</h1>
          <p>Phiên không hoạt động quá 24 giờ nên đã đóng. Việc này không tính là trượt.</p>
          <button className="btn primary" onClick={() => setReload((n) => n + 1)}>
            Bắt đầu lại
          </button>{" "}
          <Link className="btn" to={`/s/${subtopicId}`}>
            Về bài học
          </Link>
        </section>
      </div>
    );
  }
  if (phase.kind === "error" || !session || !step) {
    const message = phase.kind === "error" ? phase.error.message : "";
    const notFound = phase.kind === "error" && phase.error instanceof ApiError && phase.error.code === "check_not_found";
    return (
      <div className="page error-block" role="alert">
        <strong>{notFound ? "Mục này chưa có bài kiểm tra" : "Không mở được bài kiểm tra"}</strong>
        <p>{message}</p>
        {!notFound && (
          <button className="btn" onClick={() => setReload((n) => n + 1)}>
            Thử lại
          </button>
        )}{" "}
        <Link className="btn" to={`/s/${subtopicId}`}>
          Về bài học
        </Link>
      </div>
    );
  }

  if (finished && outcome) {
    return (
      <div className="page check-page">
        <OutcomeCard subtopicId={subtopicId} outcome={outcome} score={score} last={last ?? undefined} />
      </div>
    );
  }

  const box = timebox(itemElapsed, step.minutes);
  return (
    <div className="check-page">
      <header className="check-header">
        <strong>
          {session.context === "test_out" ? "Test out" : "Kiểm tra"}: {subtopicId}
        </strong>
        <span>
          {LEVEL_TEXT[step.level] ?? `Mức ${step.level}`} (bước {step.index + 1}/{step.count})
        </span>
        <span className={`check-timer ${box.phase}`} role="timer" aria-label="Thời gian dự kiến">
          ⏱ {formatClock(itemElapsed)} → {box.label}
        </span>
        <span className="grow" />
        {last === null && (
          <button className="btn sm" disabled={busy} onClick={() => setConfirm("giveup")}>
            Không biết
          </button>
        )}
        <button className="btn sm ghost" onClick={() => setConfirm("exit")}>
          Thoát
        </button>
      </header>
      <Stepper step={step} results={results} />
      {box.phase === "over" && last === null && (
        <div className="check-banner warn" role="status">
          Đã quá giờ. Bạn vẫn có thể làm tiếp và nộp; kết quả đúng sẽ không còn được tính là “sạch”.
        </div>
      )}
      {last ? (
        <section className="card" aria-label="Kết quả bước">
          <ResultBanner result={last} />
          <div className="toolbar">
            <button className="btn primary" onClick={next}>
              Tiếp tục
            </button>
          </div>
        </section>
      ) : step.type === "write_code" ? (
        <WriteCodeStep key={step.item_id} session={session} step={step} busy={busy} commit={commit} />
      ) : step.type === "read_code" ? (
        <ReadCodeStep key={step.item_id} step={step} busy={busy} onAnswer={(answer) => void commit({ answer })} />
      ) : (
        <ConceptStep key={step.item_id} step={step} busy={busy} onGrade={(self_grade) => void commit({ self_grade })} />
      )}
      {step.level >= 2 && last === null && (
        <p className="muted check-footnote">
          Trả lời sai ở mức này sẽ chuyển sang câu chẩn đoán mức 1 và khoá làm lại 24 giờ. Chỉ hiện test sai, không hiện
          đáp án chuẩn. “Không biết” không bị khoá.
        </p>
      )}
      {confirm === "exit" && (
        <ConfirmModal
          title="Thoát bài kiểm tra?"
          confirmLabel="Thoát"
          onCancel={() => setConfirm(null)}
          onConfirm={() => navigate(`/s/${subtopicId}`)}
        >
          <p>Phiên được giữ lại 24 giờ; bạn có thể quay lại để làm tiếp từ bước này.</p>
        </ConfirmModal>
      )}
      {confirm === "giveup" && (
        <ConfirmModal
          title="Chọn “Không biết”?"
          confirmLabel="Không biết"
          onCancel={() => setConfirm(null)}
          onConfirm={() => {
            setConfirm(null);
            void commit({ gave_up: true });
          }}
        >
          <p>Bước này tính là bỏ qua (không bị khoá làm lại) và bạn chuyển sang bước tiếp theo.</p>
        </ConfirmModal>
      )}
    </div>
  );
}

function WriteCodeStep(props: {
  session: CheckSession;
  step: CheckStep;
  busy: boolean;
  commit: (body: CheckAnswerBody) => Promise<boolean>;
}) {
  const problem = useAsync(() => getProblem(props.step.problem_id!), [props.step.problem_id]);
  if (problem.loading) {
    return (
      <div className="page" aria-busy="true">
        <div className="skeleton" style={{ width: "60%" }} />
        <div className="skeleton" style={{ height: 200 }} />
      </div>
    );
  }
  if (problem.error || !problem.data) {
    return (
      <div className="error-block" role="alert">
        <strong>Không tải được đề bài</strong>
        <p>{problem.error?.message}</p>
        <button className="btn" onClick={problem.reload}>
          Thử lại
        </button>
      </div>
    );
  }
  return <WriteCodeView {...props} problem={problem.data} />;
}

interface FailedSubmit {
  body: CheckAnswerBody;
}

function WriteCodeView(props: {
  session: CheckSession;
  step: CheckStep;
  problem: Problem;
  busy: boolean;
  commit: (body: CheckAnswerBody) => Promise<boolean>;
}) {
  const { problem, step } = props;
  const notify = useToast();
  const online = useOnline();
  const runnerState = useRunnerState();
  const draftKey = `prep:check:${props.session.session_id}:${step.item_id}`;
  const [code, setCode] = useState(() => lsGet(draftKey) ?? problem.starter);
  const [panel, setPanel] = useState<PanelState | null>(null);
  const [running, setRunning] = useState(false);
  const [hints, setHints] = useState<string[]>(problem.hints_opened);
  const [failed, setFailed] = useState<FailedSubmit | null>(null);
  const [confirmReset, setConfirmReset] = useState(false);
  const codeRef = useRef(code);

  const onChange = useCallback(
    (next: string) => {
      codeRef.current = next;
      setCode(next);
      setFailed(null);
      lsSet(draftKey, next);
    },
    [draftKey],
  );

  const execute = async (kind: "run" | "submit") => {
    if (running || props.busy) return;
    setRunning(true);
    if (kind === "submit") setFailed(null); // Run keeps a pending "Chốt kết quả" option
    const source = codeRef.current;
    try {
      const result = await runProblem(kind, problem, source, setPanel);
      if (kind === "submit") {
        const body: CheckAnswerBody = {
          code: source,
          language: "python",
          verdict: result.verdict,
          passed_tests: result.passed,
          total: result.total,
          runtime_ms: result.elapsed_ms,
        };
        // AC is sent at once; anything else waits for an explicit "Chốt kết quả" (a wrong answer is final).
        if (result.verdict === "AC") await props.commit(body);
        else setFailed({ body });
      }
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

  const takeHint = async () => {
    try {
      const hint = await openHint(problem.id);
      setHints((list) => (list.length >= hint.level ? list : [...list, hint.hint]));
    } catch (error) {
      notify(`Không mở được gợi ý: ${(error as Error).message}`, { kind: "error" });
    }
  };

  const left = (
    <article>
      <h1>{problem.title_vi || problem.title}</h1>
      <Markdown md={step.prompt_md} />
      <Markdown md={problem.statement_en_md} lang="en" />
      {problem.statement_vi_md && <Markdown md={problem.statement_vi_md} lang="vi" />}
      <h3>Ví dụ</h3>
      {problem.examples.map((ex, i) => (
        <div className="block-card" key={i} style={{ marginBottom: 8 }}>
          <div>
            <strong>Input:</strong> <code>{ex.input}</code>
          </div>
          <div>
            <strong>Output:</strong> <code>{ex.output}</code>
          </div>
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
          {hints.length > 1 && (
            <p className="muted">Dùng nhiều hơn 1 gợi ý thì đáp án đúng không còn tính là “sạch”.</p>
          )}
        </>
      )}
    </article>
  );

  const right = (
    <>
      <EditorPanel
        code={code}
        onChange={onChange}
        onRun={() => void execute("run")}
        onSubmit={() => void execute("submit")}
        onReset={() => setConfirmReset(true)}
        running={running || props.busy}
        runnerLoading={runnerState === "loading"}
        submitDisabledReason={online ? undefined : "Cần server"}
        hintButton={{
          used: hints.length,
          total: problem.hints_total,
          onClick: () => void takeHint(),
          disabled: !online,
        }}
        status={{ state: "idle" }}
      />
      <TestResultPanel state={panel} />
      {failed && (
        <div className="check-banner bad" role="alert">
          <strong>Chưa qua hết test ẩn.</strong>
          <div>Bạn có thể sửa code rồi Submit lại, hoặc chốt kết quả hiện tại (tính là chưa đúng).</div>
          <div className="toolbar">
            <button className="btn sm" disabled={props.busy} onClick={() => void props.commit(failed.body)}>
              Chốt kết quả này
            </button>
          </div>
        </div>
      )}
      {confirmReset && (
        <ConfirmModal
          title="Reset về starter?"
          confirmLabel="Reset"
          onCancel={() => setConfirmReset(false)}
          onConfirm={() => {
            setConfirmReset(false);
            onChange(problem.starter);
          }}
        >
          <p>Code hiện tại sẽ bị thay bằng khung code ban đầu.</p>
        </ConfirmModal>
      )}
    </>
  );

  return <SplitLayout left={left} right={right} leftTab="Đề bài" rightTab="Code" />;
}
