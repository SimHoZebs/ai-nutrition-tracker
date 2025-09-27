import styles from './textarea.module.css'

interface TextAreaProps {
  value: string,
  onChange: (value: string) => void,
}

export default function TextArea({ value, onChange }: TextAreaProps) {
  return (
    <textarea
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className={styles.textbox}
    />
  )
}
