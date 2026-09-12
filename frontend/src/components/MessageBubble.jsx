const AGENT_LABELS = {
  invoice_information_subagent: "Billing agent",
  music_catalog_subagent: "Catalog agent",
  supervisor: "Supervisor",
};

export default function MessageBubble({ role, name, content }) {
  const isUser = role === "user";
  const isSystem = role === "system";
  const label = AGENT_LABELS[name];

  if (isSystem) {
    return (
      <div className="flex justify-center my-2">
        <span className="text-xs text-muted bg-canvas border border-line rounded-full px-3 py-1">
          {content}
        </span>
      </div>
    );
  }

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} my-1.5`}>
      <div
        className={`max-w-[75%] rounded-xl2 px-4 py-3 text-sm leading-relaxed ${
          isUser
            ? "bg-forest text-white rounded-br-sm"
            : "bg-surface border border-line text-ink rounded-bl-sm shadow-panel"
        }`}
      >
        {!isUser && label && (
          <div className="text-[11px] text-teal mb-1 font-medium">{label}</div>
        )}
        <p className="whitespace-pre-wrap">{content}</p>
      </div>
    </div>
  );
}
