package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"server/routes"

	"github.com/danielgtaylor/huma/v2"
	"github.com/joho/godotenv"

	"github.com/danielgtaylor/huma/v2/adapters/humachi"
	"github.com/go-chi/chi/v5"
)

// GreetingOutput represents the greeting operation response.
type GreetingOutput struct {
	Body struct {
		Message string `json:"message" example:"Hello, world!" doc:"Greeting message"`
	}
}

func main() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("No .env file found, proceeding with environment variables")
	}
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

	routes.RegisterAgentEndpoints(api)

	fmt.Println("Server starting at http://localhost:8080")
	http.ListenAndServe(":8080", r)
}
