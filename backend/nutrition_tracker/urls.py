"""
URL configuration for nutrition_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from foods import views as foods_views
from users import views as users_views
from . import views

router = DefaultRouter()
router.register(r'custom-foods', foods_views.CustomFoodViewSet)
router.register(r'user-profiles', users_views.UserProfileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/transcribe/', views.transcribe_audio, name='transcribe'),
    path('api/usda/search/', foods_views.search_usda_foods, name='usda_search'),
    path('api/usda/food/<int:fdc_id>/', foods_views.get_usda_food_details, name='usda_food_details'),
]
