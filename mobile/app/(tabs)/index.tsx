import { Image } from "expo-image";
import { Platform, StyleSheet, View, Text } from "react-native";

import { HelloWave } from "@/components/hello-wave";
import ParallaxScrollView from "@/components/parallax-scroll-view";
import { ThemedText } from "@/components/themed-text";
import { ThemedView } from "@/components/themed-view";
import { Link } from "expo-router";

export default function HomeScreen() {
  return (
    <ThemedView
      className="pt-16 h-full w-full"
      lightColor="bg-stone-50"
      darkColor="bg-stone-950"
    >
      <ThemedText type="title">Tuesday</ThemedText>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingTop: 64,
    padding: 16,
    height: "100%",
    width: "100%",
    display: "flex",
  },
  text: {
    fontSize: 24,
    fontWeight: "bold",
    color: "white",
  },
});
