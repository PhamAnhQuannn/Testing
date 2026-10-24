import { defaultKeymap, history, historyKeymap, indentWithTab } from "@codemirror/commands";
import { python } from "@codemirror/lang-python";
import { bracketMatching, indentOnInput, indentUnit } from "@codemirror/language";
import { searchKeymap } from "@codemirror/search";
import { EditorState, Prec } from "@codemirror/state";
import {
  EditorView,
  drawSelection,
  highlightActiveLine,
  highlightActiveLineGutter,
  keymap,
  lineNumbers,
} from "@codemirror/view";
import { syntaxHighlighting, HighlightStyle } from "@codemirror/language";
import { tags } from "@lezer/highlight";
import { useEffect, useRef } from "react";

const theme = EditorView.theme({
  "&": { backgroundColor: "var(--surface)", color: "var(--text)" },
  ".cm-content": { fontFamily: "var(--font-code)", caretColor: "var(--text)" },
  ".cm-gutters": { backgroundColor: "var(--code-bg)", color: "var(--muted)", border: "none" },
  ".cm-activeLine, .cm-activeLineGutter": { backgroundColor: "color-mix(in srgb, var(--primary) 8%, transparent)" },
  "&.cm-focused .cm-selectionBackground, .cm-selectionBackground": {
    backgroundColor: "color-mix(in srgb, var(--primary) 28%, transparent)",
  },
  ".cm-scroller": { fontFamily: "var(--font-code)", lineHeight: "1.55" },
});

const highlight = HighlightStyle.define([
  { tag: [tags.keyword, tags.controlKeyword, tags.definitionKeyword], color: "var(--primary)", fontWeight: "600" },
  { tag: [tags.string, tags.special(tags.string)], color: "var(--success)" },
  { tag: [tags.number, tags.bool, tags.null], color: "var(--score-3-fg)" },
  { tag: tags.comment, color: "var(--muted)", fontStyle: "italic" },
  { tag: [tags.function(tags.variableName), tags.definition(tags.variableName)], color: "var(--warn)" },
]);

export interface CodeEditorProps {
  value: string;
  onChange?: (code: string, cursor: number) => void;
  onRun?: () => void;
  onSubmit?: () => void;
  onSave?: () => void;
  onBlur?: () => void;
  readOnly?: boolean;
  minHeight?: number;
  maxHeight?: number;
  initialCursor?: number;
  ariaLabel?: string;
}

/** CodeMirror 6, Python mode. Ctrl/Cmd+Enter = Run, Ctrl/Cmd+Shift+Enter = Submit. */
export function CodeEditor(props: CodeEditorProps) {
  const host = useRef<HTMLDivElement>(null);
  const view = useRef<EditorView | null>(null);
  const handlers = useRef(props);
  useEffect(() => {
    handlers.current = props;
  });

  useEffect(() => {
    const parent = host.current!;
    const state = EditorState.create({
      doc: props.value,
      selection: { anchor: Math.min(props.initialCursor ?? 0, props.value.length) },
      extensions: [
        Prec.highest(
          keymap.of([
            {
              key: "Mod-Shift-Enter",
              preventDefault: true,
              run: () => (handlers.current.onSubmit?.(), true),
            },
            { key: "Mod-Enter", preventDefault: true, run: () => (handlers.current.onRun?.(), true) },
            { key: "Mod-s", preventDefault: true, run: () => (handlers.current.onSave?.(), true) },
          ]),
        ),
        lineNumbers(),
        highlightActiveLineGutter(),
        highlightActiveLine(),
        history(),
        drawSelection(),
        indentOnInput(),
        bracketMatching(),
        indentUnit.of("    "),
        EditorState.tabSize.of(4),
        keymap.of([indentWithTab, ...defaultKeymap, ...historyKeymap, ...searchKeymap]),
        python(),
        syntaxHighlighting(highlight),
        theme,
        EditorView.contentAttributes.of({
          "aria-label": props.ariaLabel ?? "Trình soạn thảo code Python",
          lang: "en",
        }),
        EditorState.readOnly.of(Boolean(props.readOnly)),
        EditorView.updateListener.of((update) => {
          if (update.docChanged) {
            handlers.current.onChange?.(update.state.doc.toString(), update.state.selection.main.head);
          }
        }),
        EditorView.domEventHandlers({ blur: () => (handlers.current.onBlur?.(), false) }),
      ],
    });
    const editor = new EditorView({ state, parent });
    view.current = editor;
    return () => {
      editor.destroy();
      view.current = null;
    };
    // The editor is created once per mount; `value` changes flow through the effect below.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [props.readOnly]);

  useEffect(() => {
    const editor = view.current;
    if (editor && editor.state.doc.toString() !== props.value) {
      editor.dispatch({ changes: { from: 0, to: editor.state.doc.length, insert: props.value } });
    }
  }, [props.value]);

  return (
    <div
      className="editor-wrap"
      ref={host}
      style={{
        minHeight: props.minHeight,
        maxHeight: props.maxHeight,
        overflow: props.maxHeight ? "auto" : undefined,
      }}
    />
  );
}
