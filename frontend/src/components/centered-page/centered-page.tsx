import styles from './centered-page.module.css'
import type {ReactNode} from "react";
import BackButton from "../back-button/back-button.tsx";

interface CenteredPageProps {
  innerClassName? : string;
  children: ReactNode | ReactNode[];
}

export default function CenteredPage({ innerClassName = "", children }: CenteredPageProps) {
  return (
    <div className={styles.centeredPage}>
      <BackButton />

      <div className={innerClassName}>
        {children}
      </div>
    </div>
  )
}
