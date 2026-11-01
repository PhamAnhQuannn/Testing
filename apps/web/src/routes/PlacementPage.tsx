// Placement, Phase A (UI_SPEC S2 session + reduced S3 result; docs/API_M2A.md "Placement").
// Focus mode: no side nav (App.tsx). The sitting lives on the server, so reloading resumes it.
// The API drives the gate sequence; this page renders the open item, runs write_code through the
// same Pyodide Submit path as the mastery check (WriteCodeStep) and posts the outcome. It never
// shows a reference solution, and "Không biết" is a give-up, not a failure.
import { useCallback, useEffect, useRef, useState } from "react";
import { Link, useLocation, useNavigate, useParams } from "react-router-dom";
import { ConceptStep, McqStep, ReadCodeStep, ResultBanner } from "../components/CheckParts";
import { formatClock } from "../components/EditorPanel";
import { ConfirmModal } from "../components/Modal";
import { useToast } from "../components/Toast";
import {
  answerPlacement,
  ApiError,
  finishPlacement,
  getPlacement,
  getPlacementResult,
  newIdempotencyKey,
  placementHeartbeat,
  selectPlacementModules,
  skipPlacement,
  type CheckAnswerBody,
  type CheckStep,
  type CheckStepResult,
  type PlacementConceptOffer,
  type PlacementResult,
  type PlacementView,
} from "../lib/api";
import { formatRetry, LEVEL_TEXT, timebox } from "../lib/checkFlow";
import { useAsync, usePageExit } from "../lib/hooks";
import {
  budgetView,
  CONCEPT_OUTCOME_TEXT,
  currentLabel,
  GATE_TEXT,
  gateChips,
  gateProgressText,
  groupByModule,
  minutesText,
  OUTCOME_NOTE,
  skillChip,
} from "../lib/placementFlow";
import { WriteCodeStep } from "./CheckPage";

const HEARTBEAT_MS = 15_000;

export default function PlacementPage() {
  const { sessionId } = useParams();
  const { pathname } = useLocation();
  const id = Number(sessionId);
  if (pathname.endsWith("/result")) return <PlacementResultPage key={id} id={id} />;
  return <PlacementRunner key={id} id={id} />;
}

// ---------------------------------------------------------------- S2: session

export type PlacementConfirm = "exit" | "giveup" | "finish" | null;

