import styles from './modal.module.css'
import type {ReactNode} from "react";

interface ModalProps {
  children: ReactNode | ReactNode[],
}

export default function Modal({ children }: ModalProps) {
  return (
    <div className={styles.backdrop}>
      <div className={styles.modal}>
        {children}
      </div>
    </div>
  )
}
