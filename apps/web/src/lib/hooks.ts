import { useEffect, useRef, useState, useSyncExternalStore } from "react";
import { getRunner } from "../runner";

export function useMedia(query: string): boolean {
  const [matches, setMatches] = useState(() => window.matchMedia(query).matches);
  useEffect(() => {
    const list = window.matchMedia(query);
    const handler = () => setMatches(list.matches);
    list.addEventListener("change", handler);
    return () => list.removeEventListener("change", handler);
  }, [query]);
  return matches;
}

export type Layout = "split" | "tabs" | "narrow";

/** >= 1280 split view, 768-1279 two tabs, < 768 read-only (UI_SPEC 3.5). */
export function useLayout(): Layout {
  const wide = useMedia("(min-width: 1280px)");
  const medium = useMedia("(min-width: 768px)");
  return wide ? "split" : medium ? "tabs" : "narrow";
}

export function useOnline(): boolean {
  const [online, setOnline] = useState(() => navigator.onLine);
  useEffect(() => {
    const on = () => setOnline(true);
    const off = () => setOnline(false);
    window.addEventListener("online", on);
    window.addEventListener("offline", off);
    return () => {
      window.removeEventListener("online", on);
      window.removeEventListener("offline", off);
    };
  }, []);
  return online;
}

export interface Async<T> {
  data: T | null;
  error: Error | null;
  loading: boolean;
  reload: () => void;
}

export function useAsync<T>(load: () => Promise<T>, deps: readonly (string | number | undefined)[]): Async<T> {
  const [tick, setTick] = useState(0);
  const key = `${deps.join("|")}#${tick}`;
  const [state, setState] = useState<{ key: string; data: T | null; error: Error | null }>({
    key: "",
    data: null,
    error: null,
  });
  const loadRef = useRef(load);
  useEffect(() => {
    loadRef.current = load;
  });
  useEffect(() => {
    let cancelled = false;
    loadRef.current().then(
      (data) => !cancelled && setState({ key, data, error: null }),
      (error: Error) => !cancelled && setState({ key, data: null, error }),
    );
    return () => {
      cancelled = true;
    };
  }, [key]);
  const settled = state.key === key;
  return {
    data: settled ? state.data : null,
    error: settled ? state.error : null,
    loading: !settled,
    reload: () => setTick((t) => t + 1),
  };
}

/** Runs `fn` when the page is hidden/closed (blur, tab switch, pagehide). */
export function usePageExit(fn: (keepalive: boolean) => void): void {
  useEffect(() => {
    const hide = () => fn(true);
    const visibility = () => document.visibilityState === "hidden" && fn(true);
    window.addEventListener("pagehide", hide);
    document.addEventListener("visibilitychange", visibility);
    return () => {
      window.removeEventListener("pagehide", hide);
      document.removeEventListener("visibilitychange", visibility);
    };
  }, [fn]);
}

export function lsGet(key: string): string | null {
  try {
    return localStorage.getItem(key);
  } catch {
    return null;
  }
}
export function lsSet(key: string, value: string): void {
  try {
    localStorage.setItem(key, value);
  } catch {
    /* storage blocked */
  }
}

/** "loading" while Pyodide boots (also after a TLE restart), "ready", or "error". */
export function useRunnerState() {
  const runner = getRunner();
  return useSyncExternalStore(
    (listener) => runner.subscribe(listener),
    () => runner.getState(),
  );
}
