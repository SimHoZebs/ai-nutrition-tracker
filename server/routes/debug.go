package routes

import (
	"context"
	"fmt"
	"log"
	"server/agents"
	"server/runners"

	"github.com/danielgtaylor/huma/v2"
	"google.golang.org/genai"
)

func registerDebugEndpoints(api huma.API) {
	debugGroup := huma.NewGroup(api, "/debug")

	huma.Get(debugGroup, "/get-messages/{app-name}/{session-id}", func(ctx context.Context, input *struct {
		appName   string `path:"app-name"`
		sessionID string `path:"session-id"`
	}) (*DebugMessagesResponse, error) {

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
	},
	)
}
