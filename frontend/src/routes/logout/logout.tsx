import {useNavigate} from "react-router";
import {useMutation, useQuery} from "@tanstack/react-query";
import {handleRequest} from "../../util.ts";
import {useEffect} from "react";

export default function Logout() {
  const navigate = useNavigate()

  const logoutMutation = useMutation({
    mutationKey: ["logout"],
    mutationFn: async () => {
      await handleRequest("GET", "/api/logout/")
    },
    onSettled: () => {
      navigate("/login")
    }
  })

  useEffect(() => {
    logoutMutation.mutate();
  }, [])

  return "Logging you out..."
}
