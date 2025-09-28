import { useState, useRef } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useNavigate } from "react-router";
import { Icon } from "@iconify/react";
import Modal from "../modal/modal.tsx";
import Button from "../button/button.tsx";
import TextArea from "../textarea/textarea.tsx";
import styles from './ai-input-modal.module.css';
import { handleRequest, checkIfQuestions } from "../../util.ts";
import type { LogResponse, QuestionResponse, UserProfile } from "../../models.ts";

interface AIInputModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function AIInputModal({ isOpen, onClose }: AIInputModalProps) {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<'text' | 'image'>('text');
  const [textValue, setTextValue] = useState<string>("");
  const [isProcessing, setIsProcessing] = useState(false);
  
  // Audio recording state
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  
  // Image upload/capture state
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreviewUrl, setImagePreviewUrl] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const userQuery = useQuery({
    queryKey: ['user-profile'],
    queryFn: async () => {
      const [jsonRes, status] = await handleRequest("GET", "/api/user-profiles/me/");
      if (Math.floor(status / 100) !== 2) {
        throw new Error('Unknown error');
      }
      return jsonRes as UserProfile;
    },
    retry: false,
  });

  if (userQuery.isError) {
    navigate('/login');
  }

  const textMutation = useMutation({
    mutationFn: async (mealDescription: string) => {
      const body = { food_description: mealDescription };
      let [jsonRes, status] = await handleRequest("POST", "/api/process/", body);
      if (Math.floor(status / 100) !== 2) {
        throw new Error("Unknown error");
      }
      return JSON.parse((jsonRes as any)?.["parts"]?.[0]?.["text"]);
    },
    onSuccess: handleSuccess,
  });

  const audioMutation = useMutation({
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
    onSuccess: handleSuccess,
  });

  const imageMutation = useMutation({
    mutationFn: async (imageFile: File) => {
      const formData = new FormData();
      formData.append("image", imageFile);

      const res = await fetch("http://localhost:8000/api/process/", {
        method: "POST",
        body: formData,
        credentials: "include",
        headers: {
          "X-CSRFToken": getCSRFToken(),
        },
      });

      if (!res.ok) {
        throw new Error("Failed to process image");
      }

      const jsonRes = await res.json();
      return JSON.parse((jsonRes as any)?.[0]?.["parts"]?.[0]?.["text"]);
    },
    onSuccess: handleSuccess,
  });

  function handleSuccess(result: LogResponse | QuestionResponse) {
    setIsProcessing(false);
    onClose();
    
    const isQuestionResponse = checkIfQuestions(result);
    
    if (isQuestionResponse) {
      navigate("/follow-up", {
        state: { 
          followUpQuestions: result.questions, 
          description: textValue || undefined
        },
      });
    } else {
      navigate("/");
    }
  }

  const getCSRFToken = () => {
    const cookies = document.cookie.split(";");
    for (const cookie of cookies) {
      if (cookie.trim().startsWith("csrftoken=")) {
        return cookie.split("=")[1];
      }
    }
    return "";
  };

  // Audio recording functions
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          channelCount: 1,
          echoCancellation: true,
          noiseSuppression: true
        }
      });

      const mediaRecorder = new MediaRecorder(stream);
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
        audioMutation.mutate(audioBlob);
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

  // Image upload functions
  const handleImageSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreviewUrl(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleImageSubmit = () => {
    if (selectedImage) {
      setIsProcessing(true);
      imageMutation.mutate(selectedImage);
    }
  };

  const clearImage = () => {
    setSelectedImage(null);
    setImagePreviewUrl(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleTextSubmit = () => {
    if (textValue.trim()) {
      setIsProcessing(true);
      textMutation.mutate(textValue);
    }
  };

  const handleAudioClick = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  if (!isOpen) return null;

  return (
    <Modal>
      <div className={styles.container}>
        <div className={styles.header}>
          <h2>Log your meal</h2>
          <button className={styles.closeButton} onClick={onClose}>
            <Icon icon="mdi:close" width={24} height={24} />
          </button>
        </div>

        <div className={styles.tabs}>
          <button
            className={`${styles.tab} ${activeTab === 'text' ? styles.active : ''}`}
            onClick={() => setActiveTab('text')}
          >
            <Icon icon="mdi:text" width={20} height={20} />
            Describe
          </button>
          <button
            className={`${styles.tab} ${activeTab === 'image' ? styles.active : ''}`}
            onClick={() => setActiveTab('image')}
          >
            <Icon icon="mdi:camera" width={20} height={20} />
            Upload Photo
          </button>
        </div>

        <div className={styles.content}>
          {activeTab === 'text' && (
            <div className={styles.textTab}>
              <p className={styles.description}>
                Describe your meal with details like portion size and ingredients, or record your voice.
              </p>
              <TextArea value={textValue} onChange={setTextValue} />
              <div className={styles.textActions}>
                <Button
                  variant={isRecording ? "danger" : "secondary"}
                  onClick={handleAudioClick}
                  disabled={isProcessing}
                  className={styles.audioButton}
                >
                  <Icon 
                    icon={isRecording ? "material-symbols:stop-rounded" : "mdi:microphone-outline"} 
                    width={20} 
                  />
                  {isRecording ? "Stop" : "Record"}
                </Button>
                <Button
                  variant="primary"
                  text="Log Meal"
                  disabled={isProcessing || !textValue.trim()}
                  onClick={handleTextSubmit}
                />
              </div>
            </div>
          )}

          {activeTab === 'image' && (
            <div className={styles.imageTab}>
              <p className={styles.description}>
                Upload a photo of your meal for analysis.
              </p>
              
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleImageSelect}
                style={{ display: 'none' }}
              />
              
              {imagePreviewUrl ? (
                <div className={styles.imagePreview}>
                  <img
                    src={imagePreviewUrl}
                    alt="Selected meal"
                    className={styles.selectedImage}
                  />
                  <div className={styles.imageActions}>
                    <Button
                      variant="secondary"
                      text="Change Image"
                      onClick={() => fileInputRef.current?.click()}
                      disabled={isProcessing}
                    />
                    <Button
                      variant="danger"
                      text="Remove"
                      onClick={clearImage}
                      disabled={isProcessing}
                    />
                    <Button
                      variant="primary"
                      text="Analyze Image"
                      onClick={handleImageSubmit}
                      disabled={isProcessing}
                    />
                  </div>
                </div>
              ) : (
                <div className={styles.uploadArea}>
                  <div className={styles.uploadPrompt}>
                    <Icon icon="mdi:camera-plus" width={48} height={48} />
                    <p>Select an image of your meal</p>
                    <Button
                      variant="primary"
                      text="Choose Image"
                      onClick={() => fileInputRef.current?.click()}
                      disabled={isProcessing}
                    />
                  </div>
                </div>
              )}
            </div>
          )}

          {isProcessing && (
            <div className={styles.processing}>
              <Icon icon="eos-icons:loading" width={24} />
              <span>Processing...</span>
            </div>
          )}
        </div>
      </div>
    </Modal>
  );
}