import styles from './add-memory.module.css'
import CenteredPage from "../../components/centered-page/centered-page.tsx";
import TextArea from "../../components/textarea/textarea.tsx";
import Button from "../../components/button/button.tsx";
import {useState} from "react";
import {useMutation} from "@tanstack/react-query";
import {handleRequest} from "../../util.ts";
import {useNavigate} from "react-router";

export default function AddMemory() {
  const navigate = useNavigate();

  const [memoryValue, setMemoryValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const memoryMutation = useMutation({
    mutationKey: ["createMemory"],
    mutationFn: async () => {
      const body = {
        content: memoryValue,
      }
      const [_, status] = await handleRequest("POST", "/api/memories/", body)
      if (Math.floor(status / 100) !== 2) {
        throw new Error('Unknown error')
      }
    },
    onSuccess: () => {
      navigate('/user')
    }
  })

  const submitMemory = () => {
    setIsLoading(true);
    memoryMutation.mutate()
  }

  return (
    <CenteredPage innerClassName={styles.addMemoryContainer}>
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        <h1>Add a Memory</h1>
        <p style={{ color: 'var(--note)'}}>LazyFood will take into consideration your memories when analyzing food.</p>
      </div>
      <TextArea value={memoryValue} onChange={setMemoryValue} />
      <Button variant="primary" text="Log" disabled={isLoading} onClick={submitMemory} />

      {isLoading && (
        <p className={styles.loadingText}>Saving memory...</p>
      )}
    </CenteredPage>
  )
}
