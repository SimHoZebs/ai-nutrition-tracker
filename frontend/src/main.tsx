import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import {createBrowserRouter, RouterProvider} from "react-router";
import {QueryClient, QueryClientProvider} from "@tanstack/react-query";
import Dashboard from "./routes/dashboard/dashboard.tsx";
import Onboarding from "./routes/onboarding/onboarding.tsx";
import LogWithText from "./routes/log-with-text/log-with-text.tsx";
import FollowUp from "./routes/follow-up/follow-up.tsx";
import History from "./routes/history/history.tsx";
import UserProfile from "./routes/user-profile/user-profile.tsx";
import RootLayout from "./routes/root-layout/root-layout.tsx";
import Signup from './routes/signup/signup.tsx';
import Login from './routes/login/login.tsx';

const queryClient = new QueryClient()

const router = createBrowserRouter([
  {
    Component: RootLayout,
    children: [
      {
        path: '/',
        Component: Dashboard,
      },
      {
        path: '/history',
        Component: History,
      },
      {
        path: '/user',
        Component: UserProfile,
      }
    ]
  },
  {
    path: '/onboarding',
    Component: Onboarding,
  },
  {
    path: '/text-log',
    Component: LogWithText,
  },
  {
    path: '/follow-up',
    Component: FollowUp,
  },
  {
    path: "/login",
    Component: Login 
  },
  {
    path: "/Signup",
    Component: Signup 
  },
])

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </StrictMode>,
)
