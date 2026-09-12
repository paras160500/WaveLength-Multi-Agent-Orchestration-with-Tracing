# Frontend — Orchestra Support Console (React + Tailwind)

A three-column support console for the multi-agent backend:

- **Left** — workspace nav + recent conversation sessions (in-memory for now;
  see Notes below).
- **Center** — the chat itself, with a header showing verification status and
  quick-start suggestion cards on a fresh conversation.
- **Right** — a live view into what the agents are actually doing:
  - **Agent activity** — a timeline of routing decisions and tool calls for
    the current turn (who was called, what tool, what came back).
  - **Verified context** — shows the verified customer ID once identity
    checks pass.
  - **Long-term memory** — the customer's saved preferences (e.g. favorite
    artists), pulled straight from the backend's memory store.

## Setup

```bash
cd frontend
npm install
npm run dev
```

Runs at `http://localhost:5173` and proxies `/api/*` to the FastAPI backend
at `http://localhost:8000` (see `vite.config.js`). Start the backend first.

## Structure

```
frontend/src/
├── App.jsx                       # Session state, routing between conversations
├── components/
│   ├── Sidebar.jsx                # Workspace nav + session list
│   ├── ConversationHeader.jsx     # Title, verification status pill, thread id
│   ├── SuggestionCards.jsx        # Empty-state quick actions
│   ├── ChatWindow.jsx / MessageBubble.jsx / ChatInput.jsx
│   ├── TracePanel.jsx             # Live agent-activity feed
│   ├── VerifiedContextCard.jsx    # Verified customer badge
│   └── MemoryCard.jsx             # Saved long-term preferences
└── api/client.js
```

## How the trace/memory panels get their data

Every `POST /api/chat/message` response now includes, alongside `messages`:

- `trace`: a list of `{ agent, action, label, detail }` events generated
  during that turn (routing between supervisor/sub-agents, tool calls, tool
  results). The frontend appends these to a running feed per conversation
  (capped at 40 events).
- `memory`: the customer's current saved preferences, once verified.
- `customer_id`: set once identity verification succeeds.

No polling — this all arrives with the normal chat response.

## Notes / known limitations

- **Session list is in-memory only.** Refreshing the browser loses the
  sidebar history (though each *thread* itself is preserved server-side by
  the backend's checkpointer — you'd just need to know its ID to resume it).
  Persisting the session list would mean adding a "list my threads" endpoint
  backed by a real database instead of the in-memory checkpointer.
- **Conversation titles** are just the first message you send, truncated —
  there's no LLM call to generate a nicer title (that'd be an easy addition
  if wanted).
- The left nav items other than "Support workspace" are placeholders — this
  console currently only implements the chat + trace experience.
