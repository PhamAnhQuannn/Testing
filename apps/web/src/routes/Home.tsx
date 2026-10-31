import { Link, Navigate, useNavigate } from "react-router-dom";
import ReassessButton from "../components/ReassessButton";
import {
  getNext,
  getOnboarding,
  getResumeView,
  getSettings,
  type LockedPreview,
  type MapSubtopic,
  type MustRaise,
  type NextData,
  type NextItem,
  type ResumeView,
} from "../lib/api";
import { useAsync } from "../lib/hooks";
import { needsWelcome } from "../lib/onboarding";

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

/** "1h20" / "25 phút" / "0 phút": neutral study time, view only (no goal). */
export function formatStudy(seconds: number): string {
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes} phút`;
  const m = String(minutes % 60).padStart(2, "0");
  return `${Math.floor(minutes / 60)}h${m}`;
}

/** Local "HH:mm" of an ISO time, for "chờ đến 14:30". */
export function clock(iso: string): string {
  const d = new Date(iso);
  return `${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
}

const MODE_LABEL: Record<string, string> = {
  lesson: "bài học",
  problem: "bài tập",
  check: "bài kiểm tra",
  placement: "đánh giá",
  review: "ôn tập",
  other: "việc đang dở",
};

/** S12 banner on `/`. A button (not a link) so the subtopic keeps a single `a[href]` on this screen. */
export function ResumeBanner({
  resume,
  names,
  onGo,
}: {
  resume: ResumeView;
  names: Record<string, string>;
  onGo: (route: string) => void;
}) {
  const p = resume.primary;
  if (!p) return null;
  const ref = p.ref as { subtopic_id?: string; problem_id?: string };
  const target = ref.subtopic_id ?? ref.problem_id ?? "";
  const label = names[target] ?? target;
  const more = resume.others.length;
  return (
    <div className="check-banner neutral resume-banner" role="note" data-testid="resume-banner">
      <div className="toolbar">
        <span>
          <strong>Tiếp tục nơi bạn dừng:</strong> {MODE_LABEL[p.mode] ?? MODE_LABEL.other}
          {label ? ` · ${label}` : ""}
          {more > 0 ? ` (+${more} việc khác)` : ""}
        </span>
        <span className="grow" />
        <button className={`btn sm${p.stale ? "" : " primary"}`} onClick={() => onGo(p.route)}>
          {p.stale ? "Mở lại" : "Tiếp tục"}
        </button>
      </div>
    </div>
  );
}

function SuggestedLink({ problem }: { problem: NonNullable<NextItem["suggested_problem"]> }) {
  return (
    <Link className="muted" to={`/p/${problem.id}`}>
      Luyện: {problem.title_vi ?? problem.title} ({problem.difficulty})
    </Link>
  );
}

export function MustRaiseRow({ m }: { m: MustRaise }) {
  const p = m.prerequisite;
  return (
    <li className="card home-row" data-testid="must-raise">
      <ScoreBadge score={p.score} />
      <span>
        <strong>{p.name_vi}</strong> cần điểm {p.need} để mở <strong>{m.unlocks.name_vi}</strong>
        {m.also_blocks > 0 ? ` (và ${m.also_blocks} mục khác)` : ""}
        {!m.sole_blocker ? " · còn mục tiền đề khác" : ""}
      </span>
      <span className="grow" />
      {m.suggested_problem && <SuggestedLink problem={m.suggested_problem} />}
      {m.test_out.available &&
        (m.test_out.retry_after ? (
          <span className="chip neutral">Test out sau {clock(m.test_out.retry_after)}</span>
        ) : (
          <Link className="btn sm" to={`/check/${p.id}?ctx=test_out`}>
            Test out
          </Link>
        ))}
    </li>
  );
}

/** One up-next row. The only `a[href="/s/:id"]` of the subtopic on this screen; text starts with the score badge. */
export function UpNextRow({ item, first }: { item: NextItem; first: boolean }) {
  const waiting = item.check_retry_after;
  return (
    <li className="home-row-wrap">
      <Link
        to={`/s/${item.id}`}
        className={`subchip home-item${first ? " first" : ""}`}
        data-testid={first ? "up-next-first" : "up-next"}
      >
        <ScoreBadge score={item.score} />
        <span>{item.name_vi}</span>
        {item.status === "in_progress" && <span className="chip neutral">đang học</span>}
        {item.known_basic && <span className="chip neutral">đã biết sơ</span>}
        {item.due_card && <span className="chip warn">● ôn</span>}
        {waiting && <span className="chip neutral">chờ đến {clock(waiting)}</span>}
        {first && !waiting && <span className="chip ok">Học tiếp ▶</span>}
      </Link>
      {item.suggested_problem && !waiting && <SuggestedLink problem={item.suggested_problem} />}
    </li>
  );
}

