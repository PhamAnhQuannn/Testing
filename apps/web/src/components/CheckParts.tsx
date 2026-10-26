// Presentational pieces of the mastery check (S8). No data fetching here; CheckPage owns the flow.
import { useState } from "react";
import { Link } from "react-router-dom";
import type { CheckOutcome, CheckScore, CheckStep, CheckStepResult } from "../lib/api";
import { formatRetry, LEVEL_TEXT, outcomeView, stepResultView } from "../lib/checkFlow";
import { Markdown } from "./Markdown";

export function Stepper({ step, results }: { step: CheckStep; results: CheckStepResult[] }) {
  return (
    <ol className="check-stepper" aria-label="Tiến độ kiểm tra">
      {results.map((r) => (
        <li key={r.item_id} className={`done ${r.gave_up ? "neutral" : r.correct ? "ok" : "bad"}`}>
          {LEVEL_TEXT[r.level] ?? `Mức ${r.level}`} · {r.gave_up ? "bỏ qua" : r.correct ? "đúng" : "sai"}
        </li>
      ))}
      <li className="current" aria-current="step">
        {LEVEL_TEXT[step.level] ?? `Mức ${step.level}`} · bước {results.length + 1}
      </li>
    </ol>
  );
}

export function ResultBanner({ result }: { result: CheckStepResult }) {
  const view = stepResultView(result);
  return (
    <div className={`check-banner ${view.tone}`} role="status">
      <strong>{view.title}</strong>
      {view.detail.map((line, i) => (
        <div key={i}>{line}</div>
      ))}
    </div>
  );
}

export function ReadCodeStep(props: {
  step: CheckStep;
  busy: boolean;
  onAnswer: (answer: string) => void;
}) {
  const [answer, setAnswer] = useState("");
  return (
    <section className="card" aria-label="Đọc code">
      <Markdown md={props.step.prompt_md} />
      <pre className="output" aria-label="Code cần đọc">
        {props.step.code}
      </pre>
      <label htmlFor="check-read-answer">
        <strong>Output dự đoán</strong>
      </label>
      <textarea
        id="check-read-answer"
        className="check-answer"
        rows={4}
        value={answer}
        spellCheck={false}
        onChange={(e) => setAnswer(e.target.value)}
      />
      <div className="toolbar">
        <button className="btn primary" disabled={props.busy} onClick={() => props.onAnswer(answer)}>
          Nộp đáp án
        </button>
      </div>
    </section>
  );
}

export function ConceptStep(props: {
  step: CheckStep;
  busy: boolean;
  onGrade: (selfGrade: boolean) => void;
}) {
  const [revealed, setRevealed] = useState(false);
  return (
    <section className="card" aria-label="Câu khái niệm">
      <Markdown md={props.step.prompt_md} />
      {!revealed ? (
        <div className="toolbar">
          <span className="muted">Tự trả lời trong đầu (hoặc viết ra), rồi mở đáp án để tự chấm.</span>
          <span className="grow" />
          <button className="btn primary" onClick={() => setRevealed(true)}>
            Hiện đáp án
          </button>
        </div>
      ) : (
        <>
          <h3>Đáp án</h3>
          <Markdown md={props.step.answer_md ?? ""} />
          <div className="toolbar">
            <strong>Bạn trả lời đúng ý chính?</strong>
            <span className="grow" />
            <button className="btn" disabled={props.busy} onClick={() => props.onGrade(false)}>
              Chưa đúng
            </button>
            <button className="btn primary" disabled={props.busy} onClick={() => props.onGrade(true)}>
              Đúng
            </button>
          </div>
        </>
      )}
    </section>
  );
}

export function LockedCard({ subtopicId, retryAfter, level }: { subtopicId: string; retryAfter: string; level?: number }) {
  return (
    <section className="card check-locked" role="alert">
      <h1>Chưa làm lại được</h1>
      <p>
        {level ? `${LEVEL_TEXT[level] ?? `Mức ${level}`} bị khoá sau một lần trả lời sai. ` : ""}
        Làm lại được sau <strong>{formatRetry(retryAfter)}</strong>.
      </p>
      <p className="muted">Trong lúc chờ bạn có thể ôn lại bài học hoặc luyện thêm bài tập.</p>
      <div className="toolbar">
        <Link className="btn primary" to={`/s/${subtopicId}`}>
          Về bài học
        </Link>
        <Link className="btn" to="/">
          Về trang chính
        </Link>
      </div>
    </section>
  );
}

export function OutcomeCard(props: {
  subtopicId: string;
  outcome: CheckOutcome;
  score?: CheckScore;
  last?: CheckStepResult;
}) {
  const view = outcomeView(props.outcome, props.score);
  return (
    <section className="card check-outcome" aria-label="Kết quả kiểm tra">
      {props.last && <ResultBanner result={props.last} />}
      <div className={`check-banner ${view.tone}`} role="status">
        <h1 style={{ margin: 0 }}>{view.title}</h1>
        {view.lines.map((line, i) => (
          <div key={i}>{line}</div>
        ))}
      </div>
      {view.unlocked.length > 0 && (
        <>
          <h3>Mục vừa mở khoá</h3>
          <div className="chips">
            {view.unlocked.map((id) => (
              <Link key={id} className="subchip" to={`/s/${id}`}>
                {id}
              </Link>
            ))}
          </div>
        </>
      )}
      {view.retryAfter && (
        <p role="alert">
          Làm lại sau <strong>{formatRetry(view.retryAfter)}</strong> (khoá 24 giờ sau câu trả lời sai).
        </p>
      )}
      <div className="toolbar">
        <Link className="btn primary" to={`/s/${props.subtopicId}`}>
          {props.outcome.need_lesson || (!props.outcome.tested_out && view.retryAfter) ? "Về bài học" : "Xong"}
        </Link>
        <Link className="btn" to="/">
          Về trang chính
        </Link>
      </div>
    </section>
  );
}
