/// <reference lib="webworker" />
// Pyodide worker: loads the self-hosted runtime, writes the shared harness.py into the Pyodide
// file system and `pyimport`s it, then runs one test at a time, posting a result after each.
// The main thread owns the watchdog: an infinite loop here blocks this thread by design and the
// main thread terminates the whole worker.
import harnessSource from "./harness.py?raw";
import type { FromWorker, ToWorker } from "./protocol";

interface PyodideInterface {
  FS: { mkdirTree(path: string): void; writeFile(path: string, data: string): void };
  globals: { set(name: string, value: unknown): void };
  runPython(code: string): unknown;
}
type LoadPyodide = (options: { indexURL: string }) => Promise<PyodideInterface>;

const ctx = self as unknown as DedicatedWorkerGlobalScope;
const post = (message: FromWorker) => ctx.postMessage(message);

const base = `${import.meta.env.BASE_URL}pyodide/`;

const STEP = `
def _prep_run(request_json):
    global _gen
    request = json.loads(request_json)
    _gen = harness.run_tests(request["code"], request["io"], request["tests"])

def _next_result():
    result = next(_gen, None)
    return None if result is None else harness.encode_result(result)
`;

async function boot(): Promise<PyodideInterface> {
  const module = (await import(/* @vite-ignore */ `${base}pyodide.mjs`)) as {
    loadPyodide: LoadPyodide;
  };
  const pyodide = await module.loadPyodide({ indexURL: base });
  pyodide.FS.mkdirTree("/harness");
  pyodide.FS.writeFile("/harness/harness.py", harnessSource);
  pyodide.runPython(`
import sys, json
sys.path.insert(0, "/harness")
import harness
`);
  pyodide.runPython(STEP);
  return pyodide;
}

const booted = boot();
booted.then(
  () => post({ type: "ready" }),
  (error: unknown) => post({ type: "init-error", message: String(error) }),
);

ctx.onmessage = async (event: MessageEvent<ToWorker>) => {
  const request = event.data;
  if (request.type !== "run") return;
  const { runId } = request;
  try {
    const pyodide = await booted;
    pyodide.globals.set("_request_json", JSON.stringify(request));
    pyodide.runPython("_prep_run(_request_json)");
    for (;;) {
      const line = pyodide.runPython("_next_result()") as string | undefined | null;
      if (line == null) break;
      post({ type: "progress", runId, result: JSON.parse(line) });
    }
    post({ type: "done", runId });
  } catch (error) {
    post({ type: "error", runId, message: String(error) });
  }
};
