const BASE_URL = "/api";

async function handle(response) {
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed with status ${response.status}`);
  }
  return response.json();
}

export async function createThread() {
  const res = await fetch(`${BASE_URL}/chat/thread`, { method: "POST" });
  return handle(res);
}

export async function sendMessage({ message, threadId, userId }) {
  const res = await fetch(`${BASE_URL}/chat/message`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, thread_id: threadId, user_id: userId }),
  });
  return handle(res);
}

export async function getHistory(threadId) {
  const res = await fetch(`${BASE_URL}/chat/${threadId}/history`);
  return handle(res);
}
