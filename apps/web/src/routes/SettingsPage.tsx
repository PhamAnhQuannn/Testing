// S11 Settings (minimal): profile/theme/review preset + the backup section. Export/import/reset: M2b.
import { useRef, useState } from "react";
import { ConfirmModal } from "../components/Modal";
import { useToast } from "../components/Toast";
import {
  ApiError,
  createBackup,
  getSettings,
  listBackups,
  newIdempotencyKey,
  putProfile,
  putSettings,
  restoreBackup,
  type BackupInfo,
  type SettingsView,
} from "../lib/api";
import { useAsync } from "../lib/hooks";
import { THEME_LABEL, useTheme, type Theme } from "../lib/theme";

export const RESTORE_PHRASE = "KHOI PHUC";

/** The typed phrase gates the restore button (UI_SPEC S11); case/space-insensitive, never empty. */
export function restoreAllowed(typed: string): boolean {
  return typed.trim().toUpperCase() === RESTORE_PHRASE;
}

export function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1).replace(".", ",")} KB`;
  return `${(bytes / 1024 / 1024).toFixed(1).replace(".", ",")} MB`;
}

export function formatCreated(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleString("vi-VN", { dateStyle: "short", timeStyle: "short" });
}

const errText = (e: unknown, what: string) =>
  e instanceof ApiError && e.isNetwork ? "Server chưa chạy nên chưa thực hiện được." : `${what}: ${(e as Error).message}`;

export function BackupList({
  backups,
  busy,
  onRestore,
}: {
  backups: BackupInfo[];
  busy: boolean;
  onRestore: (b: BackupInfo) => void;
}) {
  if (!backups.length) {
    return <p className="muted">Chưa có bản sao lưu. Backup đầu tiên sẽ chạy lúc khởi động, hoặc bấm "Sao lưu ngay".</p>;
  }
  return (
    <ul className="backup-list" aria-label="Danh sách bản sao lưu" style={{ listStyle: "none", padding: 0 }}>
      {backups.map((b) => (
        <li
          key={b.name}
          style={{ display: "flex", gap: "0.75rem", alignItems: "center", flexWrap: "wrap", padding: "0.25rem 0" }}
        >
          <span>
            <strong>{formatCreated(b.created_at)}</strong> <span className="muted">({formatSize(b.size)})</span>
          </span>
          <code className="muted">{b.name}</code>
          <span className="spacer" />
          <button className="btn sm" disabled={busy} onClick={() => onRestore(b)} aria-label={`Khôi phục ${b.name}`}>
            Khôi phục
          </button>
        </li>
      ))}
    </ul>
  );
}

export function RestoreDialog({
  backup,
  typed,
  onTyped,
  onConfirm,
  onCancel,
}: {
  backup: BackupInfo;
  typed: string;
  onTyped: (v: string) => void;
  onConfirm: () => void;
  onCancel: () => void;
}) {
  return (
    <ConfirmModal
      title="Khôi phục bản sao lưu?"
      confirmLabel="Khôi phục và thay dữ liệu"
      onCancel={onCancel}
      onConfirm={() => restoreAllowed(typed) && onConfirm()}
    >
      <p>
        Sẽ <strong>thay toàn bộ dữ liệu hiện tại</strong> bằng bản {formatCreated(backup.created_at)} ({backup.name}).
        Mọi tiến độ sau thời điểm đó sẽ mất khỏi app. Server tự sao lưu bản hiện tại trước khi thay.
      </p>
      <label>
        Gõ <code>{RESTORE_PHRASE}</code> để xác nhận{" "}
        <input value={typed} onChange={(e) => onTyped(e.target.value)} autoComplete="off" />
      </label>
      {!restoreAllowed(typed) && <p className="muted">Nút xác nhận chỉ có tác dụng khi bạn gõ đúng cụm trên.</p>}
    </ConfirmModal>
  );
}

export interface SettingsDraft {
  display_name: string;
  tz: string;
  review_preset: string;
}

export function SettingsForm({
  value,
  theme,
  busy,
  onChange,
  onTheme,
  onSave,
}: {
  value: SettingsDraft;
  theme: Theme;
  busy: boolean;
  onChange: (v: SettingsDraft) => void;
  onTheme: (t: Theme) => void;
  onSave: () => void;
}) {
  return (
    <form
      aria-labelledby="set-general"
      onSubmit={(e) => {
        e.preventDefault();
        onSave();
      }}
    >
      <h2 id="set-general">Chung</h2>
      <p>
        <label>
          Tên hiển thị{" "}
          <input
            value={value.display_name}
            maxLength={60}
            onChange={(e) => onChange({ ...value, display_name: e.target.value })}
          />
        </label>
      </p>
      <p>
        <label>
          Múi giờ <input value={value.tz} onChange={(e) => onChange({ ...value, tz: e.target.value })} />
        </label>
      </p>
      <p>
        <label>
          Giao diện{" "}
          <select value={theme} onChange={(e) => onTheme(e.target.value as Theme)}>
            {(Object.keys(THEME_LABEL) as Theme[]).map((t) => (
              <option key={t} value={t}>
                {THEME_LABEL[t]}
              </option>
            ))}
          </select>
        </label>
      </p>
      <p>
        <label>
          Cỡ "Phiên ôn ngắn" (số thẻ, để trống = tắt){" "}
          <input
            type="number"
            min={1}
            max={50}
            value={value.review_preset}
            onChange={(e) => onChange({ ...value, review_preset: e.target.value })}
          />
        </label>
      </p>
      <button type="submit" className="btn primary" disabled={busy}>
        Lưu cài đặt
      </button>
    </form>
  );
}

function toForm(s: SettingsView): SettingsDraft {
  return { display_name: s.display_name, tz: s.tz, review_preset: s.review_preset == null ? "" : String(s.review_preset) };
}

export default function SettingsPage() {
  const notify = useToast();
  const [theme, setTheme] = useTheme();
  const settings = useAsync(getSettings, []);
  const backups = useAsync(listBackups, []);
  const [form, setForm] = useState<SettingsDraft | null>(null);
  const [saving, setSaving] = useState(false);
  const [busy, setBusy] = useState(false);
  const [target, setTarget] = useState<BackupInfo | null>(null);
  const [typed, setTyped] = useState("");
  const [restored, setRestored] = useState<BackupInfo | null>(null);
  const [error, setError] = useState<string | null>(null);
  const backupKey = useRef(newIdempotencyKey());

  const current = form ?? (settings.data ? toForm(settings.data) : null);

  const save = async () => {
    if (!current) return;
    const preset = current.review_preset.trim();
    const n = Number(preset);
    if (preset && !(Number.isInteger(n) && n >= 1 && n <= 50)) {
      notify("Cỡ phiên ôn ngắn phải từ 1 đến 50.", { kind: "error" });
      return;
    }
    if (saving) return; // guard against a double submit
    setSaving(true);
    try {
      // A fresh key per save attempt: a retry after a partial failure re-applies the edit
      // instead of replaying a stored response that would silently drop it.
      await putProfile(
        { display_name: current.display_name.trim(), tz: current.tz.trim() || undefined },
        newIdempotencyKey(),
      );
      await putSettings({ review_preset: preset ? n : null });
      notify("Đã lưu cài đặt.");
      settings.reload();
      setForm(null);
    } catch (e) {
      notify(errText(e, "Không lưu được"), { kind: "error" });
    } finally {
      setSaving(false);
    }
  };

  const backupNow = async () => {
    setBusy(true);
    setError(null);
    try {
      const b = await createBackup(backupKey.current);
      backupKey.current = newIdempotencyKey();
      notify(`Đã sao lưu: ${b.name}`);
      backups.reload();
    } catch (e) {
      setError(errText(e, "Không sao lưu được"));
    } finally {
      setBusy(false);
    }
  };

  const doRestore = async () => {
    if (busy || !target || !restoreAllowed(typed)) return; // busy guard: no double restore
    const chosen = target;
    setBusy(true);
    setError(null);
    try {
      const info = await restoreBackup(chosen.name);
      setRestored(info.name ? info : chosen);
      setTarget(null);
      setTyped("");
      backups.reload();
      settings.reload();
      setForm(null);
    } catch (e) {
      setTarget(null);
      setTyped("");
      setError(errText(e, "Khôi phục thất bại, dữ liệu hiện tại giữ nguyên"));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="page settings">
      <h1>Cài đặt</h1>

      {settings.error && (
        <div className="error-block" role="alert">
          Không tải được cài đặt: {settings.error.message}{" "}
          <button className="btn sm" onClick={settings.reload}>
            Thử lại
          </button>
        </div>
      )}
      {current ? (
        <SettingsForm value={current} theme={theme} busy={saving} onChange={setForm} onTheme={setTheme} onSave={save} />
      ) : (
        !settings.error && <p className="muted">Đang tải…</p>
      )}

      <section aria-labelledby="set-backup" style={{ marginTop: "2rem" }}>
        <h2 id="set-backup">Dữ liệu và sao lưu</h2>
        {restored && (
          <div className="banner" role="status" data-testid="restore-result">
            Đã khôi phục bản {formatCreated(restored.created_at)} ({restored.name}). Dữ liệu trước đó đã được sao lưu tự
            động.{" "}
            <button className="btn sm primary" onClick={() => window.location.reload()}>
              Tải lại ứng dụng
            </button>
          </div>
        )}
        {error && (
          <div className="error-block" role="alert">
            {error}
          </div>
        )}
        <p>
          <button className="btn primary" disabled={busy} onClick={backupNow}>
            Sao lưu ngay
          </button>
        </p>
        {backups.error ? (
          <div className="error-block" role="alert">
            Không tải được danh sách sao lưu: {backups.error.message}{" "}
            <button className="btn sm" onClick={backups.reload}>
              Thử lại
            </button>
          </div>
        ) : backups.data ? (
          <BackupList
            backups={backups.data}
            busy={busy}
            onRestore={(b) => {
              setTyped("");
              setTarget(b);
            }}
          />
        ) : (
          <p className="muted">Đang tải…</p>
        )}
        <p className="muted">
          Export JSON, Import JSON và Xoá toàn bộ tiến độ: <em>sắp có</em>.
        </p>
      </section>

      {target && (
        <RestoreDialog
          backup={target}
          typed={typed}
          onTyped={setTyped}
          onConfirm={doRestore}
          onCancel={() => {
            setTarget(null);
            setTyped("");
          }}
        />
      )}
    </div>
  );
}
