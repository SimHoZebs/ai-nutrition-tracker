import { Image } from "expo-image";
import { Platform, StyleSheet, View, Text, Pressable } from "react-native";
import { useState } from "react";

import { HelloWave } from "@/components/hello-wave";
import ParallaxScrollView from "@/components/parallax-scroll-view";
import { ThemedText } from "@/components/themed-text";
import { ThemedView } from "@/components/themed-view";
import { Link } from "expo-router";
import TotalMacroPanel from "@/components/TotalMacroPanel";
import MealCard from "@/components/MealCard";
import InputBar from "@/components/InputBar";
import { ProgressRing } from "@/components/ProgressRing";
import { api } from "@/lib/api";

export default function HomeScreen() {
  const [serverResponse, setServerResponse] = useState<string>("");

  const testServerConnection = async () => {
    try {
      const response = await api.api.health.get();
      if (response.data) {
        setServerResponse(`Server says: ${JSON.stringify(response.data)}`);
      }
    } catch (error) {
      setServerResponse(`Error: ${error}`);
      console.error("Error connecting to server:", error);
    }
  };

  return (
    <ThemedView className="pt-16 h-full w-full gap-4">
      <ThemedText className="px-4" type="title">
        Tuesday
      </ThemedText>
      <Pressable onPress={() => alert("Hello!")} className="px-4">
        <HelloWave />
      </Pressable>

      <Pressable
        onPress={testServerConnection}
        className="mx-4 p-4 bg-blue-500 rounded-lg"
      >
        <ThemedText className="text-white text-center">
          Test Server Connection
        </ThemedText>
      </Pressable>

      {serverResponse && (
        <ThemedView className="mx-4 p-4 bg-gray-100 rounded-lg">
          <ThemedText>{serverResponse}</ThemedText>
        </ThemedView>
      )}

      <TotalMacroPanel />
      <ThemedView className="flex-1 gap-4 p-4">
        <MealCard />
        <MealCard />
        <ProgressRing
          label="Calories"
          current={1200}
          goal={2000}
          color="#34D399"
          size="lg"
          unit="kcal"
        />
      </ThemedView>
      <InputBar />
    </ThemedView>
  );
}
