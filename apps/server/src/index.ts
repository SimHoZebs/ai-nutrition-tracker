import { Elysia } from "elysia";
import { HumanMessage } from "@langchain/core/messages";
import { agent } from "./agents/base";

const app = new Elysia()
  .get("/hello", () => "Hello Elysia")
  .get("/llm", async () => {
    const result = await agent.invoke({
      messages: [new HumanMessage("Add 3 and 4.")],
    });

    for (const message of result.messages) {
      console.log(`[${message.getType()}]: ${message.text}`);
    }
  })
  .listen(3000);

console.log(
  `🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`,
);

export type App = typeof app;
