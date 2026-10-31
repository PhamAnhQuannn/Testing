import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ApiError, getOnboarding, newIdempotencyKey, putProfile, startPlacement, type Profile } from "../lib/api";
import { useRunnerState } from "../lib/hooks";
import { defaultTz, profilePayload, type ProfileDraft } from "../lib/onboarding";
import type { RunnerState } from "../runner/pyodide/PyodideRunner";

const PYODIDE_TEXT: Record<RunnerState, string> = {
  loading: "Đang chuẩn bị trình chạy code…",
  ready: "Trình chạy code đã sẵn sàng ✓",
  error: "Không tải được trình chạy code. Bạn vẫn đọc được bài học không cần chạy code; tải lại trang để thử lại.",
};

export function IntroStep({ runner, onNext }: { runner: RunnerState; onNext: () => void }) {
  return (
    <section aria-labelledby="w1">
      <h1 id="w1">Chào bạn. Prep App giúp bạn học, luyện và ôn phỏng vấn.</h1>
      <ul>
        <li>Tự chọn nhịp, không có định mức hay thông báo trễ</li>
        <li>Điểm 0-3 chỉ lên khi có bài làm được đo, không tự chấm</li>
        <li>Dữ liệu nằm trên máy bạn (data/app.db), có backup tự động</li>
      </ul>
      <p data-testid="pyodide-status" className={runner === "error" ? "error-block" : "muted"} role="status">
        {PYODIDE_TEXT[runner]}
      </p>
      <button className="btn primary" onClick={onNext}>
        Tiếp
      </button>
    </section>
  );
}

function Radio({
  legend,
  name,
  value,
  options,
  onChange,
}: {
  legend: string;
  name: string;
  value: string;
  options: { v: string; label: string; disabled?: boolean }[];
  onChange: (v: string) => void;
}) {
  return (
    <fieldset>
      <legend>{legend}</legend>
      {options.map((o) => (
        <label key={o.v} style={{ marginRight: "1rem" }}>
          <input
            type="radio"
            name={name}
            value={o.v}
            checked={value === o.v}
            disabled={o.disabled}
            onChange={() => onChange(o.v)}
          />{" "}
          {o.label}
        </label>
      ))}
    </fieldset>
  );
}

export function ProfileStep({
  draft,
  onChange,
  onBack,
  onSubmit,
  busy,
  error,
}: {
  draft: ProfileDraft;
  onChange: (d: ProfileDraft) => void;
  onBack: () => void;
  onSubmit: () => void;
  busy: boolean;
  error: string | null;
}) {
  const set = (k: keyof ProfileDraft, v: string) => onChange({ ...draft, [k]: v } as ProfileDraft);
  return (
    <form
      aria-labelledby="w2"
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit();
      }}
    >
      <h2 id="w2">Hồ sơ ngắn</h2>
      <Radio
        legend="Mục tiêu"
        name="target_role"
        value={draft.target_role}
        onChange={(v) => set("target_role", v)}
        options={[
          { v: "intern", label: "Intern" },
          { v: "fresher", label: "Fresher" },
          { v: "junior", label: "Junior" },
          { v: "senior", label: "Senior" },
        ]}
      />
      <Radio
        legend="Track"
        name="track"
        value={draft.track}
        onChange={(v) => set("track", v)}
        options={[
          { v: "swe", label: "SWE" },
          { v: "ai", label: "AI engineer" },
        ]}
      />
      <p className="muted">
        Cả hai track học chung nền tảng Python + DSA; SWE có thêm System Design, AI engineer có thêm
        track LLM (RAG, agent, eval/serving). Track chỉ đổi vòng đích hiển thị, không đổi thứ tự học.
      </p>
      <Radio
        legend="Ngôn ngữ"
        name="language"
        value={draft.language}
        onChange={(v) => set("language", v)}
        options={[
          { v: "python", label: "Python" },
          { v: "java", label: "Java (sắp có, M5)", disabled: true },
        ]}
      />
      <Radio
        legend="Kinh nghiệm"
        name="experience"
        value={draft.experience}
        onChange={(v) => set("experience", v)}
        options={[
          { v: "none", label: "Mới bắt đầu" },
          { v: "some", label: "Biết ít (đã học cú pháp)" },
          { v: "solid", label: "Khá (đã giải bài LeetCode easy)" },
        ]}
      />
      <p>
        <label>
          Tên hiển thị{" "}
          <input value={draft.display_name} maxLength={60} onChange={(e) => set("display_name", e.target.value)} />
        </label>{" "}
        <label>
          Múi giờ <input value={draft.tz} onChange={(e) => set("tz", e.target.value)} />
        </label>
      </p>
      {error && (
        <div className="error-block" role="alert">
          {error}
        </div>
      )}
      <button type="button" className="btn" onClick={onBack}>
        Quay lại
      </button>{" "}
      <button type="submit" className="btn primary" disabled={busy || !draft.experience}>
        Tiếp
      </button>
    </form>
  );
}

