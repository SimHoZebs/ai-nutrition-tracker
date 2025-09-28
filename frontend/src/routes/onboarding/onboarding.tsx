import Button from "../../components/button/button";
import styles from './onboarding.module.css'
import CenteredPage from "../../components/centered-page/centered-page";

export default function Onboarding() {
  return (
  

    <div className={styles.container}>
      <CenteredPage>
        <h1>Personalization</h1>
        <p style={{ color: 'var(--note)' }}>
          Please answer these question. 
        </p>

      

      {/* <p style = {{color: 'var(--note)'}}></p> */}
      <form className={styles.form}>
        <label className= {styles.label}>
          Date of Birth
        <input
          type="date"
          name="dob"
        />
        </label>

        <label className= {styles.label}>
          Height
        <input
        type="text"
        name="height"
        placeholder="e.g: 5'5"
        />
        </label>

        <label className={styles.label}>
          Weight
          <input
        type="number"
        name="weight"
        placeholder="lbs"
        />
        </label>
        
      <label className={styles.label}> 
         Activity Level
        <select name="activityLevel" className={styles.select}>
         
            <option value="Sedentary">Sedentary</option>
            <option value="Lightly Active">Lightly Active</option>
            <option value="Moderately Active">Moderately Active</option>
            <option value="Very Active">Very Active</option>
            <option value="Extremely Active">Extremely Active</option>
          </select>
      </label>


      <label className={styles.label}>
        Dietary goals
        <textarea
          name="textingArea"
          placeholder="e.g: lose 20 pounds"/>
      </label>  
        
      <Button>Save</Button>
      </form>
     </CenteredPage>
    </div>
  )
}
