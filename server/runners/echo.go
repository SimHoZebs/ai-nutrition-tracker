package runners

import (
	"google.golang.org/adk/runner"
	"google.golang.org/adk/session"
	"log"
	"server/agents"
)

func NewEcho() (*agents.AgentService, error) {
	sessionService := session.InMemoryService()
	agent, err := agents.NewEchoAgent()
	if err != nil {
		log.Fatalf("failed to create echo agent: %v", err)
	}

	runnerConfig := runner.Config{
		Agent:          agent,
		AppName:        "demo_app",
		SessionService: sessionService,
	}

	agentRunner, err := runner.New(runnerConfig)
	if err != nil {
		log.Fatalf("Failed to create runner: %v", err)
	}

	return &agents.AgentService{
		Runner: agentRunner,
		Config: runnerConfig,
	}, nil
}
