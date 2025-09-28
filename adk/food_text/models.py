from pydantic import BaseModel, RootModel


class Qna(BaseModel):
    question: str
    type: str  # e.g., "slider" or "multiple_choice"
    mcqOptions: list[str]
    sliderValue: int


class Food(BaseModel):
    name: str
    serving_size: float
    calories: float
    protein: float
    carbohydrates: float
    trans_fat: float = 0
    saturated_fat: float = 0
    unsaturated_fat: float = 0
    others: dict = {}
    meal_type: str


class UnknownFood(BaseModel):
    name: str
    description: str
    meal_type: str
    quantity: float = 1.0
    unit: str = "serving"
    ambiguous: bool = False


class ParsedFoods(BaseModel):
    foods: list[UnknownFood] = []
    questions: list[Qna] = []


class FoodSearchResult(BaseModel):
    name: str
    meal_type: str
    serving_size: int = 1
    calories: float = 0.0
    protein_g: float = 0.0
    carbs_g: float = 0.0
    trans_fat_g: float = 0.0
    saturated_fat_g: float = 0.0
    unsaturated_fat_g: float = 0.0
    others: dict = {}


class RequestResponse(RootModel[list[FoodSearchResult]]):
    pass
