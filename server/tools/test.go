package tools

import (
	"context"
	"fmt"
	"os"

	"google.golang.org/adk/tool"
	"google.golang.org/adk/tool/functiontool"
)

type TestArgs struct {
	// Empty struct for tools that don't need input parameters
}

type TestResponse struct {
	Value string `json:"value" example:"test response" doc:"Response from the test tool"`
}

func yeet(ctx tool.Context, args TestArgs) TestResponse {

	content, err := os.ReadFile("./tools/test.md")
	if err != nil {
		return TestResponse{
			Value: fmt.Sprintf("Error reading file: %v", err),
		}
	}

	return TestResponse{
		Value: string(content),
	}
}

func TestTool(ctx context.Context) (tool.Tool, error) {

	return functiontool.New(
		functiontool.Config{
			Name:        "test_tool",
			Description: "A tool that reads content from a test file.",
		},
		yeet,
	)

}
