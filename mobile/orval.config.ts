import { defineConfig } from "orval";

export default defineConfig({
  api: {
    input: {
      // Huma usually serves the spec here by default
      target: "http://localhost:8888/openapi.json",
    },
    output: {
      mode: "single",
      // We'll generate the client here
      target: "./lib/generated-api.ts",
      client: "fetch", // Uses native fetch (perfect for React Native)
      baseUrl: "http://localhost:8888", // Default base URL
    },
  },
});