/** Presentational S2 screen: header (gate progress, budget, actions), the open item, the step result. */
export function PlacementSessionView(props: {
  view: PlacementView;
  step: CheckStep;
  activeMs: number;
  itemMs: number;
  last: CheckStepResult | null;
  busy: boolean;
  confirm: PlacementConfirm;
  softOffer: boolean;
  onConfirm: (kind: PlacementConfirm) => void;
  onGiveUp: () => void;
  onFinish: () => void;
  onExit: () => void;
  onNext: () => void;
  onKeepGoing: () => void;
  commit: (body: CheckAnswerBody) => Promise<boolean>;
}) {
  const { view, step, last } = props;
  const budget = budgetView(props.activeMs, view.budget.soft_ms, view.budget.hard_ms);
  const box = timebox(props.itemMs, step.minutes);
  const chips = gateChips(view);
  const done = view.status !== "in_progress";
  return (
    <div className="check-page placement-page">
      <header className="check-header">
        <strong>Đánh giá đầu vào</strong>
        <span data-testid="gate-progress">{gateProgressText(view)}</span>
        <span className={`check-timer ${budget.phase}`} role="timer" aria-label="Thời gian đánh giá đã dùng">
          {budget.label}
        </span>
        <span className="grow" />
        {last === null && !done && (
          <button className="btn sm" disabled={props.busy} onClick={() => props.onConfirm("giveup")}>
            Không biết
          </button>
        )}
        {!done && (
          <button className="btn sm" disabled={props.busy} onClick={() => props.onConfirm("finish")}>
            Kết thúc
          </button>
        )}
        <button className="btn sm ghost" onClick={() => props.onConfirm("exit")}>
          Tạm dừng
        </button>
      </header>
      <div className="budget-bar" role="progressbar" aria-label="Ngân sách thời gian" aria-valuenow={budget.pct}>
        <div className={`budget-fill ${budget.phase}`} style={{ width: `${budget.pct}%` }} />
      </div>
      <ol className="check-stepper" aria-label="Các cổng đánh giá">
        {chips.map(({ gate, current }) => (
          <li
            key={gate.code}
            className={current ? "current" : gate.outcome === "passed" || gate.outcome === "known" ? "ok" : "neutral"}
            aria-current={current ? "step" : undefined}
          >
            {gate.name_vi || gate.code} · {current ? "đang làm" : (GATE_TEXT[gate.outcome ?? ""] ?? gate.outcome)}
          </li>
        ))}
      </ol>
      {view.current && last === null && (
        // Hidden while a result is shown: `view` already holds the NEXT gate then.
        <p className="muted">
          {currentLabel(view.current, LEVEL_TEXT[step.level] ?? `Mức ${step.level}`)}
          <span className={`check-timer ${box.phase}`}> · ⏱ {formatClock(props.itemMs)} → {box.label}</span>
        </p>
      )}
      {budget.phase === "hard" && !done && (
        <div className="check-banner warn" role="status">
          Đã dùng hết 60 phút của lần đánh giá này. Bạn hoàn thành mục đang làm, sau đó sẽ xem kết quả.
        </div>
      )}
      {last ? (
        <section className="card" aria-label="Kết quả bước">
          <ResultBanner result={last} />
          {done && view.message_vi && <p>{view.message_vi}</p>}
          <div className="toolbar">
            <button className="btn primary" onClick={props.onNext}>
              {done ? "Xem kết quả" : "Tiếp tục"}
            </button>
          </div>
        </section>
      ) : step.type === "write_code" ? (
        <WriteCodeStep
          key={step.item_id}
          session={{ session_id: view.current?.check_session_id ?? view.placement_id }}
          step={step}
          busy={props.busy}
          commit={props.commit}
        />
      ) : step.type === "write_test" ? (
        <div className="error-block" role="alert">
          Loại câu hỏi này chưa hỗ trợ trong bài xếp lớp.
        </div>
      ) : step.type === "read_code" ? (
        <ReadCodeStep key={step.item_id} step={step} busy={props.busy} onAnswer={(answer) => void props.commit({ answer })} />
      ) : step.type === "mcq" ? (
        <McqStep key={step.item_id} step={step} busy={props.busy} onSubmit={(choice) => void props.commit({ choice })} />
      ) : (
        <ConceptStep
          key={step.item_id}
          step={step}
          busy={props.busy}
          onGrade={(self_grade) => void props.commit({ self_grade })}
        />
      )}
      <p className="muted check-footnote">
        Không hiện lời giải code trong lúc đánh giá. “Không biết” không bị khoá và không bị trừ gì; mục bỏ
        qua chỉ nghĩa là chưa đo được.
      </p>
      {props.confirm === "exit" && (
        <ConfirmModal
          title="Tạm dừng đánh giá?"
          confirmLabel="Tạm dừng"
          onCancel={() => props.onConfirm(null)}
          onConfirm={props.onExit}
        >
          <p>Lần đánh giá được giữ lại; bạn có thể quay lại làm tiếp từ mục này.</p>
        </ConfirmModal>
      )}
      {props.confirm === "giveup" && (
        <ConfirmModal
          title="Chọn “Không biết”?"
          confirmLabel="Không biết"
          onCancel={() => props.onConfirm(null)}
          onConfirm={props.onGiveUp}
        >
          <p>Mục này tính là chưa đo được (không bị khoá làm lại) và bạn đi tiếp.</p>
        </ConfirmModal>
      )}
      {props.confirm === "finish" && (
        <ConfirmModal
          title="Kết thúc đánh giá?"
          confirmLabel="Kết thúc và xem kết quả"
          onCancel={() => props.onConfirm(null)}
          onConfirm={props.onFinish}
        >
          <p>Những gì đã đo được được giữ lại; mục đang mở không bị tính là sai.</p>
        </ConfirmModal>
      )}
      {props.softOffer && props.confirm === null && last === null && (
        <ConfirmModal
          title="Đã dùng 45 phút"
          confirmLabel="Xem kết quả"
          cancelLabel="Làm thêm mục này"
          onCancel={props.onKeepGoing}
          onConfirm={props.onFinish}
        >
          <p>Xem kết quả bây giờ, hay làm thêm mục đang mở? Tối đa 60 phút cho lần đánh giá này.</p>
        </ConfirmModal>
      )}
    </div>
  );
}

