import styles from './back-button.module.css'
import {Icon} from "@iconify/react";
import {useNavigate} from "react-router";

export default function BackButton() {
  const navigate = useNavigate();

  return (
    <button
      className={styles.backButton}
      onClick={() => navigate("/")}
    >
      <Icon icon="mdi:arrow-back" width={28}/>
    </button>
  )
}
