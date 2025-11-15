package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"server/agents"

	"github.com/danielgtaylor/huma/v2"
	"github.com/danielgtaylor/huma/v2/adapters/humachi"
	"github.com/go-chi/chi/v5"

	"google.golang.org/adk/agent"
	"google.golang.org/adk/session"
	"google.golang.org/genai"
)

// GreetingOutput represents the greeting operation response.
type GreetingOutput struct {
	Body struct {
		Message string `json:"message" example:"Hello, world!" doc:"Greeting message"`
	}
}

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

func main() {
	r := chi.NewMux()
	api := humachi.New(r, huma.DefaultConfig("Conversation API", "0.1.0"))

	// Register GET /greeting/{name} handler.
	huma.Get(api, "/greeting/{name}", func(ctx context.Context, input *struct {
		Name string `path:"name" maxLength:"30" example:"world" doc:"Name to greet"`
	}) (*GreetingOutput, error) {
		resp := &GreetingOutput{}
		resp.Body.Message = fmt.Sprintf("Hello, %s!", input.Name)
		return resp, nil
	})

	// Create the agent service once.
	agentService, err := agents.NewEchoAgent()
	if err != nil {
		log.Fatalf("failed to create echo agent: %v", err)
	}

	// Conversation endpoint
	huma.Post(api, "/conversation", func(ctx context.Context, input *struct {
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

		text, err := agentService.ProcessQuery(ctx, input.Body.UserID, input.Body.SessionID, content, agent.RunConfig{})
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
	})

	fmt.Println("Server starting at http://localhost:8080")
	http.ListenAndServe(":8080", r)
}
