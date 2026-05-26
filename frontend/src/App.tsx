import { ChatWindow } from "./components/ChatWindow/ChatWindow";
import styles from "./App.module.css";

export function App() {
  return (
    <div className={styles.root}>
      <header className={styles.header}>
        <span className={styles.logo}>🌸</span>
        <div>
          <h1 className={styles.title}>PerfumeShop AI</h1>
          <p className={styles.subtitle}>Tu asistente experto en fragancias</p>
        </div>
      </header>
      <main className={styles.main}>
        <ChatWindow />
      </main>
    </div>
  );
}
