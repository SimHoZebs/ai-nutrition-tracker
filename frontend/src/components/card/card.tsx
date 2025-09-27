import type {ReactNode} from 'react';
import styles from './card.module.css';
import clsx from 'clsx';

interface CardProps {
  variant?: 'plain' | 'blue';
  className?: string;
  children: ReactNode | ReactNode[];
}

export default function Card({variant = 'plain', className = "", children}: CardProps) {
  return (
    <div
      className={clsx(styles.card, {
        [styles.plain]: variant === 'plain',
        [styles.blue]: variant === 'blue',
        [className]: true,
      })}
    >
      {}
      {children}
    </div>
  );
}
