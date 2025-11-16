package shared

import "google.golang.org/adk/runner"

type AgentService struct {
	runner.Config
	Runner *runner.Runner
}
