import { useState } from "react";
import { Link } from "react-router-dom";
import type { MapSubtopic } from "../lib/api";
import { getMap } from "../lib/api";
import { useAsync } from "../lib/hooks";
import { isLocked, lockSummary, reasonText, statusLabel } from "../lib/lock";
import { groupByModule, ScoreBadge } from "./Home";

/** Which section a subtopic belongs to (the id prefix: py.core.x -> "py"). */
const sectionOf = (item: MapSubtopic) => item.id.split(".")[0];

/** Track filters over the skill map (client-only; sections, not the display track). */
const TRACK_FILTERS: { key: string; label: string; sections: string[] | null }[] = [
  { key: "all", label: "Tất cả", sections: null },
  { key: "foundation", label: "Nền tảng", sections: ["py", "dsa", "cs"] },
  { key: "sd", label: "System Design", sections: ["sd"] },
  { key: "ai", label: "AI engineer", sections: ["ml"] },
];

/** One skill-map node. Colour is never the only channel: score number + status label + lock icon. */
export function MapNode({ item }: { item: MapSubtopic }) {
  const locked = isLocked(item);
  return (
    <li className="map-node-wrap">
      <Link
        to={`/s/${item.id}`}
        className={`subchip map-node status-${item.status}${locked ? " locked" : ""}`}
        data-status={item.status}
        title={locked ? lockSummary(item) : undefined}
      >
        <ScoreBadge score={item.score} />
        <span className="name">{item.name_vi}</span>
        <span className={`chip neutral status-label`}>
          {locked ? "🔒 " : item.status === "done" ? "✔ " : ""}
          {statusLabel(item.status)}
        </span>
        <span className="muted">
          {item.score}/3 · mục tiêu {item.target_intern}
        </span>
        {item.due_cards > 0 && (
          <span className="chip warn" aria-label={`${item.due_cards} thẻ đến hạn ôn`}>
            ● {item.due_cards} ôn
          </span>
        )}
      </Link>
      {locked && (
        <div className="lock-reasons muted">
          <ul>
            {item.lock_reasons.length ? (
              item.lock_reasons.map((r) => <li key={r.prerequisite}>{reasonText(r)}</li>)
            ) : (
              <li>{lockSummary(item)}</li>
            )}
          </ul>
          <span>Vẫn xem trước được. </span>
          <Link to={`/check/${item.id}?ctx=test_out`}>Test out</Link>
        </div>
      )}
    </li>
  );
}

export function MapView({ items }: { items: MapSubtopic[] }) {
  const done = items.filter((i) => i.status === "done").length;
  const due = items.reduce((sum, i) => sum + i.due_cards, 0);
  return (
    <>
      {due > 0 && (
        <p>
          <Link className="chip warn" to="/review" aria-label={`${due} thẻ đến hạn ôn, mở trang ôn tập`}>
            ● {due} thẻ đến hạn · Ôn tập
          </Link>
        </p>
      )}
      <p className="muted" role="status">
        {done}/{items.length} mục hoàn thành · điểm 0-3 (số trong vòng tròn)
      </p>
      {groupByModule(items).map(([module, group]) => (
        <section className="module" key={module} aria-label={module}>
          <h2>{module}</h2>
          <ul className="map-nodes">
            {group.map((item) => (
              <MapNode key={item.id} item={item} />
            ))}
          </ul>
        </section>
      ))}
    </>
  );
}

export default function MapPage() {
  const map = useAsync(getMap, []);
  const [track, setTrack] = useState<string>("all");
  const filter = TRACK_FILTERS.find((f) => f.key === track) ?? TRACK_FILTERS[0];
  const items = map.data
    ? filter.sections
      ? map.data.filter((i) => filter.sections!.includes(sectionOf(i)))
      : map.data
    : [];
  return (
    <div className="page">
      <h1>Skill map</h1>
      <p className="muted">Mục khoá vẫn xem trước được; mở khi mọi mục tiên quyết đạt điểm ≥ 2.</p>
      {map.data && (
        <div className="track-filter" role="tablist" aria-label="Lọc theo mảng" style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", margin: "0.5rem 0" }}>
          {TRACK_FILTERS.map((f) => (
            <button
              key={f.key}
              role="tab"
              aria-selected={f.key === track}
              className={`btn sm${f.key === track ? " primary" : ""}`}
              onClick={() => setTrack(f.key)}
            >
              {f.label}
            </button>
          ))}
        </div>
      )}
      {map.loading && (
        <div aria-busy="true">
          <div className="skeleton" style={{ width: "60%" }} />
          <div className="skeleton" style={{ width: "80%" }} />
        </div>
      )}
      {map.error && (
        <div className="error-block" role="alert">
          <strong>Không tải được skill map</strong>
          <p>{map.error.message}</p>
          <button className="btn" onClick={map.reload}>
            Thử lại
          </button>
        </div>
      )}
      {map.data && map.data.length === 0 && <div className="empty">Chưa có mục nào.</div>}
      {map.data && items.length === 0 && map.data.length > 0 && (
        <div className="empty">Chưa có mục nào trong mảng này.</div>
      )}
      {map.data && items.length > 0 && <MapView items={items} />}
    </div>
  );
}
