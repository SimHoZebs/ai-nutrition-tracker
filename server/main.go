package main

import (
	"context"
	"fmt"
	"github.com/danielgtaylor/huma/v2"
	"github.com/danielgtaylor/huma/v2/adapters/humachi"
	"github.com/go-chi/chi/v5"
	"github.com/joho/godotenv"
	"google.golang.org/adk/cmd/launcher/adk"
	"google.golang.org/adk/cmd/launcher/full"
	"google.golang.org/adk/server/restapi/services"
	"log"
	"net/http"
	"os"
	"server/agents"
	"server/routes"
)

// GreetingOutput represents the greeting operation response.
type GreetingOutput struct {
	Body struct {
		Message string `json:"message" example:"Hello, world!" doc:"Greeting message"`
	}
}

func main() {
	ctx := context.Background()
	err := godotenv.Load()
	if err != nil {
		log.Fatal("No .env file found, proceeding with environment variables")
	}

	go func() {
		weatherAgent, err := agents.Weather()
		echoAgent, err := agents.NewEchoAgent()
		agentLoader, err := services.NewMultiAgentLoader(weatherAgent, echoAgent)
		if err != nil {
			log.Fatalf("Failed to create agent loader: %v", err)
		}
		config := &adk.Config{
			AgentLoader: agentLoader,
		}

		l := full.NewLauncher()
		if err = l.Execute(ctx, config, os.Args[1:]); err != nil {
			log.Fatalf("Run failed: %v\n\n%s", err, l.CommandLineSyntax())
		}

	}()

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

	routes.RegisterAgentEndpoints(api, "/agents")
	routes.RegisterDebugEndpoints(api, "/debug")

	fmt.Println("Server starting at http://localhost:8888")
	http.ListenAndServe(":8888", r)
}
