import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { SplitLayout } from "../components/SplitLayout";
import { useToast } from "../components/Toast";
import {
  completeLesson,
  getLesson,
  getNext,
  getResume,
  pickNextSubtopic,
  newLessonRun,
  putResume,
  newIdempotencyKey,
  nowIso,
  type Lesson,
  type LessonCompleteResult,
  type ResumeState,
} from "../lib/api";
import { tally } from "../lib/grade";
import { PreviewBanner } from "../components/PreviewBanner";
import { isLocked, useSubtopicLock } from "../lib/lock";
import { lsGet, lsSet, useAsync, useLayout, usePageExit } from "../lib/hooks";
import { idbStore } from "../lib/idb";
import { ResumeReporter } from "../lib/resumeReporter";
import { BlockView, type BlockContext } from "../lesson/Blocks";
import { SectionPane } from "../lesson/SectionPane";
import { SectionRail } from "../lesson/SectionRail";
import {
  canAdvance,
  deriveSections,
  sectionIndexOfBlock,
  sectionStatus,
  type Section,
} from "../lesson/sections";

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

const viewedKey = (id: string) => `prep:secviewed:${id}`;

function readViewed(id: string): Set<string> {
  try {
    return new Set(JSON.parse(lsGet(viewedKey(id)) ?? "[]") as string[]);
  } catch {
    return new Set();
  }
}

