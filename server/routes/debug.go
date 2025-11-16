package routes

import (
	"context"
	"fmt"
	"github.com/danielgtaylor/huma/v2"
	"google.golang.org/adk/session"
	"server/constants"
	"server/shared"
)

type debugResponse struct {
	Messages []string `json:"messages"`
}

func RegisterDebugEndpoints(api huma.API, prefix string) {
	debugGroup := huma.NewGroup(api, prefix)

	huma.Get(debugGroup, "/get-messages/{user-id}/{session-id}", func(ctx context.Context, input *struct {
		UserId    string `path:"user-id" example:"user_12345" doc:"User ID associated with the session"`
		SessionId string `path:"session-id" example:"session_12345" doc:"Session ID to retrieve messages from"`
	}) (response *debugResponse, err error) {

		getResp, err := shared.GetGlobalInMemorySessionService().Get(
			ctx, &session.GetRequest{
				AppName:   constants.AppName,
				UserID:    input.UserId,
				SessionID: input.SessionId,
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

		return &debugResponse{
			Messages: messages,
		}, nil
	},
	)
}
