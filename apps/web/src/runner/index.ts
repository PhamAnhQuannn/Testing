import { PyodideRunner } from "./pyodide/PyodideRunner";
import type { WorkerLike } from "./pyodide/protocol";
import type { Runner } from "./Runner";

export type { Runner } from "./Runner";

let instance: PyodideRunner | null = null;

/** Lazily created singleton; the worker starts booting Pyodide in the background on first use. */
export function getRunner(): PyodideRunner {
  instance ??= new PyodideRunner(
    () =>
      new Worker(new URL("./pyodide/worker.ts", import.meta.url), {
        type: "module",
      }) as unknown as WorkerLike,
  );
  return instance;
}

export function getPythonRunner(): Runner {
  return getRunner();
}
