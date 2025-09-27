import type {ReactNode} from "react";
import styles from './button.module.css'
import clsx from "clsx";

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger'
  text?: string
  fill?: boolean,
  onClick?: () => void,
  children?: ReactNode[] | ReactNode;
}

export default function Button({
  variant = 'primary',
  text,
  fill = false,
  onClick = () => {},
  children = [],
}: ButtonProps) {
  return (
    <button
      className={clsx({
        [styles.baseButton]: true,
        [styles.fill]: fill,
        [styles.primary]: variant === 'primary',
        [styles.secondary]: variant === 'secondary',
        [styles.danger]: variant === 'danger',
      })}
      onClick={onClick}
    >
      { text ? text : children }
    </button>
  )
}
