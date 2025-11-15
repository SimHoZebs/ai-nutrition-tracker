import styles from './user-profile.module.css'
import {Icon} from "@iconify/react";
import Button from "../../components/button/button.tsx";
import MemoryItem from "../../components/memory-item/memory-item.tsx";
import {useNavigate} from "react-router";
import {useQuery} from "@tanstack/react-query";
import {handleRequest} from "../../util.ts";
import type {Memory, UserProfile} from "../../models.ts";

export default function UserProfile() {
  const navigate = useNavigate();

  const userQuery = useQuery({
    queryKey: ['user-profile'],
    queryFn: async () => {
      const [jsonRes, status] = await handleRequest("GET", "/api/user-profiles/me/")
      if (Math.floor(status / 100) !== 2) {
        throw new Error('Unknown error')
      }
      return jsonRes as UserProfile
    }
  })

  const memoriesQuery = useQuery({
    queryKey: ["memories"],
    queryFn: async () => {
      const [jsonRes, status] = await handleRequest("GET", "/api/memories/")
      if (Math.floor(status / 100) !== 2) {
        throw new Error('Unknown error')
      }
      return jsonRes as Memory[]
    }
  })

  if (userQuery.isLoading || memoriesQuery.isLoading) {
    return "Loading..."
  }

  return (
    <>
      <h1>Your Profile</h1>
      <div className={styles.userHeader}>
        <Icon icon="ri:user-line" width={85} />

        <div className={styles.userHeaderRight}>
          <h2>{userQuery.data?.user.first_name} {userQuery.data?.user.last_name}</h2>
          <p style={{ marginBottom: '5px' }}>{userQuery.data?.user.email}</p>
          <Button variant="secondary" text="Logout" onClick={() => navigate('/logout')} />
        </div>
      </div>

      <div className={styles.section}>
        <div className={styles.buttonHeader}>
          <h2>Memories</h2>
          <Button
            variant="primary"
            text="Add"
            onClick={() => navigate('/add-memory', {state: {lastLocation: '/user'}})}
          />
        </div>

        {memoriesQuery.data?.map((memory) => (
          <MemoryItem key={memory.id} memory={memory} />
        ))}

      </div>
    </>
  )
}
