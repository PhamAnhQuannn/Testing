import type { SaveStatus } from "../lib/draftStore";
import { CodeEditor } from "./CodeEditor";

export function formatClock(ms: number): string {
  const total = Math.floor(ms / 1000);
  const m = String(Math.floor(total / 60)).padStart(2, "0");
  const s = String(total % 60).padStart(2, "0");
  return `${m}:${s}`;
}

export function SaveChip({ status }: { status: SaveStatus }) {
  let text = "";
  if (status.state === "saving") text = "⟳ Đang lưu";
  else if (status.state === "saved") text = `✓ Đã lưu ${new Date(status.at).toLocaleTimeString("vi-VN")}`;
  else if (status.state === "error") text = "⚠ Chưa lưu được lên server (đã giữ trên máy)";
  return (
    <span className="status-line" role="status">
      {text}
    </span>
  );
}

export function EditorPanel(props: {
  code: string;
  initialCursor?: number;
  onChange: (code: string, cursor: number) => void;
  onRun: () => void;
  onSubmit?: () => void;
  onSave?: () => void;
  onBlur?: () => void;
  onReset: () => void;
  running: boolean;
  runnerLoading: boolean;
  submitDisabledReason?: string;
  hintButton?: { used: number; total: number; onClick: () => void; disabled?: boolean };
  status: SaveStatus;
  elapsed?: string;
  height?: number;
}) {
  const busy = props.running || props.runnerLoading;
  return (
    <>
      <CodeEditor
        value={props.code}
        initialCursor={props.initialCursor}
        onChange={props.onChange}
        onRun={props.onRun}
        onSubmit={props.onSubmit}
        onSave={props.onSave}
        onBlur={props.onBlur}
        minHeight={props.height ?? 280}
      />
      <div className="toolbar">
        <button className="btn sm primary" onClick={props.onRun} disabled={busy} title="Ctrl/Cmd+Enter">
          {props.runnerLoading ? "Đang chuẩn bị…" : "▶ Run"}
        </button>
        {props.onSubmit && (
          <button
            className="btn sm"
            onClick={props.onSubmit}
            disabled={busy || Boolean(props.submitDisabledReason)}
            title={props.submitDisabledReason ?? "Ctrl/Cmd+Shift+Enter"}
          >
            ✔ Submit
          </button>
        )}
        {props.hintButton && (
          <button
            className="btn sm"
            onClick={props.hintButton.onClick}
            disabled={props.hintButton.disabled || props.hintButton.used >= props.hintButton.total}
          >
            💡 Gợi ý {props.hintButton.used}/{props.hintButton.total}
          </button>
        )}
        <button className="btn sm ghost" onClick={props.onReset} aria-label="Reset về starter">
          ⟲ Reset
        </button>
        <span className="grow" />
        {props.elapsed && <span className="status-line">⏱ {props.elapsed}</span>}
        <SaveChip status={props.status} />
      </div>
    </>
  );
}
