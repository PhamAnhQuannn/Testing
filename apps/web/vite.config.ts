import react from "@vitejs/plugin-react";
import type { Plugin } from "vite";
import { defineConfig } from "vitest/config";

// SPEC 6.2 #4 + UI_SPEC 3.1: user code can not call out, WebAssembly still runs, worker has no DOM.
export const CSP = [
  "default-src 'self'",
  "script-src 'self' 'wasm-unsafe-eval'",
  "worker-src 'self'",
  "connect-src 'self'",
  "font-src 'self'",
  "style-src 'self' 'unsafe-inline'",
  "img-src 'self' data:",
].join("; ");

// The page gets the policy through a <meta> in production builds (the dev server needs inline
// scripts for HMR). Worker scripts only honour the *header*: the FastAPI static mount and
// `vite preview` send the same string as a Content-Security-Policy response header.
const cspMeta = (): Plugin => ({
  name: "csp-meta",
  apply: "build",
  transformIndexHtml: () => [
    { tag: "meta", attrs: { "http-equiv": "Content-Security-Policy", content: CSP }, injectTo: "head-prepend" },
  ],
});

// dist/csp.txt lets the FastAPI static mount send exactly this string as a header.
const cspFile = (): Plugin => ({
  name: "csp-file",
  apply: "build",
  generateBundle() {
    this.emitFile({ type: "asset", fileName: "csp.txt", source: `${CSP}\n` });
  },
});

const api = { "/api": "http://127.0.0.1:8000" };

export default defineConfig({
  plugins: [react(), cspMeta(), cspFile()],
  build: { assetsInlineLimit: 0 }, // no data: URIs, so CSP font-src/img-src stay on 'self'
  server: { proxy: api },
  preview: { proxy: api, headers: { "Content-Security-Policy": CSP } },
  test: { include: ["src/**/*.test.{ts,tsx}"], environment: "node" },
});
