package routes

import (
	"net/http"
)

// @router / [get]
// @description test
// @response 200 {string} string "Hello, World!"
func Hello(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("Hello, World!"))
}
