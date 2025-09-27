import styles from './multiple-choice-question.module.css'
import {useState} from 'react'
import Button from "../button/button.tsx";

interface MultipleChoiceQuestionProps {
  question: string;
  choices: string[];
  onSelect?: (choice: string) => void;
}

export default function MultipleChoiceQuestion({question, choices, onSelect}: MultipleChoiceQuestionProps) {
  const [selectedChoice, setSelectedChoice] = useState<number | null>(null);

  return (
    <div className={styles.multipleChoiceContainer}>
      <h2>{question}</h2>
      <div className={styles.choices}>
        {choices.map((choice, index) => (
          <Button
            key={index}
            variant={index === selectedChoice ? 'primary' : 'secondary'}
            text={choice}
            onClick={() => setSelectedChoice(index)}
          />
        ))}
      </div>
    </div>
  )
}
