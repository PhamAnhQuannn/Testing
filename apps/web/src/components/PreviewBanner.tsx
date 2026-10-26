import { Link } from "react-router-dom";
import type { MapSubtopic } from "../lib/api";
import { lockSummary } from "../lib/lock";

/** Shown on a locked subtopic's lesson / problem: readable, but nothing can be submitted. */
export function PreviewBanner({ item }: { item: MapSubtopic }) {
  return (
    <div className="banner preview" role="status">
      <strong>🔒 Xem trước.</strong> Mục này chưa mở ({lockSummary(item)}). Bạn đọc được nội dung,
      nhưng trình soạn code, Run và Submit đang tắt.{" "}
      <Link to={`/check/${item.id}?ctx=test_out`}>Đã biết rồi? Test out</Link>
    </div>
  );
}
