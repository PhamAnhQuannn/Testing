// Downloads the numpy/pandas wheels (and their pure-Python deps) matching the pinned Pyodide into
// node_modules/pyodide/, the default indexURL of loadPyodide, so `loadPackage(["numpy","pandas"])`
// works offline afterwards. Runs as the `postinstall` of this package; node_modules is gitignored.
import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

export const WHEELS = [
  "numpy-2.2.5-cp313-cp313-pyemscripten_2025_0_wasm32.whl",
  "pandas-2.3.3-cp313-cp313-pyemscripten_2025_0_wasm32.whl",
  "python_dateutil-2.9.0.post0-py2.py3-none-any.whl",
  "pytz-2025.2-py2.py3-none-any.whl",
  "six-1.17.0-py2.py3-none-any.whl",
];

const target = join(dirname(fileURLToPath(import.meta.url)), "node_modules", "pyodide");
if (!existsSync(join(target, "package.json"))) {
  console.error("node_modules/pyodide not found: run `npm ci` first");
  process.exit(1);
}
const { version } = JSON.parse(readFileSync(join(target, "package.json"), "utf8"));
mkdirSync(target, { recursive: true });
for (const name of WHEELS) {
  const file = join(target, name);
  if (existsSync(file)) continue;
  const url = `https://cdn.jsdelivr.net/pyodide/v${version}/full/${name}`;
  const response = await fetch(url);
  if (!response.ok) {
    console.error(`download failed (${response.status}): ${url}`);
    process.exit(1);
  }
  // Write-then-rename: an interrupted download must not leave a truncated .whl behind.
  writeFileSync(`${file}.tmp`, Buffer.from(await response.arrayBuffer()));
  renameSync(`${file}.tmp`, file);
  console.log(`pyodide ${version}: downloaded ${name}`);
}
console.log(`pyodide ${version}: ${WHEELS.length} wheels present in node_modules/pyodide`);
