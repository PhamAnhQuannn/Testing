// Real-browser smoke test: runs ransom-note through Pyodide in Chromium (sample Run, hidden
// Submit, an infinite loop that must be cut by the watchdog) with the API mocked from the files
// in content/. Needs `npm run build` first; starts `vite preview` itself (CSP header included).
// Usage: npm run e2e   (requires `playwright` resolvable by require(), Chromium preinstalled)
const { spawn } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");

const root = path.join(__dirname, "..", "..", "..");
const dir = path.join(root, "content/problems/py.datastructs.dict/ransom-note");
const jsonl = (file) =>
  fs.readFileSync(path.join(dir, "tests", file), "utf8").split("\n").filter(Boolean).map((l) => JSON.parse(l));
const sample = jsonl("sample.jsonl");
const hidden = jsonl("hidden.jsonl");
const solution = fs.readFileSync(path.join(dir, "solution.py"), "utf8");

const problem = {
  id: "ransom-note",
  subtopic_id: "py.datastructs.dict",
  title: "Ransom Note",
  title_vi: "Thư tống tiền",
  difficulty: "easy",
  statement_en_md: "Given two strings `ransom_note` and `magazine`...",
  statement_vi_md: "Cho hai chuỗi...",
  constraints: ["1 <= len <= 10^5"],
  examples: [{ input: 'ransom_note = "a", magazine = "b"', output: "false" }],
  io: {
    mode: "function",
    entry: "can_construct",
    params: [{ name: "ransom_note", type: "str" }, { name: "magazine", type: "str" }],
    returns: "bool",
    compare: "exact",
  },
  starter: { python: "def can_construct(ransom_note, magazine):\n    pass\n" },
  limits: { time_ms: 1000, memory_mb: 256, time_multiplier: { pyodide: 3 } },
  sample_tests: sample,
  hints_opened: [],
  hints_total: 3,
};

const lesson = JSON.parse(
  require("node:child_process").execFileSync(
    "python3",
    ["-c", "import sys,json,yaml;print(json.dumps(yaml.safe_load(open(sys.argv[1]))))", path.join(root, "content/lessons/py/py.datastructs.dict.yaml")],
    { encoding: "utf8" },
  ),
);
for (const b of lesson.blocks) if (b.type === "code_exercise") delete b.solution; // API strips it

const log = [];
const check = (name, ok, extra = "") => {
  log.push(`${ok ? "PASS" : "FAIL"} ${name} ${extra}`);
  if (!ok) process.exitCode = 1;
};

