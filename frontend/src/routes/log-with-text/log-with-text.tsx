import styles from './log-with-text.module.css'
import CenteredPage from "../../components/centered-page/centered-page.tsx";
import TextArea from "../../components/textarea/textarea.tsx";
import Button from "../../components/button/button.tsx";
import {useState} from "react";
import {useNavigate} from "react-router";
import {useMutation} from "@tanstack/react-query";

export default function LogWithText() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);

  const [descriptionValue, setDescriptionValue] = useState<string>("");

  const submitMutation = useMutation({
    mutationFn: async (mealDescription: string) => {
      const body = {
        description: mealDescription,
      }
      const res = await fetch('http://localhost:1234/api/do_smth', {
        method: 'POST',
        body: JSON.stringify(body),
      })
      return res.json()
    },
    onSuccess: async (result: string) => {
      console.log(result);
    }
  });

  const submitLog = () => {
    setIsLoading(true);
    // setTimeout(() => {
    //   navigate("/follow-up");
    // }, 1000)

    submitMutation.mutate(descriptionValue)
  }

  return (
    <CenteredPage innerClassName={styles.logWithTextContainer}>
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        <h1>Describe your Meal</h1>
        <p style={{ color: 'var(--note)'}}>Be sure to include details like portion size and ingredients!</p>
      </div>
      <TextArea value={descriptionValue} onChange={setDescriptionValue} />
      <Button variant="primary" text="Log" disabled={isLoading} onClick={submitLog} />

      {submitMutation.isSuccess && submitMutation.data}
      {submitMutation.isError && "Oopsie shit blew up"}

      {isLoading && (
        <p className={styles.loadingText}>
          Submitting log...
        </p>
      )}
    </CenteredPage>
  )
}
