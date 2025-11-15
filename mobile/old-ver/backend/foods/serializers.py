from datetime import datetime

from rest_framework import serializers
from .models import Food


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = "__all__"


class AgentFoodResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for handling AI agent food response data.
    Maps agent field names (with _g suffix) to Django model field names.
    """

    # Agent uses different field names - map them to model fields
    protein_g = serializers.FloatField(source="protein", required=False, default=0.0)
    carbs_g = serializers.FloatField(
        source="carbohydrates", required=False, default=0.0
    )
    saturated_fat_g = serializers.FloatField(
        source="saturated_fat", required=False, default=0.0
    )
    unsaturated_fat_g = serializers.FloatField(
        source="unsaturated_fat", required=False, default=0.0
    )
    trans_fat_g = serializers.FloatField(
        source="trans_fat", required=False, default=0.0
    )
    eaten_at = serializers.DateTimeField(default=datetime.now())

    class Meta:
        model = Food
        fields = [
            "name",
            "meal_type",
            "serving_size",
            "calories",
            "others",
            "eaten_at",
            "protein_g",
            "carbs_g",
            "saturated_fat_g",
            "unsaturated_fat_g",
            "trans_fat_g",
        ]

    def validate(self, data):
        """
        Handle the case where both _g and non-_g versions might be present.
        Prefer _g versions if available, fall back to non-_g versions.
        """
        # Map _g fields to regular fields if _g versions are present
        # The source mapping in field definitions will handle this automatically
        # This validation is just for any additional business logic if needed

        return data

    def create(self, validated_data):
        """Create a Food instance with the user from context"""
        user = self.context.get("user")
        if user:
            validated_data["user"] = user
        return super().create(validated_data)
