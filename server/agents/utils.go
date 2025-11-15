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
	runner.Config
	Runner *runner.Runner
}

func (s *AgentService) ProcessQuery(ctx context.Context, userID string, sessionID string, msg *genai.Content, cfg agent.RunConfig) (string, error) {
	println("ProcessQuery called with userID:", userID, "sessionID:", sessionID)
	getRes, err := s.SessionService.List(ctx, &session.ListRequest{
		AppName: s.AppName,
		UserID:  userID,
	})
	if err != nil {
		return "", err
	}

	found := false
	for _, session := range getRes.Sessions {
		println("Checking existing session:", session.ID())
		if session.ID() == sessionID {
			println("Found existing session:", sessionID)
			found = true
			break
		}
	}

	if !found {
		// Create a new session if it doesn't exist
		println("Creating new session for userID:", userID, "sessionID:", sessionID)
		_, err := s.SessionService.Create(ctx, &session.CreateRequest{
			AppName:   s.AppName,
			UserID:    userID,
			SessionID: sessionID,
		})
		if err != nil {
			return "", err
		}
	}

	// Run the runner which returns an iterator of events/errors
	res := s.Runner.Run(ctx, userID, sessionID, msg, cfg)

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
