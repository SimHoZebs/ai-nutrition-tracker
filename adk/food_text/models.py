from pydantic import BaseModel


class Qna(BaseModel):
    question: str
    type: str  # e.g., "slider" or "multiple_choice"
    mcqOptions: list[str]
    sliderValue: int


class FoodItem(BaseModel):
    name: str
    quantity: float = 1.0
    unit: str = "serving"


class ParsedFoods(BaseModel):
    foods: list[FoodItem]
    questions: list[Qna]


class Nutrition(BaseModel):
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float

    class Config:
        extra = "allow"


class FoodResult(BaseModel):
    name: str
    nutrition: Nutrition
    serving_size: str


class FoodSearchOutput(BaseModel):
    questions: list[Qna]
    foods: list[FoodResult]


class TotalNutrition(BaseModel):
    total_calories: float
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float

    class Config:
        extra = "allow"


class Meal(BaseModel):
    name: str
    foods: list[FoodItem]
    questions: list[Qna] = []


class ParsedMeals(BaseModel):
    meals: list[Meal]


class MealNutrition(BaseModel):
    meal_name: str
    nutrition: TotalNutrition

