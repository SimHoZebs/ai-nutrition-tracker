import styles from './textbox.module.css'

interface TextboxProps {
  value: string,
  onChange: (value: string) => void,
}

export default function Textbox({ value, onChange }: TextboxProps) {
  return (
    <input
      className={styles.textbox}
      type="text"
      value={value}
      onChange={(e) => onChange(e.target.value)}
    />
  )
}
