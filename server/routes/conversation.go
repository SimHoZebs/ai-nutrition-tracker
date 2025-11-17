package routes

import (
	"context"
	"fmt"
	"google.golang.org/adk/session"
	"google.golang.org/genai"
	"log"
	"server/constants"
	"server/shared"
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
		Text string `json:"text"`
	}
}

func ConversationHandler(ctx context.Context, agentService *shared.AgentService, input *struct {
	Body ConversationRequest `body:""`
}) (*ConversationResponse, error) {
	content := genai.NewContentFromText(input.Body.Message, genai.RoleUser)

	log.Printf("Handler parsed input: %+v", input.Body)
	log.Printf("Calling runner.Run with user=%q session=%q app=%q", input.Body.UserID, input.Body.SessionID, "demo_app")

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

	listRes, err := agentService.SessionService.List(ctx, &session.ListRequest{
		AppName: constants.AppName,
		UserID:  input.Body.UserID,
	})

	var sessionIds []string
	for _, s := range listRes.Sessions {
		sessionIds = append(sessionIds, s.ID())
	}
	println("Current sessions for user:", input.Body.UserID, len(sessionIds))

	resp := &ConversationResponse{}
	resp.Body.Text = text

	return resp, nil
}
