package agents

import (
	"context"
	"log"
	"os"
	"server/constants"

	"google.golang.org/adk/agent"
	"google.golang.org/adk/agent/llmagent"
	"google.golang.org/adk/model/gemini"
	"google.golang.org/genai"
)

type NutritionRequest struct {
	Body struct {
		UserID    string `json:"user_id" example:"user_12345" doc:"User ID of the requester"`
		SessionID string `json:"session_id" example:"session_12345" doc:"Session ID for the conversation"`
		Text      string `json:"text" example:"I ate a chicken sandwich" doc:"Description of food eaten"`
	}
}

type NutritionResponse struct {
	Body struct {
		Analysis string `json:"analysis" example:"{...}" doc:"Nutritional analysis and assumptions"`
	}
}

func Nutrition() (agent.Agent, error) {
	ctx := context.Background()
	model, err := gemini.NewModel(ctx,
		constants.ModelName,
		&genai.ClientConfig{APIKey: os.Getenv("GOOGLE_API_KEY")})
	if err != nil {
		log.Fatalf("Failed to create model: %v", err)
	}

	schema := &genai.Schema{
		Type: genai.TypeObject,
		Properties: map[string]*genai.Schema{
			"macros": {
				Type: genai.TypeObject,
				Properties: map[string]*genai.Schema{
					"calories": {Type: genai.TypeString, Description: "e.g. 500 kcal"},
					"protein":  {Type: genai.TypeString, Description: "e.g. 30 g"},
					"carbs":    {Type: genai.TypeString, Description: "e.g. 40 g"},
					"fat":      {Type: genai.TypeString, Description: "e.g. 20 g"},
				},
				Required: []string{"calories", "protein", "carbs", "fat"},
			},
			"assumptions": {
				Type: genai.TypeArray,
				Items: &genai.Schema{
					Type: genai.TypeString,
				},
			},
		},
		Required: []string{"macros", "assumptions"},
	}

	return llmagent.New(llmagent.Config{
		Name:        "nutrition_agent",
		Model:       model,
		Description: "Estimates nutritional value (macros) and lists assumptions based on food description.",
		Instruction: `You are a nutritional estimation assistant.
Your goal is to estimate the macronutrients for the food described by the user.
You MUST also provide a list of assumptions you made to reach these estimates.
`,
		OutputSchema: schema,
	})
}
