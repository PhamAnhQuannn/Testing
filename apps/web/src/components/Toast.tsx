import { createContext, useCallback, useContext, useState, type ReactNode } from "react";

interface ToastItem {
  id: number;
  text: string;
  kind: "info" | "error";
  action?: { label: string; run: () => void };
}
type Notify = (text: string, options?: { kind?: "info" | "error"; action?: ToastItem["action"] }) => void;

const ToastContext = createContext<Notify>(() => undefined);
export const useToast = () => useContext(ToastContext);

export function ToastProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<ToastItem[]>([]);
  const notify = useCallback<Notify>((text, options = {}) => {
    const id = Date.now() + Math.random();
    const kind = options.kind ?? "info";
    setItems((list) => [...list.slice(-2), { id, text, kind, action: options.action }]);
    setTimeout(() => setItems((list) => list.filter((t) => t.id !== id)), kind === "error" ? 8000 : 4000);
  }, []);
  return (
    <ToastContext.Provider value={notify}>
      {children}
      <div className="toasts">
        {items.map((t) => (
          <div key={t.id} className={`toast ${t.kind}`} role={t.kind === "error" ? "alert" : "status"}>
            {t.text}
            {t.action && (
              <button className="btn sm ghost" onClick={t.action.run}>
                {t.action.label}
              </button>
            )}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}
