import styles from './food-entry.module.css'
import CenteredPage from "../../components/centered-page/centered-page.tsx";
import Divider from "../../components/divider/divider.tsx";
import NutrientCard from "../../components/nutrient-card/nutrient-card.tsx";
import {useLocation} from "react-router";
import {useQuery} from "@tanstack/react-query";
import {handleRequest} from "../../util.ts";


export default function FoodEntry() {
  const location = useLocation()
  const foodEntryId = location.hash.substring(1)
  console.log(foodEntryId)

  const foodEntryQuery = useQuery({
    queryKey: ['food-query', foodEntryId],
    queryFn: async () => {
      const [resp, status] = await handleRequest("GET", `/api/food/${foodEntryId}`);
      if (Math.floor(status / 100) !== 2) {
        throw new Error("Unknown error")
      }
      return resp
    }
  })

  if (foodEntryQuery.isLoading) {
    return "Loading..."
  }

  return (
    <CenteredPage innerClassName={styles.container}>
      <div>
        <p style={{ color: 'var(--note)' }}>Food Entry</p>
        <h1>Chicken Sandwich</h1>
      </div>

      <Divider />

      <div className={styles.baseInfoContainer}>
        <h3>Logged at</h3>
        <p>{foodEntry.created_at}</p>
        <h3>Meal</h3>
        <p>{foodEntry.meal_type}</p>
      </div>

      <Divider />

      <div>
        <h2>Nutrients</h2>
        <p style={{ color: 'var(--note)' }}>
          Tap any card to edit
        </p>
      </div>

      <div className={styles.nutrientsContainer}>
        <NutrientCard nutrient="Calories" count={foodEntry.calories} unit="kcal" />
        <NutrientCard nutrient="Protein" count={foodEntry.protein} unit="kcal"/>
        <NutrientCard nutrient="Carbohydrates" count={foodEntry.carbohydrates} unit="kcal"/>
        <NutrientCard nutrient="Trans Fat" count={foodEntry.trans_fat} unit="kcal"/>
        <NutrientCard nutrient="Saturated Fat" count={foodEntry.saturated_fat} unit="kcal"/>
        <NutrientCard nutrient="Unsaturated Fat" count={foodEntry.unsaturated_fat} unit="kcal"/>
      </div>
    </CenteredPage>
  )
}
