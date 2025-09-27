import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import {createBrowserRouter, RouterProvider} from "react-router";
import {QueryClient, QueryClientProvider} from "@tanstack/react-query";
import Dashboard from "./routes/dashboard/dashboard.tsx";
import Onboarding from "./routes/onboarding/onboarding.tsx";
import LogWithText from "./routes/log-with-text/log-with-text.tsx";
import FollowUp from "./routes/follow-up/follow-up.tsx";

const queryClient = new QueryClient()

const router = createBrowserRouter([
  {
    path: '/',
    Component: Dashboard,
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
  }
])

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </StrictMode>,
)
