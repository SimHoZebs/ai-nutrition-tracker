import type {ReactNode, MouseEvent} from "react";
import styles from './button.module.css'
import clsx from "clsx";

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger',
  size?: 'md' | 'lg',
  text?: string,
  fill?: boolean,
  disabled?: boolean,
  onClick?: (e: MouseEvent) => void,
  children?: ReactNode[] | ReactNode,
}

export default function Button({
  variant = 'primary',
  size = 'md',
  text,
  fill = false,
  disabled = false,
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
        [styles.large]: size === 'lg',
        [styles.medium]: size === 'md',
        [styles.disabled]: disabled,
      })}
      onClick={(e) => onClick(e)}
    >
      { text ? text : children }
    </button>
  )
}
