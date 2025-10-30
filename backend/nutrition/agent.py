import requests
from .utils import strip_code_blocks
from foods.models import Food
from foods.serializers import FoodSerializer, AgentFoodResponseSerializer


def create_foods_from_data(foods_data, user):
    """Create Food objects using the AgentFoodResponseSerializer"""
    created_foods = []
    for food_data in foods_data:
        serializer = AgentFoodResponseSerializer(data=food_data, context={"user": user})
        if serializer.is_valid():
            food_obj = serializer.save()
            created_foods.append(food_obj)
            print(f"Created food entry: {food_obj.name} (ID: {food_obj.id})")
        else:
            print(f"Invalid food data: {serializer.errors}")
            print(f"Food data was: {food_data}")
    return created_foods


def update_existing_foods(foods_data, user):
    """Update existing Food objects based on agent response data"""
    updated_foods = []
    for food_data in foods_data:
        if "id" in food_data:
            try:
                food = Food.objects.get(id=food_data["id"], user=user)
                serializer = AgentFoodResponseSerializer(
                    food, data=food_data, partial=True, context={"user": user}
                )
                if serializer.is_valid():
                    food_obj = serializer.save()
                    updated_foods.append(food_obj)
                    print(f"Updated food entry: {food_obj.name} (ID: {food_obj.id})")
                else:
                    print(f"Invalid update data: {serializer.errors}")
                    print(f"Food data was: {food_data}")
            except Food.DoesNotExist:
                print(f"Food with id {food_data['id']} not found for user {user}")
    return updated_foods


def build_agent_payload(user_id, session_id, message_text=None, image_data=None, personalization=None):
    """
    Build payload for agent API request.

    Args:
        user_id: User identifier
        session_id: Session identifier
        message_text: Optional text message
        image_data: Optional dict with 'mimeType' and 'data' keys for image
        personalization: Optional personalization data
    """
    parts = []

    if message_text:
        parts.append({"text": message_text})

    if image_data:
        parts.append({
            "inlineData": {
                "mimeType": image_data["mimeType"],
                "data": image_data["data"]
            }
        })

    payload = {
        "app_name": "food_text",
        "user_id": user_id,
        "session_id": session_id,
        "new_message": {"role": "user", "parts": parts},
    }

    if personalization:
        payload["personalization"] = personalization

    return payload


def send_agent_request(agent_base_url, payload):
    agent_response = requests.post(f"{agent_base_url}/run", json=payload)
    return agent_response


def process_agent_response(content, user, clear_session_callback=None):
    print(f"Agent response content: {content}")
    questions = []
    foods = []
    request_type = content.get("request_type", "new")

    # Check for questions/foods in parts structure
    if "parts" in content and content["parts"]:
        for part in content["parts"]:
            if "text" in part:
                try:
                    import json

                    text_content = json.loads(strip_code_blocks(part["text"]))
                    questions = text_content.get("questions", [])
                    foods = text_content.get("foods", [])

                    # Check if this part contains questions
                    if isinstance(text_content, dict) and "questions" in text_content:
                        questions.extend(text_content["questions"])

                    # Check if this part contains foods (as JSON array)
                    elif isinstance(text_content, list) and len(text_content) > 0:
                        # Assume this is a list of foods if it has typical food fields
                        if all(
                            isinstance(item, dict) and "name" in item
                            for item in text_content
                        ):
                            foods.extend(text_content)

                except (json.JSONDecodeError, TypeError):
                    continue

    if questions:
        print(f"Questions detected: {questions}")
        return content
    elif foods:
        print(f"No questions - saving {len(foods)} foods to database")
        try:
            if request_type == "update":
                update_existing_foods(foods, user)

            # Use the serializer to handle field mapping and validation
            created_foods = create_foods_from_data(foods, user)
            serialized_foods = FoodSerializer(created_foods, many=True).data

            response_content = content.copy()
            response_content["response"] = serialized_foods

            if clear_session_callback:
                clear_session_callback()

            return response_content
        except Exception as e:
            print(f"Error creating food entries: {e}")
            response_content = content.copy()
            response_content["error"] = str(e)
            return response_content
    else:
        print("No foods or questions detected in agent response")
        if clear_session_callback:
            clear_session_callback()
        return content