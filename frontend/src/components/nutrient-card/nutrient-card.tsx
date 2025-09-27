import styles from './nutrient-card.module.css'
import Card from '../card/card.tsx';

export default function NutrientCard() {
  return (
    <Card className={styles.nutrientCard} variant='plain'>
      <h2>Calories</h2>
      <p>100</p>
    </Card>
  )
}
