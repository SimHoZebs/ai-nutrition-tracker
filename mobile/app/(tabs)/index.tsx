import { Image } from "expo-image";
import { Platform, StyleSheet, View, Text } from "react-native";

import { HelloWave } from "@/components/hello-wave";
import ParallaxScrollView from "@/components/parallax-scroll-view";
import { ThemedText } from "@/components/themed-text";
import { ThemedView } from "@/components/themed-view";
import { Link } from "expo-router";
import TotalMacroPanel from "@/components/TotalMacroPanel";
import MealCard from "@/components/MealCard";
import InputBar from "@/components/InputBar";

export default function HomeScreen() {
  return (
    <ThemedView className="pt-16 p-4 h-full w-full">
      <ThemedText type="title">Tuesday</ThemedText>
      <TotalMacroPanel />
      <ThemedView className="flex-1 gap-4">
        <MealCard />
        <MealCard />
      </ThemedView>
      <InputBar />
    </ThemedView>
  );
}
