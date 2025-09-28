export const baseUrl = 'http://localhost:8000'

type HttpMethods = "GET" | "POST" | "PUT" | "DELETE"
export async function handleRequest(method: HttpMethods, endpoint: string, jsonBody: unknown) {
  const res = await fetch(baseUrl + endpoint, {
    method,
    body: JSON.stringify(jsonBody),
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    }
  })

  return await res.json()
}
