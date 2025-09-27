import styles from './textarea.module.css'

interface TextAreaProps {
}

export default function TextArea() {
  return (
    <textarea
      className={styles.textbox}
    />
  )
}
