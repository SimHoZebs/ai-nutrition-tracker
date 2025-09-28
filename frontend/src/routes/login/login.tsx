import Button from "../../components/button/button";
import styles from './login.module.css'
import CenteredPage from "../../components/centered-page/centered-page";
import { useState } from "react";


export default function Login(){

  const [email, setEmail] = useState('');
  const [password,setPassword] = useState('');

  
  const isFormIncomplete = Boolean((email.trim() && !password.trim()) || (password.trim() && !email.trim()));


  return (
    <div>
      <CenteredPage>
        <h1>Login</h1>
        <p style={{ color: 'var(--note)' }}>
          Welcome back! Please enter to log in.
        </p>
      <form className = {styles.form}>
        <label className= {styles.label}>
          <input type="text" name="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)}/>
        </label>
        <label className= {styles.label}>
          <input type="password" name="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
        </label>
        <Button disabled={isFormIncomplete}>Log In</Button>
      </form>
      </CenteredPage>
    </div>

  )

}
