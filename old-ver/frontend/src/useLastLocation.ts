import {useLocation} from "react-router";

export default function useLastLocation(): string {
  const location = useLocation()
  return location.state?.lastLocation ?? '/'
}
