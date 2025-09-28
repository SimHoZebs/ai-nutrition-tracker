import Button from "../../components/button/button";
import CenteredPage from "../../components/centered-page/centered-page";
import styles from './signup.module.css'

export default function Signup(){
  return(
  
    <CenteredPage innerClassName={styles.container}>
      <h1>Sign Up</h1>
      <p style={{ color: 'var(--note)' }}>
      </p>
      <form className = {styles.form}>
        <label className= {styles.label}>
          <input type="text" name="username" placeholder="Username"/>
        </label> 
        <label className= {styles.label}>
          <input type="text" name = "firstName" placeholder="First Name"/>
        </label>
        <label className= {styles.label}>
          <input type="text" name = "lastName" placeholder="Last Name"/>
        </label>
        <label className= {styles.label}>
          <input type="text" name="email" placeholder="Email"/>
        </label>     
        <label className= {styles.label}>
          <input type="password" name="password" placeholder="Password"/>
        </label>


        <Button >Sign Up</Button>

      </form>
    </CenteredPage>

  );
}
