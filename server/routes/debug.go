package routes

import (
	"context"
	"fmt"
	"github.com/danielgtaylor/huma/v2"
	"google.golang.org/adk/session"
	"net/http"
	"server/constants"
	"server/shared"
)

type DebugGetMessagesRequest struct {
	UserId    string `path:"user_id" example:"user_12345" doc:"User ID associated with the session"`
	SessionId string `path:"session_id" example:"session_12345" doc:"Session ID to retrieve messages from"`
}

type debugGetMessagesResponse struct {
	Body struct {
		Messages []string `json:"messages"`
	}
}

type debugListSessionsResponse struct {
	Body struct {
		SessionIds []string `json:"session_ids"`
	}
}

func RegisterDebugEndpoints(api huma.API, prefix string) {
	debugGroup := huma.NewGroup(api, prefix)

	huma.Register(
		debugGroup,
		huma.Operation{
			OperationID: "debug_list_sessions",
			Summary:     "List all session IDs for a user",
			Method:      http.MethodGet,
			Path:        "/sessions/{user_id}",
		},
		func(ctx context.Context, input *struct {
			UserId string `path:"user_id" example:"user_12345" doc:"User ID to list sessions for"`
		}) (response *debugListSessionsResponse, err error) {
			listRes, err := shared.GetGlobalInMemorySessionService().List(ctx, &session.ListRequest{
				AppName: constants.AppName,
				UserID:  input.UserId,
			})

			if err != nil {
				return nil, huma.Error400BadRequest(fmt.Sprintf("Error listing sessions: %v", err))
			}

			var sessionIds []string
			for _, s := range listRes.Sessions {
				sessionIds = append(sessionIds, s.ID())
			}

			resp := &debugListSessionsResponse{}
			resp.Body.SessionIds = sessionIds
			return resp, nil

		},
	)

	huma.Register(
		debugGroup,
		huma.Operation{
			OperationID: "debug_get_messages",
			Method:      http.MethodGet,
			Path:        "/messages/{user_id}/{session_id}",
			Summary:     "Retrieve messages from a user session",
			Responses: map[string]*huma.Response{
				"400": {
					Description: "Bad Request - Error retrieving session",
				},
			},
		},

		func(ctx context.Context, input *DebugGetMessagesRequest) (response *debugGetMessagesResponse, err error) {

			getResp, err := shared.GetGlobalInMemorySessionService().Get(
				ctx, &session.GetRequest{
					AppName:   constants.AppName,
					UserID:    input.UserId,
					SessionID: input.SessionId,
				})
			if err != nil {
				resp := &debugGetMessagesResponse{}
				resp.Body.Messages = []string{fmt.Sprintf("Error retrieving session: %v", err)}
				return resp, huma.Error400BadRequest(fmt.Sprintf("Error retrieving session: %v", err))
			}

			stored := getResp.Session
			events := stored.Events().All()
			var messages []string
			for ev := range events {
				if ev.Content == nil {
					continue
				}

				for _, p := range ev.Content.Parts {

					if p != nil {
						messages = append(messages, p.Text)
					}
				}

			}

			resp := &debugGetMessagesResponse{}
			resp.Body.Messages = messages
			return resp, nil
		},
	)
}
