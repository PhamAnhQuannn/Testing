import type { Onboarding, Profile } from "./api";

/** `/` sends a first-time user to `/welcome` (UI_SPEC S1: onboarding.profile_done=false). Unknown state never redirects. */
export function needsWelcome(onboarding: Onboarding | null): boolean {
  return onboarding !== null && !onboarding.profile_done;
}

export interface ProfileDraft {
  target_role: Profile["target_role"];
  track: Profile["track"];
  language: Profile["language"];
  experience: Profile["experience"] | "";
  display_name: string;
  tz: string;
}

export const defaultTz = (): string => {
  try {
    return Intl.DateTimeFormat().resolvedOptions().timeZone || "Asia/Ho_Chi_Minh";
  } catch {
    return "Asia/Ho_Chi_Minh";
  }
};

/** Body for PUT /profile; null while the required experience answer is missing. */
export function profilePayload(d: ProfileDraft): Profile | null {
  if (!d.experience) return null;
  const name = d.display_name.trim();
  return {
    target_role: d.target_role,
    track: d.track,
    language: d.language,
    experience: d.experience,
    ...(name ? { display_name: name } : {}),
    ...(d.tz ? { tz: d.tz } : {}),
  };
}

/** Whether the thin S12 strip shows on this route (Home has the big card; focus screens have none). */
export function showResumeStrip(pathname: string, target: string): boolean {
  if (pathname === "/" || pathname.startsWith("/welcome") || pathname.startsWith("/check/")) return false;
  return pathname !== target.split("?")[0];
}
