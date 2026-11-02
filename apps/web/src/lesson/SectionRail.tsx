import type { Section } from "./sections";

/** Thin TOC / stepper: one dot per section (done / viewed / current). */
export function SectionRail({
  sections,
  idx,
  done,
  viewed,
  onSelect,
}: {
  sections: Section[];
  idx: number;
  done: (s: Section) => boolean;
  viewed?: Set<string>;
  onSelect: (i: number) => void;
}) {
  return (
    <nav className="section-rail" aria-label="Các phần của bài học">
      <ol style={{ listStyle: "none", margin: 0, padding: 0, display: "flex", flexWrap: "wrap", gap: 6 }}>
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
                <span aria-hidden="true">{dot}</span> {i + 1}. {s.title || "Mở đầu"}
              </button>
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
