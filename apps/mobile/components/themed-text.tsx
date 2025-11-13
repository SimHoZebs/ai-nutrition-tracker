import { type TextProps } from "react-native";
import { Text } from "react-native";

import { useThemeColor } from "@/hooks/use-theme-color";

export type ThemedTextProps = TextProps & {
  lightColor?: string;
  darkColor?: string;
  type?: "default" | "title" | "defaultSemiBold" | "subtitle" | "link";
};

export function ThemedText({
  lightColor,
  darkColor,
  type = "default",
  className,
  ...rest
}: ThemedTextProps & { className?: string }) {
  const color = useThemeColor({ light: lightColor, dark: darkColor }, "text");

  const typeClasses = {
    default: "text-base leading-6",
    defaultSemiBold: "text-base leading-6 font-semibold",
    title: "text-2xl font-bold leading-8",
    subtitle: "text-xl font-bold",
    link: "text-base leading-[30px] text-cyan-700",
  };

  return (
    <Text
      className={[typeClasses[type], `${color}`, className].join(" ")}
      {...rest}
    />
  );
}
