import styles from './meal-card.module.css'
import Card from "../card/card.tsx";

interface MealCardProps {
  processing: boolean;
}

export default function MealCard({ processing }: MealCardProps) {
  return (
    <Card className={styles.mealCard} variant="blue">
      <p><b>Chicken Sandwich</b></p>
      {processing && (
        <p className={styles.subText} style={{ fontStyle: 'italic' }}>Processing...</p>
      )}
      {!processing && (
        <p className={styles.subText}>10:24AM &bull; 489kcal &bull; 10g protein</p>
      )}
    </Card>
  )
}
