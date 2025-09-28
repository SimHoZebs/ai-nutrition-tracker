import Button from "../../components/button/button";
import CenteredPage from "../../components/centered-page/centered-page";
import styles from './signup.module.css'
import {useMutation} from "@tanstack/react-query";
import {useState} from "react";
import {handleRequest} from "../../util.ts";
import {useLocation, useNavigate} from "react-router";
import useLastLocation from "../../useLastLocation.ts";

interface SignupMutateData {
  username: string,
  email: string,
  firstName: string,
  lastName: string,
  password: string,
}

export default function Signup(){
  const [username, setUsername] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const lastLocation = useLastLocation()
  const navigate = useNavigate();

  const signupMutation = useMutation({
    mutationKey: ['signup'],
    mutationFn: async ({username, email, firstName, lastName, password}: SignupMutateData) => {
      const body = {
        username,
        email,
        first_name: firstName,
        last_name: lastName,
        password,
      }

      const [resp, status] = await handleRequest("POST", "/api/register/", body)
      if (Math.floor(status / 100) !== 2) {
        throw new Error("Unknown error")
      }
      return resp
    },
    onSuccess: () => {
      navigate(lastLocation)
    },
    onError: (error) => {
      console.log(error)
    }
  });

  return(
    <CenteredPage innerClassName={styles.container}>
      <h1>Sign Up</h1>
      <p style={{ color: 'var(--note)' }}>
      </p>
      <form className = {styles.form}>
        <label className= {styles.label}>
          <input
            type="text"
            name="username"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </label>
        <label className= {styles.label}>
          <input
            type="text"
            name="firstName"
            placeholder="First Name"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
          />
        </label>
        <label className= {styles.label}>
          <input
            type="text"
            name="lastName"
            placeholder="Last Name"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
          />
        </label>
        <label className= {styles.label}>
          <input
            type="text"
            name="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </label>
        <label className= {styles.label}>
          <input
            type="password"
            name="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>


        <Button
          onClick={(e) => {
            e.preventDefault()
            signupMutation.mutate({username, firstName, lastName, email, password})
          }}
        >
          Sign Up
        </Button>

      </form>
    </CenteredPage>

  );
}
