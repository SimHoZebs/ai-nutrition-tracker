import styles from "./dashboard.module.css"
import Button from "../../components/button/button.tsx"
import {Icon} from "@iconify/react";
import Divider from "../../components/divider/divider.tsx";
import {useNavigate} from "react-router";
import FoodCard from "../../components/meal-card/food-card.tsx";
import {useQuery} from "@tanstack/react-query";
import {handleRequest} from "../../util.ts";
import type {FoodEntry} from "../../models.ts";
import AudioRecorder from "../../components/audio-recorder/audio-recorder.tsx";

export default function Dashboard() {
  const navigate = useNavigate();

  const historyQuery = useQuery({
    queryKey: ['history'],
    queryFn: async () => {
      const [resp, status] = await handleRequest("GET", "/api/foods/")
      if (Math.floor(status / 100) !== 2) {
        throw new Error("Unknown error")
      }

      return resp as FoodEntry[]
    }
  })

  return (
    <>
      <h1>LazyFood.</h1>

      <h2>Today's Goals</h2>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gridTemplateRows: '50% 50%', gap: '10px' }}>
      </div>

      <Divider />

      <h2>Today's Meals</h2>
      {
        historyQuery.data?.slice(0, 3).map((item) => (
          <FoodCard key={item.id} foodEntry={item} />
        ))
      }

      {(historyQuery.data?.length ?? 0 > 3) && (
        <button
          className={styles.seeMoreLink}
          onClick={() => {navigate('/history')}}
        >
          See more <Icon icon="mdi:arrow-right" />
        </button>
      )}

      <Divider />

      <h2>Log your Meal</h2>
      <div className={styles.logButtonContainer}>
        <Button variant="primary" size="lg" fill>
          <div className={styles.logButton}>
            <Icon
              icon="material-symbols:photo-camera-outline-rounded"
              width={28}
            />
            Camera
          </div>
        </Button>

        <div className={styles.logButtonContainerRight}>
          <Button
            variant="secondary"
            size="md"
            onClick={() => navigate("/text-log")}
          >
            <div className={styles.logButton}>
              <Icon
                icon="material-symbols:business-messages-outline-rounded"
                width={24}
              />
              Text
            </div>
          </Button>

          <AudioRecorder variant="secondary" size="md" />
        </div>
      </div>
    </>
  );
}
