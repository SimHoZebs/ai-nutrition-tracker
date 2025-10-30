import styles from "./history.module.css";
import { handleRequest } from "../../util.ts";
import { useQuery } from "@tanstack/react-query";
import type { FoodEntry } from "../../models.ts";
import FoodCard from "../../components/meal-card/food-card.tsx";

export default function History() {
  const historyQuery = useQuery({
    queryKey: ["history"],
    queryFn: async () => {
      const [resp, status] = await handleRequest("GET", "/api/foods/");
      if (Math.floor(status / 100) !== 2) {
        throw new Error("Unknown error");
      }

      return resp as FoodEntry[];
    },
  });

  if (historyQuery.isLoading) {
    return "Loading...";
  }

  const groupedByDate = historyQuery.data?.reduce<{
    [key: string]: FoodEntry[];
  }>((acc, item) => {
    const date = new Date(item.eaten_at).toLocaleDateString();
    acc[date] = acc[date] || [];
    acc[date].push(item);
    return acc;
  }, {});

  console.log(groupedByDate);

  return (
    <div className={styles.container}>
      <div>
        <h1>History</h1>
        <p style={{ color: "var(--note)" }}>View your previous meal logging</p>
      </div>
      {Object.entries(groupedByDate || {})
        .sort(
          ([dateA], [dateB]) =>
            new Date(dateB).getTime() - new Date(dateA).getTime(),
        )
        .map(([date, items]) => (
          <div key={date}>
            <div className={styles.container}>
              <h2>
                {date === new Date().toLocaleDateString() ? "Today" : date}
              </h2>
              {items.map((item) => (
                <FoodCard key={item.id} foodEntry={item} />
              ))}
            </div>
          </div>
        ))}
    </div>
  );
}
