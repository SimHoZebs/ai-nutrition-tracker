import styles from './user-profile.module.css'
import {Icon} from "@iconify/react";
import Button from "../../components/button/button.tsx";
import MemoryItem from "../../components/memory-item/memory-item.tsx";
import Divider from "../../components/divider/divider.tsx";
export default function UserProfile() {
  return (
    <>
      <h1>Your Profile</h1>
      <div className={styles.userHeader}>
        <Icon icon="ri:user-line" width={85} />

        <div className={styles.userHeaderRight}>
          <h2>John Doe</h2>
          <p>johndoe@gmail.com</p>
        </div>
      </div>

      <div className={styles.section}>
        <h2>Goals</h2>
      </div>

      <div className={styles.section}>
        <div className={styles.buttonHeader}>
          <h2>Memories</h2>
          <Button variant="primary" text="Add" />
        </div>

        <MemoryItem />
        <Divider />
        <MemoryItem />
        <Divider />
        <MemoryItem />
        <Divider />

        <MemoryItem />
      </div>
    </>
  )
}
