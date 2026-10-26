import { Link } from "react-router-dom";
import { getMap, type MapSubtopic } from "../lib/api";
import { useAsync } from "../lib/hooks";

export function ScoreBadge({ score }: { score: number }) {
  return (
    <span className={`badge s${Math.min(3, Math.max(0, score))}`} aria-label={`Điểm ${score} trên 3`}>
      {score}
    </span>
  );
}

export function groupByModule(items: MapSubtopic[]): [string, MapSubtopic[]][] {
  const groups = new Map<string, MapSubtopic[]>();
  for (const item of items) groups.set(item.module, [...(groups.get(item.module) ?? []), item]);
  return [...groups.entries()];
}

export default function Home() {
  const map = useAsync(getMap, []);
  return (
    <div className="page">
      <h1>Học tiếp</h1>
      <p className="muted">
        Chọn một mục để học. Mục khoá vẫn xem trước được. <Link to="/review">Ôn tập thẻ đến hạn</Link>
      </p>
      {map.loading && (
        <div aria-busy="true">
          <div className="skeleton" style={{ width: "60%" }} />
          <div className="skeleton" style={{ width: "80%" }} />
          <div className="skeleton" style={{ width: "40%" }} />
        </div>
      )}
      {map.error && (
        <div className="error-block" role="alert">
          <strong>Không tải được danh sách mục</strong>
          <p>{map.error.message}</p>
          <button className="btn" onClick={map.reload}>
            Thử lại
          </button>
        </div>
      )}
      {map.data && map.data.length === 0 && <div className="empty">Chưa có mục nào.</div>}
      {map.data &&
        groupByModule(map.data).map(([module, items]) => (
          <section className="module" key={module}>
            <h2>{module}</h2>
            <div className="chips">
              {items.map((item) => (
                <Link
                  key={item.id}
                  to={`/s/${item.id}`}
                  className={`subchip${item.unlocked ? "" : " locked"}`}
                  title={item.lock_reason ?? undefined}
                >
                  <ScoreBadge score={item.score} />
                  <span>{item.name_vi}</span>
                  {!item.unlocked && <span className="muted">🔒 {item.lock_reason ?? "khoá"}</span>}
                  {item.due_cards > 0 && <span className="chip warn">● {item.due_cards}</span>}
                </Link>
              ))}
            </div>
          </section>
        ))}
    </div>
  );
}
