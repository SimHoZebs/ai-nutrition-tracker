import type {LogResponse, QuestionResponse} from "./models.ts";

export const baseUrl = 'http://localhost:8000'

type HttpMethods = "GET" | "POST" | "PUT" | "DELETE"

export async function handleRequest(method: HttpMethods, endpoint: string, jsonBody?: unknown): Promise<[unknown | null, number]> {
  const res = await fetch(baseUrl + endpoint, {
    method,
    body: jsonBody ? JSON.stringify(jsonBody) : undefined,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'X-CSRFToken': getCSRFToken(),
    }
  })

  try {
    const jsonRes = await res.json()
    return [jsonRes, res.status]
  } catch {
    // JSON was not returned - likely an empty response. Return null.
    return [null, res.status]
  }

}

export const getCSRFToken = () => {
  const cookies = document.cookie.split(';')
  for (const cookie of cookies) {
    if(cookie.trim().startsWith('csrftoken=')) {
      return cookie.split('=')[1]
    }
  }
  return ''
}

export const checkIfQuestions = (resp: LogResponse | QuestionResponse) => {
  if (Array.isArray(resp)) {
    return false
  } else {
    return (resp.questions ?? []).length > 0;
  }
}
