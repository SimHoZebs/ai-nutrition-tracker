import styles from "./dashboard.module.css";
import Button from "../../components/button/button.tsx";
import { Icon } from "@iconify/react";
import Divider from "../../components/divider/divider.tsx";
import { useNavigate } from "react-router";
import FoodCard from "../../components/meal-card/food-card.tsx";
import { useQuery } from "@tanstack/react-query";
import { handleRequest } from "../../util.ts";
import type { FoodEntry } from "../../models.ts";
import AudioRecorder from "../../components/audio-recorder/audio-recorder.tsx";
import GoalCard from "../../components/goal-card/goal-card.tsx";
import { useMemo } from "react";

export default function Dashboard() {
  const navigate = useNavigate();

  const historyQuery = useQuery({
    queryKey: ["history"],
    queryFn: async () => {
      const [resp, status] = await handleRequest("GET", "/api/foods/");
      if (Math.floor(status / 100) !== 2) {
        throw new Error("Unknown error");
      }

      return resp as FoodEntry[];
    },
    staleTime: 5000,
  });

  // Calculate goals
  const [calP, proP, carP, fatP] = useMemo(() => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const todayEntries =
      historyQuery.data?.filter((entry) => {
        const entryDate = new Date(entry.eaten_at);
        entryDate.setHours(0, 0, 0, 0);
        return entryDate.getTime() === today.getTime();
      }) ?? [];

    const calories = todayEntries.reduce(
      (sum, entry) => sum + entry.calories,
      0,
    );
    const protein = todayEntries.reduce((sum, entry) => sum + entry.protein, 0);
    const carbs = todayEntries.reduce(
      (sum, entry) => sum + entry.carbohydrates,
      0,
    );
    const fats = todayEntries.reduce(
      (sum, entry) =>
        sum + entry.trans_fat + entry.saturated_fat + entry.unsaturated_fat,
      0,
    );

    const caloriesPercent = Math.round((calories / 2000) * 100);
    const proteinPercent = Math.round((protein / 50) * 100);
    const carbsPercent = Math.round((carbs / 275) * 100);
    const fatsPercent = Math.round((fats / 65) * 100);

    return [caloriesPercent, proteinPercent, carbsPercent, fatsPercent];
  }, [historyQuery.data]);

  return (
    <>
      <h1>LazyFood.</h1>

      {/*<h2>Today's Goals</h2>*/}
      {/*<div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gridTemplateRows: '50% 50%', gap: '10px', marginBottom: '10px' }}>*/}
      {/*  <GoalCard nutrient="Calories" count={calP} unit="kcal"/>*/}
      {/*  <GoalCard nutrient="Protein" count={proP} unit="g"/>*/}
      {/*  <GoalCard nutrient="Carbs" count={carP} unit="g"/>*/}
      {/*  <GoalCard nutrient="Fats" count={fatP} unit="g"/>*/}
      {/*</div>*/}

      <Divider />

      <h2>Recent Meals</h2>

      {historyQuery.data?.slice(0, 6).map((item) => (
        <FoodCard key={item.id} foodEntry={item} />
      ))}

      {(historyQuery.data?.length ?? 0) > 6 && (
        <button
          className={styles.seeMoreLink}
          onClick={() => {
            navigate("/history");
          }}
        >
          See more <Icon icon="mdi:arrow-right" />
        </button>
      )}
    </>
  );
}
