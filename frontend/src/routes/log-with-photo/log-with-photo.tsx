import styles from './log-with-photo.module.css'
import CenteredPage from "../../components/centered-page/centered-page.tsx";
import Button from "../../components/button/button.tsx";
import {useEffect, useRef, useState} from "react";
import {handleRequestGeneric} from "../../util.ts";
import {useMutation} from "@tanstack/react-query";
import type {LogResponse, QuestionResponse} from "../../models.ts";
import {checkIfQuestions} from "../../util.ts";
import {useNavigate} from "react-router";

export default function LogWithPhoto() {
  const navigate = useNavigate();
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [photoUrl, setPhotoUrl] = useState<string | null>(null);

  const submitPhotoMutation = useMutation({
    mutationKey: ['submit-photo'],
    mutationFn: async (photoUrl: string) => {
      const base64Response = await fetch(photoUrl);
      const blob = await base64Response.blob();

      const formData = new FormData();
      formData.append("photo", blob, "photo.jpeg");

      const [jsonRes, status] = await handleRequestGeneric("POST", "/api/process/", formData);
      if (Math.floor(status / 100) !== 2) {
        throw new Error('Unknown error')
      }
      return jsonRes as LogResponse | QuestionResponse;
    },
    onSuccess: (resp: LogResponse | QuestionResponse) => {
      const isQuestionResponse = checkIfQuestions(resp)
      if (isQuestionResponse) {
        navigate("/follow-up", {
          state: { followUpQuestions: resp.questions },
        });
      } else {
        navigate("/");
      }
    }
  })

  useEffect(() => {
    async function enableStream() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: {facingMode: 'environment'}
        });
        setStream(stream);
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error('Error accessing camera:', err);
      }
    }

    enableStream();

    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  const takePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d')?.drawImage(video, 0, 0);
      const url = canvas.toDataURL('image/jpeg');
      setPhotoUrl(url);
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }

      submitPhotoMutation.mutate(url);
    }
  }

  return (
    <CenteredPage>
      <div className={styles.container}>
        <div>
          <h1>Snap your Meal</h1>
          <p style={{color: 'var(--note)'}}>
            Be sure to get a great picture with as much details as possible
          </p>
        </div>

        <>
          <canvas ref={canvasRef} style={{display: 'none'}}/>
          {photoUrl ? (
            <img
              src={photoUrl}
              alt="Captured meal"
              style={{
                width: '100%',
                borderRadius: 'var(--border-radius-1)',
              }}
            />
          ) : (
            <video
              ref={videoRef}
              autoPlay
              playsInline
              style={{
                width: '100%',
                borderRadius: 'var(--border-radius-1)',
                backgroundColor: '#000'
              }}
            />
          )}
        </>

        <Button variant="primary" text="Take Photo" onClick={takePhoto} disabled={photoUrl !== null}/>

        {photoUrl !== null && <p className={styles.loadingText}>Submitting photo...</p>}
      </div>

    </CenteredPage>
  )
}
