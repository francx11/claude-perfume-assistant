import { useChatStore } from "../../store/chatStore";
import { ChatInput } from "../ChatInput/ChatInput";
import { MessageList } from "../MessageList/MessageList";
import styles from "./ChatWindow.module.css";

export function ChatWindow() {
  const messages = useChatStore((s) => s.messages);
  const isLoading = useChatStore((s) => s.isLoading);
  const error = useChatStore((s) => s.error);
  const sendMessage = useChatStore((s) => s.sendMessage);
  const clearError = useChatStore((s) => s.clearError);

  return (
    <div className={styles.root}>
      <MessageList messages={messages} isLoading={isLoading} />
      {error && (
        <div className={styles.error} role="alert">
          <span>{error}</span>
          <button className={styles.errorClose} onClick={clearError} aria-label="Cerrar error">
            ✕
          </button>
        </div>
      )}
      <ChatInput onSend={sendMessage} disabled={isLoading} />
    </div>
  );
}
