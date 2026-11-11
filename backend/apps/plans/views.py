from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import TiffinPlan, Tag
from .serializers import TiffinPlanSerializer, TagSerializer
from accounts.permissions import IsAdminRole


class PlanListCreateView(APIView):
    """
    GET /api/plans - List all plans (public)
    POST /api/plans - Create a new plan (admin only)
    """
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminRole()]
        return [permissions.AllowAny()]

    def get(self, request):
        queryset = TiffinPlan.objects.filter(is_active=True).prefetch_related('tags')
        
        # Filtering support
        meal_type = request.query_params.get('mealType') or request.query_params.get('meal_type')
        duration = request.query_params.get('duration')
        search = request.query_params.get('search')
        tag = request.query_params.get('tag')

        if meal_type:
            queryset = queryset.filter(meal_type__iexact=meal_type)
        if duration:
            queryset = queryset.filter(duration__iexact=duration)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        if tag:
            queryset = queryset.filter(tags__slug=tag)

        # Order by meal_type asc, price asc (matching Express)
        queryset = queryset.order_by('meal_type', 'price')
        serializer = TiffinPlanSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TiffinPlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlanDetailUpdateDeleteView(APIView):
    """
    GET /api/plans/<id> - Retrieve single plan (public)
    PUT /api/plans/<id> - Update plan (admin only)
    DELETE /api/plans/<id> - Delete plan (admin only)
    """
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminRole()]
        return [permissions.AllowAny()]

    def get_object(self, pk):
        return get_object_or_404(TiffinPlan, pk=pk)

    def get(self, request, pk):
        plan = self.get_object(pk)
        serializer = TiffinPlanSerializer(plan)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        plan = self.get_object(pk)
        serializer = TiffinPlanSerializer(plan, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        plan = self.get_object(pk)
        plan.delete()
        return Response({"message": "Plan deleted successfully"}, status=status.HTTP_200_OK)


class PlanAjaxSearchView(APIView):
    """
    GET /api/plans/search - Asynchronous AJAX search endpoint for Module 6.
    Performs real-time search across titles, descriptions, and tags.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        meal_type = request.query_params.get('mealType', '').strip()
        duration = request.query_params.get('duration', '').strip()

        queryset = TiffinPlan.objects.filter(is_active=True).prefetch_related('tags')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()

        if meal_type:
            queryset = queryset.filter(meal_type__iexact=meal_type)

        if duration:
            queryset = queryset.filter(duration__iexact=duration)

        queryset = queryset.order_by('meal_type', 'price')
        serializer = TiffinPlanSerializer(queryset, many=True)
        return Response({
            "count": queryset.count(),
            "query": query,
            "results": serializer.data
        }, status=status.HTTP_200_OK)