export function LockedRow({ item }: { item: LockedPreview }) {
  const why = item.lock_reasons
    .map((r) => `${r.name_vi ?? r.prerequisite} ≥ ${r.need}`)
    .join(", ");
  return (
    <li className="home-row-wrap">
      <Link to={`/s/${item.id}`} className="subchip locked" title={why}>
        <span>🔒</span>
        <span>{item.name_vi}</span>
        {why && <span className="muted">cần {why}</span>}
      </Link>
      <Link className="btn sm ghost" to={`/check/${item.id}?ctx=test_out`}>
        Test out
      </Link>
    </li>
  );
}

export function HomeView({
  next,
  resume,
  experience,
  onGo,
}: {
  next: NextData;
  resume: ResumeView | null;
  experience?: "none" | "some" | "solid";
  onGo: (route: string) => void;
}) {
  const level = experience ?? "some";
  const names: Record<string, string> = {};
  for (const i of next.up_next) names[i.id] = i.name_vi;
  for (const m of next.must_raise) names[m.prerequisite.id] = m.prerequisite.name_vi;
  return (
    <>
      <ReassessButton experience={level} />
      {resume && <ResumeBanner resume={resume} names={names} onGo={onGo} />}
      <p className="muted" data-testid="study-time">
        Hôm nay {formatStudy(next.study.today_s)} · tuần này {formatStudy(next.study.week_s)} (chỉ để xem)
      </p>
      {next.backlog && (
        <div className="check-banner warn" role="note" data-testid="backlog-banner">
          Có {next.due_count} thẻ đang chờ ôn. Ôn lúc nào cũng được, từng phần cũng được.{" "}
          <Link to="/review">Ôn ngay</Link>
        </div>
      )}
      {next.must_raise.length > 0 && (
        <section aria-labelledby="h-must">
          <h2 id="h-must">Cần lên điểm 2 để mở mục sau</h2>
          <ul className="home-list">
            {next.must_raise.map((m) => (
              <MustRaiseRow key={m.prerequisite.id} m={m} />
            ))}
          </ul>
        </section>
      )}
      <section aria-labelledby="h-next">
        <h2 id="h-next">Học tiếp</h2>
        {next.up_next.length === 0 ? (
          <div className="empty">Chưa có mục nào đang mở. Xem Map để chọn mục.</div>
        ) : (
          <ul className="home-list">
            {next.up_next.map((item, i) => (
              <UpNextRow key={item.id} item={item} first={i === 0} />
            ))}
          </ul>
        )}
        {next.locked_preview.length > 0 && (
          <>
            <h3 className="muted">Sắp mở</h3>
            <ul className="home-list">
              {next.locked_preview.map((l) => (
                <LockedRow key={l.id} item={l} />
              ))}
            </ul>
          </>
        )}
      </section>
      <section aria-labelledby="h-review">
        <h2 id="h-review">Ôn tập đến hạn{next.due_count > 0 ? ` (${next.due_count})` : ""}</h2>
        {next.due_count > 0 ? (
          <p>
            <Link className="btn primary" to="/review" data-testid="review-entry">
              Ôn {next.due_count} thẻ
            </Link>{" "}
            <span className="muted">Dừng lúc nào cũng được.</span>
          </p>
        ) : (
          <p className="muted" data-testid="review-entry">
            Không có thẻ đến hạn.
          </p>
        )}
      </section>
    </>
  );
}

export default function Home() {
  const next = useAsync(getNext, []);
  const resume = useAsync(() => getResumeView().catch(() => null), []);
  // First-time user (profile_done=false) is sent to S1. Unknown state (server down) never redirects.
  const onboarding = useAsync(() => getOnboarding().catch(() => null), []);
  const settings = useAsync(getSettings, []);
  const navigate = useNavigate();
  if (onboarding.loading) return <div className="page" aria-busy="true" />;
  if (needsWelcome(onboarding.data)) return <Navigate to="/welcome" replace />;
  return (
    <div className="page">
      <h1>Học tiếp</h1>
      {next.loading && (
        <div aria-busy="true">
          <div className="skeleton" style={{ width: "60%" }} />
          <div className="skeleton" style={{ width: "80%" }} />
          <div className="skeleton" style={{ width: "40%" }} />
        </div>
      )}
      {next.error && (
        <div className="error-block" role="alert">
          <strong>Không tải được danh sách</strong>
          <p>{next.error.message}</p>
          <button className="btn" onClick={next.reload}>
            Thử lại
          </button>
        </div>
      )}
      {next.data && (
        <HomeView
          next={next.data}
          resume={resume.data}
          experience={settings.data?.experience}
          onGo={(route) => navigate(route)}
        />
      )}
    </div>
  );
}
