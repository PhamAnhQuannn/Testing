import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export function Markdown({ md, lang }: { md: string; lang?: string }) {
  return (
    <div className="md" lang={lang}>
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{md}</ReactMarkdown>
    </div>
  );
}
