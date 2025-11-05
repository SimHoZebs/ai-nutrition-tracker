import { useState } from "react";
import { Button, Pressable, TextInput } from "react-native";
import { ThemedView } from "./themed-view";
import { ThemedText } from "./themed-text";

const InputBar = () => {
  const [text, onChangeText] = useState("");

  return (
    <ThemedView className="flex-row w-full justify-evenly gap-4">
      <Pressable className="w-16 h-16 bg-stone-900 justify-center items-center rounded-full">
        <ThemedText>Mic</ThemedText>
      </Pressable>

      <TextInput
        className="bg-stone-900 text-stone-100 flex-1"
        onChangeText={onChangeText}
        value={text}
        placeholder="Describe your meals..."
      />

      <Pressable className="w-16 h-16 bg-stone-900 justify-center items-center rounded-full">
        <ThemedText>Cam</ThemedText>
      </Pressable>
    </ThemedView>
  );
};

export default InputBar;
