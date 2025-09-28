import styles from './memory-item.module.css'
import Button from "../button/button.tsx";
import {Icon} from "@iconify/react";

export default function MemoryItem() {
  return (
    <div className={styles.memoryItem}>
      No salt on fries

      <Button variant="secondary">
        <Icon icon="mdi:trash-outline" />
      </Button>
    </div>
  )
}
