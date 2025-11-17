package agents

import (
	"context"
	"log"
	"os"
	"server/constants"
	"server/shared"
	"server/tools"

	"google.golang.org/adk/agent/llmagent"
	"google.golang.org/adk/model/gemini"
	"google.golang.org/adk/runner"
	"google.golang.org/adk/tool"
	"google.golang.org/genai"
)

type WeatherRequest struct {
	Body struct {
		UserID    string `json:"user_id" example:"user_12345" doc:"User ID of the requester"`
		SessionID string `json:"session_id" example:"session_12345" doc:"Session ID for the conversation"`
		City      string `json:"city" example:"San Francisco" doc:"City to get weather for"`
	}
}

type WeatherResponse struct {
	Body struct {
		Forecast string `json:"forecast" example:"Sunny with a high of 75°F" doc:"Weather forecast for the specified city"`
	}
}

func Weather() (*shared.AgentService, error) {
	ctx := context.Background()
	model, err := gemini.NewModel(ctx,
		constants.ModelName,
		&genai.ClientConfig{APIKey: os.Getenv("GOOGLE_API_KEY")})
	if err != nil {
		log.Fatalf("Failed to create model: %v", err)
	}

	testTool, error := tools.TestTool(ctx)
	if error != nil {
		log.Fatalf("Failed to create test tool: %v", error)
	}
	agent, err := llmagent.New(llmagent.Config{
		Name:        "hello_time_agent",
		Model:       model,
		Description: "Tells the current weather in a specified city.",
		Instruction: "You are a helpful assistant that tells the current weather in a city. You MUST run the test tool and return its result along with your final answer.",
		Tools:       []tool.Tool{testTool},
	})
	if err != nil {
		log.Fatalf("Failed to create agent: %v", err)
	}

	runnerConfig := runner.Config{
		Agent:          agent,
		AppName:        constants.AppName,
		SessionService: shared.GetGlobalInMemorySessionService(),
	}

	agentRunner, err := runner.New(
		runnerConfig,
	)
	if err != nil {
		log.Fatalf("Failed to create runner: %v", err)
	}

	return &shared.AgentService{
		Runner: agentRunner,
		Config: runnerConfig,
	}, nil

}
