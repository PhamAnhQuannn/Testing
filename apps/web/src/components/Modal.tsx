import { useEffect, useRef, type ReactNode } from "react";

export function ConfirmModal(props: {
  title: string;
  children: ReactNode;
  confirmLabel: string;
  cancelLabel?: string;
  onConfirm: () => void;
  onCancel: () => void;
}) {
  const cancelRef = useRef<HTMLButtonElement>(null);
  const onCancel = useRef(props.onCancel);
  useEffect(() => {
    onCancel.current = props.onCancel;
  });
  useEffect(() => {
    cancelRef.current?.focus(); // dangerous action is never the default focus
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") onCancel.current();
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, []);
  return (
    <div className="modal-backdrop" onClick={props.onCancel}>
      <div
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-label={props.title}
        onClick={(event) => event.stopPropagation()}
      >
        <h3 style={{ marginTop: 0 }}>{props.title}</h3>
        {props.children}
        <div className="actions">
          <button ref={cancelRef} className="btn" onClick={props.onCancel}>
            {props.cancelLabel ?? "Huỷ"}
          </button>
          <button className="btn danger" onClick={props.onConfirm}>
            {props.confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}
