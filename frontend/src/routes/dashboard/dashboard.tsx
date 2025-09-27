import Button from "../../components/button/button.tsx";
import Card from "../../components/card/card.tsx";
import NutrientCard from "../../components/nutrient-card/nutrient-card.tsx";

export default function Dashboard() {
  return (
    <div style={{ padding: '10px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
      <Button variant="primary" text="Get started" />
      <Button variant="secondary" text="Get started" />
      <Card variant="plain">
        Hello!
      </Card>

      <div style={{ display: 'grid', gridTemplateColumns: '50% 50%', gridTemplateRows: '50% 50%', gap: '10px' }}>
        <NutrientCard />
        <NutrientCard />
        <NutrientCard />
        <NutrientCard />
      </div>
    </div>
  )
}
