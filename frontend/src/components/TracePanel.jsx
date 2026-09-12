const ACTION_STYLES = {
  routing: { dot: "bg-teal", label: "Routing" },
  tool_call: { dot: "bg-amber", label: "Tool call" },
  tool_result: { dot: "bg-amber", label: "Tool result" },
  responded: { dot: "bg-forest2", label: "Response" },
  verifying: { dot: "bg-amber", label: "Verifying" },
  verified: { dot: "bg-teal", label: "Verified" },
};

export default function TracePanel({ trace, isLive }) {
  return (
    <div className="bg-surface border border-line rounded-xl2 p-4">
      <div className="flex items-center justify-between mb-3">
        <span className="text-[11px] font-medium text-faint">Live trace</span>
        {isLive && (
          <span className="inline-flex items-center gap-1 text-[11px] text-teal font-medium">
            <span className="h-1.5 w-1.5 rounded-full bg-teal pulse-dot" />
            Live
          </span>
        )}
      </div>
      <h3 className="text-sm font-semibold text-ink mb-3">Agent activity</h3>

      {trace.length === 0 ? (
        <div className="flex flex-col items-center text-center py-8">
          <div className="h-9 w-9 rounded-full bg-canvas flex items-center justify-center mb-3">
            <svg viewBox="0 0 24 24" className="h-4 w-4 text-faint" fill="none" stroke="currentColor" strokeWidth="1.6">
              <rect x="4" y="8" width="16" height="10" rx="2" />
              <path d="M9 8V6a3 3 0 016 0v2" strokeLinecap="round" />
            </svg>
          </div>
          <p className="text-xs text-faint max-w-[16rem]">
            Send a message to watch the supervisor coordinate the graph.
          </p>
        </div>
      ) : (
        <ol className="relative pl-4 max-h-80 overflow-y-auto scrollbar-thin">
          <div className="absolute left-[7px] top-1 bottom-1 w-px bg-line" />
          {trace.map((event, i) => {
            const style = ACTION_STYLES[event.action] || { dot: "bg-faint", label: event.action };
            return (
              <li key={i} className="relative pb-4 last:pb-0">
                <span className={`absolute -left-4 top-1 h-2.5 w-2.5 rounded-full ${style.dot}`} />
                <div className="flex items-baseline justify-between gap-2">
                  <span className="text-xs font-medium text-ink">{event.agent}</span>
                  <span className="text-[10px] text-faint">{style.label}</span>
                </div>
                <p className="text-xs text-muted mt-0.5">{event.label}</p>
                {event.detail && (
                  <p className="text-[11px] text-faint mt-0.5 font-mono truncate">{event.detail}</p>
                )}
              </li>
            );
          })}
        </ol>
      )}
    </div>
  );
}
