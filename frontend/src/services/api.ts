import type { ChatRequest, ChatResponse, HistoryEntry, SessionSummary } from "../types/chat";

const BASE_URL = "";

const CLIENT_ID_KEY = "perfumeshop_client_id";

export function getClientId(): string {
  let id = localStorage.getItem(CLIENT_ID_KEY);
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem(CLIENT_ID_KEY, id);
  }
  return id;
}

export async function sendMessage(
  message: string,
  conversationId?: string
): Promise<ChatResponse> {
  const body: ChatRequest = {
    message,
    client_id: getClientId(),
    ...(conversationId ? { conversation_id: conversationId } : {}),
  };

  const res = await fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`Error ${res.status}: ${detail}`);
  }

  return res.json() as Promise<ChatResponse>;
}

export async function getHistory(conversationId: string): Promise<HistoryEntry[]> {
  try {
    const res = await fetch(`${BASE_URL}/sessions/${conversationId}/history`);
    if (!res.ok) return [];
    return res.json() as Promise<HistoryEntry[]>;
  } catch {
    return [];
  }
}

export async function listSessions(): Promise<SessionSummary[]> {
  try {
    const res = await fetch(`${BASE_URL}/sessions?client_id=${getClientId()}`);
    if (!res.ok) return [];
    return res.json() as Promise<SessionSummary[]>;
  } catch {
    return [];
  }
}
