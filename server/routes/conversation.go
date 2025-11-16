package routes

import (
	"context"
	"fmt"
	"log"
	"server/agents"

	"google.golang.org/adk/session"
	"google.golang.org/genai"
)

// ConversationRequest is the request body for conversation endpoint.
type ConversationRequest struct {
	UserID    string `json:"user_id"`
	SessionID string `json:"session_id"`
	Message   string `json:"message"`
}

// ConversationResponse is the response body for conversation endpoint.
type ConversationResponse struct {
	Body struct {
		Text     string   `json:"text"`
		Messages []string `json:"messages,omitempty"`
	}
}

func ConversationHandler(ctx context.Context, agentService *agents.AgentService, input *struct {
	Body ConversationRequest `body:""`
}) (*ConversationResponse, error) {
	content := &genai.Content{
		Parts: []*genai.Part{{Text: input.Body.Message}},
	}

	// Debug: log parsed input and runner args
	log.Printf("Handler parsed input: %+v", input.Body)
	log.Printf("Calling runner.Run with user=%q session=%q app=%q", input.Body.UserID, input.Body.SessionID, "demo_app")
	// Run the agentService. Runner will call sessionService.AppendEvent for the user message
	// (appendMessageToSession) and for non-partial agent events.

	text, err := ProcessQuery(ctx, ProcessAgentRequest{
		UserID:       input.Body.UserID,
		SessionID:    input.Body.SessionID,
		AgentService: *agentService,
		Message:      content,
	},
	)
	if err != nil {
		return nil, fmt.Errorf("agent processing failed: %w", err)
	}

	// After runner finishes, fetch the session and show stored events
	getResp, err := agentService.SessionService.Get(ctx, &session.GetRequest{
		AppName:   "demo_app",
		UserID:    input.Body.UserID,
		SessionID: input.Body.SessionID,
	})
	if err != nil {
		return nil, fmt.Errorf("session get failed: %w", err)
	}

	stored := getResp.Session
	events := stored.Events().All()
	var messages []string
	for ev := range events {
		if ev.Content != nil {
			for _, p := range ev.Content.Parts {
				if p != nil && p.Text != "" {
					messages = append(messages, p.Text)
				}
			}
		}

	}

	// Log session contents to demonstrate persistence

	resp := &ConversationResponse{}
	resp.Body.Text = text
	resp.Body.Messages = messages

	return resp, nil
}
