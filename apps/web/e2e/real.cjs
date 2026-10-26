// End-to-end acceptance of SPEC 7 M1 against the REAL stack: uvicorn (FastAPI + SQLite in a temp
// data dir, serving apps/web/dist) driven by Chromium + Pyodide. No API mocks.
// Needs `npm run build` first. Usage: `make e2e` (or `node e2e/real.cjs` in apps/web).
// Env: E2E_PYTHON (python with the api deps; default <repo>/.venv/bin/python), E2E_KEEP=1 keeps the temp dir.
const { spawn, execFileSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { chromium } = require("playwright");

const root = path.join(__dirname, "..", "..", "..");
const dist = path.join(root, "apps/web/dist");
const python = process.env.E2E_PYTHON || path.join(root, ".venv/bin/python");
const dictId = "py.datastructs.dict";
const problemId = "ransom-note";
const solution = fs.readFileSync(path.join(root, "content/problems", dictId, problemId, "solution.py"), "utf8");
const lesson = JSON.parse(
  execFileSync(python, ["-c", "import sys,json,yaml;print(json.dumps(yaml.safe_load(open(sys.argv[1]))))", path.join(root, `content/lessons/py/${dictId}.yaml`)], { encoding: "utf8" }),
);
const block = (id) => lesson.blocks.find((b) => b.id === id);

const log = [];
let failed = false;
const t0 = Date.now();
const check = (name, ok, extra = "") => {
  log.push(`${ok ? "PASS" : "FAIL"} ${name}${extra ? "  [" + extra + "]" : ""}`);
  console.log(log[log.length - 1]);
  if (!ok) failed = true;
};
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ------------------------------------------------------------------ server control
const dataDir = fs.mkdtempSync(path.join(os.tmpdir(), "prep-e2e-"));
const port = 18000 + Math.floor(Math.random() * 2000);
const base = `http://127.0.0.1:${port}`;
let server = null;

async function startServer() {
  server = spawn(python, ["-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", String(port), "--workers", "1"], {
    cwd: path.join(root, "apps/api"),
    env: { ...process.env, DATA_DIR: dataDir, WEB_DIST: dist, BACKUP_DIR: path.join(dataDir, "backups") },
    stdio: ["ignore", fs.openSync(path.join(dataDir, "server.log"), "a"), fs.openSync(path.join(dataDir, "server.log"), "a")],
  });
  for (let i = 0; i < 100; i++) {
    try {
      const r = await fetch(`${base}/api/health`);
      if (r.status === 200 || r.status === 503) return r;
    } catch {
      /* not up yet */
    }
    await sleep(100);
  }
  throw new Error("server did not start; see " + path.join(dataDir, "server.log"));
}
const killServer = async (signal = "SIGKILL") => {
  const s = server;
  server = null;
  if (!s) return;
  const exited = new Promise((r) => s.once("exit", r));
  s.kill(signal);
  await exited;
};
const api = async (method, p, body, headers = {}) => {
  const r = await fetch(`${base}/api${p}`, {
    method,
    headers: { "Content-Type": "application/json", ...headers },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  return { status: r.status, headers: r.headers, json: await r.json().catch(() => null) };
};
const sql = (query) =>
  execFileSync(python, ["-c", "import sqlite3,sys;c=sqlite3.connect(sys.argv[1]);print(c.execute(sys.argv[2]).fetchone()[0])", path.join(dataDir, "app.db"), query], { encoding: "utf8" }).trim();

// ------------------------------------------------------------------ main
async function main() {
  const health = await (await startServer()).json();
  check("server up: WAL + synchronous=FULL", health.status === "ok" && health.journal_mode === "wal" && String(health.synchronous) === "2", JSON.stringify(health));

  // static serving: CSP header, MIME, SPA fallback, /api not shadowed
  const html = await fetch(`${base}/s/${dictId}`);
  const csp = html.headers.get("content-security-policy") ?? "";
  check("SPA fallback /s/:id serves index.html with CSP header", html.status === 200 && csp.includes("worker-src 'self'") && csp.includes("'wasm-unsafe-eval'"));
  check("/p/:id and /map fall back too", (await fetch(`${base}/p/${problemId}`)).status === 200 && (await fetch(`${base}/map`)).status === 200);
  const wasm = await fetch(`${base}/pyodide/pyodide.asm.wasm`);
  check(".wasm served as application/wasm", wasm.headers.get("content-type") === "application/wasm");
  check("/api/nope stays a JSON 404", (await api("GET", "/nope")).json?.error?.code === "http_404");

  const browser = await chromium.launch();
  const errors = [];
  const watch = (page) => {
    page.on("pageerror", (e) => errors.push(String(e)));
    page.on("console", (m) => m.type() === "error" && !/Failed to load resource|ERR_CONNECTION|Failed to fetch/.test(m.text()) && errors.push(m.text()));
  };
  const newPage = async (ctx) => {
    const page = await ctx.newPage();
    await page.setViewportSize({ width: 1366, height: 800 });
    watch(page);
    return page;
  };
  const waitVerdict = (page, text, timeout) =>
    page.waitForFunction((t) => document.querySelector(".results header")?.textContent?.includes(t), text, { timeout });
  const setCode = async (page, code, sel = ".cm-content") => {
    await page.click(sel);
    await page.keyboard.press("Control+A");
    await page.keyboard.press("Delete");
    await page.keyboard.insertText(code);
  };
  const editorText = (page) => page.locator(".cm-content").first().innerText();

  try {
    const ctx = await browser.newContext();
    let page = await newPage(ctx);
    const posts = [];
    page.on("request", (r) => r.method() !== "GET" && r.url().includes("/api/") && posts.push({ method: r.method(), path: new URL(r.url()).pathname, key: r.headers()["idempotency-key"] }));

    // ---- map -> lesson
    await page.goto(base);
    await page.waitForSelector(`a[href="/s/${dictId}"]`);
    const chip = page.locator(`a[href="/s/${dictId}"]`);
    check("map lists py.datastructs.dict (score 0)", (await chip.innerText()).trim().startsWith("0"));
    await chip.click();
    await page.waitForSelector(".lesson .block");
    const blocks = await page.locator(".lesson .block").count();
    check(`lesson renders all ${lesson.blocks.length} blocks`, blocks === lesson.blocks.length, String(blocks));

    // ---- read: runnable sample, then quizzes (b12 answered wrong on purpose: quiz_best 0.8)
    await page.locator("#block-b02 button:has-text('Chạy')").click();
    await page.waitForFunction(() => document.body.innerText.includes("Khớp output mong đợi"), null, { timeout: 60000 });
    check("code_sample runs in Pyodide and matches expected_output", true);
    const mcq = async (id, optionText) => {
      const f = page.locator(`#block-${id} fieldset`);
      await f.locator("label", { hasText: optionText }).click();
      await f.locator("button:has-text('Kiểm tra')").click();
      await f.locator("[role=status]").waitFor({ timeout: 5000 });
      return f.locator("[role=status]").innerText();
    };
    check("b04 quiz_mcq correct (graded by server)", (await mcq("b04", "KeyError")).includes("Đúng"));
    let f = page.locator("#block-b06 fieldset");
    await f.locator("input.text-input").fill("get");
    await f.locator("button:has-text('Kiểm tra')").click();
    await f.locator("[role=status]").waitFor({ timeout: 5000 });
    check("b06 quiz_fill correct", (await f.locator("[role=status]").innerText()).includes("Đúng"));
    const predict = async (id, text) => {
      const p = page.locator(`#block-${id} fieldset`);
      await p.locator("textarea").fill(text);
      await p.locator("button:has-text('Kiểm tra')").click();
      await p.locator("[role=status]").waitFor({ timeout: 5000 });
      return p.locator("[role=status]").innerText();
    };
    check("b10 predict_output correct", (await predict("b10", block("b10").expected_output.trim())).includes("Đúng"));
    const wrong = await mcq("b12", "(1, 2)");
    check("b12 wrong answer shows 'Chưa đúng' + explanation", wrong.includes("Chưa đúng") && wrong.length > 20);
    check("b13 predict_output correct", (await predict("b13", block("b13").expected_output.trim())).includes("Đúng"));

    // ---- code_exercise in the lesson
    await page.locator("#block-b14 button:has-text('Làm bài này')").click();
    await page.waitForSelector(".pane.right .cm-content");
    await setCode(page, block("b14").solution, ".pane.right .cm-content");
    await page.keyboard.press("Control+Enter");
    await waitVerdict(page, "test qua", 30000);
    check("code_exercise passes in the lesson editor", (await page.locator("#block-b14").innerText()).includes("Xong"));

    // ---- resume position: move to b10, wait for the 3 s debounce, GET /resume
    await page.locator("#block-b10").click();
    await page.waitForTimeout(3500);
    const resume = (await api("GET", "/resume")).json.primary;
    check("resume saved on the server (block b10)", resume?.mode === "lesson" && resume.ref.block_id === "b10", JSON.stringify(resume?.ref));

    // ---- reload keeps quiz progress and resume position
    await page.reload();
    await page.waitForSelector(".lesson .block");
    await page.waitForFunction(() => document.querySelector(".block.current")?.id === "block-b10", null, { timeout: 5000 }).catch(() => undefined);
    const cur = await page.evaluate(() => document.querySelector(".block.current")?.id);
    check("reload: resume position restored (block b10 current)", cur === "block-b10", String(cur));
    const stateText = await page.locator("#block-b04 fieldset").innerText();
    const stillDisabled = await page.locator("#block-b04 fieldset").evaluate((e) => e.disabled);
    check("reload: answered quiz stays answered (server progress)", stillDisabled && stateText.includes("Đúng"));
    check("reload: wrong answer b12 remembered as wrong", (await page.locator("#block-b12 fieldset").innerText()).includes("Chưa đúng"));
    check("reload: quiz tally 4/5", (await page.locator(".crumbs").innerText()).includes("Quiz 4/5"), (await page.locator(".crumbs").innerText()).replace(/\n/g, " "));

    // ---- complete the lesson: quiz passed (4/5), no problem solved yet -> score 1
    await page.locator("button:has-text('Hoàn thành bài học')").click();
    await page.waitForSelector("text=Đạt", { timeout: 5000 });
    const outcome = await page.locator("[aria-label='Hoàn thành bài học']").innerText();
    const shown = /Điểm mục: (\d)\/3/.exec(outcome)?.[1];
    check("complete: 'Đạt' and score shown", Boolean(shown), outcome.replace(/\s+/g, " "));
    check("score shown after completing = 1 (SPEC 7 M1)", shown === "1", `shown ${shown}`);
    check("API agrees: score 1 and lesson_done after complete", (await api("GET", "/map")).json.subtopics.find((x) => x.id === dictId).score === 1);

    // ---- problem: draft survives reload, TLE cut, Submit AC
    await page.locator(`a[href="/p/${problemId}"]`).first().click();
    await page.waitForSelector(".cm-content");
    await page.waitForFunction(() => !document.querySelector("button.primary")?.textContent?.includes("chuẩn bị"), null, { timeout: 60000 });
    await setCode(page, "def can_construct(ransom_note, magazine):\n    # draft-marker-7f3\n    return False\n");
    await page.waitForTimeout(2600); // server copy lands 2 s after the last key
    await page.reload();
    await page.waitForSelector(".cm-content");
    await page.waitForFunction(() => document.querySelector(".cm-content")?.innerText?.includes("draft-marker-7f3"), null, { timeout: 5000 }).catch(() => undefined);
    check("reload keeps the problem draft", (await editorText(page)).includes("draft-marker-7f3"));
    const srvDraft = (await api("GET", `/drafts/${problemId}?language=python`)).json.draft;
    check("draft stored on the server", srvDraft?.code.includes("draft-marker-7f3"));

    await setCode(page, "def can_construct(a, b):\n    while True:\n        pass\n");
    await page.waitForFunction(() => !document.querySelector("button.primary")?.textContent?.includes("chuẩn bị"), null, { timeout: 60000 });
    let t = Date.now();
    await page.click("button:has-text('Run')");
    await waitVerdict(page, "TLE", 10000);
    const cut = Date.now() - t;
    check("infinite loop cut as TLE within 4 s", cut <= 4000, `${cut} ms`);
    t = Date.now();
    await page.evaluate(() => new Promise((r) => requestAnimationFrame(() => r())));
    check("page responsive right after TLE", Date.now() - t < 500, `${Date.now() - t} ms`);

    await page.click("button:has-text('Gợi ý')");
    await page.waitForSelector("text=Gợi ý đã mở", { timeout: 5000 });
    check("hint 1/3 opened via POST /hints and listed", (await page.locator("button:has-text('Gợi ý')").innerText()).includes("1/3"));
    await setCode(page, solution);
    await page.waitForTimeout(300);
    t = Date.now();
    await page.keyboard.press("Control+Shift+Enter");
    await waitVerdict(page, "AC", 30000);
    const verdictText = await page.locator(".results header").innerText();
    check("Submit ransom-note -> AC with all hidden tests", /AC/.test(verdictText) && /(\d+)\/\1 test qua/.test(verdictText), `${Date.now() - t} ms; ${verdictText.replace(/\s+/g, " ")}`);
    await page.waitForSelector("text=Accepted", { timeout: 5000 });
    await page.waitForTimeout(500);
    const ac = sql("select count(*) from attempts where mode='submit' and verdict='AC'");
    check("AC attempt recorded in SQLite", ac === "1", `rows=${ac}`);

    await page.click("button:has-text('Xem lời giải mẫu')"); // solved: no confirm
    await page.waitForSelector("text=Lời giải mẫu", { timeout: 5000 });
    check("solution shown after AC (GET /solution)", (await page.locator("pre.output").last().innerText()).includes("def can_construct"));
    await page.goto(base);
    await page.waitForSelector(`a[href="/s/${dictId}"]`);
    const badge = (await page.locator(`a[href="/s/${dictId}"] .badge`).innerText()).trim();
    const mapScore = (await api("GET", "/map")).json.subtopics.find((s) => s.id === dictId);
    check("map badge = score from the API", badge === String(mapScore.score), `badge ${badge}, api ${mapScore.score}, status ${mapScore.status}`);
    // After T2.2b the D1 fallback is gone: py.datastructs.dict has a level-2 write_code check, so a
    // clean practice AC alone no longer reaches score 2 (needs tested_out or the SPEC 5.2 practice
    // exit). Lesson done + one clean AC keeps the score at 1; reaching 2 is covered by the mastery
    // check API tests (apps/api/tests/test_api_checks.py).
    check("clean Submit AC after the lesson keeps score 1 (D1 fallback removed, T2.2b)", mapScore.score === 1);
    await page.goto(`${base}/s/${dictId}`);
    await page.waitForSelector(".lesson .block");
    check("reload: lesson shows as completed", (await page.locator("[aria-label='Hoàn thành bài học']").innerText()).includes("đã hoàn thành"));
    check("every UI write carried an Idempotency-Key", posts.length > 5 && posts.every((r) => r.key), `${posts.length} writes`);

    // ---- T1.7: kill -9 the server while typing, restart, draft loss <= 3 s
    await page.goto(`${base}/p/${problemId}`);
    await page.waitForSelector(".cm-content");
    await setCode(page, solution);
    await page.waitForTimeout(2600);
    await page.click(".cm-content");
    await page.keyboard.press("Control+End");
    const text = "\n# typed while the server dies: abcdefghijklmnopqrstuvwxyz";
    const stamps = [];
    for (const ch of text) {
      await page.keyboard.type(ch === "\n" ? "" : ch, { delay: 0 });
      if (ch === "\n") await page.keyboard.press("Enter");
      stamps.push(Date.now());
      await sleep(25);
    }
    await killServer("SIGKILL");
    const killedAt = Date.now();
    await sleep(600); // the tab itself is alive: IndexedDB write (300 ms debounce)
    const up = await (await startServer()).json();
    check("restart after SIGKILL: DB healthy (WAL recovery)", up.status === "ok" && up.journal_mode === "wal");

    const full = (await editorText(page)).trimEnd();
    const ctx2 = await browser.newContext(); // fresh profile: no IndexedDB, only what the server has
    const page2 = await newPage(ctx2);
    await page2.goto(`${base}/p/${problemId}`);
    await page2.waitForSelector(".cm-content");
    await page2.waitForTimeout(800);
    const fromServer = (await editorText(page2)).trimEnd();
    const typedTail = text.replace(/^\n/, "");
    const k = Math.max(0, fromServer.length - (full.length - typedTail.length));
    const lossMs = fromServer.includes("typed while") || fromServer.length >= full.length ? (fromServer.length >= full.length ? 0 : killedAt - stamps[Math.min(stamps.length - 1, k + 1)]) : killedAt - stamps[0];
    // The server copy lags by at most remoteMaxMs (10 s, draftStore) while typing continuously; the
    // <= 3 s guarantee comes from the browser (IndexedDB, checked next) surviving a server kill.
    check("kill -9 mid-typing: server-side draft lag <= remoteMaxMs (10 s) + 1 s (fresh browser profile)", lossMs <= 11000, `lost ~${lossMs} ms, server draft ${fromServer.length}/${full.length} chars`);
    await ctx2.close();

    await page.reload();
    await page.waitForSelector(".cm-content");
    await page.waitForFunction((n) => document.querySelector(".cm-content")?.innerText?.trimEnd().length >= n, full.length, { timeout: 5000 }).catch(() => undefined);
    const reopened = (await editorText(page)).trimEnd();
    check("kill -9 mid-typing: reopening the same browser loses nothing", reopened === full, `${reopened.length}/${full.length} chars`);
    let healed = null;
    for (let i = 0; i < 20; i++) {
      healed = (await api("GET", `/drafts/${problemId}?language=python`)).json.draft;
      if (healed?.code.replace(/\s+/g, " ").trim() === full.replace(/\s+/g, " ").trim()) break;
      await sleep(250);
    }
    check("local draft re-pushed to the restarted server", healed?.code.replace(/\s+/g, " ").trim() === full.replace(/\s+/g, " ").trim(), `${healed?.code.length}/${full.length} chars`);

    // ---- T1.7: same Idempotency-Key 5x writes once
    const key = "11111111-2222-4333-8444-555555555555";
    const before = sql("select count(*) from attempts");
    const body = { problem_id: problemId, mode: "run", language: "python", code: solution, verdict: "AC", passed: 3, total: 3, elapsed_ms: 1000, occurred_at: new Date().toISOString() };
    const results = [];
    for (let i = 0; i < 5; i++) results.push(await api("POST", "/attempts", body, { "Idempotency-Key": key }));
    const after = sql("select count(*) from attempts");
    const ids = new Set(results.map((r) => r.json.attempt_id));
    check("same Idempotency-Key sent 5x -> recorded once", after - before === 1 && ids.size === 1 && results.slice(1).every((r) => r.headers.get("idempotent-replay") === "true"), `rows +${after - before}, ids ${[...ids]}`);
    const qBefore = sql("select count(*) from quiz_answers");
    const qb = { quiz_item_id: `${dictId}#b04`, run_no: 1, answer: ["b"] };
    for (let i = 0; i < 5; i++) await api("POST", "/quiz/answers", qb, { "Idempotency-Key": "aaaaaaaa-2222-4333-8444-555555555555" });
    check("same key 5x on /quiz/answers -> recorded once", sql("select count(*) from quiz_answers") - qBefore === 1);

    // ---- T1.7: corrupt DB -> health says so -> restore from backup
    const backup = await api("POST", "/backups", {});
    const scoreBefore = (await api("GET", "/map")).json.subtopics.find((s) => s.id === dictId).score;
    await killServer("SIGTERM");
    for (const f of ["app.db", "app.db-wal", "app.db-shm"]) fs.rmSync(path.join(dataDir, f), { force: true });
    fs.writeFileSync(path.join(dataDir, "app.db"), Buffer.alloc(8192, 7));
    const bad = await startServer();
    const badJson = await bad.json();
    check("corrupt DB detected at start (503 db_corrupt)", bad.status === 503 && badJson.status === "db_corrupt", JSON.stringify(badJson));
    const restored = await api("POST", `/backups/${backup.json.name}/restore`, {});
    const good = await (await fetch(`${base}/api/health`)).json();
    const scoreAfter = (await api("GET", "/map")).json.subtopics.find((s) => s.id === dictId).score;
    check("restore from backup works; progress is back", restored.status === 200 && good.status === "ok" && scoreAfter === scoreBefore, `restore ${restored.status}, score ${scoreAfter}`);
    check("no console/page errors (CSP respected)", errors.length === 0, errors.join(" | ").slice(0, 400));
  } finally {
    await browser.close();
    await killServer("SIGKILL");
    if (process.env.E2E_KEEP) console.log("data dir kept:", dataDir);
    else fs.rmSync(dataDir, { recursive: true, force: true });
  }
}

main()
  .catch((e) => {
    console.error(e);
    failed = true;
  })
  .finally(() => {
    console.log(`\n${log.filter((l) => l.startsWith("PASS")).length}/${log.length} checks passed in ${((Date.now() - t0) / 1000).toFixed(1)} s`);
    process.exit(failed ? 1 : 0);
  });
