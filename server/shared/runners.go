package shared

import (
	"sync"

	"google.golang.org/adk/session"
)

func GetGlobalInMemorySessionService() session.Service {
	var once sync.Once
	var globalInMemorySessionService session.Service

	once.Do(func() {
		globalInMemorySessionService = session.InMemoryService()
	})

	return globalInMemorySessionService
}
