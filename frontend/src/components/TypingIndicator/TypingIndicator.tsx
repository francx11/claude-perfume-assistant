import styles from "./TypingIndicator.module.css";

export function TypingIndicator() {
  return (
    <div className={styles.root} aria-label="Escribiendo...">
      <span className={styles.dot} />
      <span className={styles.dot} />
      <span className={styles.dot} />
    </div>
  );
}
