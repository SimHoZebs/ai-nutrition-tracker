from rest_framework import viewsets
from .models import Food
from .serializers import FoodSerializer


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.none()
    serializer_class = FoodSerializer

    def get_queryset(self):
        return Food.objects.filter(user=self.request.user).order_by("-created_at")