/** The sitting ended on the last answer (no open item): show that result and the server message. */
export function PlacementFinishedView(props: { view: PlacementView; last: CheckStepResult; onNext: () => void }) {
  return (
    <div className="page check-page placement-page">
      <section className="card" aria-label="Kết quả bước">
        <ResultBanner result={props.last} />
        {props.view.message_vi && <p>{props.view.message_vi}</p>}
        <div className="toolbar">
          <button className="btn primary" onClick={props.onNext}>
            Xem kết quả
          </button>
        </div>
      </section>
    </div>
  );
}

/** Concept phase, step 1: the user ticks the modules they already know; those get a quick check. */
export function ModuleOfferView(props: {
  offer: PlacementConceptOffer[];
  checked: string[];
  busy: boolean;
  onToggle: (module: string) => void;
  onMeasure: () => void;
  onSkip: () => void;
}) {
  return (
    <div className="page check-page placement-page">
      <section className="card" aria-labelledby="pl-modules">
        <h1 id="pl-modules">Chọn các mảng bạn đã nắm</h1>
        <p>Chọn các mảng bạn đã nắm để kiểm tra nhanh; bỏ trống nếu muốn bắt đầu học luôn.</p>
        <ul className="module-offer" style={{ listStyle: "none", padding: 0 }}>
          {props.offer.map((o) => (
            <li key={o.module}>
              <label>
                <input
                  type="checkbox"
                  checked={props.checked.includes(o.module)}
                  disabled={props.busy}
                  onChange={() => props.onToggle(o.module)}
                />{" "}
                {o.name_vi}
              </label>
            </li>
          ))}
        </ul>
        <div className="toolbar">
          <button className="btn primary" disabled={props.busy || props.checked.length === 0} onClick={props.onMeasure}>
            Đo các mục đã chọn
          </button>
          <button className="btn" disabled={props.busy} onClick={props.onSkip}>
            Bỏ qua
          </button>
        </div>
      </section>
    </div>
  );
}

type Phase = { kind: "loading" } | { kind: "error"; error: Error } | { kind: "running" };

