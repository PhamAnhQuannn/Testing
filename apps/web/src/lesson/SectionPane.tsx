import { useState } from "react";
import { Link } from "react-router-dom";
import { Markdown } from "../components/Markdown";
import { BlockView, type BlockContext } from "./Blocks";
import { ExercisePane } from "./ExercisePane";
import type { InteractiveBlock, LessonInteractiveEntry, Section } from "./sections";

const TYPE_LABEL: Record<InteractiveBlock["type"], string> = {
  code_exercise: "Code",
  quiz_mcq: "Trắc nghiệm",
  quiz_fill: "Điền chỗ trống",
  predict_output: "Đoán output",
};

/** Short label for one item in the jump list: the entry for code, else the item type. */
function itemLabel(block: InteractiveBlock): string {
  if (block.type === "code_exercise") return block.entry ? `${block.entry}()` : "Bài code";
  return TYPE_LABEL[block.type];
}

/** Whether an interactive item is "done" (code passed, or a quiz/predict answered). */
function itemDone(block: InteractiveBlock, done: Set<string>, results: Record<string, boolean>): boolean {
  return block.type === "code_exercise" ? done.has(block.id) : block.id in results;
}

/**
 * Right-pane navigation above the active item: ◄ "Câu i/N" ► over the CURRENT section's interactive
 * items, plus a toggle that opens the whole-lesson list to jump to any item or practice problem.
 * Rendered outside the keyed item so switching never loses the open/closed list state.
 */
function ExerciseNav({
  interactive,
  index,
  onPrev,
  onNext,
  allInteractive,
  currentId,
  practice,
  extra,
  onJump,
  done,
  results,
}: {
  interactive: InteractiveBlock[];
  index: number;
  onPrev: () => void;
  onNext: () => void;
  allInteractive: LessonInteractiveEntry[];
  currentId?: string;
  practice: string[];
  extra: string[];
  onJump: (sectionIdx: number, blockId: string) => void;
  done: Set<string>;
  results: Record<string, boolean>;
}) {
  const [open, setOpen] = useState(false);
  const total = interactive.length;
  const hasMany = allInteractive.length > 1 || practice.length + extra.length > 0;
  return (
    <div className="exnav">
      <div className="exnav-bar">
        <button
          className="btn sm"
          onClick={onPrev}
          disabled={index <= 0}
          aria-label="Câu trước"
          title="Câu trước"
        >
          ◄
        </button>
        <span className="exnav-count" aria-live="polite">
          Câu {total > 0 ? Math.min(index + 1, total) : 0}/{total}
        </span>
        <button
          className="btn sm"
          onClick={onNext}
          disabled={index < 0 || index >= total - 1}
          aria-label="Câu sau"
          title="Câu sau"
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
          {allInteractive.length > 0 && (
            <ol className="exnav-exercises">
              {allInteractive.map((e) => {
                const isCurrent = e.block.id === currentId;
                const isDone = itemDone(e.block, done, results);
                return (
                  <li key={e.block.id}>
                    <button
                      className={`exnav-item${isCurrent ? " current" : ""}`}
                      data-block-id={e.block.id}
                      aria-current={isCurrent || undefined}
                      onClick={() => {
                        onJump(e.sectionIdx, e.block.id);
                        setOpen(false);
                      }}
                    >
                      <span aria-hidden="true">{isDone ? "✔ " : isCurrent ? "▶ " : ""}</span>
                      <span className="muted">{e.ordinal}.</span> {itemLabel(e.block)}
                      <span className="chip neutral">{TYPE_LABEL[e.block.type]}</span>
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

/** Render the active interactive item: the keyed editor for code, else the quiz/predict block. */
function CurrentItem({
  block,
  subtopicId,
  canEdit,
  onPassed,
  ctx,
}: {
  block: InteractiveBlock;
  subtopicId: string;
  canEdit: boolean;
  onPassed: (blockId: string) => void;
  ctx: BlockContext;
}) {
  if (block.type === "code_exercise") {
    if (!canEdit) {
      return (
        <div>
          <div className="toolbar">
            <strong>Bài tập: {block.entry}()</strong>
          </div>
          <Markdown md={block.md} />
          <div className="card muted">Mở trên máy tính (và mở khoá mục này) để viết code.</div>
        </div>
      );
    }
    // keyed: exactly one editor is mounted, and it unmounts on item change
    return <ExercisePane key={block.id} subtopicId={subtopicId} block={block} onPassed={onPassed} />;
  }
  return (
    <div id={`block-${block.id}`} className="block">
      <BlockView block={block} ctx={ctx} />
    </div>
  );
}

/** Next-section footer, shared by every pane kind. */
function NextFooter({
  isLast,
  canNext,
  nextHint,
  onNext,
  label = "Phần sau ►",
}: {
  isLast: boolean;
  canNext: boolean;
  nextHint: string;
  onNext: () => void;
  label?: string;
}) {
  if (isLast) return null;
  return (
    <div className="exnav-footer">
      <button className="btn sm primary" onClick={onNext} disabled={!canNext}>
        {label}
      </button>
      {!canNext && nextHint && <p className="muted">{nextHint}</p>}
    </div>
  );
}

/** Right pane. Shows the section's interactive items (quiz/predict/code); never blank. */
export function SectionPane({
  subtopicId,
  section,
  current,
  ctx,
  preview,
  canEdit,
  results,
  done,
  practice,
  extra = [],
  interactive = [],
  index = -1,
  allInteractive = [],
  onPrev,
  onNext,
  onJump,
  onPassed,
  onNextSection,
  isLast,
  canNext = true,
  nextHint = "",
}: {
  subtopicId: string;
  section: Section;
  /** The active interactive item (explicit selection, else section default). */
  current?: InteractiveBlock;
  ctx: BlockContext;
  preview: boolean;
  canEdit: boolean;
  results: Record<string, boolean>;
  done: Set<string>;
  practice: string[];
  extra?: string[];
  /** The current section's interactive items, in order (for the ◄ i/N ► counter). */
  interactive?: InteractiveBlock[];
  index?: number;
  /** Every interactive item in the whole lesson (for the jump list). */
  allInteractive?: LessonInteractiveEntry[];
  onPrev: () => void;
  onNext: () => void;
  onJump: (sectionIdx: number, blockId: string) => void;
  onPassed: (blockId: string) => void;
  onNextSection: () => void;
  isLast: boolean;
  canNext?: boolean;
  nextHint?: string;
}) {
  if (current) {
    return (
      <div>
        <ExerciseNav
          interactive={interactive}
          index={index}
          onPrev={onPrev}
          onNext={onNext}
          allInteractive={allInteractive}
          currentId={current.id}
          practice={practice}
          extra={extra}
          onJump={onJump}
          done={done}
          results={results}
        />
        {preview && (
          <div className="card muted" role="note">
            Mục đang khoá — xem trước, chưa làm được. Đạt điểm 2 ở các mục tiên quyết để mở.
          </div>
        )}
        <fieldset className="preview-fieldset" disabled={preview}>
          <CurrentItem
            block={current}
            subtopicId={subtopicId}
            canEdit={canEdit}
            onPassed={onPassed}
            ctx={ctx}
          />
        </fieldset>
        <NextFooter isLast={isLast} canNext={canNext} nextHint={nextHint} onNext={onNextSection} />
      </div>
    );
  }

  // No interactive item in this section: a "remember" card.
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
      <NextFooter
        isLast={isLast}
        canNext={canNext}
        nextHint={nextHint}
        onNext={onNextSection}
        label="Tiếp tục ►"
      />
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
