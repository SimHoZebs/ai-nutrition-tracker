package agents

import (
	"google.golang.org/adk/agent"
	"google.golang.org/adk/model"
	"google.golang.org/adk/session"
	"iter"
)

// Create a simple echo agent that returns the same user content as an agent event.
func NewEchoAgent() (agent.Agent, error) {
	return agent.New(agent.Config{
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

}
