import styles from './log-with-text.module.css'
import CenteredPage from "../../components/centered-page/centered-page.tsx";
import TextArea from "../../components/textarea/textarea.tsx";
import Button from "../../components/button/button.tsx";
import {useState} from "react";
import {useNavigate} from "react-router";

export default function LogWithText() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);

  const submitLog = () => {
    setIsLoading(true);
    setTimeout(() => {
      navigate("/follow-up");
    }, 1000)
  }

  return (
    <CenteredPage innerClassName={styles.logWithTextContainer}>
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        <h1>Describe your Meal</h1>
        <p style={{ color: 'var(--note)'}}>Be sure to include details like portion size and ingredients!</p>
      </div>
      <TextArea />
      <Button variant="primary" text="Log" disabled={isLoading} onClick={submitLog} />

      {isLoading && (
        <p className={styles.loadingText}>
          Submitting log...
        </p>
      )}
    </CenteredPage>
  )
}
