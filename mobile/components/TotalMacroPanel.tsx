import { ThemedText } from "@/components/themed-text";
import { ThemedView } from "@/components/themed-view";

export default function TotalMacroPanel() {
  return (
    <ThemedView>
      <ThemedText>Calories: 0</ThemedText>
      <ThemedText>Protein: 0</ThemedText>
      <ThemedText>Carbs: 0</ThemedText>
      <ThemedText>Fat: 0</ThemedText>
    </ThemedView>
  );
}
