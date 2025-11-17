package routes

import (
	"context"
	"strings"

	"server/shared"

	"google.golang.org/adk/agent"
	"google.golang.org/adk/session"
	"google.golang.org/genai"
)

type ProcessAgentRequest struct {
	shared.AgentService
	UserID    string         `json:"user_id"`
	SessionID string         `json:"session_id"`
	Message   *genai.Content `json:"message"`
}

func ProcessQuery(ctx context.Context, req ProcessAgentRequest) (string, error) {
	println("ProcessQuery called with userID:", req.UserID, "sessionID:", req.SessionID)
	getRes, err := req.SessionService.List(ctx, &session.ListRequest{
		AppName: req.AgentService.AppName,
		UserID:  req.UserID,
	})
	if err != nil {
		return "", err
	}

	found := false
	for _, session := range getRes.Sessions {
		println("Checking existing session:", session.ID())
		if session.ID() == req.SessionID {
			println("Found existing session:", session.ID())
			found = true
			break
		}
	}

	if !found {
		// Create a new session if it doesn't exist
		println("Creating new session for userID:", req.UserID, "sessionID:", req.SessionID)
		_, err := req.SessionService.Create(ctx, &session.CreateRequest{
			AppName:   req.AppName,
			UserID:    req.UserID,
			SessionID: req.SessionID,
		})
		if err != nil {
			return "", err
		}
	}

	// Run the runner which returns an iterator of events/errors
	res := req.Runner.Run(ctx, req.UserID, req.SessionID, req.Message, agent.RunConfig{})

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
