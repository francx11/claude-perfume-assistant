import { useChatStore } from "../../store/chatStore";
import styles from "./Sidebar.module.css";

export function Sidebar() {
  const sessions = useChatStore((s) => s.sessions);
  const conversationId = useChatStore((s) => s.conversationId);
  const switchSession = useChatStore((s) => s.switchSession);
  const newConversation = useChatStore((s) => s.newConversation);

  return (
    <aside className={styles.root}>
      <div className={styles.top}>
        <span className={styles.brand}>🌸 PerfumeShop</span>
        <button className={styles.newBtn} onClick={newConversation} title="Nueva conversación">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="12" y1="5" x2="12" y2="19" />
            <line x1="5" y1="12" x2="19" y2="12" />
          </svg>
          Nueva
        </button>
      </div>

      <nav className={styles.list}>
        {sessions.length === 0 && (
          <p className={styles.empty}>Sin conversaciones</p>
        )}
        {sessions.map((s) => (
          <button
            key={s.session_id}
            className={`${styles.item} ${s.session_id === conversationId ? styles.active : ""}`}
            onClick={() => switchSession(s.session_id)}
            title={s.title}
          >
            <span className={styles.itemTitle}>{s.title}</span>
            <span className={styles.itemDate}>
              {new Date(s.updated_at).toLocaleDateString("es-ES", { day: "2-digit", month: "short" })}
            </span>
          </button>
        ))}
      </nav>
    </aside>
  );
}
