import Button from "../../components/button/button";
import styles from './login.module.css'
import { useState } from "react";
import {useMutation} from "@tanstack/react-query";
import {handleRequest} from "../../util.ts";
import {useNavigate} from "react-router";


export default function Login(){
  const navigate = useNavigate();

  const [username, setUsername] = useState('');
  const [password,setPassword] = useState('');

  const isFormIncomplete = Boolean(!password.trim() || !username.trim());

  const loginMutation = useMutation({
    mutationFn: async () => {
      const [res, status] = await handleRequest("POST", "/api/login/", {username, password})
      if (status === 401) {
        throw new Error(res['error']);
      } else if (Math.floor(status / 100)  !== 2) {
        throw new Error('Unknown error')
      }
    },
    onSuccess: () => {
      navigate('/');
    },
    onError: (e) => {
      console.log("Login failed");
      console.log(e)
    }
  })

  return (
    <div className={styles.container}>
      <div>
        <h1>Login</h1>
        <p style={{ color: 'var(--note)' }}>
          Welcome back! Please enter to log in.
        </p>
      </div>
      <form className={styles.form} onSubmit={(e) => {
        e.preventDefault();
        loginMutation.mutate()
      }}>
        <label className= {styles.label}>
          <input type="text" name="username" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)}/>
        </label>
        <label className= {styles.label}>
          <input type="password" name="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
        </label>
        <Button disabled={isFormIncomplete}>Log In</Button>
      </form>

      <p style={{ color: 'var(--note)' }}>
        Don't have an account? <a href="/signup">Register here!</a>
      </p>
    </div>

  )

}
