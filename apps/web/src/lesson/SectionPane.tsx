import { useState } from "react";
import { Link } from "react-router-dom";
import { Markdown } from "../components/Markdown";
import { isGraded } from "../lib/grade";
import { ExercisePane } from "./ExercisePane";
import type { CodeExerciseBlock, LessonExerciseEntry, Section } from "./sections";

/** Label for one exercise in the jump list. */
function exLabel(ex: CodeExerciseBlock): string {
  return ex.entry ? `${ex.entry}()` : ex.id;
}

/**
 * Right-pane navigation above the editor: ◄ "Bài i/N" ► over the CURRENT section's exercises, plus a
 * toggle that opens the whole-lesson exercise list to jump to any exercise or practice problem.
 * Rendered outside the keyed ExercisePane so switching does not lose the open/closed list state.
 */
function ExerciseNav({
  exercises,
  index,
  onPrev,
  onNext,
  allExercises,
  currentId,
  practice,
  extra,
  onJump,
  doneExercises,
}: {
  exercises: CodeExerciseBlock[];
  index: number;
  onPrev: () => void;
  onNext: () => void;
  allExercises: LessonExerciseEntry[];
  currentId?: string;
  practice: string[];
  extra: string[];
  onJump: (sectionIdx: number, exerciseId: string) => void;
  doneExercises: Set<string>;
}) {
  const [open, setOpen] = useState(false);
  const total = exercises.length;
  const hasMany = allExercises.length > 1 || practice.length + extra.length > 0;
  return (
    <div className="exnav">
      <div className="exnav-bar">
        <button
          className="btn sm"
          onClick={onPrev}
          disabled={index <= 0}
          aria-label="Bài tập trước"
          title="Bài tập trước"
        >
          ◄
        </button>
        <span className="exnav-count" aria-live="polite">
          Bài {total > 0 ? Math.min(index + 1, total) : 0}/{total}
        </span>
        <button
          className="btn sm"
          onClick={onNext}
          disabled={index < 0 || index >= total - 1}
          aria-label="Bài tập sau"
          title="Bài tập sau"
        >
          ►
        </button>
        {hasMany && (
          <button
            className="btn sm ghost"
            aria-expanded={open}
            onClick={() => setOpen((v) => !v)}
            title="Danh sách bài tập của cả bài"
          >
            ☰ Danh sách bài tập
          </button>
        )}
      </div>
      {open && (
        <div className="exnav-list card">
          {allExercises.length > 0 && (
            <ol className="exnav-exercises">
              {allExercises.map((e) => {
                const isCurrent = e.exercise.id === currentId;
                const isDone = doneExercises.has(e.exercise.id);
                return (
                  <li key={e.exercise.id}>
                    <button
                      className={`exnav-item${isCurrent ? " current" : ""}`}
                      aria-current={isCurrent || undefined}
                      onClick={() => {
                        onJump(e.sectionIdx, e.exercise.id);
                        setOpen(false);
                      }}
                    >
                      <span aria-hidden="true">{isDone ? "✔ " : isCurrent ? "▶ " : ""}</span>
                      {exLabel(e.exercise)}
                      {e.sectionTitle && <span className="muted"> · {e.sectionTitle}</span>}
                    </button>
                  </li>
                );
              })}
            </ol>
          )}
          {(practice.length > 0 || extra.length > 0) && (
            <div className="exnav-problems">
              <strong>Bài luyện (trang riêng)</strong>
              <ul>
                {practice.map((id) => (
                  <li key={id}>
                    <Link to={`/p/${id}`}>{id}</Link> <span className="chip neutral">chính</span>
                  </li>
                ))}
                {extra.map((id) => (
                  <li key={id}>
                    <Link to={`/p/${id}`}>{id}</Link>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

/** Right pane, switched on section.kind. Never blank. */
export function SectionPane({
  subtopicId,
  section,
  exercise,
  canEdit,
  results,
  practice,
  extra = [],
  exercises = [],
  exIndex = -1,
  allExercises = [],
  doneExercises,
  onPrevExercise,
  onNextExercise,
  onJump,
  onPassed,
  onNext,
  isLast,
  canNext = true,
  nextHint = "",
}: {
  subtopicId: string;
  section: Section;
  /** The exercise paired with this section (override by explicit open, else section.exercise). */
  exercise?: CodeExerciseBlock;
  canEdit: boolean;
  results: Record<string, boolean>;
  practice: string[];
  extra?: string[];
  /** The current section's exercises, in order (for the ◄ i/N ► counter). */
  exercises?: CodeExerciseBlock[];
  exIndex?: number;
  /** Every exercise in the whole lesson (for the jump list). */
  allExercises?: LessonExerciseEntry[];
  doneExercises?: Set<string>;
  onPrevExercise?: () => void;
  onNextExercise?: () => void;
  onJump?: (sectionIdx: number, exerciseId: string) => void;
  onPassed: (blockId: string) => void;
  onNext: () => void;
  isLast: boolean;
  canNext?: boolean;
  nextHint?: string;
}) {
  if (exercise) {
    const nav =
      onPrevExercise && onNextExercise && onJump ? (
        <ExerciseNav
          exercises={exercises}
          index={exIndex}
          onPrev={onPrevExercise}
          onNext={onNextExercise}
          allExercises={allExercises}
          currentId={exercise.id}
          practice={practice}
          extra={extra}
          onJump={onJump}
          doneExercises={doneExercises ?? new Set()}
        />
      ) : null;
    if (!canEdit) {
      return (
        <div>
          {nav}
          <div className="toolbar">
            <strong>Bài tập: {exercise.entry}()</strong>
          </div>
          <Markdown md={exercise.md} />
          <div className="card muted">Mở trên máy tính (và mở khoá mục này) để viết code.</div>
        </div>
      );
    }
    // keyed: exactly one editor is mounted, and it unmounts on exercise change
    return (
      <div>
        {nav}
        <ExercisePane key={exercise.id} subtopicId={subtopicId} block={exercise} onPassed={onPassed} />
      </div>
    );
  }

  if (section.kind === "quiz") {
    const graded = section.blocks.filter(isGraded);
    const answered = graded.filter((b) => b.id in results).length;
    return (
      <div className="card">
        <strong>Câu hỏi của phần này</strong>
        <p>
          Trả lời các câu hỏi ở khung bên trái: {answered}/{graded.length} câu đã có kết quả.
        </p>
        {!isLast && (
          <button className="btn sm" onClick={onNext} disabled={!canNext}>
            Phần sau ►
          </button>
        )}
        {!isLast && !canNext && nextHint && <p className="muted">{nextHint}</p>}
      </div>
    );
  }

  const callouts = section.blocks.filter((b) => b.type === "callout");
  const last = callouts[callouts.length - 1];
  return (
    <div className="card">
      <strong>Ghi nhớ</strong>
      {section.summary ? (
        <Markdown md={section.summary} />
      ) : last && last.type === "callout" ? (
        <Markdown md={last.md} />
      ) : (
        <p className="muted">Đọc xong phần này thì tiếp tục.</p>
      )}
      {!isLast && (
        <button className="btn sm primary" onClick={onNext} disabled={!canNext}>
          Tiếp tục ►
        </button>
      )}
      {!isLast && !canNext && nextHint && <p className="muted">{nextHint}</p>}
      {practice.length > 0 && (
        <p>
          Bài luyện chính:{" "}
          {practice.map((id) => (
            <Link key={id} to={`/p/${id}`}>
              {id}
            </Link>
          ))}
        </p>
      )}
    </div>
  );
}
