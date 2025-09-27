import styles from './root-layout.module.css';
import Navbar from "../../components/navbar/navbar.tsx";
import {Outlet} from "react-router";

export default function RootLayout() {
  return (
    <div className={styles.page}>
      <div className={styles.content}>
        <Outlet />
      </div>
      <Navbar />
    </div>
  )
}