function LessonView({ lesson }: { lesson: Lesson }) {
  const notify = useToast();
  const navigate = useNavigate();
  const layout = useLayout();
  const lock = useSubtopicLock(lesson.id);
  const preview = lock !== null && isLocked(lock);
  const next = useAsync(getNext, []);
  const upNext = next.data?.up_next ?? [];
  // done <=> the server omits it from up_next; unknown while loading / on error.
  // Guard on !preview: a locked subtopic is also omitted from up_next, so without this a
  // preview-mode lesson would falsely read as done.
  const currentDone = next.data && !preview ? !upNext.some((x) => x.id === lesson.id) : false;
  const nextStudy = pickNextSubtopic(upNext, lesson.id);
  const [tab, setTab] = useState<"lesson" | "problems">("lesson");
  const [pane, setPane] = useState<"left" | "right">("left");
  const sections = useMemo(() => deriveSections(lesson.blocks), [lesson.blocks]);
  const [sectionIdx, setSectionIdx] = useState(0);
  const [viewed, setViewed] = useState<Set<string>>(() => readViewed(lesson.id));
  const [skipped, setSkipped] = useState<Set<string>>(new Set());
  const [tocOpen, setTocOpen] = useState<boolean>(() => {
    try {
      const v = lsGet("prep:toc:open");
      return v === null ? layout === "split" : v === "1";
    } catch {
      return true;
    }
  });
  const toggleToc = () => {
    const next = !tocOpen;
    setTocOpen(next);
    lsSet("prep:toc:open", next ? "1" : "0");
  };
  const [runNo, setRunNo] = useState(lesson.run_no);
  const [results, setResults] = useState<Record<string, boolean>>(() =>
    Object.fromEntries(Object.entries(lesson.answers).map(([id, a]) => [id, a.correct])),
  );
  const [active, setActive] = useState<string | null>(null);
  const [done, setDone] = useState<Set<string>>(() => readDone(lesson.id));
  const [completing, setCompleting] = useState(false);
  const [outcome, setOutcome] = useState<LessonCompleteResult | null>(null);
  const [completed, setCompleted] = useState(lesson.completed);
  const topRef = useRef<HTMLDivElement | null>(null);
  const completeKey = useRef(newIdempotencyKey());

  const reporter = useMemo(() => new ResumeReporter(putResume, idbStore<ResumeState>("resume")), []);
  usePageExit(useCallback((keepalive: boolean) => void reporter.flush(keepalive), [reporter]));
  useEffect(() => () => void reporter.flush(), [reporter]);

  const section: Section = sections[Math.min(sectionIdx, sections.length - 1)];
  const isLast = sectionIdx >= sections.length - 1;

  const markViewed = useCallback(
    (sectionId: string) => {
      setViewed((previous) => {
        if (previous.has(sectionId)) return previous;
        const next = new Set(previous).add(sectionId);
        lsSet(viewedKey(lesson.id), JSON.stringify([...next]));
        return next;
      });
    },
    [lesson.id],
  );

  // arriving on a section counts as visiting it (so the last section counts too)
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- persists to localStorage; idempotent
    markViewed(sections[Math.min(sectionIdx, sections.length - 1)].id);
  }, [sectionIdx, sections, markViewed]);

  const goTo = useCallback(
    (index: number, scroll = true) => {
      const clamped = Math.max(0, Math.min(sections.length - 1, index));
      if (clamped !== sectionIdx) {
        markViewed(sections[sectionIdx].id); // leaving counts as viewed
        setPane("left"); // never auto-switch to the exercise tab on section change
      }
      setSectionIdx(clamped);
      if (scroll) topRef.current?.scrollIntoView?.({ block: "start", behavior: "smooth" });
    },
    [sections, sectionIdx, markViewed],
  );

  // Restore position: newest of IndexedDB and GET /resume for this lesson (block id -> its section).
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
      const index = sectionIndexOfBlock(sections, mine?.ref.block_id as string | undefined);
      if (alive && index > 0) setSectionIdx(index);
    })();
    return () => {
      alive = false;
    };
  }, [lesson.id, sections]);

  useEffect(() => {
    reporter.report({
      mode: "lesson",
      route: `/s/${lesson.id}`,
      ref: { subtopic_id: lesson.id, block_id: section.id, tab },
    });
  }, [reporter, lesson.id, section.id, tab]);

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (!event.altKey) return;
      if (event.key === "ArrowRight") {
        event.preventDefault();
        goTo(sectionIdx + 1);
      } else if (event.key === "ArrowLeft") {
        event.preventDefault();
        goTo(sectionIdx - 1);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [sectionIdx, goTo]);

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

  const exercisesInSection = section.blocks.filter((b) => b.type === "code_exercise");
  const exercise =
    exercisesInSection.find((b) => b.id === active && b.type === "code_exercise") ?? section.exercise;
  const status = (s: Section) => sectionStatus(s, { visited: viewed, done, results, skipped });
  const sectionDone = (s: Section) => status(s) === "done";
  const curStatus = status(section);
  const doneCount = sections.filter((s) => status(s) === "done").length;
  const visitedCount = sections.filter((s) => viewed.has(s.id)).length;
  const nextHint =
    curStatus !== "todo" || isLast
      ? ""
      : section.kind === "quiz"
        ? "Trả lời hết câu hỏi để mở phần sau"
        : section.kind === "code"
          ? "Giải bài tập (hoặc Bỏ qua) để tiếp"
          : "";
  const lastHint = currentDone
    ? "Chưa có mục tiếp theo để gợi ý — về Map để chọn"
    : "Làm Kiểm tra đạt điểm 2 để mở mục sau";
  const skipAndNext = () => {
    setSkipped((prev) => new Set(prev).add(section.id));
    goTo(sectionIdx + 1);
  };
  const ctx: BlockContext = {
    subtopicId: lesson.id,
    runNo,
    known: runNo === lesson.run_no ? lesson.answers : {},
    onAnswered,
    activeExercise: exercise?.id ?? null,
    doneExercises: done,
    onOpenExercise: (id) => {
      setActive(id);
      setPane("right");
    },
    canEdit: layout !== "narrow" && !preview,
    showOpen: layout === "tabs" || exercisesInSection.length > 1,
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
  const showWrong = (id: string) => {
    const i = sectionIndexOfBlock(sections, id);
    if (i >= 0) {
      goTo(i, false);
      setTimeout(() => document.getElementById(`block-${id}`)?.scrollIntoView?.({ block: "start" }), 0);
    }
  };

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
        <button role="tab" aria-selected={false} onClick={() => navigate(`/check/${lesson.id}`)}>
          Kiểm tra
        </button>
        <Link
          className="btn sm ghost"
          to={`/check/${lesson.id}?ctx=test_out`}
          title="Đã biết rồi? Làm bài kiểm tra để bỏ qua mục này"
        >
          Test out
        </Link>
      </div>
      {preview && lock && <PreviewBanner item={lock} />}
      {tab === "problems" ? (
        <ProblemList lesson={lesson} />
      ) : (
        <div className="lesson">
          <div ref={topRef} />
          <h1>{lesson.title_vi}</h1>
          {sectionIdx === 0 && (
            <ul>
              {lesson.objectives_vi.map((o, i) => (
                <li key={i}>{o}</li>
              ))}
            </ul>
          )}
          {sections.length > 1 && (
            <SectionRail
              sections={sections}
              idx={sectionIdx}
              done={sectionDone}
              viewed={viewed}
              onSelect={goTo}
              open={tocOpen}
              onToggle={toggleToc}
              doneCount={doneCount}
            />
          )}
          <fieldset className="preview-fieldset" disabled={preview}>
          {section.title && <h2>{section.title}</h2>}
          {section.title && section.summary && <p className="muted">{section.summary}</p>}
          {section.blocks.map((b) => (
            <div key={b.id} id={`block-${b.id}`} className="block">
              <BlockView block={b} ctx={ctx} />
            </div>
          ))}
          {isLast && (
          <section className="card" aria-label="Hoàn thành bài học">
            {!completed && (
              <button className="btn primary" onClick={() => void complete()} disabled={completing || preview}>
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
                          <a href={`#block-${id}`} onClick={(e) => {
                            e.preventDefault();
                            showWrong(id);
                          }}>
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
            {sections.length > 1 &&
              (visitedCount < sections.length ? (
                <p className="muted">
                  Xem hết {sections.length} phần để mở Kiểm tra (còn {sections.length - visitedCount} phần). Làm
                  Kiểm tra để lên Điểm mục 2/3.
                </p>
              ) : (
                <div style={{ marginTop: 12 }}>
                  {currentDone && nextStudy ? (
                    <>
                      <button className="btn primary" onClick={() => navigate(`/s/${nextStudy.id}`)}>
                        Học mục tiếp theo: {nextStudy.name_vi} →
                      </button>{" "}
                      <button className="btn" onClick={() => navigate(`/check/${lesson.id}`)}>
                        Kiểm tra để lên điểm 2/3 ►
                      </button>
                    </>
                  ) : (
                    <button className="btn primary" onClick={() => navigate(`/check/${lesson.id}`)}>
                      Kiểm tra để lên điểm 2/3 ►
                    </button>
                  )}
                  <p className="muted">
                    Điểm 1 = đọc bài + quiz ≥70%. Điểm 2 = làm Kiểm tra/giải bài sạch. Điểm 3 = nâng cao + ôn giữ
                    ≥7 ngày.
                  </p>
                  {!currentDone && (
                    <p className="muted">Cần đạt điểm 2 (làm Kiểm tra / giải bài code sạch) để mở mục sau.</p>
                  )}
                  <p>
                    <Link to={`/check/${lesson.id}?ctx=test_out`}>Test out</Link> ·{" "}
                    <Link to="/">◄ Chọn mục khác</Link>
                  </p>
                </div>
              ))}
          </section>
          )}
          </fieldset>
          {sections.length > 1 && (
            <>
              <div className="blocknav">
                <button className="btn sm" onClick={() => goTo(sectionIdx - 1)} disabled={sectionIdx === 0}>
                  ◄ Phần trước
                </button>
                <span aria-live="polite">
                  Phần {sectionIdx + 1}/{sections.length} · xong {doneCount}/{sections.length}
                </span>
                {section.exercise && curStatus !== "done" && !isLast && (
                  <button className="btn sm ghost" onClick={skipAndNext} title="Bỏ qua bài tập, sang phần sau">
                    Bỏ qua
                  </button>
                )}
                {isLast ? (
                  currentDone && nextStudy ? (
                    <button className="btn sm primary" onClick={() => navigate(`/s/${nextStudy.id}`)}>
                      Mục tiếp theo ►
                    </button>
                  ) : (
                    <>
                      <button className="btn sm" disabled title={lastHint}>
                        Mục tiếp theo ►
                      </button>
                      <span className="muted">{lastHint}</span>
                    </>
                  )
                ) : (
                  <button
                    className={`btn sm${curStatus === "done" ? " primary" : ""}`}
                    onClick={() => goTo(sectionIdx + 1)}
                    disabled={!canAdvance(curStatus)}
                    title={nextHint || undefined}
                  >
                    Phần sau ►
                  </button>
                )}
                {nextHint && <span className="muted">{nextHint}</span>}
              </div>
              <div className="progress" aria-hidden="true">
                <div style={{ width: `${(doneCount / Math.max(1, sections.length)) * 100}%` }} />
              </div>
            </>
          )}
        </div>
      )}
    </>
  );

  const right = (
    <SectionPane
      subtopicId={lesson.id}
      section={section}
      exercise={exercise}
      canEdit={ctx.canEdit}
      results={results}
      practice={lesson.problems.practice}
      onPassed={onPassed}
      onNext={() => goTo(sectionIdx + 1)}
      isLast={isLast}
      canNext={canAdvance(curStatus)}
      nextHint={nextHint}
    />
  );

  return (
    <SplitLayout
      left={left}
      right={right}
      leftTab="Lý thuyết"
      rightTab="Bài tập"
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
