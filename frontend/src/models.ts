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
