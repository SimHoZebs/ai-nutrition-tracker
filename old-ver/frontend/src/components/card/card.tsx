import type {ReactNode, MouseEvent} from 'react';
import styles from './card.module.css';
import clsx from 'clsx';

interface CardProps {
  variant?: 'plain' | 'blue';
  className?: string;
  onClick?: (e: MouseEvent) => void;
  children: ReactNode | ReactNode[];
}

export default function Card({variant = 'plain', className = "", onClick = () => {}, children}: CardProps) {
  return (
    <div
      className={clsx(styles.card, {
        [styles.plain]: variant === 'plain',
        [styles.blue]: variant === 'blue',
        [className]: true,
      })}
      onClick={e => onClick(e)}
    >
      {}
      {children}
    </div>
  );
}
