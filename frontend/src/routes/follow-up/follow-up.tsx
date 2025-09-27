import styles from './follow-up.module.css'
import CenteredPage from "../../components/centered-page/centered-page.tsx";

export default function FollowUp() {

  const followUps = [
    {
      id: 1,
      followUpType: 'multiple-choice',
      choices: [
        'Chicken',
        'Beef',
        'Pork',
      ]
    }
  ]

  return (
    <CenteredPage>
      <h1>Follow Up Questions</h1>
      <p style={{ color: 'var(--note)' }}>
        For a more accurate estimate, please answer the following questions.
      </p>
    </CenteredPage>
  )
}
