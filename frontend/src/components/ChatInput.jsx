import { useState } from "react";

export default function ChatInput({ onSend, disabled, placeholder, footerNote }) {
  const [value, setValue] = useState("");

  const submit = (e) => {
    e.preventDefault();
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue("");
  };

  return (
    <div className="border-t border-line bg-surface">
      <form onSubmit={submit} className="flex items-end gap-3 px-6 py-4 max-w-2xl mx-auto">
        <textarea
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) submit(e);
          }}
          rows={1}
          placeholder={placeholder || "Ask the supervisor about catalog or billing..."}
          className="flex-1 resize-none rounded-lg bg-canvas border border-line text-ink placeholder:text-faint px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-teal/40 focus:border-teal/50"
          disabled={disabled}
        />
        <button
          type="submit"
          disabled={disabled || !value.trim()}
          className="rounded-lg bg-forest px-4 py-3 text-white disabled:opacity-40 disabled:cursor-not-allowed hover:bg-forest2 transition-colors"
          aria-label="Send message"
        >
          <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="1.8">
            <path d="M4 12h16M13 6l6 6-6 6" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </button>
      </form>
      {footerNote && (
        <p className="text-[11px] text-faint px-6 pb-3 max-w-2xl mx-auto">{footerNote}</p>
      )}
    </div>
  );
}
