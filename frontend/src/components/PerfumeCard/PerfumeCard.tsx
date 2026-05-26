import type { Perfume } from "../../types/chat";
import styles from "./PerfumeCard.module.css";

interface Props {
  perfume: Perfume;
}

export function PerfumeCard({ perfume }: Props) {
  return (
    <article className={styles.root}>
      <header className={styles.header}>
        <span className={styles.name}>{perfume.name}</span>
        <span className={styles.brand}>{perfume.brand}</span>
      </header>
      <dl className={styles.meta}>
        {perfume.gender && (
          <div className={styles.metaItem}>
            <dt>Género</dt>
            <dd>{perfume.gender}</dd>
          </div>
        )}
        {perfume.season && (
          <div className={styles.metaItem}>
            <dt>Temporada</dt>
            <dd>{perfume.season}</dd>
          </div>
        )}
        {perfume.notes && (
          <div className={styles.metaItem}>
            <dt>Notas</dt>
            <dd>{perfume.notes}</dd>
          </div>
        )}
        {perfume.rating !== undefined && (
          <div className={styles.metaItem}>
            <dt>Rating</dt>
            <dd className={styles.rating}>{perfume.rating.toFixed(1)}</dd>
          </div>
        )}
      </dl>
    </article>
  );
}
