export interface Question {
  type: "multiple_choice" | "slider",
  question: string,
  mcqOptions: string[],
  sliderValue: number,
}

export interface LogResponse {
  foods: {
    name: string,
    quantity: number,
    unit: string,
  }[],
  questions: Question[],
}

export interface User {
  id: number,
  username: string,
  email: string,
  first_name: string,
  last_name: string,
  date_joined: string,
}

export interface UserProfile {
  user: User,
  date_of_birth: string,
  height: number,
  width: number,
  activity_level: "sedentary" | "lightly_active" | "moderately_active" | "very_active" | "extra_active",
  dietary_goals: DietaryGoals,
  created_at: string,
  updated_at: string,
}

export interface DietaryGoals {
  calories: number,
  protein: number,
}

export interface Memory {
  id: number,
  content: string,
  created_at: string,
  updated_at: string,
  user_id: number,
}
