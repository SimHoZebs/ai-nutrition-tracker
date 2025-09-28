import styles from './back-button.module.css'
import {Icon} from "@iconify/react";
import {useLocation, useNavigate} from "react-router";
import type {Question} from "../../models.ts";

export default function BackButton() {
  const navigate = useNavigate();

  const location = useLocation()
  const lastLocation: string = location.state?.lastLocation ?? '/'

  return (
    <button
      className={styles.backButton}
      onClick={() => navigate(lastLocation)}
    >
      <Icon icon="mdi:arrow-back" width={28}/>
    </button>
  )
}
