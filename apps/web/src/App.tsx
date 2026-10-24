import { BrowserRouter, NavLink, Route, Routes } from "react-router-dom";
import { ToastProvider } from "./components/Toast";
import { lsGet, lsSet, useOnline } from "./lib/hooks";
import Home from "./routes/Home";
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
  const [theme, setTheme] = useTheme();
  const cycle = () => setTheme(theme === "auto" ? "light" : theme === "light" ? "dark" : "auto");
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
              <Route path="/map" element={<Home />} />
              <Route path="/s/:subtopicId" element={<LessonPage />} />
              <Route path="/p/:problemId" element={<ProblemPage />} />
              <Route path="*" element={<div className="page empty">Không tìm thấy trang.</div>} />
            </Routes>
          </main>
        </div>
      </ToastProvider>
    </BrowserRouter>
  );
}
