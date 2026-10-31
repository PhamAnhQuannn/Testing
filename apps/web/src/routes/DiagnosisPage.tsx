import { useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useToast } from "../components/Toast";
import {
  ApiError,
  getDiagnosis,
  newIdempotencyKey,
  startPlacement,
  type DiagnosisDomain,
  type DiagnosisImprove,
  type DiagnosisModule,
  type DiagnosisView,
} from "../lib/api";
import { useAsync } from "../lib/hooks";
import { ScoreBadge } from "./Home";

const TIER_CLASS: Record<string, string> = {
  "đã đo": "measured",
  "suy luận": "inferred",
  "chưa đo": "unmeasured",
};

const pct = (coverage: number) => `${Math.round(Math.min(1, Math.max(0, coverage)) * 100)}%`;

export function TierChip({ tier, coverage }: { tier: string; coverage: number }) {
  return (
    <span className={`tier-chip ${TIER_CLASS[tier] ?? "unmeasured"}`}>
      {tier} {pct(coverage)}
    </span>
  );
}

function ImproveItem({ item: i }: { item: DiagnosisImprove }) {
  return (
    <li>
      <span>{i.name_vi}</span>
      {i.concepts.length > 0 && <span className="muted">Trọng tâm: {i.concepts.join(", ")}</span>}
      {i.has_lesson && (
        <Link to={`/s/${i.subtopic_id}`} aria-label={`Học ${i.name_vi}`}>
          Học
        </Link>
      )}
      <Link to={`/check/${i.subtopic_id}?ctx=test_out`} aria-label={`Kiểm tra ${i.name_vi}`}>
        Kiểm tra
      </Link>
    </li>
  );
}

/** "Đo sâu": a module-scoped placement (knowledge rungs only) to fill in this module's coverage. */
function DeepDiveButton({ module }: { module: string }) {
  const navigate = useNavigate();
  const notify = useToast();
  const inFlight = useRef(false);
  const [busy, setBusy] = useState(false);
  const start = async () => {
    if (inFlight.current) return;
    inFlight.current = true;
    setBusy(true);
    try {
      const view = await startPlacement({ kind: "deep_dive", module }, newIdempotencyKey());
      navigate(`/placement/${view.placement_id}`);
    } catch (e) {
      notify(
        e instanceof ApiError && e.isNetwork ? "Server chưa chạy nên chưa thực hiện được." : (e as Error).message,
        { kind: "error" },
      );
      inFlight.current = false;
      setBusy(false);
    }
  };
  return (
    <button
      className="btn sm"
      data-testid="deep-dive-button"
      onClick={start}
      disabled={busy}
      title="Đo các chủ đề của module này bằng câu hỏi ngắn"
    >
      Đo sâu
    </button>
  );
}

function ModuleCard({ module: m }: { module: DiagnosisModule }) {
  // Split by per-item evidence, not the module tier: a measured gap (firm) is a real "cần cải thiện"
  // even in a low-coverage module, while an inferred gap stays under the hedged header.
  const firm = m.improve.filter((i) => i.firm);
  const inferred = m.improve.filter((i) => !i.firm);
  return (
    <div className="card profile-module" data-testid="diagnosis-module">
      <div className="profile-head">
        <h3>{m.name_vi}</h3>
        <TierChip tier={m.tier} coverage={m.coverage} />
        <span className="muted">{m.level}</span>
        <DeepDiveButton module={m.module} />
      </div>
      {m.strong.length > 0 && (
        <>
          <h4>Đã vững</h4>
          <div className="chips">
            {m.strong.map((s) => (
              <span key={s.subtopic_id} className="subchip">
                {s.name_vi} <ScoreBadge score={s.score} />
              </span>
            ))}
          </div>
        </>
      )}
      {firm.length > 0 && (
        <>
          <h4>Cần cải thiện</h4>
          <ul className="profile-improve">
            {firm.map((i) => (
              <ImproveItem key={i.subtopic_id} item={i} />
            ))}
          </ul>
        </>
      )}
      {inferred.length > 0 && (
        <>
          <h4>Có thể cần xem lại (chưa đủ dữ liệu)</h4>
          <ul className="profile-improve">
            {inferred.map((i) => (
              <ImproveItem key={i.subtopic_id} item={i} />
            ))}
          </ul>
        </>
      )}
      {m.not_assessed_count > 0 && <p className="muted">{m.not_assessed_count} chủ đề chưa đo</p>}
    </div>
  );
}

function DomainSection({ domain: d }: { domain: DiagnosisDomain }) {
  return (
    <section className="profile-domain" aria-label={d.name_vi}>
      <div className="profile-head">
        <h2>{d.name_vi}</h2>
        <TierChip tier={d.tier} coverage={d.coverage} />
        <span className="muted">{d.level}</span>
      </div>
      <div className="profile-modules">
        {d.modules.map((m) => (
          <ModuleCard key={m.module} module={m} />
        ))}
      </div>
    </section>
  );
}

export function DiagnosisContent({ view }: { view: DiagnosisView }) {
  if (view.domains.length === 0) return <div className="empty">Chưa có dữ liệu hồ sơ.</div>;
  return (
    <>
      {view.domains.map((d) => (
        <DomainSection key={d.section} domain={d} />
      ))}
    </>
  );
}

export default function DiagnosisPage() {
  const diagnosis = useAsync(getDiagnosis, []);
  return (
    <div className="page">
      <h1>Hồ sơ kỹ năng</h1>
      <p className="muted">Mức độ tin cậy: đã đo (có bài kiểm tra), suy luận (ước tính), chưa đo.</p>
      {diagnosis.loading && (
        <div aria-busy="true">
          <div className="skeleton" style={{ width: "60%" }} />
          <div className="skeleton" style={{ width: "80%" }} />
        </div>
      )}
      {diagnosis.error && (
        <div className="error-block" role="alert">
          <strong>Không tải được hồ sơ kỹ năng</strong>
          <p>{diagnosis.error.message}</p>
          <button className="btn" onClick={diagnosis.reload}>
            Thử lại
          </button>
        </div>
      )}
      {diagnosis.data && <DiagnosisContent view={diagnosis.data} />}
    </div>
  );
}
