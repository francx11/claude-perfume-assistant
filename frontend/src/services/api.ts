import type { ChatRequest, ChatResponse } from "../types/chat";

const BASE_URL = "";

export async function sendMessage(
  message: string,
  conversationId?: string
): Promise<ChatResponse> {
  const body: ChatRequest = {
    message,
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