async function main() {
  const port = 4173 + Math.floor(Math.random() * 500);
  const server = spawn("npx", ["vite", "preview", "--port", String(port), "--strictPort"], {
    cwd: path.join(__dirname, ".."),
    stdio: "ignore",
  });
  const base = `http://127.0.0.1:${port}`;
  for (let i = 0; i < 50; i++) {
    try {
      if ((await fetch(base)).ok) break;
    } catch {
      /* not up yet */
    }
    await new Promise((r) => setTimeout(r, 200));
  }
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage();
    const requests = [];
    const errors = [];
    page.on("pageerror", (e) => errors.push(String(e)));
    page.on("console", (m) => m.type() === "error" && errors.push(m.text()));
    await page.route("**/api/**", async (route) => {
      const req = route.request();
      const url = new URL(req.url());
      const body = req.postData() ? JSON.parse(req.postData()) : null;
      requests.push({ method: req.method(), path: url.pathname + url.search, body, key: req.headers()["idempotency-key"] });
      const reply = (data) => route.fulfill({ json: data });
      if (url.pathname === "/api/problems/ransom-note") return reply(problem);
      if (url.pathname === "/api/problems/ransom-note/start-submit") return reply({ token: "t1" });
      if (url.pathname === "/api/problems/ransom-note/tests/hidden") return reply({ tests: hidden });
      if (url.pathname === "/api/problems/ransom-note/solution") return reply({ code: solution, complexity: "O(n + m)" });
      if (url.pathname === "/api/attempts") return reply({ clean: true });
      if (url.pathname === "/api/lessons/py.datastructs.dict") return reply(lesson);
      if (url.pathname === "/api/lessons/py.datastructs.dict/complete") return reply({ quiz_best: 1, passed: true, score: 1 });
      if (url.pathname === "/api/quiz/answers") return reply({});
      return reply({});
    });

    await page.setViewportSize({ width: 1366, height: 800 });
    await page.goto(`${base}/p/ransom-note`);
    await page.waitForSelector(".cm-content");
    const setCode = async (code) => {
      await page.click(".cm-content");
      await page.keyboard.press("Control+A");
      await page.keyboard.press("Delete");
      await page.keyboard.insertText(code);
    };
    const waitVerdict = async (text, timeout) => {
      await page.waitForFunction(
        (t) => document.querySelector(".results header")?.textContent?.includes(t),
        text,
        { timeout },
      );
    };

    // Run with the reference solution (Ctrl+Enter)
    await setCode(solution);
    let t0 = Date.now();
    await page.keyboard.press("Control+Enter");
    await waitVerdict("3/3 test qua", 60000);
    check("Run ransom-note samples -> AC 3/3 (incl. Pyodide cold start)", true, `${Date.now() - t0} ms`);

    // Wrong answer shows expected vs got
    await setCode("def can_construct(a, b):\n    return True\n");
    await page.keyboard.press("Control+Enter");
    await waitVerdict("WA", 20000);
    const text = await page.locator(".results").innerText();
    check("WA shows expected/got", /expected/.test(text) && /got/.test(text));

    // Submit (Ctrl+Shift+Enter) with hidden tests
    await setCode(solution);
    t0 = Date.now();
    await page.keyboard.press("Control+Shift+Enter");
    await waitVerdict(`${hidden.length}/${hidden.length} test qua`, 30000);
    check(`Submit -> AC ${hidden.length}/${hidden.length}`, true, `${Date.now() - t0} ms`);

    // Infinite loop is cut by the watchdog; page stays responsive
    await setCode("def can_construct(a, b):\n    while True:\n        pass\n");
    t0 = Date.now();
    await page.click("button:has-text('Run')");
    await waitVerdict("TLE", 10000);
    const cut = Date.now() - t0;
    check("infinite loop -> TLE within 4 s", cut <= 4000, `${cut} ms`);
    const t1 = Date.now();
    await page.evaluate(() => new Promise((r) => requestAnimationFrame(() => r())));
    check("page responsive after TLE", Date.now() - t1 < 500);
    await page.click(".cm-content");
    await page.keyboard.type("# still typing");
    check("editor still accepts input", (await page.locator(".cm-content").innerText()).includes("still typing"));

    // Worker restarted: next run works again
    await setCode(solution);
    await page.waitForFunction(() => !document.querySelector("button.primary")?.textContent?.includes("chuẩn bị"), null, { timeout: 30000 });
    await page.keyboard.press("Control+Enter");
    await waitVerdict("3/3 test qua", 30000);
    check("run after worker restart works", true);

    // Draft flush + API calls
    await page.waitForTimeout(2500);
    const puts = requests.filter((r) => r.method === "PUT" && r.path === "/api/drafts/ransom-note");
    check("draft autosaved to server (PUT /api/drafts)", puts.length > 0, `${puts.length} PUTs`);
    const posts = requests.filter((r) => r.method === "POST");
    check("every POST/PUT has Idempotency-Key", requests.filter((r) => r.method !== "GET").every((r) => r.key));
    check("attempts recorded", posts.some((r) => r.path === "/api/attempts" && r.body.mode === "submit" && r.body.verdict === "AC"));
    const idb = await page.evaluate(
      () =>
        new Promise((resolve) => {
          const open = indexedDB.open("prep-app");
          open.onsuccess = () => {
            const get = open.result.transaction("drafts").objectStore("drafts").get("problem:ransom-note");
            get.onsuccess = () => resolve(get.result?.code?.length ?? 0);
          };
        }),
    );
    check("draft in IndexedDB", idb > 0);
    // ---- lesson: every block type renders; sample runs; quiz; exercise; complete
    await page.goto(`${base}/s/py.datastructs.dict`);
    await page.waitForSelector(".lesson .block");
    const rendered = await page.locator(".lesson .block").count();
    check(`lesson renders ${lesson.blocks.length} blocks`, rendered === lesson.blocks.length, `${rendered}`);
    await page.locator("button:has-text('Chạy')").first().click();
    await page.waitForFunction(() => document.body.innerText.includes("Khớp output mong đợi"), null, { timeout: 30000 });
    check("code_sample runs in place and matches expected_output", true);
    const mcq = page.locator("fieldset", { hasText: "KeyError" }).first();
    await mcq.locator("label").nth(1).click();
    await mcq.locator("button:has-text('Kiểm tra')").click();
    check("quiz_mcq graded", (await mcq.innerText()).includes("Đúng"));
    await page.locator("button:has-text('Làm bài này')").click();
    await page.waitForSelector(".pane.right .cm-content");
    await page.click(".pane.right .cm-content");
    await page.keyboard.press("Control+A");
    await page.keyboard.press("Delete");
    await page.keyboard.insertText("def unique_sorted(nums):\n    return sorted(set(nums))\n");
    await page.keyboard.press("Control+Enter");
    await waitVerdict("3/3 test qua", 30000);
    check("code_exercise passes with the same Runner", true);
    check("exercise block ticked", (await page.locator("text=✔ Xong").count()) > 0);
    await page.locator("button:has-text('Hoàn thành bài học')").click();
    await page.waitForSelector("text=Đạt");
    check("Hoàn thành bài học posts /complete", requests.some((r) => r.path === "/api/lessons/py.datastructs.dict/complete" && r.key));
    check("quiz answer posted with run_no", requests.some((r) => r.path === "/api/quiz/answers" && r.body.run_no === 1));
    await page.waitForTimeout(3300);
    check("resume saved (PUT /api/resume)", requests.some((r) => r.method === "PUT" && r.path === "/api/resume" && r.body.mode === "lesson"));

    if (process.env.SHOT) await page.screenshot({ path: process.env.SHOT });
    check("no console/page errors (CSP ok)", errors.length === 0, errors.join(" | ").slice(0, 300));
  } finally {
    await browser.close();
    server.kill();
    console.log(log.join("\n"));
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
