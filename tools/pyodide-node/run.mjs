// Run harness.py under Pyodide in Node: the Pyodide half of tools/run_problem.py.
//
//   node run.mjs <path to harness.py>      request JSON on stdin, one result JSON line per test
//
// Same contract as running harness.py as a script, so run_problem.py reads both engines the same
// way. The parent process owns the watchdog and kills this process on a time-limit overrun.
import { readFileSync } from "node:fs";
import { loadPyodide } from "pyodide";

const harnessPath = process.argv[2];
const request = readFileSync(0, "utf8");

// Anything Python writes outside the harness's own redirection must not reach the result channel.
const pyodide = await loadPyodide({ stdout: () => {}, stderr: () => {} });
pyodide.FS.writeFile("/harness.py", readFileSync(harnessPath, "utf8"));
pyodide.globals.set("request_json", request);
pyodide.runPython(`
import json, sys
sys.path.insert(0, "/")
import harness

_request = json.loads(request_json)
_results = harness.run_tests(_request["code"], _request["io"], _request["tests"])

def next_result():
    result = next(_results, None)
    return None if result is None else harness.encode_result(result)
`);
const nextResult = pyodide.globals.get("next_result");
for (let line = nextResult(); line != null; line = nextResult()) {
  process.stdout.write(line + "\n");
}
