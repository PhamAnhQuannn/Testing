import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { SplitLayout } from "../components/SplitLayout";
import { useToast } from "../components/Toast";
import {
  completeLesson,
  getLesson,
  getResume,
  newLessonRun,
  putResume,
  newIdempotencyKey,
  nowIso,
  type Lesson,
  type LessonCompleteResult,
  type ResumeState,
} from "../lib/api";
import { tally } from "../lib/grade";
import { lsGet, lsSet, useAsync, useLayout, usePageExit } from "../lib/hooks";
import { idbStore } from "../lib/idb";
import { ResumeReporter } from "../lib/resumeReporter";
import { BlockView, type BlockContext } from "../lesson/Blocks";
import { ExercisePane } from "../lesson/ExercisePane";

export default function LessonPage() {
  const { subtopicId } = useParams();
  const lesson = useAsync(() => getLesson(subtopicId!), [subtopicId]);
  if (lesson.loading) {
    return (
      <div className="page" aria-busy="true">
        <div className="skeleton" style={{ width: "40%", height: 28 }} />
        <div className="skeleton" style={{ width: "95%" }} />
        <div className="skeleton" style={{ width: "85%" }} />
        <div className="skeleton" style={{ width: "90%" }} />
      </div>
    );
  }
  if (lesson.error || !lesson.data) {
    return (
      <div className="page error-block" role="alert">
        <strong>Không tải được bài học</strong>
        <p>{lesson.error?.message}</p>
        <button className="btn" onClick={lesson.reload}>
          Thử lại
        </button>
        <p>
          <Link to="/">Về danh sách mục</Link>
        </p>
      </div>
    );
  }
  if (lesson.data.status && lesson.data.status !== "published" && lesson.data.blocks.length === 0) {
    return (
      <div className="page empty">
        <h1>{lesson.data.title_vi}</h1>
        <p>Bài này đang soạn.</p>
        <Link to="/">Về danh sách mục</Link>
      </div>
    );
  }
  return <LessonView key={lesson.data.id} lesson={lesson.data} />;
}

const doneKey = (id: string) => `prep:exdone:${id}`;

function readDone(id: string): Set<string> {
  try {
    return new Set(JSON.parse(lsGet(doneKey(id)) ?? "[]") as string[]);
  } catch {
    return new Set();
  }
}

