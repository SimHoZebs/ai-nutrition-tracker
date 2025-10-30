import { Icon } from "@iconify/react";
import styles from './floating-ai-button.module.css';

interface FloatingAIButtonProps {
  onClick: () => void;
}

export default function FloatingAIButton({ onClick }: FloatingAIButtonProps) {
  return (
    <button 
      className={styles.floatingButton}
      onClick={onClick}
      aria-label="Open AI Assistant"
    >
      <Icon icon="mdi:robot-outline" width={24} height={24} />
    </button>
  );
}