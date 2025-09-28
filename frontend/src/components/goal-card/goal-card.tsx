import styles from './goal-card.module.css'
import Card from "../card/card.tsx";

interface GoalCardProps {
  nutrient: string
  count: number
  unit: string
}

export default function GoalCard({ nutrient, count, unit }: GoalCardProps) {
  return (
    <Card className={styles.goalCard} variant='plain'>
      <h2 style={{ fontSize: 'var(--font-size-1)' }}>{nutrient}</h2>
      <div className={styles.counter}>
        <p>{count}</p>
        <p className={styles.unit}>{unit}</p>
      </div>
    </Card>
  )
}
