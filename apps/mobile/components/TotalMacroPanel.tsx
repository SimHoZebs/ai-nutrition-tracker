import { ThemedText } from "@/components/themed-text";
import { ThemedView } from "@/components/themed-view";

export default function TotalMacroPanel() {
  return (
    <ThemedView className="p-4 w-full border-b border-stone-700 rounded-lg flex-row justify-between">
      <ThemedText>Calories: 0</ThemedText>
      <ThemedText>Protein: 0</ThemedText>
      <ThemedText>Carbs: 0</ThemedText>
      <ThemedText>Fat: 0</ThemedText>
    </ThemedView>
  );
}
