import { Image } from "expo-image";
import { Platform, StyleSheet, View, Text, Pressable } from "react-native";

import { HelloWave } from "@/components/hello-wave";
import ParallaxScrollView from "@/components/parallax-scroll-view";
import { ThemedText } from "@/components/themed-text";
import { ThemedView } from "@/components/themed-view";
import { Link } from "expo-router";
import TotalMacroPanel from "@/components/TotalMacroPanel";
import MealCard from "@/components/MealCard";
import InputBar from "@/components/InputBar";
import { ProgressRing } from "@/components/ProgressRing";

export default function HomeScreen() {
  return (
    <ThemedView className="pt-16 h-full w-full gap-4">
      <ThemedText className="px-4" type="title">
        Tuesday
      </ThemedText>
      <Pressable onPress={() => alert("Hello!")} className="px-4">
        <HelloWave />
      </Pressable>
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
