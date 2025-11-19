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

func RegisterAgentEndpoints(api huma.API, prefix string) {
	agentsGroup := huma.NewGroup(api, prefix)

	// Create the agent service once.
	echo, err := runners.NewEcho()
	if err != nil {
		log.Fatalf("failed to create echo agent: %v", err)
	}

	// Conversation endpoint
	huma.Post(api, "/conversation", func(ctx context.Context, input *struct {
		Body ConversationRequest `body:""`
	}) (*ConversationResponse, error) {
		return ConversationHandler(ctx, echo, input)
	})

	weatherRunner, err := runners.NewWeather()
	if err != nil {
		log.Fatal("failed to create weather agent: " + err.Error())
	}

	huma.Post(agentsGroup, "/weather", func(ctx context.Context, input *agents.WeatherRequest) (*agents.WeatherResponse, error) {

		println("Received weather request for city:", input.Body.City)
		content := genai.NewContentFromText(input.Body.City, genai.RoleUser)

		text, err := ProcessQuery(ctx, ProcessAgentRequest{
			UserID:       input.Body.UserID,
			SessionID:    input.Body.SessionID,
			AgentService: *weatherRunner,
			Message:      content,
		},
		)
		if err != nil {
			return nil, fmt.Errorf("weather agent processing failed: %w", err)
		}

		resp := &agents.WeatherResponse{}
		resp.Body.Forecast = text
		return resp, nil

	})
}