export function StartStep({
  experience,
  onSkip,
  onPlacement,
  onRestart,
  resume = false,
  busy,
  error,
}: {
  experience: ProfileDraft["experience"];
  onSkip: () => void;
  /** Start (or resume) the placement sitting. */
  onPlacement: () => void;
  /** Only offered when a sitting is already in progress: abandon it and start over. */
  onRestart?: () => void;
  resume?: boolean;
  busy: boolean;
  error: string | null;
}) {
  return (
    <section aria-labelledby="w3">
      <h2 id="w3">Chọn cách bắt đầu</h2>
      <div className="toolbar" style={{ alignItems: "stretch", gap: "1rem" }}>
        <div className="card">
          <h3>Đánh giá trình độ</h3>
          <p className="muted">~30-45 phút, bắt đầu bằng vài câu hỏi kiến thức nhanh rồi chuyển sang code; dừng/tiếp tục được, bỏ qua phần bạn đã biết.</p>
          <button className={`btn${experience === "none" ? "" : " primary"}`} onClick={onPlacement} disabled={busy}>
            {resume ? "Tiếp tục đánh giá" : "Đánh giá trình độ"}
          </button>
          {resume && onRestart && (
            <>
              {" "}
              <button className="btn" onClick={onRestart} disabled={busy}>
                Làm lại từ đầu
              </button>
            </>
          )}
        </div>
        <div className="card">
          <h3>Bắt đầu từ đầu</h3>
          <p className="muted">Vào mục đầu của plan, đi theo thứ tự.</p>
          <button className={`btn${experience === "none" ? " primary" : ""}`} onClick={onSkip} disabled={busy}>
            Bắt đầu từ đầu
          </button>
        </div>
      </div>
      {error && (
        <div className="error-block" role="alert">
          {error}
        </div>
      )}
    </section>
  );
}

export default function Welcome() {
  const navigate = useNavigate();
  const runner = useRunnerState();
  const [step, setStep] = useState(1);
  const [draft, setDraft] = useState<ProfileDraft>({
    target_role: "intern",
    track: "swe",
    language: "python",
    experience: "",
    display_name: "",
    tz: defaultTz(),
  });
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [resume, setResume] = useState(false);
  const key = useRef(newIdempotencyKey());

  // Reopening mid-way resumes at the right step; an already-finished onboarding goes home.
  useEffect(() => {
    getOnboarding()
      .then((o) => {
        if (o.profile_done) {
          if (o.placement === "none") setStep(3);
          else if (o.placement === "in_progress") {
            setResume(true); // flow H: offer to continue the sitting
            setStep(3);
          } else navigate("/", { replace: true });
        }
      })
      .catch(() => undefined);
  }, [navigate]);

  const save = async (body: Partial<Profile>, then: () => void) => {
    setBusy(true);
    setError(null);
    try {
      await putProfile(body, key.current);
      key.current = newIdempotencyKey();
      then();
    } catch (e) {
      setError(
        e instanceof ApiError && e.isNetwork
          ? "Server chưa chạy. Chạy `docker compose up` rồi thử lại."
          : `Không lưu được hồ sơ: ${(e as Error).message}`,
      );
    } finally {
      setBusy(false);
    }
  };

  const beginPlacement = async (restart: boolean) => {
    setBusy(true);
    setError(null);
    try {
      const view = await startPlacement(restart ? { restart: true } : {}, newIdempotencyKey());
      navigate(`/placement/${view.placement_id}`, { replace: true });
    } catch (e) {
      setError(
        e instanceof ApiError && e.isNetwork
          ? "Server chưa chạy. Chạy `docker compose up` rồi thử lại."
          : `Không bắt đầu được đánh giá: ${(e as Error).message}`,
      );
    } finally {
      setBusy(false);
    }
  };

  const payload = profilePayload(draft);
  return (
    <div className="page welcome">
      {step === 1 && <IntroStep runner={runner} onNext={() => setStep(2)} />}
      {step === 2 && (
        <ProfileStep
          draft={draft}
          onChange={setDraft}
          onBack={() => setStep(1)}
          busy={busy}
          error={error}
          onSubmit={() => payload && save(payload, () => setStep(3))}
        />
      )}
      {step === 3 && (
        <StartStep
          experience={draft.experience}
          busy={busy}
          error={error}
          resume={resume}
          onPlacement={() => void beginPlacement(false)}
          onRestart={() => void beginPlacement(true)}
          onSkip={() => save({ placement: "skipped" }, () => navigate("/", { replace: true }))}
        />
      )}
    </div>
  );
}
