import { BrowserRouter, NavLink, Route, Routes, useLocation, useNavigate } from "react-router-dom";
import { ToastProvider } from "./components/Toast";
import { useActivityPing } from "./lib/activity";
import { getResumeView, type ResumeView } from "./lib/api";
import { showResumeStrip } from "./lib/onboarding";
import { useOnline } from "./lib/hooks";
import { useTheme } from "./lib/theme";
import CheckPage from "./routes/CheckPage";
import Home from "./routes/Home";
import MapPage from "./routes/MapPage";
import SettingsPage from "./routes/SettingsPage";
import Welcome from "./routes/Welcome";
import ReviewPage from "./routes/ReviewPage";
import LessonPage from "./routes/LessonPage";
import ProblemPage from "./routes/ProblemPage";
import { useEffect, useState } from "react";

function Nav() {
  const path = useLocation().pathname;
  const focus = path.startsWith("/check/") || path.startsWith("/welcome"); // focus mode (UI_SPEC S8): no side nav
  const [theme, setTheme] = useTheme();
  const cycle = () => setTheme(theme === "auto" ? "light" : theme === "light" ? "dark" : "auto");
  if (focus) return null;
  return (
    <nav className="nav" aria-label="Điều hướng chính">
      <NavLink to="/" className="logo">
        Prep App
      </NavLink>
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
      <span className="spacer" />
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
          <main className="main" id="main">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/welcome" element={<Welcome />} />
              <Route path="/map" element={<MapPage />} />
              <Route path="/review" element={<ReviewPage />} />
              <Route path="/settings" element={<SettingsPage />} />
              <Route path="/s/:subtopicId" element={<LessonPage />} />
              <Route path="/check/:subtopicId" element={<CheckPage />} />
              <Route path="/p/:problemId" element={<ProblemPage />} />
              <Route path="*" element={<div className="page empty">Không tìm thấy trang.</div>} />
            </Routes>
          </main>
        </div>
      </ToastProvider>
    </BrowserRouter>
  );
}
