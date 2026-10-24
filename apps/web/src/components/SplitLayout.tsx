import { useCallback, useRef, useState, type CSSProperties, type ReactNode } from "react";
import { lsGet, lsSet, useLayout } from "../lib/hooks";

const KEY = "prep:split";

export function SplitLayout(props: {
  left: ReactNode;
  right: ReactNode;
  leftTab: string;
  rightTab: string;
  /** Tab to show first / forced (e.g. when an exercise is opened on a medium screen). */
  activeTab?: "left" | "right";
  onTabChange?: (tab: "left" | "right") => void;
  /** Extra element above the tabs (breadcrumb etc.) is not needed: pane content carries its own. */
  narrowNotice?: ReactNode;
}) {
  const layout = useLayout();
  const [ratio, setRatio] = useState(() => {
    const saved = Number(lsGet(KEY));
    return saved >= 25 && saved <= 70 ? saved : 45;
  });
  const [localTab, setLocalTab] = useState<"left" | "right">("left");
  const tab = props.activeTab ?? localTab;
  const container = useRef<HTMLDivElement>(null);

  const startDrag = useCallback((event: React.PointerEvent) => {
    event.preventDefault();
    const box = container.current!.getBoundingClientRect();
    const move = (e: PointerEvent) => {
      const percent = Math.min(70, Math.max(25, ((e.clientX - box.left) / box.width) * 100));
      setRatio(percent);
      lsSet(KEY, String(Math.round(percent)));
    };
    const up = () => {
      window.removeEventListener("pointermove", move);
      window.removeEventListener("pointerup", up);
    };
    window.addEventListener("pointermove", move);
    window.addEventListener("pointerup", up);
  }, []);

  if (layout === "split") {
    return (
      <div
        className="split wide"
        ref={container}
        style={{ "--split": `${ratio}%` } as CSSProperties}
      >
        <div className="pane left">{props.left}</div>
        <div
          className="divider"
          role="separator"
          aria-orientation="vertical"
          aria-label="Kéo để đổi độ rộng"
          tabIndex={0}
          onPointerDown={startDrag}
          onKeyDown={(e) => {
            if (e.key === "ArrowLeft") setRatio((r) => Math.max(25, r - 3));
            if (e.key === "ArrowRight") setRatio((r) => Math.min(70, r + 3));
          }}
        />
        <div className="pane right">{props.right}</div>
      </div>
    );
  }
  if (layout === "narrow") {
    return (
      <div className="split">
        <div className="pane left">
          {props.left}
          {props.narrowNotice ?? (
            <div className="card muted" style={{ marginTop: 16 }}>
              Mở trên máy tính để viết code.
            </div>
          )}
        </div>
      </div>
    );
  }
  const select = (next: "left" | "right") => {
    setLocalTab(next);
    props.onTabChange?.(next);
  };
  return (
    <div className="split tabs">
      <div className="tabbar" role="tablist">
        <button role="tab" aria-selected={tab === "left"} onClick={() => select("left")}>
          {props.leftTab}
        </button>
        <button role="tab" aria-selected={tab === "right"} onClick={() => select("right")}>
          {props.rightTab}
        </button>
      </div>
      <div className={tab === "left" ? "pane left" : "pane right"}>
        {tab === "left" ? props.left : props.right}
      </div>
    </div>
  );
}
