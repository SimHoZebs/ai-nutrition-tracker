package agents

import (
	"google.golang.org/adk/agent"
	"google.golang.org/adk/model"
	"google.golang.org/adk/runner"
	"google.golang.org/adk/session"
	"iter"
	"log"
)

// Create a simple echo agent that returns the same user content as an agent event.
func NewEchoAgent() (*AgentService, error) {
	echoAgent, err := agent.New(agent.Config{
		Name:        "echo_agent",
		Description: "Echoes the user content as an agent response.",
		Run: func(ctx agent.InvocationContext) iter.Seq2[*session.Event, error] {
			return func(yield func(*session.Event, error) bool) {
				userContent := ctx.UserContent()
				ev := session.NewEvent(ctx.InvocationID())
				ev.Author = "echo_agent"
				ev.LLMResponse = model.LLMResponse{
					Content: userContent,
					Partial: false,
				}
				yield(ev, nil)
			}
		},
	})

	if err != nil {
		log.Fatalf("failed to create echo agent: %v", err)
	}

	// In-memory session store so we can introspect stored events
	sessionService := session.InMemoryService()
	runnerConfig := runner.Config{
		Agent:          echoAgent,
		AppName:        "demo_app",
		SessionService: sessionService,
	}

	agentRunner, err := runner.New(runnerConfig)
	if err != nil {
		log.Fatalf("failed to create runner: %v", err)
	}

	return &AgentService{
		Runner: agentRunner,
		Config: runnerConfig,
	}, nil
}
