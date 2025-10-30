import styles from './nutrient-card.module.css'
import Card from '../card/card.tsx'
import Button from "../button/button.tsx";
import Modal from "../modal/modal.tsx";
import {useState} from "react";
import Textbox from "../textbox/textbox.tsx";

interface NutrientCardProps {
  nutrient: string
  count: number
  unit: string
  onSave: (newValue: string) => void
}

export default function NutrientCard({ nutrient, count, unit, onSave }: NutrientCardProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [value, setValue] = useState<string>(count.toString())

  const openEditPage = () => {
    setIsOpen(true)
  }

  const save = () => {
    setIsOpen(false)
    onSave(value)
  }

  return (
    <>
      <Card className={styles.nutrientCard} variant='plain' onClick={openEditPage}>
        <h2 style={{ fontSize: 'var(--font-size-1)' }}>{nutrient}</h2>
        <div className={styles.counter}>
          <p>{count}</p>
          <p className={styles.unit}>{unit}</p>
        </div>
      </Card>

      {isOpen && (
        <Modal>
          <div className={styles.editValueModalContainer}>
            <h2>Edit {nutrient}</h2>
            <Textbox value={value} onChange={setValue} />
            <div className={styles.buttons}>
              <Button variant="secondary" text="Cancel" fill onClick={() => {setIsOpen(false)}} />
              <Button variant="primary" text="Save" fill onClick={save} />
            </div>
          </div>
        </Modal>
      )}
    </>
  )
}
