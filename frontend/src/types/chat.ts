export interface Perfume {
  id: string;
  name: string;
  brand: string;
  gender?: string;
  season?: string;
  notes?: string;
  description?: string;
  rating?: number;
}

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  perfumes?: Perfume[];
  timestamp: number;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
}

export interface ChatResponse {
  response: string;
  perfumes?: Perfume[];
  conversation_id: string;
}
