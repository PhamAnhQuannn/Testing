import { useEffect, useState } from "react";

type ApiStatus = "checking" | "ok" | "down";

export default function App() {
  const [api, setApi] = useState<ApiStatus>("checking");

  useEffect(() => {
    fetch("/api/health")
      .then((response) => setApi(response.ok ? "ok" : "down"))
      .catch(() => setApi("down"));
  }, []);

  return (
    <main>
      <h1>Prep App</h1>
      <p>API: {api}</p>
    </main>
  );
}
