import styles from "./log-with-text.module.css";
import CenteredPage from "../../components/centered-page/centered-page.tsx";
import TextArea from "../../components/textarea/textarea.tsx";
import Button from "../../components/button/button.tsx";
import { useState } from "react";
import { useNavigate } from "react-router";
import { useMutation } from "@tanstack/react-query";
import {checkIfQuestions, handleRequest} from "../../util.ts";
import type {LogResponse, QuestionResponse} from "../../models.ts";

export default function LogWithText() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);

  const [descriptionValue, setDescriptionValue] = useState<string>("");

  const submitMutation = useMutation({
    mutationFn: async (mealDescription: string) => {
      const body = {
        food_description: mealDescription,
      };
      let [jsonRes, status] = await handleRequest("POST", "/api/process/", body);
      if (Math.floor(status / 100) !== 2) {
        throw new Error("Unknown error");
      }
      return JSON.parse(jsonRes?.["parts"]?.[0]?.["text"]);
    },
    onSuccess: (result: LogResponse | QuestionResponse) => {
      const isQuestionResponse = checkIfQuestions(result)

      if (isQuestionResponse) {
        navigate("/follow-up", {
          state: { followUpQuestions: result.questions, description: descriptionValue },
        });
      } else {
        navigate("/");
      }
    },
  });

  const submitLog = () => {
    setIsLoading(true);
    submitMutation.mutate(descriptionValue);
  };

  return (
    <CenteredPage innerClassName={styles.logWithTextContainer}>
      <div style={{ display: "flex", flexDirection: "column" }}>
        <h1>Describe your Meal</h1>
        <p style={{ color: "var(--note)" }}>
          Be sure to include details like portion size and ingredients!
        </p>
      </div>
      <TextArea value={descriptionValue} onChange={setDescriptionValue} />
      <Button
        variant="primary"
        text="Log"
        disabled={isLoading}
        onClick={submitLog}
      />

      {submitMutation.isError && "Oopsie shit blew up"}

      {isLoading && <p className={styles.loadingText}>Submitting log...</p>}
    </CenteredPage>
  );
}
