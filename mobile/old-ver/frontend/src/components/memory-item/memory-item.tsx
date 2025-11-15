import styles from './memory-item.module.css'
import Button from "../button/button.tsx";
import {Icon} from "@iconify/react";
import type {Memory} from "../../models.ts";
import {useMutation, useQueryClient} from "@tanstack/react-query";
import {handleRequest} from "../../util.ts";

interface MemoryItemProps {
  memory: Memory
}

export default function MemoryItem({ memory }: MemoryItemProps) {
  const queryClient = useQueryClient()

  const deleteMutation = useMutation({
    mutationKey: ['delete-memory', memory.id],
    mutationFn: async (memoryId: number) => {
      const [resp, status] = await handleRequest("DELETE", `/api/memories/${memoryId}/`)
      if (Math.floor(status / 100) !== 2) {
        throw new Error('Unknown error');
      }
      return resp
    },
    onSuccess: async (_, memoryId: number) => {
      await queryClient.cancelQueries({ queryKey: ['memories'] })
      const oldQueryData: Memory[] = queryClient.getQueryData(['memories']) ?? []
      const newQueryData = oldQueryData.filter((memory) => memory.id !== memoryId)
      queryClient.setQueryData(['memories'], newQueryData)
    }
  })

  return (
    <div className={styles.memoryItem}>
      {memory.content}

      <Button variant="secondary" onClick={() => deleteMutation.mutate(memory.id)}>
        <Icon icon="mdi:trash-outline" />
      </Button>
    </div>
  )
}
