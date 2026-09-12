import { useEffect, useRef, useState } from "react";
import Sidebar from "./components/Sidebar.jsx";
import ConversationHeader from "./components/ConversationHeader.jsx";
import ChatWindow from "./components/ChatWindow.jsx";
import ChatInput from "./components/ChatInput.jsx";
import TracePanel from "./components/TracePanel.jsx";
import VerifiedContextCard from "./components/VerifiedContextCard.jsx";
import MemoryCard from "./components/MemoryCard.jsx";
import { createThread, sendMessage } from "./api/client.js";

const MAX_TRACE_EVENTS = 40;

function emptySessionData(threadId, index) {
  return {
    threadId,
    index,
    title: `Conversation ${String(index).padStart(2, "0")}`,
    subtitle: "just now",
    status: "ready", // ready | waiting | verified
    customerId: null,
    messages: [],
    trace: [],
    memory: null,
    titleIsCustom: false,
  };
}

export default function App() {
  const [sessionsById, setSessionsById] = useState({});
  const [order, setOrder] = useState([]); // threadIds, most recent first
  const [activeThreadId, setActiveThreadId] = useState(null);
  const [isThinking, setIsThinking] = useState(false);
  const [error, setError] = useState(null);
  const sessionCounter = useRef(0);
  const backendUnreachable = useRef(false);

  const startNewConversation = async () => {
    try {
      const res = await createThread();
      sessionCounter.current += 1;
      const data = emptySessionData(res.thread_id, sessionCounter.current);
      setSessionsById((prev) => ({ ...prev, [res.thread_id]: data }));
      setOrder((prev) => [res.thread_id, ...prev]);
      setActiveThreadId(res.thread_id);
      setError(null);
      backendUnreachable.current = false;
    } catch (err) {
      backendUnreachable.current = true;
      setError(
        "The FastAPI service is not reachable. Start it with uvicorn app.main:app --reload."
      );
    }
  };

  useEffect(() => {
    startNewConversation();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const activeSession = activeThreadId ? sessionsById[activeThreadId] : null;

  const handleSend = async (text) => {
    if (!activeThreadId) return;
    const threadId = activeThreadId;

    setSessionsById((prev) => ({
      ...prev,
      [threadId]: {
        ...prev[threadId],
        messages: [...prev[threadId].messages, { role: "user", content: text }],
        title: prev[threadId].titleIsCustom
          ? prev[threadId].title
          : text.length > 32
          ? text.slice(0, 32) + "…"
          : text,
        titleIsCustom: true,
        subtitle: "just now",
      },
    }));

    setIsThinking(true);
    setError(null);

    try {
      const current = sessionsById[threadId];
      const res = await sendMessage({
        message: text,
        threadId,
        userId: current?.customerId || null,
      });

      setSessionsById((prev) => {
        const existing = prev[threadId];
        const mergedTrace = [...existing.trace, ...res.trace].slice(-MAX_TRACE_EVENTS);
        const status = res.awaiting_input ? "waiting" : res.customer_id ? "verified" : existing.status;

        return {
          ...prev,
          [threadId]: {
            ...existing,
            messages: [...existing.messages, ...res.messages],
            trace: mergedTrace,
            memory: res.memory || existing.memory,
            customerId: res.customer_id || existing.customerId,
            status,
            subtitle: res.awaiting_input
              ? "verification pending"
              : res.customer_id
              ? `verified #${res.customer_id}`
              : "in progress",
          },
        };
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setIsThinking(false);
    }
  };

  const sessionList = order.map((id) => sessionsById[id]).filter(Boolean);

  return (
    <div className="h-full flex bg-canvas">
      <Sidebar
        sessions={sessionList}
        activeThreadId={activeThreadId}
        onSelect={setActiveThreadId}
        onNewConversation={startNewConversation}
      />

      <div className="flex-1 flex flex-col min-w-0">
        <ConversationHeader session={activeSession} />

        <ChatWindow
          messages={activeSession?.messages || []}
          isThinking={isThinking}
          onPickSuggestion={handleSend}
        />

        {error && (
          <div className="mx-6 mb-2 rounded-lg bg-roseLight border border-rose/30 px-4 py-2 text-xs text-rose">
            {error}
          </div>
        )}

        <ChatInput
          onSend={handleSend}
          disabled={!activeThreadId || isThinking}
          placeholder={
            activeSession?.status === "waiting"
              ? "Share your customer ID, email, or phone number..."
              : undefined
          }
          footerNote="Responses are scoped to verified customer data."
        />
      </div>

      <aside className="w-80 shrink-0 border-l border-line bg-canvas p-4 space-y-4 overflow-y-auto scrollbar-thin hidden lg:block">
        <TracePanel trace={activeSession?.trace || []} isLive={!!activeThreadId} />
        <VerifiedContextCard customerId={activeSession?.customerId} />
        <MemoryCard memory={activeSession?.memory} />
      </aside>
    </div>
  );
}