function PlacementRunner({ id }: { id: number }) {
  const notify = useToast();
  const navigate = useNavigate();
  const [phase, setPhase] = useState<Phase>({ kind: "loading" });
  const [view, setView] = useState<PlacementView | null>(null);
  const [last, setLast] = useState<CheckStepResult | null>(null);
  const [busy, setBusy] = useState(false);
  const [confirm, setConfirm] = useState<PlacementConfirm>(null);
  const [softDismissed, setSoftDismissed] = useState(false);
  const [reload, setReload] = useState(0);
  const [checkedModules, setCheckedModules] = useState<string[]>([]);
  const [clock, setClock] = useState({ item: 0, active: 0 });
  const itemRef = useRef(0);
  const activeRef = useRef(0);
  const committing = useRef(false);

  const goResult = useCallback(() => navigate(`/placement/${id}/result`, { replace: true }), [navigate, id]);

  const adopt = useCallback((next: PlacementView) => {
    setView(next);
    itemRef.current = next.current?.elapsed_ms ?? 0;
    activeRef.current = Math.max(activeRef.current, next.active_ms);
    setClock({ item: itemRef.current, active: activeRef.current });
  }, []);

  useEffect(() => {
    let alive = true;
    getPlacement(id)
      .then((v) => {
        if (!alive) return;
        if (v.status === "skipped") return void navigate("/", { replace: true });
        if (v.status !== "in_progress") return goResult();
        adopt(v);
        setLast(null);
        setPhase({ kind: "running" });
      })
      .catch((error: Error) => alive && setPhase({ kind: "error", error }));
    return () => {
      alive = false;
    };
  }, [id, reload, adopt, goResult, navigate]);

  const step = view?.current?.step ?? null;
  const running = phase.kind === "running" && view?.status === "in_progress" && step !== null && last === null;

  // Active time: only while an item is on screen and the tab is visible; sent as an absolute value.
  useEffect(() => {
    if (!running) return;
    const timer = setInterval(() => {
      if (document.visibilityState !== "visible") return;
      itemRef.current += 1000;
      activeRef.current += 1000;
      setClock({ item: itemRef.current, active: activeRef.current });
    }, 1000);
    return () => clearInterval(timer);
  }, [running]);

  useEffect(() => {
    if (!running) return;
    const beat = () =>
      void placementHeartbeat(id, activeRef.current, itemRef.current)
        .then((h) => h.status !== "in_progress" && goResult())
        .catch(() => undefined);
    const timer = setInterval(beat, HEARTBEAT_MS);
    return () => clearInterval(timer);
  }, [id, running, goResult]);

  const flush = useCallback(
    (keepalive: boolean) => {
      if (running) void placementHeartbeat(id, activeRef.current, itemRef.current, { keepalive }).catch(() => undefined);
    },
    [id, running],
  );
  usePageExit(flush);

  const handle = async (call: () => Promise<{ result: CheckStepResult; placement: PlacementView }>) => {
    if (!step || committing.current) return false;
    committing.current = true;
    setBusy(true);
    try {
      const res = await call();
      setLast(res.result);
      setView(res.placement);
      activeRef.current = Math.max(activeRef.current, res.placement.active_ms);
      return true;
    } catch (error) {
      const code = error instanceof ApiError ? error.code : "";
      if (code === "placement_finished") goResult();
      else if (["placement_item_expired", "check_item_answered", "check_wrong_item", "check_session_done"].includes(code)) {
        notify("Phiên đã thay đổi ở nơi khác, đang tải lại…", { kind: "error" });
        setReload((n) => n + 1);
      } else notify(`Chưa gửi được kết quả: ${(error as Error).message}`, { kind: "error" });
      return false;
    } finally {
      committing.current = false;
      setBusy(false);
    }
  };

  const commit = (body: CheckAnswerBody) =>
    handle(() =>
      answerPlacement(
        id,
        { item_id: step!.item_id, elapsed_ms: itemRef.current, session_elapsed_ms: activeRef.current, ...body },
        newIdempotencyKey(), // one answer = one key
      ),
    );

  const giveUp = () => {
    setConfirm(null);
    void handle(() =>
      skipPlacement(
        id,
        { item_id: step!.item_id, elapsed_ms: itemRef.current, session_elapsed_ms: activeRef.current },
        newIdempotencyKey(),
      ),
    );
  };

  const finish = async () => {
    setConfirm(null);
    setBusy(true);
    try {
      await finishPlacement(id, activeRef.current, newIdempotencyKey());
      goResult();
    } catch (error) {
      notify(`Không kết thúc được: ${(error as Error).message}`, { kind: "error" });
    } finally {
      setBusy(false);
    }
  };

  const sendModules = async (selected: string[]) => {
    if (committing.current) return;
    committing.current = true;
    setBusy(true);
    try {
      const next = await selectPlacementModules(id, selected, newIdempotencyKey(), activeRef.current);
      setLast(null);
      adopt(next);
      if (next.status !== "in_progress") goResult();
    } catch (error) {
      notify(`Chưa gửi được lựa chọn: ${(error as Error).message}`, { kind: "error" });
    } finally {
      committing.current = false;
      setBusy(false);
    }
  };

  const exit = async () => {
    await placementHeartbeat(id, activeRef.current, itemRef.current).catch(() => undefined);
    navigate("/");
  };

  const next = () => {
    if (!view) return;
    if (view.status !== "in_progress") return goResult();
    itemRef.current = view.current?.elapsed_ms ?? 0;
    setClock({ item: itemRef.current, active: activeRef.current });
    setLast(null);
  };

  if (phase.kind === "loading") {
    return (
      <div className="page" aria-busy="true">
        <div className="skeleton" style={{ width: "50%" }} />
        <div className="skeleton" style={{ width: "90%" }} />
      </div>
    );
  }
  if (phase.kind === "error" || !view) {
    return (
      <div className="page error-block" role="alert">
        <strong>Không mở được phiên đánh giá</strong>
        <p>{phase.kind === "error" ? phase.error.message : ""}</p>
        <button className="btn" onClick={() => setReload((n) => n + 1)}>
          Thử lại
        </button>{" "}
        <Link className="btn" to="/">
          Về trang chính
        </Link>
      </div>
    );
  }
  if (view.status === "in_progress" && (view.awaiting_modules || view.phase === "concept_offer") && !step) {
    // The last code answer's result banner is skipped here: the offer replaces the empty state.
    return (
      <ModuleOfferView
        offer={view.concept_offer ?? []}
        checked={checkedModules}
        busy={busy}
        onToggle={(m) => setCheckedModules((cur) => (cur.includes(m) ? cur.filter((x) => x !== m) : [...cur, m]))}
        onMeasure={() => void sendModules(checkedModules)}
        onSkip={() => void sendModules([])}
      />
    );
  }
  if (!step && last && view.status !== "in_progress") {
    return <PlacementFinishedView view={view} last={last} onNext={next} />;
  }
  if (!step) {
    return (
      <div className="page check-page">
        <section className="card" role="status">
          <h1>Chưa có mục đánh giá nào đang mở</h1>
          <p>Bạn có thể kết thúc đánh giá và xem những gì đã đo được.</p>
          <button className="btn primary" disabled={busy} onClick={() => void finish()}>
            Kết thúc và xem kết quả
          </button>{" "}
          <Link className="btn" to="/">
            Về trang chính
          </Link>
        </section>
      </div>
    );
  }
  const softOffer =
    !softDismissed && view.status === "in_progress" && clock.active >= view.budget.soft_ms && view.budget.remaining_ms > 0;
  return (
    <PlacementSessionView
      view={view}
      step={step}
      activeMs={clock.active}
      itemMs={clock.item}
      last={last}
      busy={busy}
      confirm={confirm}
      softOffer={softOffer}
      onConfirm={setConfirm}
      onGiveUp={giveUp}
      onFinish={() => void finish()}
      onExit={() => void exit()}
      onNext={next}
      onKeepGoing={() => setSoftDismissed(true)}
      commit={commit}
    />
  );
}

