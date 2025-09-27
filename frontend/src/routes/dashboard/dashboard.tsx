import styles from "./dashboard.module.css"
import Button from "../../components/button/button.tsx"
import Card from "../../components/card/card.tsx"
import NutrientCard from "../../components/nutrient-card/nutrient-card.tsx"
import {Icon} from "@iconify/react";
import Divider from "../../components/divider/divider.tsx";
import {useNavigate} from "react-router";

export default function Dashboard() {
  const navigate = useNavigate();

  return (
    <div className={styles.page}>
      <Button variant="primary" text="Get started" />
      <Button variant="secondary" text="Get started" />

      <Card variant="plain">
        Hello!
      </Card>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gridTemplateRows: '50% 50%', gap: '10px' }}>
        <NutrientCard />
        <NutrientCard />
        <NutrientCard />
        <NutrientCard />
      </div>

      <Divider />

      <h2>Log your Meal</h2>
      <div className={styles.logButtonContainer}>
        <Button
          variant="primary"
          size="lg"
          fill
        >
          <div className={styles.logButton}>
            <Icon icon="material-symbols:photo-camera-outline-rounded" width={28} />
            Camera
          </div>
        </Button>

        <div className={styles.logButtonContainerRight}>
          <Button variant="secondary" size="md" onClick={() => navigate("/text-log")}>
            <div className={styles.logButton}>
              <Icon icon="material-symbols:business-messages-outline-rounded" width={24} />
              Text
            </div>
          </Button>

          <Button variant="secondary" size="md">
            <div className={styles.logButton}>
              <Icon icon="mdi:microphone-outline" width={24} />
              Speak
            </div>
          </Button>
        </div>
      </div>

    </div>
  )
}
