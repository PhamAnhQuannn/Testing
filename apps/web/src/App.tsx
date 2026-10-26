import { BrowserRouter, NavLink, Route, Routes, useLocation } from "react-router-dom";
import { ToastProvider } from "./components/Toast";
import { lsGet, lsSet, useOnline } from "./lib/hooks";
import CheckPage from "./routes/CheckPage";
import Home from "./routes/Home";
import MapPage from "./routes/MapPage";
import ReviewPage from "./routes/ReviewPage";
import LessonPage from "./routes/LessonPage";
import ProblemPage from "./routes/ProblemPage";
import { useEffect, useState } from "react";

type Theme = "auto" | "light" | "dark";

function useTheme() {
  const [theme, setTheme] = useState<Theme>(() => (lsGet("prep:theme") as Theme) || "auto");
  useEffect(() => {
    const root = document.documentElement;
    if (theme === "auto") root.removeAttribute("data-theme");
    else root.setAttribute("data-theme", theme);
    lsSet("prep:theme", theme);
  }, [theme]);
  return [theme, setTheme] as const;
}

function Nav() {
  const focus = useLocation().pathname.startsWith("/check/"); // focus mode (UI_SPEC S8): no side nav
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
      <span className="spacer" />
      <button className="btn sm ghost" onClick={cycle} aria-label={`Giao diện: ${theme}`}>
        {theme === "dark" ? "🌙" : theme === "light" ? "☀️" : "🌓"}
      </button>
    </nav>
  );
}

export default function App() {
  const online = useOnline();
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
          <main className="main" id="main">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/map" element={<MapPage />} />
              <Route path="/review" element={<ReviewPage />} />
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
