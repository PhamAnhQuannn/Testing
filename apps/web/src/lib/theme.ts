import { useEffect, useState } from "react";
import { lsGet, lsSet } from "./hooks";

export type Theme = "auto" | "light" | "dark";
export const THEME_KEY = "prep:theme";
const EVENT = "prep:theme-change";

export const THEME_LABEL: Record<Theme, string> = { auto: "Tự động", light: "Sáng", dark: "Tối" };

export function readTheme(): Theme {
  const v = lsGet(THEME_KEY);
  return v === "light" || v === "dark" ? v : "auto";
}

/** Apply + persist; other `useTheme` instances (nav button, Settings) follow via an event. */
export function applyTheme(theme: Theme): void {
  const root = document.documentElement;
  if (theme === "auto") root.removeAttribute("data-theme");
  else root.setAttribute("data-theme", theme);
  lsSet(THEME_KEY, theme);
  window.dispatchEvent(new Event(EVENT));
}

export function useTheme() {
  const [theme, setTheme] = useState<Theme>(readTheme);
  useEffect(() => {
    const root = document.documentElement;
    if (theme === "auto") root.removeAttribute("data-theme");
    else root.setAttribute("data-theme", theme);
  }, [theme]);
  useEffect(() => {
    const sync = () => setTheme(readTheme());
    window.addEventListener(EVENT, sync);
    return () => window.removeEventListener(EVENT, sync);
  }, []);
  return [theme, applyTheme] as const;
}
