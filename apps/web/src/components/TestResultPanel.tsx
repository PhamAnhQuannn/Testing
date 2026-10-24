import { useState } from "react";
import type { Verdict } from "../runner/Runner";

export interface ResultRow {
  label: string;
  verdict: Verdict | "PENDING";
  input?: string;
  expected?: string;
  got?: string;
  error?: string;
  stdout?: string;
  elapsed_ms?: number;
  /** Hidden tests only show the name unless the test is small. */
  hidden?: boolean;
}

export interface PanelState {
  kind: "run" | "submit";
  rows: ResultRow[];
  total: number;
  running: boolean;
  verdict: Verdict | null;
  elapsed_ms?: number;
  stdout: string;
  stderr: string;
  note?: string;
}

const VERDICT_TEXT: Record<Verdict, string> = {
  AC: "Accepted",
  WA: "Sai kết quả",
  TLE: "Quá thời gian",
  RE: "Lỗi lúc chạy",
  CE: "Lỗi cú pháp",
};
const ICON: Record<string, string> = { AC: "✔", WA: "✘", TLE: "⏱", RE: "✘", CE: "✘", PENDING: "…" };

export function show(value: unknown): string {
  if (typeof value === "string") return JSON.stringify(value);
  return JSON.stringify(value) ?? "None";
}

export function TestResultPanel({ state }: { state: PanelState | null }) {
  const [tab, setTab] = useState<"result" | "stdout" | "stderr">("result");
  const [open, setOpen] = useState<Record<number, boolean>>({});
  if (!state) {
    return (
      <section className="results" aria-label="Kết quả">
        <div className="empty">Bấm Run (Ctrl+Enter) để chạy các test mẫu.</div>
      </section>
    );
  }
  const passed = state.rows.filter((r) => r.verdict === "AC").length;
  const summary = state.running
    ? `Đang chạy… ${state.rows.length}/${state.total}`
    : `${passed}/${state.total} test qua`;
  const prefix = state.kind === "submit" ? "Submit" : "Run";
  return (
    <section className="results" aria-label="Kết quả">
      <header>
        {state.verdict && (
          <span className={`chip ${state.verdict}`}>
            {ICON[state.verdict]} {state.verdict} · {VERDICT_TEXT[state.verdict]}
          </span>
        )}
        <strong>
          {prefix}: {summary}
        </strong>
        {state.elapsed_ms !== undefined && !state.running && (
          <span className="muted">{state.elapsed_ms} ms</span>
        )}
        <div className="tabs-mini" role="tablist">
          {(["result", "stdout", "stderr"] as const).map((name) => (
            <button
              key={name}
              role="tab"
              aria-selected={tab === name}
              onClick={() => setTab(name)}
            >
              {name === "result" ? "Kết quả" : name}
            </button>
          ))}
        </div>
      </header>
      <div className="sr-only" aria-live="polite" style={{ position: "absolute", left: -9999 }}>
        {!state.running && `${passed} trên ${state.total} test qua`}
      </div>
      {state.note && <div className="detail muted" style={{ paddingTop: 8 }}>{state.note}</div>}
      {tab === "result" && (
        <ul className="tests">
          {state.rows.map((row, i) => {
            const failed = row.verdict !== "AC";
            const expandable = failed && !row.hidden || (failed && row.input !== undefined);
            return (
              <li key={i}>
                <button
                  aria-expanded={expandable ? (open[i] ?? true) : undefined}
                  onClick={() => expandable && setOpen({ ...open, [i]: !(open[i] ?? true) })}
                >
                  <span className={`chip ${row.verdict === "PENDING" ? "neutral" : row.verdict}`}>
                    {ICON[row.verdict]} {row.verdict}
                  </span>
                  <span>{row.label}</span>
                  {row.verdict === "TLE" && <span className="muted">Quá thời gian ở test {row.label}</span>}
                  {row.elapsed_ms !== undefined && row.verdict !== "TLE" && (
                    <span className="muted">{row.elapsed_ms} ms</span>
                  )}
                </button>
                {expandable && (open[i] ?? true) && (
                  <div className="detail">
                    <dl>
                      {row.input !== undefined && (
                        <>
                          <dt>input</dt>
                          <dd>{row.input}</dd>
                        </>
                      )}
                      {row.expected !== undefined && (
                        <>
                          <dt>expected</dt>
                          <dd>{row.expected}</dd>
                        </>
                      )}
                      {row.got !== undefined && (
                        <>
                          <dt>got</dt>
                          <dd>{row.got}</dd>
                        </>
                      )}
                      {row.error && (
                        <>
                          <dt>lỗi</dt>
                          <dd>{row.error}</dd>
                        </>
                      )}
                      {row.stdout && (
                        <>
                          <dt>stdout</dt>
                          <dd>{row.stdout}</dd>
                        </>
                      )}
                    </dl>
                  </div>
                )}
              </li>
            );
          })}
        </ul>
      )}
      {tab === "stdout" && <pre>{state.stdout || "(không có stdout)"}</pre>}
      {tab === "stderr" && <pre>{state.stderr || "(không có stderr)"}</pre>}
    </section>
  );
}
