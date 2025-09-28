import { useState, useRef } from "react";
import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router";
import { Icon } from "@iconify/react";
import Button from "../button/button.tsx";
import type { LogResponse } from "../../models.ts";
import styles from "./audio-recorder.module.css";

interface AudioRecorderProps {
  variant?: "primary" | "secondary" | "danger";
  size?: "md" | "lg";
  className?: string;
}

export default function AudioRecorder({
  variant = "secondary",
  size = "md",
  className,
}: AudioRecorderProps) {
  const navigate = useNavigate();
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const submitMutation = useMutation({
    mutationFn: async (audioBlob: Blob) => {
      const formData = new FormData();
      formData.append("audio", audioBlob, "recording.webm");

      const res = await fetch("http://localhost:8000/api/process/", {
        method: "POST",
        body: formData,
        credentials: "include",
        headers: {
          "X-CSRFToken": getCSRFToken(),
        },
      });

      if (!res.ok) {
        throw new Error("Failed to process audio");
      }

      const jsonRes = await res.json();
      return JSON.parse(jsonRes?.[0]?.["parts"]?.[0]?.["text"]);
    },
    onSuccess: (result: LogResponse) => {
      setIsProcessing(false);
      if (result.questions.length > 0) {
        navigate("/follow-up", {
          state: { followUpQuestions: result.questions },
        });
      } else {
        navigate("/");
      }
    },
    onError: () => {
      setIsProcessing(false);
    },
  });

  const getCSRFToken = () => {
    const cookies = document.cookie.split(";");
    for (const cookie of cookies) {
      if (cookie.trim().startsWith("csrftoken=")) {
        return cookie.split("=")[1];
      }
    }
    return "";
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          channelCount: 1,
          echoCancellation: true,
          noiseSuppression: true
        }
      });
      
      // Use the browser's default format (usually WEBM OPUS at 48kHz)
      const mediaRecorder = new MediaRecorder(stream);
      let mimeType = "audio/webm";
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, {
          type: "audio/webm",
        });
        setIsProcessing(true);
        submitMutation.mutate(audioBlob);

        // Stop all tracks to release microphone
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error("Error accessing microphone:", error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const handleClick = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  const getButtonContent = () => {
    if (isProcessing) {
      return (
        <div className={styles.logButton}>
          <Icon icon="eos-icons:loading" width={24} />
          Processing...
        </div>
      );
    }

    if (isRecording) {
      return (
        <div className={styles.logButton}>
          <Icon icon="material-symbols:stop-rounded" width={24} />
          Stop
        </div>
      );
    }

    return (
      <div className={styles.logButton}>
        <Icon icon="mdi:microphone-outline" width={24} />
        Speak
      </div>
    );
  };

  return (
    <Button
      variant={isRecording ? "danger" : variant}
      size={size}
      onClick={handleClick}
      disabled={isProcessing}
      className={className}
    >
      {getButtonContent()}
    </Button>
  );
}

