import styles from './food-entry.module.css'
import CenteredPage from "../../components/centered-page/centered-page.tsx";
import Divider from "../../components/divider/divider.tsx";
import NutrientCard from "../../components/nutrient-card/nutrient-card.tsx";
import {useLocation} from "react-router";
import {useMutation, useQuery, useQueryClient} from "@tanstack/react-query";
import {handleRequest} from "../../util.ts";
import type {FoodEntry} from "../../models.ts";

interface NutrientUpdateData {
  nutrient: string,
  newValue: number | string,
}

export default function FoodEntry() {
  const queryClient = useQueryClient()
  const location = useLocation()
  const foodEntryId = location.hash.substring(1)

  const foodEntryQuery = useQuery({
    queryKey: ['food-query', foodEntryId],
    queryFn: async () => {
      const [resp, status] = await handleRequest("GET", `/api/foods/${foodEntryId}`);
      if (Math.floor(status / 100) !== 2) {
        throw new Error("Unknown error")
      }
      return resp as FoodEntry
    }
  })

  const nutrientUpdateMutation = useMutation({
    mutationKey: ['nutrient-update'],
    mutationFn: async ({nutrient, newValue}: NutrientUpdateData) => {
      const foodEntryNew: {[key: string]: string | number | unknown} = {...foodEntryQuery.data!}
      foodEntryNew[nutrient] = newValue
      delete foodEntryNew['created_at']
      delete foodEntryNew['user_id']
      delete foodEntryNew['id']

      const [resp, status] = await handleRequest("PUT", `/api/foods/${foodEntryId}/`, foodEntryNew)
      if (Math.floor(status / 100) !== 2) {
        throw new Error("Unknown error")
      }

      return resp as FoodEntry
    },
    onSuccess: async (data) => {
      await queryClient.cancelQueries({ queryKey: ['food-query', foodEntryId] })
      // const oldQueryData: Memory[] = queryClient.getQueryData(['food-query', foodEntryId]) ?? {}
      // const newQueryData = {...oldQueryData, []}
      queryClient.setQueryData(['food-query', foodEntryId], data)
    }
  })

  if (foodEntryQuery.isLoading) {
    return "Loading..."
  }

  const foodEntry = foodEntryQuery.data!

  return (
    <CenteredPage innerClassName={styles.container}>
      <div>
        <p style={{ color: 'var(--note)' }}>Food Entry</p>
        <h1>{foodEntry.name}</h1>
      </div>

      <Divider />

      <div className={styles.baseInfoContainer}>
        <h3>Logged at</h3>
        <p>{new Date(foodEntry.created_at).toLocaleString()}</p>
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
        <NutrientCard nutrient="Calories" count={foodEntry.calories} unit="kcal"
                      onSave={(newValue: string) => nutrientUpdateMutation.mutate({nutrient: 'calories', newValue})}/>
        <NutrientCard nutrient="Protein" count={foodEntry.protein} unit="g"
                      onSave={(newValue: string) => nutrientUpdateMutation.mutate({nutrient: 'protein', newValue})}/>
        <NutrientCard nutrient="Carbohydrates" count={foodEntry.carbohydrates} unit="g"
                      onSave={(newValue: string) => nutrientUpdateMutation.mutate({
                        nutrient: 'carbohydrates',
                        newValue
                      })}/>
        <NutrientCard nutrient="Trans Fat" count={foodEntry.trans_fat} unit="g"
                      onSave={(newValue: string) => nutrientUpdateMutation.mutate({nutrient: 'trans_fat', newValue})}/>
        <NutrientCard nutrient="Saturated Fat" count={foodEntry.saturated_fat} unit="g"
                      onSave={(newValue: string) => nutrientUpdateMutation.mutate({
                        nutrient: 'saturated_fat',
                        newValue
                      })}/>
        <NutrientCard nutrient="Unsaturated Fat" count={foodEntry.unsaturated_fat} unit="g"
                      onSave={(newValue: string) => nutrientUpdateMutation.mutate({
                        nutrient: 'unsaturated_fat',
                        newValue
                      })}/>
      </div>
    </CenteredPage>
  )
}
