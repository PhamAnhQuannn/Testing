// Copies the pinned Pyodide core (npm package `pyodide`, exact version in package.json and the
// lockfile) into public/pyodide/ so the app self-hosts it (CSP connect-src 'self'; SPEC 6.2).
// The numpy/pandas wheels are downloaded from the jsDelivr Pyodide CDN at build time (runtime stays
// self-hosted). The directory is gitignored: no binaries in git, `npm ci` + this script reproduce it.
import {
  copyFileSync,
  existsSync,
  mkdirSync,
  readdirSync,
  readFileSync,
  renameSync,
  unlinkSync,
  writeFileSync,
} from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const source = join(root, "node_modules", "pyodide");
const target = join(root, "public", "pyodide");
const files = [
  "pyodide.mjs",
  "pyodide.asm.js",
  "pyodide.asm.wasm",
  "python_stdlib.zip",
  "pyodide-lock.json",
];
const wheels = [
  "numpy-2.2.5-cp313-cp313-pyemscripten_2025_0_wasm32.whl",
  "pandas-2.3.3-cp313-cp313-pyemscripten_2025_0_wasm32.whl",
  "python_dateutil-2.9.0.post0-py2.py3-none-any.whl",
  "pytz-2025.2-py2.py3-none-any.whl",
  "six-1.17.0-py2.py3-none-any.whl",
];

async function fetchWheels(version) {
  for (const name of wheels) {
    const file = join(target, name);
    if (existsSync(file)) continue;
    const url = `https://cdn.jsdelivr.net/pyodide/v${version}/full/${name}`;
    const response = await fetch(url);
    if (!response.ok) {
      console.error(`download failed (${response.status}): ${url}`);
      process.exit(1);
    }
    // Write-then-rename so an interrupted download never leaves a truncated .whl that the
    // existsSync check above would later skip.
    writeFileSync(`${file}.tmp`, Buffer.from(await response.arrayBuffer()));
    renameSync(`${file}.tmp`, file);
    console.log(`downloaded ${name}`);
  }
}

if (!existsSync(source)) {
  console.error("node_modules/pyodide not found: run `npm ci` first");
  process.exit(1);
}
const { version } = JSON.parse(readFileSync(join(source, "package.json"), "utf8"));
const stamp = join(target, "VERSION");
const upToDate = existsSync(stamp) && readFileSync(stamp, "utf8").trim() === version;
mkdirSync(target, { recursive: true });
if (upToDate) {
  await fetchWheels(version); // fills in any wheel that is missing
  console.log(`pyodide ${version} already in public/pyodide`);
  process.exit(0);
}
for (const name of files) copyFileSync(join(source, name), join(target, name));
// A new version invalidates previously downloaded wheels: they belong to the old release.
for (const name of readdirSync(target)) if (name.endsWith(".whl")) unlinkSync(join(target, name));
await fetchWheels(version);
writeFileSync(stamp, `${version}\n`);
console.log(`pyodide ${version}: copied ${files.length} files to public/pyodide`);
