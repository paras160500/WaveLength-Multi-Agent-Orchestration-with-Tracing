import { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble.jsx";
import SuggestionCards from "./SuggestionCards.jsx";

export default function ChatWindow({ messages, isThinking, onPickSuggestion }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isThinking]);

  return (
    <div className="flex-1 overflow-y-auto scrollbar-thin px-6 py-6">
      {messages.length === 0 && (
        <div className="max-w-lg mx-auto text-center pt-10">
          <span className="inline-flex items-center gap-2 text-xs font-medium text-teal bg-tealLight px-3 py-1 rounded-full">
            <span className="h-1.5 w-1.5 rounded-full bg-teal" />
            Supervisor ready
          </span>
          <h2 className="text-3xl font-semibold text-ink mt-4">
            How can I help your <span className="text-teal">customers</span> today?
          </h2>
          <p className="text-sm text-muted mt-3">
            Ask about the music catalog, purchase history, or let the supervisor route a
            request across the right specialist agents.
          </p>
          <SuggestionCards onPick={onPickSuggestion} />
        </div>
      )}

      <div className="max-w-2xl mx-auto">
        {messages.map((m, i) => (
          <MessageBubble key={i} role={m.role} name={m.name} content={m.content} />
        ))}

        {isThinking && (
          <div className="flex justify-start my-1.5">
            <div className="bg-surface border border-line rounded-xl2 rounded-bl-sm px-4 py-3 shadow-panel">
              <div className="flex gap-1.5">
                <span className="h-1.5 w-1.5 rounded-full bg-faint pulse-dot [animation-delay:-0.3s]" />
                <span className="h-1.5 w-1.5 rounded-full bg-faint pulse-dot [animation-delay:-0.15s]" />
                <span className="h-1.5 w-1.5 rounded-full bg-faint pulse-dot" />
              </div>
            </div>
          </div>
        )}
      </div>

      <div ref={bottomRef} />
    </div>
  );
}
