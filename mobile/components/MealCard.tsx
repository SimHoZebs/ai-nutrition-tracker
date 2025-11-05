import { ThemedText } from "./themed-text";
import { ThemedView } from "./themed-view";

const MealCard = () => {
  return (
    <ThemedView className="p-4 border border-gray-300 rounded-lg">
      <ThemedText type="title">Scrambled eggs</ThemedText>
      <ThemedText>2 eggs, 1 slice of toast</ThemedText>
      <ThemedView>
        <ThemedText>Calories: 250</ThemedText>
        <ThemedText>Protein: 18g</ThemedText>
        <ThemedText>Carbs: 20g</ThemedText>
        <ThemedText>Fat: 12g</ThemedText>
      </ThemedView>
    </ThemedView>
  );
};

export default MealCard;
