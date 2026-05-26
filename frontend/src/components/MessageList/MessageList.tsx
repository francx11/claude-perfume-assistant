import { useEffect, useRef } from "react";
import type { Message } from "../../types/chat";
import { MessageBubble } from "../MessageBubble/MessageBubble";
import { TypingIndicator } from "../TypingIndicator/TypingIndicator";
import styles from "./MessageList.module.css";

interface Props {
  messages: Message[];
  isLoading: boolean;
}

export function MessageList({ messages, isLoading }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  return (
    <div className={styles.root}>
      {messages.length === 0 && (
        <div className={styles.empty}>
          <span className={styles.emptyIcon}>🌸</span>
          <p>Pregúntame sobre perfumes. Te ayudaré a encontrar el tuyo.</p>
        </div>
      )}
      {messages.map((msg) => (
        <div key={msg.id} className={styles.messageGroup}>
          <MessageBubble message={msg} />
        </div>
      ))}
      {isLoading && (
        <div className={styles.messageGroup}>
          <TypingIndicator />
        </div>
      )}
      <div ref={bottomRef} />
    </div>
  );
}
