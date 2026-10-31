import { BrowserRouter, Link, NavLink, Route, Routes, useLocation, useNavigate } from "react-router-dom";
import { ToastProvider } from "./components/Toast";
import { useActivityPing } from "./lib/activity";
import { getPlacementCurrent, getResumeView, type PlacementView, type ResumeView } from "./lib/api";
import { showResumeStrip } from "./lib/onboarding";
import { useOnline } from "./lib/hooks";
import { useTheme } from "./lib/theme";
import CheckPage from "./routes/CheckPage";
import Home from "./routes/Home";
import MapPage from "./routes/MapPage";
import PlacementPage from "./routes/PlacementPage";
import SettingsPage from "./routes/SettingsPage";
import Welcome from "./routes/Welcome";
import ReviewPage from "./routes/ReviewPage";
import LessonPage from "./routes/LessonPage";
import ProblemPage from "./routes/ProblemPage";
import { useEffect, useState } from "react";

function Nav() {
  const path = useLocation().pathname;
  // Onboarding precedes Home (Home redirects to /welcome until profile_done), so a nav there would
  // loop — keep it hidden. Timed pages (check/placement) show a SLIM bar: brand (→ Home) + theme
  // only, so every page still has a route home without the full tab set distracting a timed task.
  const [theme, setTheme] = useTheme();
  const cycle = () => setTheme(theme === "auto" ? "light" : theme === "light" ? "dark" : "auto");
  if (path.startsWith("/welcome")) return null;
  const slim = path.startsWith("/check/") || path.startsWith("/placement/"); // focus mode (UI_SPEC S2/S8)
  return (
    <nav className="nav" aria-label="Điều hướng chính">
      <NavLink to="/" className="logo">
        Prep App
      </NavLink>
      {!slim && (
        <>
          <NavLink to="/" end className={({ isActive }) => `link${isActive ? " active" : ""}`}>
            Học tiếp
          </NavLink>
          <NavLink to="/map" className={({ isActive }) => `link${isActive ? " active" : ""}`}>
            Map
          </NavLink>
          <NavLink to="/review" className={({ isActive }) => `link${isActive ? " active" : ""}`}>
            Ôn tập
          </NavLink>
          <NavLink to="/settings" className={({ isActive }) => `link${isActive ? " active" : ""}`}>
            Cài đặt
          </NavLink>
        </>
      )}
      <span className="spacer" />
      {slim && <span className="muted">Chế độ tập trung</span>}
      <button className="btn sm ghost" onClick={cycle} aria-label={`Giao diện: ${theme}`}>
        {theme === "dark" ? "🌙" : theme === "light" ? "☀️" : "🌓"}
      </button>
    </nav>
  );
}

/** S12 on routes other than `/`: one thin strip, dismissible for the session. */
function ResumeStrip() {
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const [resume, setResume] = useState<ResumeView | null>(null);
  const [hidden, setHidden] = useState(false);
  useEffect(() => {
    let live = true;
    getResumeView()
      .then((r) => live && setResume(r))
      .catch(() => undefined);
    return () => {
      live = false;
    };
  }, []);
  const p = resume?.primary;
  if (!p || hidden || !showResumeStrip(pathname, p.route)) return null;
  return (
    <div className="banner resume-strip" role="note" data-testid="resume-strip">
      <span>Tiếp tục nơi bạn dừng.</span>{" "}
      <button className="btn sm primary" onClick={() => navigate(p.route)}>
        {p.stale ? "Mở lại" : "Tiếp tục"}
      </button>{" "}
      <button className="btn sm ghost" aria-label="Ẩn" onClick={() => setHidden(true)}>
        ✕
      </button>
    </div>
  );
}

/** Flow H: /resume carries no placement state yet, so ask /placement/current and offer to continue. */
function PlacementStrip() {
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const [current, setCurrent] = useState<PlacementView | null>(null);
  const [hidden, setHidden] = useState(false);
  useEffect(() => {
    let live = true;
    getPlacementCurrent()
      .then((p) => live && setCurrent(p))
      .catch(() => undefined);
    return () => {
      live = false;
    };
  }, [pathname]); // re-check on navigation so finishing a sitting clears the strip
  if (!current || current.status !== "in_progress" || hidden) return null;
  if (pathname.startsWith("/placement/") || pathname.startsWith("/welcome")) return null;
  return (
    <div className="banner resume-strip" role="note" data-testid="placement-resume-strip">
      <span>Bạn đang đánh giá trình độ dở dang.</span>{" "}
      <button className="btn sm primary" onClick={() => navigate(`/placement/${current.placement_id}`)}>
        Tiếp tục đánh giá
      </button>{" "}
      <button className="btn sm ghost" aria-label="Ẩn" onClick={() => setHidden(true)}>
        ✕
      </button>
    </div>
  );
}

export default function App() {
  const online = useOnline();
  useActivityPing();
  return (
    <BrowserRouter>
      <ToastProvider>
        <div className="app">
          <a className="skip-link" href="#main">
            Tới nội dung
          </a>
          <Nav />
          {!online && (
            <div className="banner offline" role="status">
              Mất kết nối server. Bạn vẫn đọc, gõ code và Run được; thay đổi được giữ trên máy.
            </div>
          )}
          <ResumeStrip />
          <PlacementStrip />
          <main className="main" id="main">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/welcome" element={<Welcome />} />
              <Route path="/map" element={<MapPage />} />
              <Route path="/review" element={<ReviewPage />} />
              <Route path="/settings" element={<SettingsPage />} />
              <Route path="/s/:subtopicId" element={<LessonPage />} />
              <Route path="/check/:subtopicId" element={<CheckPage />} />
              <Route path="/placement/:sessionId" element={<PlacementPage />} />
              <Route path="/placement/:sessionId/result" element={<PlacementPage />} />
              <Route path="/p/:problemId" element={<ProblemPage />} />
              <Route
                path="*"
                element={
                  <div className="page empty">
                    Không tìm thấy trang. <Link to="/">Về Trang chủ</Link>
                  </div>
                }
              />
            </Routes>
          </main>
        </div>
      </ToastProvider>
    </BrowserRouter>
  );
}
