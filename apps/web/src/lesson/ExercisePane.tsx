import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { ConfirmModal } from "../components/Modal";
import { EditorPanel } from "../components/EditorPanel";
import { Markdown } from "../components/Markdown";
import { TestResultPanel, type PanelState } from "../components/TestResultPanel";
import type { LessonBlock } from "../lib/api";
import { DraftController, type Draft, type SaveStatus } from "../lib/draftStore";
import { useRunnerState } from "../lib/hooks";
import { idbStore } from "../lib/idb";
import { buildPanel } from "../lib/runView";
import { getRunner } from "../runner";
import type { RunResult, TestCase } from "../runner/Runner";

type Exercise = Extract<LessonBlock, { type: "code_exercise" }>;

/** Right-hand pane of the lesson split view: the active code_exercise, same Runner as problems. */
export function ExercisePane({
  subtopicId,
  block,
  onPassed,
}: {
  subtopicId: string;
  block: Exercise;
  onPassed: (blockId: string) => void;
}) {
  const runnerState = useRunnerState();
  const [code, setCode] = useState<string | null>(null);
  const [cursor, setCursor] = useState(0);
  const [status, setStatus] = useState<SaveStatus>({ state: "idle" });
  const [panel, setPanel] = useState<PanelState | null>(null);
  const [running, setRunning] = useState(false);
  const [hint, setHint] = useState(false);
  const [solution, setSolution] = useState(false);
  const [confirm, setConfirm] = useState<"solution" | "reset" | null>(null);
  const codeRef = useRef("");

  const controller = useMemo(
    () =>
      new DraftController({
        key: `ex:${subtopicId}:${block.id}`,
        local: idbStore<Draft>("drafts"),
        onStatus: setStatus,
      }),
    [subtopicId, block.id],
  );
  useEffect(() => {
    let alive = true;
    controller.load(null).then((draft) => {
      if (!alive) return;
      codeRef.current = draft?.code ?? block.starter;
      setCursor(draft?.cursor ?? 0);
      setCode(codeRef.current);
    });
    return () => {
      alive = false;
      void controller.flush();
    };
  }, [controller, block.starter]);

  const tests: TestCase[] = useMemo(
    () => block.tests.map((t, i) => ({ id: `t${i + 1}`, args: t.args, expected: t.expected })),
    [block.tests],
  );

  const run = useCallback(async () => {
    if (running) return;
    setRunning(true);
    await controller.flush();
    const options = { hidden: false, label: (_t: TestCase | undefined, i: number) => `Test ${i + 1}` };
    const seen: RunResult["results"] = [];
    try {
      const result = await getRunner().run({
        code: codeRef.current,
        io: { mode: "function", entry: block.entry, params: [], compare: "exact" },
        tests,
        limits: { time_ms: 1000, memory_mb: 256, time_multiplier: 3 },
        onProgress: (r) => {
          seen.push(r);
          setPanel(buildPanel("run", tests, seen, options, true));
        },
      });
      setPanel(buildPanel("run", tests, result.results, options, false, result));
      if (result.verdict === "AC") onPassed(block.id);
    } catch (error) {
      setPanel({
        kind: "run",
        rows: [{ label: "Runner", verdict: "RE", error: (error as Error).message }],
        total: tests.length,
        running: false,
        verdict: "RE",
        stdout: "",
        stderr: "",
      });
    } finally {
      setRunning(false);
    }
  }, [running, controller, block.entry, block.id, tests, onPassed]);

  return (
    <>
      <div className="toolbar">
        <strong>Bài tập: {block.entry}()</strong>
      </div>
      <Markdown md={block.md} />
      {code === null ? (
        <div className="skeleton" style={{ height: 160 }} />
      ) : (
        <EditorPanel
          code={code}
          initialCursor={cursor}
          height={200}
          onChange={(next, at) => {
            codeRef.current = next;
            controller.update(next, at);
          }}
          onRun={() => void run()}
          onSave={() => void controller.flush()}
          onBlur={() => void controller.flush()}
          onReset={() => setConfirm("reset")}
          running={running}
          runnerLoading={runnerState === "loading"}
          hintButton={{ used: hint ? 1 : 0, total: 1, onClick: () => setHint(true) }}
          status={status}
        />
      )}
      {hint && (
        <div className="callout tip">
          <div className="label">Gợi ý</div>
          <Markdown md={block.hint_md} />
        </div>
      )}
      <TestResultPanel state={panel} />
      {block.solution && (
        <div className="toolbar">
          <button className="btn sm" onClick={() => (solution ? setSolution(false) : setConfirm("solution"))}>
            {solution ? "Ẩn lời giải" : "Xem lời giải"}
          </button>
        </div>
      )}
      {solution && block.solution && <pre className="output">{block.solution}</pre>}
      {confirm === "solution" && (
        <ConfirmModal
          title="Xem lời giải?"
          confirmLabel="Vẫn xem"
          onCancel={() => setConfirm(null)}
          onConfirm={() => {
            setSolution(true);
            setConfirm(null);
          }}
        >
          <p>Thử thêm một lần nữa trước khi xem? Bài nhỏ trong lesson không tính điểm.</p>
        </ConfirmModal>
      )}
      {confirm === "reset" && (
        <ConfirmModal
          title="Reset về starter?"
          confirmLabel="Reset"
          onCancel={() => setConfirm(null)}
          onConfirm={() => {
            codeRef.current = block.starter;
            setCode(block.starter);
            controller.update(block.starter, 0);
            setConfirm(null);
          }}
        >
          <p>Code hiện tại sẽ bị thay bằng khung code ban đầu.</p>
        </ConfirmModal>
      )}
    </>
  );
}
