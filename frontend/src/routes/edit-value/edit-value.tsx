import styles from './edit-value.module.css'
import useLastLocation from "../../useLastLocation.ts";
import {useLocation} from "react-router";
import CenteredPage from "../../components/centered-page/centered-page.tsx";
import TextArea from "../../components/textarea/textarea.tsx";
import Button from "../../components/button/button.tsx";
import {useState} from "react";

export default function EditValue() {
  const lastLocation = useLastLocation()

  const location = useLocation()
  const title = location.state?.title ?? ''
  const note = location.state?.note ?? ''
  const initialValue = location.state?.initialValue ?? ''
  const onSave = location.state?.onSave ?? (() => {})

  const [value, setValue] = useState<string>(initialValue)

  return (
    <CenteredPage innerClassName={styles.content}>
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        <h1>{title}</h1>
        {note && (
          <p style={{ color: 'var(--note)'}}>{note}</p>
        )}
      </div>
      <TextArea value={value} onChange={setValue} />
      <Button variant="primary" text="Save" onClick={onSave} />
    </CenteredPage>
  )
}
