from rest_framework import viewsets
from .models import CustomFood
from .serializers import CustomFoodSerializer

class CustomFoodViewSet(viewsets.ModelViewSet):
    queryset = CustomFood.objects.all()
    serializer_class = CustomFoodSerializer
