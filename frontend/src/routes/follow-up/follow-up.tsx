import styles from './follow-up.module.css'
import CenteredPage from "../../components/centered-page/centered-page.tsx";
import MultipleChoiceQuestion from "../../components/multiple-choice-question/multiple-choice-question.tsx";
import Divider from "../../components/divider/divider.tsx";
import Button from "../../components/button/button.tsx";

export default function FollowUp() {

  const followUps = [
    {
      id: 1,
      followUpType: 'multiple-choice',
      question: 'What is the main meat used for this dish?',
      choices: [
        'Chicken',
        'Beef',
        'Pork',
      ]
    },
    {
      id: 2,
      followUpType: 'multiple-choice',
      question: 'What type of bread was used?',
      choices: [
        'White',
        'Whole Wheat',
        'Diet Bread or smth',
      ]
    },
    {
      id: 3,
      followUpType: 'multiple-choice',
      question: 'What type of bread was used?',
      choices: [
        'White',
        'Whole Wheat',
        'Diet Bread or smth',
      ]
    }
  ]

  return (
    <CenteredPage innerClassName={styles.followUpContainer}>
      <div>
        <h1>Follow Up Questions</h1>
        <p style={{ color: 'var(--note)' }}>
          For a more accurate estimate, please answer the following questions.
        </p>
      </div>

      <div className={styles.questions}>
        {followUps.map((question, index) => (
          <div>
            <p style={{ color: 'var(--note)' }}>Question {index + 1}</p>
            <MultipleChoiceQuestion question={question.question} choices={question.choices} />
          </div>
        ))}
      </div>

      <Divider />


      <Button variant="primary" text="Submit" />

    </CenteredPage>
  )
}
