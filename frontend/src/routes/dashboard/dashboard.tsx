import styles from "./dashboard.module.css";
import Button from "../../components/button/button.tsx";
import NutrientCard from "../../components/nutrient-card/nutrient-card.tsx";
import { Icon } from "@iconify/react";
import Divider from "../../components/divider/divider.tsx";
import { useNavigate } from "react-router";
import MealCard from "../../components/meal-card/meal-card.tsx";
import AudioRecorder from "../../components/audio-recorder/audio-recorder.tsx";

export default function Dashboard() {
  const navigate = useNavigate();

  return (
    <>
      <h1>LazyFood.</h1>

      <h2>Today's Goals</h2>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gridTemplateRows: "50% 50%",
          gap: "10px",
        }}
      >
        <NutrientCard />
        <NutrientCard />
      </div>

      <Divider />

      <h2>Today's Meals</h2>
      <MealCard />
      <MealCard />
      <MealCard />

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
