import { treaty } from "@elysiajs/eden";
import type { App } from "@lazyfood/server/types";

export const api = treaty<App>(process.env.EXPO_PUBLIC_API_URL || "http://localhost:3333");

