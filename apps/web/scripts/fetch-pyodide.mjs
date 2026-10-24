// Copies the pinned Pyodide core (npm package `pyodide`, exact version in package.json and the
// lockfile) into public/pyodide/ so the app self-hosts it (CSP connect-src 'self'; SPEC 6.2).
// The directory is gitignored: no binaries in git, `npm ci` + this script reproduce it.
import { copyFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
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

if (!existsSync(source)) {
  console.error("node_modules/pyodide not found: run `npm ci` first");
  process.exit(1);
}
const { version } = JSON.parse(readFileSync(join(source, "package.json"), "utf8"));
const stamp = join(target, "VERSION");
if (existsSync(stamp) && readFileSync(stamp, "utf8").trim() === version) {
  console.log(`pyodide ${version} already in public/pyodide`);
  process.exit(0);
}
mkdirSync(target, { recursive: true });
for (const name of files) copyFileSync(join(source, name), join(target, name));
writeFileSync(stamp, `${version}\n`);
console.log(`pyodide ${version}: copied ${files.length} files to public/pyodide`);
