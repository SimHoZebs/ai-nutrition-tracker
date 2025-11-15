from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .models import Food
from .serializers import FoodSerializer


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.none()
    serializer_class = FoodSerializer

    def get_queryset(self):
        return Food.objects.filter(user=self.request.user).order_by("-eaten_at")

    @action(detail=False, methods=["get"])
    def lookup(self, request):
        """
        Find existing meals based on natural language references.
        Query params: meal_reference, user_id, context_date
        """
        meal_reference = request.GET.get("meal_reference", "")
        user_id = request.GET.get("user_id")
        context_date = request.GET.get("context_date")

        if not meal_reference or not user_id:
            return Response(
                {"error": "meal_reference and user_id are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Parse meal reference for date and meal type
        target_date = datetime.now().date()
        if "yesterday" in meal_reference.lower():
            target_date = (datetime.now() - timedelta(days=1)).date()

        meal_type = None
        if "breakfast" in meal_reference.lower():
            meal_type = "breakfast"
        elif "lunch" in meal_reference.lower():
            meal_type = "lunch"
        elif "dinner" in meal_reference.lower():
            meal_type = "dinner"
        elif "snack" in meal_reference.lower():
            meal_type = "snack"

        # Query foods
        foods_query = Food.objects.filter(user=user, eaten_at__date=target_date)

        if meal_type:
            foods_query = foods_query.filter(meal_type__icontains=meal_type)

        foods = foods_query.order_by("-eaten_at")

        if foods.exists():
            serializer = FoodSerializer(foods, many=True)
            return Response(
                {
                    "found": True,
                    "foods": serializer.data,
                    "meal_type": meal_type,
                    "date": target_date.isoformat(),
                }
            )
        else:
            return Response(
                {
                    "found": False,
                    "foods": [],
                    "meal_type": meal_type,
                    "date": target_date.isoformat(),
                }
            )

    @action(detail=False, methods=["patch"])
    def bulk_update(self, request):
        """
        Apply updates to existing meal.
        Body: {"meal_id": "...", "operations": [...], "user_id": "..."}
        """
        meal_id = request.data.get("meal_id")
        operations = request.data.get("operations", [])
        user_id = request.data.get("user_id")

        if not user_id or not operations:
            return Response(
                {"error": "user_id and operations are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        updated_foods = []

        for operation in operations:
            action = operation.get("action")
            target = operation.get("target")

            if action == "change" and "new_value" in operation:
                # Update existing food
                foods = Food.objects.filter(user=user, name__icontains=target)
                for food in foods:
                    for field, value in operation["new_value"].items():
                        if hasattr(food, field):
                            setattr(food, field, value)
                    food.save()
                    updated_foods.append(food)

            elif action == "remove":
                # Delete food
                Food.objects.filter(user=user, name__icontains=target).delete()

            elif action == "add" and "food_data" in operation:
                # Add new food
                food_data = operation["food_data"]
                food_data["user"] = user
                food = Food.objects.create(**food_data)
                updated_foods.append(food)

        serializer = FoodSerializer(updated_foods, many=True)
        return Response(
            {
                "success": True,
                "updated_foods": serializer.data,
                "message": "Meal updated successfully",
            }
        )