// ---------------------------------------------------------------- S3: reduced result

/** Presentational reduced S3: seeded skill map, strong/weak areas, where to start, test-out, content note. */
export function PlacementResultView({ result }: { result: PlacementResult }) {
  const names = new Map(result.skill_map.map((m) => [m.subtopic_id, m.name_vi]));
  const noneMeasured = result.counts.measured === 0;
  return (
    <div className="page check-page placement-result">
      <h1>Kết quả đánh giá</h1>
      <p className="muted">
        {minutesText(result.active_ms)} · đo {result.counts.measured} mục
      </p>
      {result.message_vi && (
        <div className="check-banner neutral" role="status">
          {result.message_vi}
        </div>
      )}
      <ul className="placement-counts" aria-label="Tóm tắt">
        <li>
          <strong>{result.counts.measured}</strong> đã đo
        </li>
        <li>
          <strong>{result.counts.likely_known}</strong> có thể đã biết
        </li>
        <li>
          <strong>{result.counts.likely_gap}</strong> cần học
        </li>
        <li>
          <strong>{result.counts.not_assessed}</strong> chưa đo
        </li>
      </ul>

      <section aria-labelledby="pl-map">
        <h2 id="pl-map">Skill map</h2>
        <p className="muted">Số trên chip là điểm đã được gieo từ bài đo; nét đứt là suy luận, chưa có điểm.</p>
        {groupByModule(result.skill_map).map((group) => (
          <div key={group.module} className="skill-group">
            <div className="skill-module">{group.module}</div>
            <div className="skill-chips">
              {group.nodes.map((node) => {
                const chip = skillChip(node);
                return (
                  <span key={node.subtopic_id} className={`skill-chip ${chip.kind}`}>
                    {chip.text}
                  </span>
                );
              })}
            </div>
          </div>
        ))}
      </section>

      <section aria-labelledby="pl-sw">
        <h2 id="pl-sw">Điểm mạnh và phần cần củng cố</h2>
        <p>
          <strong>Làm tốt:</strong>{" "}
          {result.strong_areas.length ? result.strong_areas.map((a) => a.name_vi).join(" · ") : "Chưa có mục nào được đo."}
        </p>
        {[...result.strong_areas, ...result.weak_areas]
          .filter((a) => a.outcome && OUTCOME_NOTE[a.outcome])
          .map((a) => (
            <p key={a.gate} className="muted">
              {a.name_vi}: {OUTCOME_NOTE[a.outcome!]}
            </p>
          ))}
        <p>
          <strong>Cần củng cố:</strong>{" "}
          {result.weak_areas.length
            ? result.weak_areas.map((a) => a.name_vi).join(" · ")
            : "Không có mục nào cần củng cố ngay."}
        </p>
        {result.weak_areas.some((a) => a.retry_after) && (
          <p className="muted">
            Một số mục có thể thử lại sau:{" "}
            {result.weak_areas
              .filter((a) => a.retry_after)
              .map((a) => `${a.name_vi} (${formatRetry(a.retry_after!)})`)
              .join(" · ")}
          </p>
        )}
      </section>

      {result.concept && result.concept.length > 0 && (
        <section aria-labelledby="pl-concept">
          <h2 id="pl-concept">Kiểm tra khái niệm</h2>
          <ul>
            {result.concept.map((c) => (
              <li key={c.gate}>
                {c.name_vi}: <strong>{CONCEPT_OUTCOME_TEXT[c.outcome ?? ""] ?? "chưa đo được"}</strong>
              </li>
            ))}
          </ul>
        </section>
      )}

      <section className="card" aria-labelledby="pl-start">
        <h2 id="pl-start">Bắt đầu từ đây</h2>
        {result.start ? (
          <p>
            <strong>{result.start.name_vi}</strong>{" "}
            <Link className="btn primary" to={`/s/${result.start.subtopic_id}`}>
              Bắt đầu học
            </Link>
          </p>
        ) : (
          <p data-testid="content-pending" role="status">
            Phần nội dung tiếp theo <strong>đang soạn</strong>, chưa có bài học nào để mở từ kết quả này.{" "}
            {noneMeasured
              ? "Bạn vẫn có thể học các mục đã có ở trang chính."
              : "Khi có bài mới, mục “Học tiếp” sẽ tự gợi ý."}
          </p>
        )}
      </section>

      {result.test_out_candidates.length > 0 && (
        <section aria-labelledby="pl-to">
          <h2 id="pl-to">Có thể đã biết: thử test out</h2>
          <ul>
            {result.test_out_candidates.map((sid) => (
              <li key={sid}>
                {names.get(sid) ?? sid}{" "}
                <Link className="btn sm" to={`/check/${sid}?ctx=test_out`}>
                  Test out
                </Link>
              </li>
            ))}
          </ul>
        </section>
      )}

      <div className="toolbar">
        <Link className="btn primary" to="/">
          Bắt đầu học
        </Link>
        <Link className="btn" to="/map">
          Xem Map
        </Link>
        <Link className="btn" to="/profile">
          Xem hồ sơ kỹ năng
        </Link>
      </div>
    </div>
  );
}

function PlacementResultPage({ id }: { id: number }) {
  const navigate = useNavigate();
  const state = useAsync(() => getPlacementResult(id), [id]);
  useEffect(() => {
    if (state.error instanceof ApiError && state.error.code === "placement_skipped") navigate("/", { replace: true });
  }, [state.error, navigate]);
  if (state.loading) {
    return (
      <div className="page" aria-busy="true">
        <div className="skeleton" style={{ width: "50%" }} />
        <div className="skeleton" style={{ width: "90%" }} />
      </div>
    );
  }
  if (state.error || !state.data) {
    return (
      <div className="page error-block" role="alert">
        <strong>Không tải được kết quả</strong>
        <p>{state.error?.message}</p>
        <button className="btn" onClick={state.reload}>
          Thử lại
        </button>{" "}
        <Link className="btn" to="/">
          Về trang chính
        </Link>
      </div>
    );
  }
  if (state.data.status === "in_progress") {
    return (
      <div className="page check-page">
        <section className="card" role="status">
          <h1>Đánh giá chưa kết thúc</h1>
          <Link className="btn primary" to={`/placement/${id}`}>
            Tiếp tục đánh giá
          </Link>
        </section>
      </div>
    );
  }
  return <PlacementResultView result={state.data} />;
}
