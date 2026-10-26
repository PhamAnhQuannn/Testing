// Activity ping (SPEC 6.4): every 30 s while the app is visible and focused. Failures are ignored;
// the server caps what one ping can add, so a missed or repeated ping cannot distort the total.
import { useEffect } from "react";
import { pingActivity } from "./api";

export const PING_INTERVAL_MS = 30_000;

export const isActive = (visibility: string, focused: boolean): boolean => visibility === "visible" && focused;

export function useActivityPing(intervalMs = PING_INTERVAL_MS): void {
  useEffect(() => {
    const active = () => isActive(document.visibilityState, document.hasFocus());
    const tick = () => {
      if (active()) void pingActivity().catch(() => undefined);
    };
    tick(); // sets the baseline `last_ping`
    const id = setInterval(tick, intervalMs);
    window.addEventListener("focus", tick);
    return () => {
      clearInterval(id);
      window.removeEventListener("focus", tick);
    };
  }, [intervalMs]);
}
