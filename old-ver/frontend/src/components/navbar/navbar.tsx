import styles from './navbar.module.css'
import {Icon} from "@iconify/react";
import clsx from "clsx";
import {useLocation, useNavigate} from "react-router";

const iconHeight = 22

export default function Navbar() {
  const location = useLocation()
  const navigate = useNavigate()

  return (
    <nav className={styles.navbar}>
      <button
        className={clsx(styles.navbarButton, {
          [styles.active]: location.pathname === '/',
        })}
        onClick={() => navigate('/')}
      >
        <Icon icon="lucide:house" width={iconHeight} />
        Home
      </button>
      <button
        className={clsx(styles.navbarButton, {
          [styles.active]: location.pathname === '/history',
        })}
        onClick={() => navigate('/history')}
      >
        <Icon icon="material-symbols:history-rounded" width={iconHeight} />
        History
      </button>
      <button
        className={clsx(styles.navbarButton, {
          [styles.active]: location.pathname === '/user',
        })}
        onClick={() => navigate('/user')}
      >
        <Icon icon="ri:user-line" width={iconHeight} />
        You
      </button>
    </nav>
  )
}
