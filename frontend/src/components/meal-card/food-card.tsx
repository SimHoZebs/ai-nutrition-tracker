import styles from './meal-card.module.css'
import Card from "../card/card.tsx";
import type {FoodEntry} from "../../models.ts";
import {useLocation, useNavigate} from "react-router";

interface FoodCardProps {
  foodEntry: FoodEntry;
  processing?: boolean;
}

export default function FoodCard({ foodEntry, processing = false }: FoodCardProps) {
  const navigate = useNavigate();
  const location = useLocation();

  const goToFoodEntry = () => {
    navigate(`/food-entry#${foodEntry.id}`, {state: {lastLocation: location.pathname}})
  }

  return (
    <Card className={styles.mealCard} variant="blue" onClick={goToFoodEntry}>
      <p><b>{foodEntry.name}</b></p>
      {processing && (
        <p className={styles.subText} style={{ fontStyle: 'italic' }}>Processing...</p>
      )}
      {!processing && (
        <p className={styles.subText}>{foodEntry.meal_type} &bull; {foodEntry.calories}kcal &bull; {foodEntry.protein}g protein</p>
      )}
    </Card>
  )
}
