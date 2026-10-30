import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ApiError, newIdempotencyKey, startPlacement } from "../lib/api";
import { useToast } from "./Toast";

export type Experience = "none" | "some" | "solid";

const OPTIONS: { v: Experience; label: string }[] = [
  { v: "none", label: "Mới bắt đầu" },
  { v: "some", label: "Biết ít (đã học cú pháp)" },
  { v: "solid", label: "Khá (đã giải bài LeetCode easy)" },
];

const errText = (e: unknown) =>
  e instanceof ApiError && e.isNetwork ? "Server chưa chạy nên chưa thực hiện được." : (e as Error).message;

/**
 * Start a fresh placement sitting at the chosen level ("Đánh giá lại" = redo), abandoning any
 * in-progress sitting (`restart: true`) so the picked experience always applies. Abandoning only
 * flips the old session's status; its measured check_results stay as evidence, so scores — which
 * are recomputed from that append-only evidence — are never lowered by a re-assessment.
 * Toast on failure, navigate on success. Returns true on success.
 */
export async function runReassess(
  experience: Experience,
  deps: { navigate: (to: string) => void; notify: (text: string, o?: { kind?: "info" | "error" }) => void },
): Promise<boolean> {
  try {
    const view = await startPlacement({ experience, restart: true }, newIdempotencyKey());
    deps.navigate(`/placement/${view.placement_id}`);
    return true;
  } catch (e) {
    deps.notify(errText(e), { kind: "error" });
    return false;
  }
}

export function ReassessModal({
  value,
  busy,
  onChange,
  onStart,
  onClose,
}: {
  value: Experience;
  busy: boolean;
  onChange: (v: Experience) => void;
  onStart: () => void;
  onClose: () => void;
}) {
  const cancelRef = useRef<HTMLButtonElement>(null);
  const onCloseRef = useRef(onClose);
  // A backdrop close counts only when the press STARTED on the backdrop too, so a text-selection
  // drag that begins inside the dialog and ends on the backdrop does not discard the choice.
  const downOnBackdrop = useRef(false);
  useEffect(() => {
    onCloseRef.current = onClose;
  });
  useEffect(() => {
    cancelRef.current?.focus();
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") onCloseRef.current();
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, []);
  return (
    <div
      className="modal-backdrop"
      onMouseDown={(event) => {
        downOnBackdrop.current = event.target === event.currentTarget;
      }}
      onMouseUp={(event) => {
        if (downOnBackdrop.current && event.target === event.currentTarget) onClose();
      }}
    >
      <div className="modal" role="dialog" aria-modal="true" aria-label="Đánh giá lại năng lực">
        <h3 style={{ marginTop: 0 }}>Đánh giá lại năng lực</h3>
        <fieldset>
          <legend>Mức kinh nghiệm</legend>
          {OPTIONS.map((o) => (
            <label key={o.v} style={{ display: "block" }}>
              <input
                type="radio"
                name="reassess-experience"
                value={o.v}
                checked={value === o.v}
                onChange={() => onChange(o.v)}
              />{" "}
              {o.label}
            </label>
          ))}
        </fieldset>
        <p className="muted">Làm lại không xoá tiến độ đã học; điểm chỉ cập nhật nếu bạn làm tốt hơn.</p>
        <div className="actions">
          <button ref={cancelRef} className="btn" onClick={onClose}>
            Huỷ
          </button>
          <button className="btn primary" data-testid="reassess-start" onClick={onStart} disabled={busy}>
            Bắt đầu đánh giá
          </button>
        </div>
      </div>
    </div>
  );
}

export default function ReassessButton({ experience }: { experience: Experience }) {
  const navigate = useNavigate();
  const notify = useToast();
  const triggerRef = useRef<HTMLButtonElement>(null);
  const inFlight = useRef(false); // survives close/reopen, so a second Start can't fire a 2nd request
  const [open, setOpen] = useState(false);
  const [choice, setChoice] = useState<Experience>(experience);
  const [busy, setBusy] = useState(false);

  const close = () => {
    setOpen(false);
    triggerRef.current?.focus(); // return focus to the opener (the dialog had taken it)
  };

  const start = async () => {
    if (inFlight.current) return;
    inFlight.current = true;
    setBusy(true);
    const ok = await runReassess(choice, { navigate, notify });
    inFlight.current = false;
    if (!ok) setBusy(false); // on success the route changes; keep the button locked until then
  };

  return (
    <>
      <button
        ref={triggerRef}
        className="btn sm ghost"
        data-testid="reassess-open"
        onClick={() => {
          setChoice(experience); // preselect the saved level each time it opens
          setBusy(inFlight.current); // still locked if a request from a prior open is running
          setOpen(true);
        }}
      >
        Đánh giá lại năng lực
      </button>
      {open && (
        <ReassessModal
          value={choice}
          busy={busy}
          onChange={setChoice}
          onStart={() => void start()}
          onClose={close}
        />
      )}
    </>
  );
}
