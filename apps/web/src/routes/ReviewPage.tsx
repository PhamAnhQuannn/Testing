// Spaced review (UI_SPEC S9, SPEC 5.4, docs/API_M2A.md "Review"). Self-paced: no cap, no streak, no
// "late" wording. The queue is the whole due list; "Phiên ngắn" is only a suggested subset.
import { useCallback, useEffect, useRef, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { EditorPanel } from "../components/EditorPanel";
import { Markdown } from "../components/Markdown";
import { SplitLayout } from "../components/SplitLayout";
import { TestResultPanel, type PanelState } from "../components/TestResultPanel";
import { useToast } from "../components/Toast";
import {
  ApiError,
  getLesson,
  getProblem,
  getReviewQueue,
  newIdempotencyKey,
  postReviewResult,
  type LessonBlock,
  type Problem,
  type ReviewQueue,
  type ReviewResult,
} from "../lib/api";
import { lsGet, lsSet, useAsync, useLayout, useOnline, useRunnerState } from "../lib/hooks";
import {
  assembleSession,
  backlogText,
  boxLabel,
  dueCountText,
  hasMoreThanPreset,
  lessonBlockOf,
  presetLabel,
  remaining,
  resultView,
  waitingText,
  type SessionCard,
  type SessionMode,
} from "../lib/review";
import { runProblem } from "../lib/runProblem";

export default function ReviewPage() {
  const layout = useLayout();
  const [search] = useSearchParams();
  // No editor on narrow screens (UI_SPEC 3.5), or forced with ?editor=false: boxes 3-5 fall back to recall.
  const editor = layout !== "narrow" && search.get("editor") !== "false";
  const queue = useAsync(() => getReviewQueue(editor), [editor ? 1 : 0]);
  if (queue.loading) {
    return (
      <div className="page" aria-busy="true">
        <div className="skeleton" style={{ width: "40%" }} />
        <div className="skeleton" style={{ width: "80%" }} />
      </div>
    );
  }
  if (queue.error || !queue.data) {
    return (
      <div className="page error-block" role="alert">
        <strong>Không tải được thẻ ôn tập</strong>
        <p>{queue.error?.message}</p>
        <button className="btn" onClick={queue.reload}>
          Thử lại
        </button>
      </div>
    );
  }
  return <ReviewSession queue={queue.data} reload={queue.reload} />;
}

function ReviewSession({ queue, reload }: { queue: ReviewQueue; reload: () => void }) {
  const notify = useToast();
  const [mode, setMode] = useState<SessionMode>("full");
  const [handled, setHandled] = useState<ReadonlySet<string>>(new Set());
  const [skipped, setSkipped] = useState(0);
  const [reviewed, setReviewed] = useState(0);
  const [last, setLast] = useState<ReviewResult | null>(null);
  const [busy, setBusy] = useState(false);
  const committing = useRef(false);
  const keyRef = useRef<{ id: string; key: string } | null>(null);

  const session = assembleSession(queue, mode);
  const pending = remaining(session, handled);
  const current = pending[0] ?? null;

  const submit = useCallback(
    async (sc: SessionCard, success: boolean) => {
      if (committing.current) return;
      committing.current = true;
      setBusy(true);
      // One answer = one key; a retry after a network error reuses it.
      const id = `${sc.card.subtopic_id}:${sc.item.ref}:${success}`;
      if (keyRef.current?.id !== id) keyRef.current = { id, key: newIdempotencyKey() };
      try {
        const res = await postReviewResult(
          sc.card.subtopic_id,
          { success, item_ref: sc.item.ref, item_kind: sc.item.kind },
          keyRef.current.key,
        );
        keyRef.current = null;
        setLast(res);
        setReviewed((n) => n + 1);
        setHandled((set) => new Set(set).add(sc.card.subtopic_id));
      } catch (error) {
        if (error instanceof ApiError && error.code === "card_not_due") {
          // Stale queue (answered elsewhere): not an error, just refresh.
          keyRef.current = null;
          notify("Thẻ này vừa được cập nhật ở nơi khác, đang làm mới danh sách…");
          reload();
        } else {
          notify(`Chưa ghi được kết quả: ${(error as Error).message}`, { kind: "error" });
        }
      } finally {
        committing.current = false;
        setBusy(false);
      }
    },
    [notify, reload],
  );

  const skip = (sc: SessionCard) => {
    setSkipped((n) => n + 1);
    setHandled((set) => new Set(set).add(sc.card.subtopic_id));
  };

  return (
    <div className="page review-page">
      <ReviewTop
        queue={queue}
        mode={mode}
        onMode={setMode}
        reviewed={reviewed}
        showPreset={reviewed === 0 && skipped === 0}
      />
      {last ? (
        <ResultCard result={last} today={queue.today} onNext={() => setLast(null)} hasNext={pending.length > 0} />
      ) : current ? (
        <ReviewStep
          key={`${current.card.subtopic_id}:${current.item.ref}`}
          sc={current}
          busy={busy}
          onResult={submit}
          onSkip={skip}
          left={pending.length}
        />
      ) : (
        <ReviewDone queue={queue} mode={mode} reviewed={reviewed} skipped={skipped} onFull={() => setMode("full")} />
      )}
    </div>
  );
}

/** Header: due count, soft backlog banner, optional "Phiên ngắn" preset toggle. */
export function ReviewTop(props: {
  queue: ReviewQueue;
  mode: SessionMode;
  onMode: (mode: SessionMode) => void;
  reviewed: number;
  showPreset: boolean;
}) {
  const { queue } = props;
  return (
    <header>
      <div className="toolbar">
        <h1>Ôn tập</h1>
        <span className="chip neutral" role="status">
          {dueCountText(queue.total_due)}
          {props.reviewed > 0 ? ` · đã ôn ${props.reviewed} thẻ` : ""}
        </span>
        <span className="grow" />
        <Link className="btn sm ghost" to="/">
          Dừng
        </Link>
      </div>
      {queue.backlog && (
        <div className="check-banner" role="note" data-testid="backlog-banner">
          {backlogText(queue.total_due)}
        </div>
      )}
      {props.showPreset && hasMoreThanPreset(queue) && (
        <div className="toolbar" role="group" aria-label="Chọn độ dài phiên">
          <button
            className={`btn sm${props.mode === "short" ? " primary" : ""}`}
            aria-pressed={props.mode === "short"}
            onClick={() => props.onMode("short")}
          >
            Phiên ngắn
          </button>
          <button
            className={`btn sm${props.mode === "full" ? " primary" : ""}`}
            aria-pressed={props.mode === "full"}
            onClick={() => props.onMode("full")}
          >
            Tất cả ({queue.total_due})
          </button>
          <span className="muted">
            {props.mode === "short"
              ? presetLabel(queue)
              : "Gợi ý: Phiên ngắn cho một lượt nhẹ; bạn vẫn ôn được tất cả."}
          </span>
        </div>
      )}
    </header>
  );
}

export function ReviewDone(props: {
  queue: ReviewQueue;
  mode: SessionMode;
  reviewed: number;
  skipped: number;
  onFull: () => void;
}) {
  const more = props.mode === "short" && props.queue.total_due > props.reviewed + props.skipped;
  if (props.queue.total_due === 0) {
    return (
      <section className="card empty" role="status">
        <h2>Hết thẻ đến hạn</h2>
        <p>Hiện chưa có thẻ nào cần ôn. Quay lại sau, hoặc học tiếp một mục mới.</p>
        <Link className="btn primary" to="/">
          Học tiếp
        </Link>
      </section>
    );
  }
  return (
    <section className="card" role="status">
      <h2>{props.mode === "short" ? "Xong phiên ngắn" : "Đã ôn xong lượt này"}</h2>
      <p>
        Đã ôn {props.reviewed} thẻ
        {props.skipped > 0 ? `, bỏ qua ${props.skipped} thẻ (các thẻ này vẫn giữ nguyên hạn)` : ""}.
      </p>
      <div className="toolbar">
        {more && (
          <button className="btn primary" onClick={props.onFull}>
            Ôn tiếp
          </button>
        )}
        <Link className={`btn${more ? "" : " primary"}`} to="/">
          Học tiếp
        </Link>
      </div>
    </section>
  );
}

export function ResultCard(props: { result: ReviewResult; today?: string; onNext: () => void; hasNext: boolean }) {
  const view = resultView(props.result, props.today);
  return (
    <section className="card" role="status" aria-label="Kết quả thẻ">
      <h2>{view.title}</h2>
      <ul>
        {view.lines.map((line) => (
          <li key={line}>{line}</li>
        ))}
      </ul>
      <div className="toolbar">
        <button className="btn primary" onClick={props.onNext}>
          {props.hasNext ? "Thẻ tiếp" : "Xong"}
        </button>
      </div>
    </section>
  );
}

export function CardHeader({ sc, left }: { sc: SessionCard; left: number }) {
  const { card } = sc;
  return (
    <div className="toolbar review-card-head">
      <strong>{card.name_vi}</strong>
      <span className="chip neutral">
        {boxLabel(card.box)} · {sc.item.kind === "code" ? "bài code" : "nhớ nhanh"}
      </span>
      <span className="muted">
        còn {left} thẻ · {waitingText(card.overdue_days)}
      </span>
    </div>
  );
}

const FOOT = "Đúng → lên hộp kế tiếp, lần sau cách xa hơn · Chưa nhớ → về hộp 1, ôn lại sớm. Không có phạt hay streak.";

interface StepProps {
  sc: SessionCard;
  busy: boolean;
  onResult: (sc: SessionCard, success: boolean) => void;
  onSkip: (sc: SessionCard) => void;
}

function ReviewStep(props: StepProps & { left: number }) {
  const { sc } = props;
  return (
    <section aria-label="Thẻ ôn tập">
      <CardHeader sc={sc} left={props.left} />
      {sc.item.kind === "code" ? <CodeStep {...props} /> : <RecallStep {...props} />}
      <p className="muted">{FOOT}</p>
    </section>
  );
}

function RecallStep(props: StepProps) {
  const ref = lessonBlockOf(props.sc.item.ref);
  const lesson = useAsync(() => (ref ? getLesson(ref.subtopicId) : Promise.resolve(null)), [ref?.subtopicId]);
  if (ref && lesson.loading) {
    return (
      <div aria-busy="true">
        <div className="skeleton" style={{ width: "70%" }} />
        <div className="skeleton" style={{ height: 80 }} />
      </div>
    );
  }
  const block = ref ? (lesson.data?.blocks.find((b) => b.id === ref.blockId) ?? null) : null;
  return <RecallView {...props} block={block} />;
}

/** Quick recall: show the prompt, the learner answers in their head and self-grades. */
export function RecallView(props: StepProps & { block: LessonBlock | null }) {
  const { sc, block } = props;
  return (
    <div className="card" aria-label="Câu nhớ nhanh">
      <RecallPrompt block={block} name={sc.card.name_vi} />
      <p className="muted">Tự trả lời trong đầu, rồi tự chấm. Cần xem lại thì mở bài học.</p>
      <div className="toolbar">
        <Link className="btn sm ghost" to={`/s/${sc.card.subtopic_id}`} target="_blank" rel="noopener noreferrer">
          Mở bài học
        </Link>
        <span className="grow" />
        <button className="btn sm" disabled={props.busy} onClick={() => props.onSkip(sc)}>
          Bỏ qua
        </button>
        <button className="btn" disabled={props.busy} onClick={() => props.onResult(sc, false)}>
          Chưa nhớ
        </button>
        <button className="btn primary" disabled={props.busy} onClick={() => props.onResult(sc, true)}>
          Nhớ rồi
        </button>
      </div>
    </div>
  );
}

export function RecallPrompt({ block, name }: { block: LessonBlock | null; name: string }) {
  if (block && (block.type === "quiz_mcq" || block.type === "quiz_fill")) {
    return (
      <>
        <Markdown md={block.prompt_md} />
        {block.type === "quiz_mcq" && (
          <ul>
            {block.options.map((o) => (
              <li key={o.id}>
                <Markdown md={o.text_md} />
              </li>
            ))}
          </ul>
        )}
      </>
    );
  }
  if (block && block.type === "predict_output") {
    return (
      <>
        <p>Dự đoán output của đoạn code sau:</p>
        <pre>
          <code>{block.code}</code>
        </pre>
      </>
    );
  }
  // check:<sid>:<item> refs have no public content endpoint; ask for the key ideas instead.
  return (
    <p>
      Nhớ lại ý chính của <strong>{name}</strong>: khái niệm, khi nào dùng, độ phức tạp và một lỗi hay gặp.
    </p>
  );
}

function CodeStep(props: StepProps) {
  const problem = useAsync(() => getProblem(props.sc.item.ref), [props.sc.item.ref]);
  if (problem.loading) {
    return (
      <div aria-busy="true">
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
        </button>{" "}
        <button className="btn" onClick={() => props.onSkip(props.sc)}>
          Bỏ qua
        </button>
      </div>
    );
  }
  return <CodeView {...props} problem={problem.data} />;
}

function CodeView(props: StepProps & { problem: Problem }) {
  const { problem, sc } = props;
  const notify = useToast();
  const online = useOnline();
  const runnerState = useRunnerState();
  const draftKey = `prep:review:${sc.card.subtopic_id}:${problem.id}`;
  const [code, setCode] = useState(() => lsGet(draftKey) ?? problem.starter);
  const [panel, setPanel] = useState<PanelState | null>(null);
  const [running, setRunning] = useState(false);
  const [failedOnce, setFailedOnce] = useState(false);
  const codeRef = useRef(code);

  const onChange = useCallback(
    (next: string) => {
      codeRef.current = next;
      setCode(next);
      lsSet(draftKey, next);
    },
    [draftKey],
  );

  useEffect(() => {
    codeRef.current = code;
  }, [code]);

  const execute = async (kind: "run" | "submit") => {
    if (running || props.busy) return;
    setRunning(true);
    try {
      const result = await runProblem(kind, problem, codeRef.current, setPanel);
      if (kind === "submit") {
        if (result.verdict === "AC") props.onResult(sc, true);
        else setFailedOnce(true);
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

  const left = (
    <article>
      <h1>{problem.title_vi || problem.title}</h1>
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
    </article>
  );

  const right = (
    <>
      <EditorPanel
        code={code}
        onChange={onChange}
        onRun={() => void execute("run")}
        onSubmit={() => void execute("submit")}
        onReset={() => onChange(problem.starter)}
        running={running || props.busy}
        runnerLoading={runnerState === "loading"}
        submitDisabledReason={online ? undefined : "Cần server"}
        status={{ state: "idle" }}
      />
      <TestResultPanel state={panel} />
      {failedOnce && (
        <div className="check-banner" role="status">
          Chưa qua hết test ẩn. Sửa rồi Submit lại, hoặc ghi là chưa nhớ để thẻ quay lại sớm. Đáp án mẫu không được hiện ở
          đây.
        </div>
      )}
      <div className="toolbar">
        <button className="btn sm" disabled={props.busy} onClick={() => props.onSkip(sc)}>
          Bỏ qua
        </button>
        <button className="btn sm" disabled={props.busy} onClick={() => props.onResult(sc, false)}>
          Chưa làm được
        </button>
      </div>
    </>
  );
  return <SplitLayout left={left} right={right} leftTab="Đề bài" rightTab="Code" />;
}
