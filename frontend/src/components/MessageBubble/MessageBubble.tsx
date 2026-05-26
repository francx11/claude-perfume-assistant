import clsx from "clsx";
import ReactMarkdown from "react-markdown";
import type { Message } from "../../types/chat";
import styles from "./MessageBubble.module.css";

interface Props {
  message: Message;
}

export function MessageBubble({ message }: Props) {
  const isUser = message.role === "user";
  return (
    <div className={clsx(styles.root, isUser ? styles.user : styles.assistant)}>
      {isUser ? (
        <p className={styles.content}>{message.content}</p>
      ) : (
        <div className={clsx(styles.content, styles.markdown)}>
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}
