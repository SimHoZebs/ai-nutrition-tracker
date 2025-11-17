package shared

import (
	"sync"

	"google.golang.org/adk/session"
)

var once sync.Once
var globalInMemorySessionService session.Service

func GetGlobalInMemorySessionService() session.Service {

	once.Do(func() {
		globalInMemorySessionService = session.InMemoryService()
	})

	return globalInMemorySessionService
}
