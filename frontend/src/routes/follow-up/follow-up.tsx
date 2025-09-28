import styles from "./follow-up.module.css";
import CenteredPage from "../../components/centered-page/centered-page.tsx";
import MultipleChoiceQuestion from "../../components/multiple-choice-question/multiple-choice-question.tsx";
import Divider from "../../components/divider/divider.tsx";
import Button from "../../components/button/button.tsx";
import { useLocation } from "react-router";
import type { LogResponse, Question } from "../../models.ts";
import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
import { useNavigate } from "react-router";
import { handleRequest } from "../../util.ts";

export default function FollowUp() {
  const location = useLocation();
  const navigate = useNavigate();
  const followUpQuestions: Question[] = location.state?.followUpQuestions;
  const [mcqResponses, setMcqResponses] = useState<string[]>([]);

  const submitMutation = useMutation({
    mutationFn: async () => {
      const body = {
        answers: mcqResponses,
      };
      const jsonRes = await handleRequest("POST", "/api/resubmit/", body);
      console.log(jsonRes);
      return JSON.parse(jsonRes?.[0]?.["parts"]?.[0]?.["text"]);
    },
    onSuccess: (result: LogResponse) => {
      console.log(result);

      if (result.questions && result.questions.length > 0) {
        navigate("/follow-up", {
          state: { followUpQuestions: result.questions },
        });
      } else {
        navigate("/");
      }
    },
  });

  return (
    <CenteredPage innerClassName={styles.followUpContainer}>
      <div>
        <h1>Follow Up Questions</h1>
        <p style={{ color: "var(--note)" }}>
          For a more accurate estimate, please answer the following questions.
        </p>
      </div>

      <div className={styles.questions}>
        {followUpQuestions.map((question, index) => (
          <div>
            <p style={{ color: "var(--note)" }}>Question {index + 1}</p>
            {question.type === "multiple_choice" && (
              <MultipleChoiceQuestion
                key={index}
                question={question.question}
                choices={question.mcqOptions}
                onSelect={(choice) =>
                  setMcqResponses((prev) => {
                    const newResponses = [...prev];
                    newResponses[index] = choice;
                    return newResponses;
                  })
                }
              />
            )}
          </div>
        ))}
      </div>

      <Divider />

      <Button
        onClick={() => {
          submitMutation.mutate();
          navigate("/");
        }}
        variant="primary"
        text="Submit"
      />
    </CenteredPage>
  );
}
