package agents

import (
	"context"
	"strings"

	"google.golang.org/adk/agent"
	"google.golang.org/adk/runner"
	"google.golang.org/adk/session"
	"google.golang.org/genai"
)

type AgentService struct {
	agent          agent.Agent
	runner         *runner.Runner
	sessionService session.Service
}

func (s *AgentService) ProcessQuery(ctx context.Context, userID string, sessionID string, msg *genai.Content, cfg agent.RunConfig) (string, error) {
	// Run the runner which returns an iterator of events/errors
	res := s.runner.Run(ctx, userID, sessionID, msg, cfg)

	var sb strings.Builder
	for ev, itErr := range res {
		if itErr != nil {
			return "", itErr
		}
		if ev == nil {
			continue
		}

		// Extract text from genai.Content parts if present
		if ev.Content != nil {
			for _, p := range ev.Content.Parts {
				if p == nil {
					continue
				}
				if p.Text != "" {
					sb.WriteString(p.Text)
				}
			}
		}
	}

	return sb.String(), nil
}
