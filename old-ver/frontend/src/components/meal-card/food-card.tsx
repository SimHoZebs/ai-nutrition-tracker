import styles from './meal-card.module.css'
import Card from "../card/card.tsx";
import type {FoodEntry} from "../../models.ts";
import {useLocation, useNavigate} from "react-router";

interface FoodCardProps {
  foodEntry: FoodEntry;
}

export default function FoodCard({ foodEntry }: FoodCardProps) {
  const navigate = useNavigate();
  const location = useLocation();

  const goToFoodEntry = () => {
    if (foodEntry.processing) return;
    navigate(`/food-entry#${foodEntry.id}`, {state: {lastLocation: location.pathname}})
  }

  return (
    <Card className={styles.mealCard} variant="blue" onClick={goToFoodEntry}>
      <p style={{ whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflowX: 'hidden' }}><b>{foodEntry.name}</b></p>
      {foodEntry.processing && (
        <p className={styles.subText} style={{ fontStyle: 'italic' }}>Processing...</p>
      )}
      {!foodEntry.processing && (
        <p className={styles.subText}>{foodEntry.meal_type} &bull; {foodEntry.calories}kcal &bull; {foodEntry.protein}g protein</p>
      )}
    </Card>
  )
}
