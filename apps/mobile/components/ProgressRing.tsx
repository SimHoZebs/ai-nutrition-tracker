import React from "react";
import { View } from "react-native";
import { ThemedText } from "@/components/themed-text";

interface ProgressRingProps {
  label: string;
  current: number;
  goal: number;
  color: string;
  size?: "sm" | "lg";
  unit?: string;
}

export function ProgressRing({
  label,
  current,
  goal,
  color,
  size = "sm",
  unit = "",
}: ProgressRingProps) {
  const percentage = Math.min((current / goal) * 100, 100);

  const dimensions = size === "lg" ? "w-24 h-24" : "w-16 h-16";
  const strokeWidth = 6;
  const containerSize = dimensions === "w-24 h-24" ? 96 : 64;
  const innerSize = containerSize - strokeWidth * 2;

  // Create progress segments for the arc
  const createProgressSegments = () => {
    const segments = [];
    const segmentAngle = 360 / 20; // Divide circle into 20 segments;

    for (let i = 0; i < 20; i++) {
      const startAngle = i * segmentAngle;
      const endAngle = (i + 1) * segmentAngle;
      const segmentPercentage = (endAngle / 360) * 100;

      if (percentage > (startAngle / 360) * 100) {
        segments.push(
          <View
            key={i}
            style={{
              position: "absolute",
              borderRadius: containerSize / 2,
              width: containerSize,
              height: containerSize,
              borderTopColor:
                percentage >= segmentPercentage ? color : "transparent",
              borderRightColor: "transparent",
              borderBottomColor: "transparent",
              borderLeftColor: "transparent",
              borderWidth: strokeWidth,
              transform: [
                { rotate: `${startAngle}deg` },
                { translateX: 0 },
                { translateY: 0 },
              ],
              transformOrigin: "center",
            }}
          />,
        );
      }
    }

    return segments;
  };

  return (
    <View className="flex flex-col items-center">
      <View className={`relative ${dimensions}`}>
        {/* Outer circle (background) */}
        <View
          style={{
            position: "absolute",
            borderRadius: containerSize / 2,
            width: containerSize,
            height: containerSize,
            borderWidth: strokeWidth,
            borderColor: "#e2e8f0",
          }}
        />

        {/* Progress arc segments */}
        <View
          style={{
            position: "absolute",
            borderRadius: containerSize / 2,
            width: containerSize,
            height: containerSize,
          }}
        >
          {createProgressSegments()}
        </View>

        {/* Inner circle (creates the ring effect) */}
        <View
          style={{
            borderRadius: innerSize,
            width: innerSize,
            height: innerSize,
            backgroundColor: "#ffffff",
            top: strokeWidth,
            left: strokeWidth,
          }}
        />

        {/* Center content */}
        <View className="absolute inset-0 flex flex-col items-center justify-center">
          <ThemedText
            darkColor="text-stone-950"
            className={
              size === "lg" ? "text-lg font-medium" : "text-sm font-medium"
            }
          >
            {Math.round(current)}
          </ThemedText>
          <ThemedText className="text-xs text-stone-950 dark:text-stone-950">
            /{goal}
            {unit}
          </ThemedText>
        </View>
      </View>
      <ThemedText className="text-xs text-slate-600 dark:text-slate-400 mt-1">
        {label}
      </ThemedText>
    </View>
  );
}

