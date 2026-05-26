import { create } from "zustand";
import { sendMessage as apiSendMessage } from "../services/api";
import type { Message } from "../types/chat";

interface ChatState {
  messages: Message[];
  isLoading: boolean;
  conversationId: string | null;
  error: string | null;
  sendMessage: (text: string) => Promise<void>;
  clearError: () => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  isLoading: false,
  conversationId: null,
  error: null,

  sendMessage: async (text: string) => {
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: text,
      timestamp: Date.now(),
    };

    set((s) => ({
      messages: [...s.messages, userMessage],
      isLoading: true,
      error: null,
    }));

    try {
      const data = await apiSendMessage(text, get().conversationId ?? undefined);

      const assistantMessage: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: data.response,
        perfumes: data.perfumes,
        timestamp: Date.now(),
      };

      set((s) => ({
        messages: [...s.messages, assistantMessage],
        isLoading: false,
        conversationId: data.conversation_id,
      }));
    } catch (err) {
      set({
        isLoading: false,
        error: err instanceof Error ? err.message : "Error desconocido",
      });
    }
  },

  clearError: () => set({ error: null }),
}));