function LessonView({ lesson }: { lesson: Lesson }) {
  const notify = useToast();
  const layout = useLayout();
  const [tab, setTab] = useState<"lesson" | "problems">("lesson");
  const [pane, setPane] = useState<"left" | "right">("left");
  const [current, setCurrent] = useState(0);
  const [runNo, setRunNo] = useState(lesson.run_no);
  const [results, setResults] = useState<Record<string, boolean>>(() =>
    Object.fromEntries(Object.entries(lesson.answers).map(([id, a]) => [id, a.correct])),
  );
  const [active, setActive] = useState<string | null>(null);
  const [done, setDone] = useState<Set<string>>(() => readDone(lesson.id));
  const [completing, setCompleting] = useState(false);
  const [outcome, setOutcome] = useState<LessonCompleteResult | null>(null);
  const [completed, setCompleted] = useState(lesson.completed);
  const blockEls = useRef<(HTMLDivElement | null)[]>([]);
  const completeKey = useRef(newIdempotencyKey());

  const reporter = useMemo(() => new ResumeReporter(putResume, idbStore<ResumeState>("resume")), []);
  usePageExit(useCallback((keepalive: boolean) => void reporter.flush(keepalive), [reporter]));
  useEffect(() => () => void reporter.flush(), [reporter]);

  const goTo = useCallback(
    (index: number, scroll = true) => {
      const clamped = Math.max(0, Math.min(lesson.blocks.length - 1, index));
      setCurrent(clamped);
      if (scroll) {
        const el = blockEls.current[clamped];
        el?.scrollIntoView({ block: "start", behavior: "smooth" });
        el?.focus({ preventScroll: true });
      }
    },
    [lesson.blocks.length],
  );

  // Restore position: newest of IndexedDB and GET /resume for this lesson.
  useEffect(() => {
    let alive = true;
    (async () => {
      const [server, local] = await Promise.all([
        getResume().catch(() => null),
        idbStore<ResumeState>("resume").get("current").catch(() => undefined),
      ]);
      const mine = [server, local]
        .filter((s): s is ResumeState => Boolean(s) && s!.mode === "lesson" && s!.ref?.subtopic_id === lesson.id)
        .sort((a, b) => Date.parse(b.updated_at) - Date.parse(a.updated_at))[0];
      const blockId = mine?.ref.block_id as string | undefined;
      const index = lesson.blocks.findIndex((b) => b.id === blockId);
      if (alive && index > 0) goTo(index);
    })();
    return () => {
      alive = false;
    };
  }, [lesson, goTo]);

  const block = lesson.blocks[current];
  useEffect(() => {
    if (!block) return;
    reporter.report({
      mode: "lesson",
      route: `/s/${lesson.id}`,
      ref: { subtopic_id: lesson.id, block_id: block.id, tab },
    });
  }, [reporter, lesson.id, block, tab]);

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (!event.altKey) return;
      if (event.key === "ArrowRight") {
        event.preventDefault();
        goTo(current + 1);
      } else if (event.key === "ArrowLeft") {
        event.preventDefault();
        goTo(current - 1);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [current, goTo]);

  const onAnswered = useCallback((blockId: string, correct: boolean) => {
    setResults((r) => ({ ...r, [blockId]: correct }));
  }, []);

  const onPassed = useCallback(
    (blockId: string) => {
      setDone((previous) => {
        if (previous.has(blockId)) return previous;
        const next = new Set(previous).add(blockId);
        lsSet(doneKey(lesson.id), JSON.stringify([...next]));
        return next;
      });
    },
    [lesson.id],
  );

  const exercise = lesson.blocks.find((b) => b.id === active && b.type === "code_exercise");
  const ctx: BlockContext = {
    subtopicId: lesson.id,
    runNo,
    known: runNo === lesson.run_no ? lesson.answers : {},
    onAnswered,
    activeExercise: active,
    doneExercises: done,
    onOpenExercise: (id) => {
      setActive(id);
      setPane("right");
    },
    canEdit: layout !== "narrow",
  };

  const stats = tally(lesson.blocks, results);
  const passRatio = lesson.checkpoint.pass_ratio;

  const complete = async () => {
    setCompleting(true);
    try {
      const result = await completeLesson(
        lesson.id,
        { occurred_at: nowIso() },
        completeKey.current,
      );
      setOutcome(result);
      setCompleted(true);
    } catch (error) {
      notify(`Chưa hoàn thành được: ${(error as Error).message}`, {
        kind: "error",
        action: { label: "Thử lại", run: () => void complete() },
      });
    } finally {
      setCompleting(false);
    }
  };

  const retry = async () => {
    try {
      const { run_no } = await newLessonRun(lesson.id);
      setRunNo(run_no);
      setResults({});
      setOutcome(null);
      setCompleted(false);
      completeKey.current = newIdempotencyKey();
      goTo(0);
    } catch (error) {
      notify(`Không mở được lượt mới: ${(error as Error).message}`, { kind: "error" });
    }
  };

  const quizBest = outcome?.quiz_best ?? stats.ratio;
  const passed = outcome ? (outcome.quiz_passed ?? quizBest >= passRatio) : false;
  const wrongBlocks = stats.wrong;

  const left = (
    <>
      <div className="crumbs">
        <Link to="/">◄ Map</Link>
        <span>›</span>
        <strong>{lesson.title_vi}</strong>
        <span className="muted">
          · ~{lesson.est_minutes} phút · Quiz {stats.correct}/{stats.graded}
        </span>
      </div>
      <div className="tabbar" role="tablist" style={{ padding: 0, marginBottom: 12 }}>
        <button role="tab" aria-selected={tab === "lesson"} onClick={() => setTab("lesson")}>
          Bài học
        </button>
        <button role="tab" aria-selected={tab === "problems"} onClick={() => setTab("problems")}>
          Bài tập
        </button>
        <button role="tab" aria-selected={false} disabled title="Có ở M2">
          Kiểm tra
        </button>
      </div>
      {tab === "problems" ? (
        <ProblemList lesson={lesson} />
      ) : (
        <div className="lesson">
          <h1>{lesson.title_vi}</h1>
          <ul>
            {lesson.objectives_vi.map((o, i) => (
              <li key={i}>{o}</li>
            ))}
          </ul>
          {lesson.blocks.map((b, i) => (
            <div
              key={b.id}
              id={`block-${b.id}`}
              ref={(el) => {
                blockEls.current[i] = el;
              }}
              tabIndex={-1}
              className={`block${i === current ? " current" : ""}`}
              onFocusCapture={() => setCurrent(i)}
              onClick={() => setCurrent(i)}
            >
              <BlockView block={b} ctx={ctx} />
            </div>
          ))}
          <section className="card" aria-label="Hoàn thành bài học">
            {!completed && (
              <button className="btn primary" onClick={() => void complete()} disabled={completing}>
                {completing ? "Đang lưu…" : "Hoàn thành bài học"}
              </button>
            )}
            {outcome && (
              <div role="status" style={{ marginTop: 12 }}>
                {passed ? (
                  <p>
                    <strong className="chip ok">✔ Đạt</strong> Quiz tốt nhất{" "}
                    {Math.round(quizBest * 100)}%.
                    {outcome.score !== undefined && <> Điểm mục: {String(outcome.score)}/3.</>} Thẻ ôn
                    đầu tiên hẹn ngày mai.
                  </p>
                ) : (
                  <>
                    <p>
                      <strong className="chip bad">Chưa đạt</strong> Quiz {Math.round(quizBest * 100)}%
                      (cần {Math.round(passRatio * 100)}%). Quiz cần xem lại:
                    </p>
                    <ul>
                      {wrongBlocks.map((id) => (
                        <li key={id}>
                          <a href={`#block-${id}`} onClick={() => goTo(lesson.blocks.findIndex((b) => b.id === id))}>
                            {id}
                          </a>
                        </li>
                      ))}
                    </ul>
                    <button className="btn" onClick={() => void retry()}>
                      Làm lại lượt
                    </button>
                  </>
                )}
              </div>
            )}
            {completed && !outcome && <p className="muted">Bạn đã hoàn thành bài học này.</p>}
          </section>
          <div className="blocknav">
            <button className="btn sm" onClick={() => goTo(current - 1)} disabled={current === 0}>
              ◄ Block trước
            </button>
            <span aria-live="polite">
              {current + 1}/{lesson.blocks.length}
            </span>
            <button
              className="btn sm"
              onClick={() => goTo(current + 1)}
              disabled={current >= lesson.blocks.length - 1}
            >
              Tiếp ►
            </button>
          </div>
          <div className="progress" aria-hidden="true">
            <div style={{ width: `${((current + 1) / Math.max(1, lesson.blocks.length)) * 100}%` }} />
          </div>
        </div>
      )}
    </>
  );

  const right = exercise && exercise.type === "code_exercise" ? (
    <ExercisePane key={exercise.id} subtopicId={lesson.id} block={exercise} onPassed={onPassed} />
  ) : (
    <div className="empty">
      <p>Chọn &quot;Làm bài này&quot; ở một bài tập trong bài học để nạp code vào đây.</p>
      {lesson.problems.practice.length > 0 && (
        <p>
          Bài luyện chính:{" "}
          {lesson.problems.practice.map((id) => (
            <Link key={id} to={`/p/${id}`}>
              {id}
            </Link>
          ))}
        </p>
      )}
    </div>
  );

  return (
    <SplitLayout
      left={left}
      right={right}
      leftTab="Bài học"
      rightTab="Code"
      activeTab={pane}
      onTabChange={setPane}
    />
  );
}

function ProblemList({ lesson }: { lesson: Lesson }) {
  const all = [...lesson.problems.practice, ...lesson.problems.extra];
  if (all.length === 0) return <div className="empty">Mục này chưa có bài tập.</div>;
  return (
    <ul>
      {lesson.problems.practice.map((id) => (
        <li key={id}>
          <Link to={`/p/${id}`}>{id}</Link> <span className="chip neutral">chính</span>
        </li>
      ))}
      {lesson.problems.extra.map((id) => (
        <li key={id}>
          <Link to={`/p/${id}`}>{id}</Link>
        </li>
      ))}
    </ul>
  );
}
