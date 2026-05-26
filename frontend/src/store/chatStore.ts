import { create } from "zustand";
import { sendMessage as apiSendMessage, getHistory, listSessions } from "../services/api";
import type { Message, SessionSummary } from "../types/chat";

const STORAGE_KEY = "perfumeshop_conversation_id";

interface ChatState {
  messages: Message[];
  isLoading: boolean;
  conversationId: string | null;
  sessions: SessionSummary[];
  error: string | null;
  sendMessage: (text: string) => Promise<void>;
  loadHistory: () => Promise<void>;
  loadSessions: () => Promise<void>;
  switchSession: (id: string) => Promise<void>;
  newConversation: () => void;
  clearError: () => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  isLoading: false,
  conversationId: localStorage.getItem(STORAGE_KEY),
  sessions: [],
  error: null,

  loadSessions: async () => {
    const data = await listSessions();
    set({ sessions: data });
  },

  loadHistory: async () => {
    const id = get().conversationId;
    if (!id) return;
    const entries = await getHistory(id);
    if (entries.length === 0) return;
    const messages: Message[] = entries.map((e) => ({
      id: crypto.randomUUID(),
      role: e.role,
      content: e.message,
      timestamp: new Date(e.timestamp).getTime(),
    }));
    set({ messages });
  },

  switchSession: async (id: string) => {
    localStorage.setItem(STORAGE_KEY, id);
    set({ conversationId: id, messages: [] });
    const entries = await getHistory(id);
    const messages: Message[] = entries.map((e) => ({
      id: crypto.randomUUID(),
      role: e.role,
      content: e.message,
      timestamp: new Date(e.timestamp).getTime(),
    }));
    set({ messages });
  },

  newConversation: () => {
    localStorage.removeItem(STORAGE_KEY);
    set({ conversationId: null, messages: [] });
  },

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

      localStorage.setItem(STORAGE_KEY, data.conversation_id);

      set((s) => ({
        messages: [...s.messages, assistantMessage],
        isLoading: false,
        conversationId: data.conversation_id,
      }));

      // refresh sidebar after each turn
      get().loadSessions();
    } catch (err) {
      set({
        isLoading: false,
        error: err instanceof Error ? err.message : "Error desconocido",
      });
    }
  },

  clearError: () => set({ error: null }),
}));
