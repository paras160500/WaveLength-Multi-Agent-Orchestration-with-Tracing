function statusPill(session) {
  if (session.status === "waiting") {
    return { text: "Identity verification required", cls: "text-amber bg-amberLight" };
  }
  if (session.status === "verified") {
    return { text: `Verified · Customer #${session.customerId}`, cls: "text-teal bg-tealLight" };
  }
  return { text: "Ready", cls: "text-muted bg-canvas" };
}

export default function ConversationHeader({ session }) {
  if (!session) return null;
  const pill = statusPill(session);
  const shortId = session.threadId.replace(/-/g, "").slice(0, 6);

  return (
    <div className="flex items-center justify-between px-6 py-4 border-b border-line bg-surface">
      <div>
        <div className="flex items-center gap-2">
          <span
            className={`h-1.5 w-1.5 rounded-full ${
              session.status === "verified" ? "bg-teal" : session.status === "waiting" ? "bg-amber" : "bg-faint"
            }`}
          />
          <h1 className="text-[15px] font-semibold text-ink">{session.title}</h1>
        </div>
        <span className={`inline-block mt-1 text-xs font-medium px-2 py-0.5 rounded-full ${pill.cls}`}>
          {pill.text}
        </span>
      </div>
      <span className="text-xs text-faint">Thread {shortId}</span>
    </div>
  );
}
