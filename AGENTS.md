# LazyFood Go Server - Agent Guidelines

## Build & Development Commands
- **Build**: `go build -o server ./server/`
- **Run**: `cd server && ./server` (runs on localhost:8080)
- **Generate Swagger docs**: `make swagger-gen` or `swag init ./server/`
- **Install dependencies**: `go mod tidy`

## Code Style Guidelines
- **Imports**: Group standard library, then third-party, then local imports (server/*)
- **API**: Use Huma v2 with Chi router, follow existing endpoint patterns in routes/
- **Environment**: Load .env with godotenv, never commit secrets

## ADK (Agent Development Kit) Guidelines
- **ADK Documentation**: https://google.github.io/adk-docs/ (primary reference)
- **Go ADK API**: https://pkg.go.dev/google.golang.org/adk
- **Agent Creation**: Use llmagent.New() with gemini models (see agents/weather.go:31)
- **Runner Pattern**: Create agents in agents/, initialize runners in runners/ (see runners/echo.go:10)
- **Session Management**: Use session.InMemoryService() for conversation state
- **Tools**: Leverage geminitool.GoogleSearch{} and other built-in tools
- **Model Config**: Use gemini.NewModel() with GOOGLE_API_KEY from environment
