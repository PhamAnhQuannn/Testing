import type { Section } from "./sections";

/** Collapsible vertical TOC: progress header + one row per section (done / viewed / current). */
export function SectionRail({
  sections,
  idx,
  done,
  viewed,
  onSelect,
  open,
  onToggle,
  doneCount,
}: {
  sections: Section[];
  idx: number;
  done: (s: Section) => boolean;
  viewed?: Set<string>;
  onSelect: (i: number) => void;
  open: boolean;
  onToggle: () => void;
  doneCount: number;
}) {
  return (
    <nav className="section-rail section-toc" aria-label="Các phần của bài học">
      <button className="toc-toggle btn sm ghost" aria-expanded={open} onClick={onToggle}>
        ☰ Mục lục · xong {doneCount}/{sections.length}
      </button>
      <div className="progress" aria-hidden="true">
        <div style={{ width: `${(doneCount / Math.max(1, sections.length)) * 100}%` }} />
      </div>
      {open && (
        <ol style={{ listStyle: "none", margin: 0, padding: 0, display: "flex", flexDirection: "column", gap: 4 }}>
          {sections.map((s, i) => {
            const isDone = done(s);
            const dot = isDone ? "●" : viewed?.has(s.id) ? "◐" : "○";
            return (
              <li key={s.id}>
                <button
                  className={`btn sm${i === idx ? " primary" : " ghost"}`}
                  aria-current={i === idx ? "step" : undefined}
                  onClick={() => onSelect(i)}
                  title={isDone ? "Đã xong" : viewed?.has(s.id) ? "Đã xem" : undefined}
                >
                  <span className="toc-dot" aria-hidden="true">{dot}</span> {i + 1}. {s.title || "Mở đầu"}
                </button>
              </li>
            );
          })}
        </ol>
      )}
    </nav>
  );
}
