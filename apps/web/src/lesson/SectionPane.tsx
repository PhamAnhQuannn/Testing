import { Link } from "react-router-dom";
import { Markdown } from "../components/Markdown";
import { isGraded } from "../lib/grade";
import { ExercisePane } from "./ExercisePane";
import type { CodeExerciseBlock, Section } from "./sections";

/** Right pane, switched on section.kind. Never blank. */
export function SectionPane({
  subtopicId,
  section,
  exercise,
  canEdit,
  results,
  practice,
  onPassed,
  onNext,
  isLast,
}: {
  subtopicId: string;
  section: Section;
  /** The exercise paired with this section (override by explicit open, else section.exercise). */
  exercise?: CodeExerciseBlock;
  canEdit: boolean;
  results: Record<string, boolean>;
  practice: string[];
  onPassed: (blockId: string) => void;
  onNext: () => void;
  isLast: boolean;
}) {
  if (exercise) {
    if (!canEdit) {
      return (
        <div>
          <div className="toolbar">
            <strong>Bài tập: {exercise.entry}()</strong>
          </div>
          <Markdown md={exercise.md} />
          <div className="card muted">Mở trên máy tính (và mở khoá mục này) để viết code.</div>
        </div>
      );
    }
    // keyed: exactly one editor is mounted, and it unmounts on section change
    return <ExercisePane key={exercise.id} subtopicId={subtopicId} block={exercise} onPassed={onPassed} />;
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
          <button className="btn sm" onClick={onNext}>
            Phần sau ►
          </button>
        )}
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
        <button className="btn sm primary" onClick={onNext}>
          Tiếp tục ►
        </button>
      )}
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
