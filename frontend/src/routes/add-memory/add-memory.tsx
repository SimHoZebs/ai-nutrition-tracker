import styles from './add-memory.module.css'
import CenteredPage from "../../components/centered-page/centered-page.tsx";
import TextArea from "../../components/textarea/textarea.tsx";
import Button from "../../components/button/button.tsx";
import {useState} from "react";

export default function AddMemory() {
  const [memoryValue, setMemoryValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const submitMemory = () => {
    setIsLoading(true);
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
