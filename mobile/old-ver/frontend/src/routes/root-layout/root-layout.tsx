import styles from './root-layout.module.css';
import Navbar from "../../components/navbar/navbar.tsx";
import FloatingAIButton from "../../components/floating-ai-button/floating-ai-button.tsx";
import AIInputModal from "../../components/ai-input-modal/ai-input-modal.tsx";
import {Outlet} from "react-router";
import { useState } from "react";

export default function RootLayout() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div className={styles.page}>
      <div className={styles.content}>
        <Outlet />
      </div>
      <Navbar />
      <FloatingAIButton onClick={() => setIsModalOpen(true)} />
      <AIInputModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
      />
    </div>
  )
}
