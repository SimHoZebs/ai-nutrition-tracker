import styles from "./button.module.css";
import clsx from "clsx";
import { useState } from "react";

interface ButtonProps extends React.HTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "danger";
  size?: "md" | "lg";
  text?: string;
  fill?: boolean;
  disabled?: boolean;
  onClickAsync?: () => Promise<void>;
}

export default function Button({
  variant = "primary",
  size = "md",
  text,
  fill = false,
  disabled = false,
  onClick = () => {},
  onClickAsync,
  children = [],
}: ButtonProps) {
  const [isLoading, setIsLoading] = useState(false);

  const handleClick = async (e: React.MouseEvent<HTMLButtonElement>) => {
    if (onClickAsync) {
      setIsLoading(true);
      await onClickAsync();
      setIsLoading(false);
    } else {
      onClick(e);
    }
  };
  return (
    <button
      className={clsx({
        [styles.baseButton]: true,
        [styles.fill]: fill,
        [styles.primary]: variant === "primary",
        [styles.secondary]: variant === "secondary",
        [styles.danger]: variant === "danger",
        [styles.large]: size === "lg",
        [styles.medium]: size === "md",
        [styles.disabled]: disabled || isLoading,
      })}
      onClick={handleClick}
      disabled={disabled || isLoading}
    >
      {isLoading ? <div className={styles.spinner} /> : text ? text : children}
    </button>
  );
}
