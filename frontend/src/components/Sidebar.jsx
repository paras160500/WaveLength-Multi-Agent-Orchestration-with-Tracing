const NAV_ITEMS = [
  { key: "support", label: "Support workspace", icon: "chat" },
  { key: "overview", label: "System overview", icon: "pulse" },
  { key: "evaluations", label: "Evaluations", icon: "pulse" },
  { key: "catalog", label: "Catalog explorer", icon: "bars" },
];

function Icon({ name, className }) {
  const common = { className, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 1.6 };
  switch (name) {
    case "chat":
      return (
        <svg {...common}>
          <path d="M4 5h16v11H8l-4 4V5z" strokeLinejoin="round" />
        </svg>
      );
    case "pulse":
      return (
        <svg {...common}>
          <path d="M3 12h4l2 6 4-14 2 8h6" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      );
    case "bars":
      return (
        <svg {...common}>
          <path d="M6 4v16M12 8v12M18 11v9" strokeLinecap="round" />
        </svg>
      );
    case "plus":
      return (
        <svg {...common}>
          <path d="M12 5v14M5 12h14" strokeLinecap="round" />
        </svg>
      );
    default:
      return null;
  }
}

function statusDot(status) {
  if (status === "verified") return "bg-teal";
  if (status === "waiting") return "bg-amber";
  return "bg-faint";
}

export default function Sidebar({ sessions, activeThreadId, onSelect, onNewConversation }) {
  return (
    <aside className="w-64 shrink-0 border-r border-line bg-surface flex flex-col h-full">
      <div className="flex items-center gap-2 px-5 pt-5 pb-4">
        <div className="h-8 w-8 rounded-lg bg-forest flex items-center justify-center text-white">
          <Icon name="pulse" className="h-4 w-4" />
        </div>
        <span className="font-semibold text-[15px] text-ink">Orchestra</span>
        <span className="ml-auto text-[10px] font-medium text-teal bg-tealLight px-2 py-0.5 rounded-full">
          Beta
        </span>
      </div>

      <div className="px-4 pb-4">
        <button
          onClick={onNewConversation}
          className="w-full flex items-center justify-center gap-2 rounded-lg bg-forest text-white text-sm font-medium py-2.5 hover:bg-forest2 transition-colors"
        >
          <Icon name="plus" className="h-4 w-4" />
          New conversation
        </button>
      </div>

      <div className="px-5 pt-2 pb-1 text-[11px] font-medium text-faint">Workspace</div>
      <nav className="px-3 pb-4">
        {NAV_ITEMS.map((item, i) => (
          <button
            key={item.key}
            disabled={i !== 0}
            className={`w-full flex items-center gap-2.5 rounded-lg px-3 py-2 text-sm text-left transition-colors ${
              i === 0
                ? "bg-tealLight text-forest2 font-medium"
                : "text-muted cursor-default opacity-60"
            }`}
          >
            <Icon name={item.icon} className="h-4 w-4 shrink-0" />
            {item.label}
          </button>
        ))}
      </nav>

      <div className="px-5 pt-2 pb-1 text-[11px] font-medium text-faint">Recent sessions</div>
      <div className="flex-1 overflow-y-auto scrollbar-thin px-3 pb-4">
        {sessions.length === 0 && (
          <p className="px-3 py-2 text-xs text-faint">No conversations yet.</p>
        )}
        {sessions.map((s) => (
          <button
            key={s.threadId}
            onClick={() => onSelect(s.threadId)}
            className={`w-full text-left rounded-lg px-3 py-2.5 mb-1 transition-colors ${
              s.threadId === activeThreadId ? "bg-canvas" : "hover:bg-canvas/70"
            }`}
          >
            <div className="flex items-center gap-2">
              <span className={`h-1.5 w-1.5 rounded-full ${statusDot(s.status)}`} />
              <span className="text-sm text-ink font-medium truncate">{s.title}</span>
            </div>
            <p className="text-[11px] text-faint mt-0.5 ml-3.5">{s.subtitle}</p>
          </button>
        ))}
      </div>

      <div className="border-t border-line px-5 py-4 flex items-center gap-3">
        <div className="h-8 w-8 rounded-full bg-amberLight text-amber flex items-center justify-center text-xs font-semibold">
          AR
        </div>
        <div className="leading-tight">
          <p className="text-sm text-ink font-medium">Alex Rivera</p>
          <p className="text-[11px] text-faint">Workspace owner</p>
        </div>
      </div>
    </aside>
  );
}
