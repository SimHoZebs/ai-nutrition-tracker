import styles from './nutrient-card.module.css'
import Card from '../card/card.tsx'

export default function NutrientCard() {
  return (
    <Card className={styles.nutrientCard} variant='plain'>
      <h2 style={{ fontSize: 'var(--font-size-1)' }}>Calories</h2>
      <div className={styles.counter}>
        <p>100/100</p>

      </div>
    </Card>
  )
}
