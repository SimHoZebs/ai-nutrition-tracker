from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CustomFood
from .serializers import CustomFoodSerializer
from .services.usda_api import USDAApiClient


class CustomFoodViewSet(viewsets.ModelViewSet):
    queryset = CustomFood.objects.all()
    serializer_class = CustomFoodSerializer


@api_view(['GET'])
def search_usda_foods(request):
    """
    Search for foods using USDA API

    Query parameters:
    - q: Search query (required)
    - page_size: Number of results (optional, default 25)
    - page: Page number (optional, default 1)
    """
    query = request.GET.get('q')
    if not query:
        return Response(
            {"error": "Query parameter 'q' is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        page_size = int(request.GET.get('page_size', 25))
        page_number = int(request.GET.get('page', 1))

        client = USDAApiClient()
        results = client.search_foods(
            query=query,
            page_size=min(page_size, 200),  # Max 200 per page
            page_number=page_number
        )

        return Response(results)

    except ValueError as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": f"Failed to fetch data from USDA API: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_usda_food_details(request, fdc_id):
    """
    Get detailed information for a specific food by FDC ID
    """
    try:
        client = USDAApiClient()
        details = client.get_food_details(fdc_id)
        return Response(details)

    except ValueError as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": f"Failed to fetch food details: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
