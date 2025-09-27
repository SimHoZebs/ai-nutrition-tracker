import styles from './follow-up.module.css'
import CenteredPage from "../../components/centered-page/centered-page.tsx";
import MultipleChoiceQuestion from "../../components/multiple-choice-question/multiple-choice-question.tsx";
import Divider from "../../components/divider/divider.tsx";
import Button from "../../components/button/button.tsx";
import {useLocation} from "react-router";
import type {Question} from "../../models.ts";

export default function FollowUp() {

  const location = useLocation()
  const followUpQuestions: Question[] = location.state?.followUpQuestions;

  return (
    <CenteredPage innerClassName={styles.followUpContainer}>
      <div>
        <h1>Follow Up Questions</h1>
        <p style={{ color: 'var(--note)' }}>
          For a more accurate estimate, please answer the following questions.
        </p>
      </div>

      <div className={styles.questions}>
        {followUpQuestions.map((question, index) => (
          <div>
            <p style={{ color: 'var(--note)' }}>Question {index + 1}</p>
            {question.type === 'multiple_choice' && (
              <MultipleChoiceQuestion key={index} question={question.question} choices={question.mcqOptions} />
            )}
          </div>
        ))}
      </div>

      <Divider />


      <Button variant="primary" text="Submit" />

    </CenteredPage>
  )
}
