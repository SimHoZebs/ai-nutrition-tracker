from rest_framework import serializers
from .models import CustomFood

class CustomFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomFood
        fields = '__all__'
