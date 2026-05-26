import { useEffect } from "react";
import { ChatWindow } from "./components/ChatWindow/ChatWindow";
import { Sidebar } from "./components/Sidebar/Sidebar";
import { useChatStore } from "./store/chatStore";
import styles from "./App.module.css";

export function App() {
  const loadHistory = useChatStore((s) => s.loadHistory);
  const loadSessions = useChatStore((s) => s.loadSessions);

  useEffect(() => {
    loadHistory();
    loadSessions();
  }, []);

  return (
    <div className={styles.root}>
      <Sidebar />
      <div className={styles.main}>
        <ChatWindow />
      </div>
    </div>
  );
}
