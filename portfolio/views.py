from portfolio.serializers import PortfolioSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
from .models import Portfolio


class UserAuthorizedPortfolio(BasePermission):
    message = "You dont have permission for the portfolio"

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_superuser


class PortfolioView(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Portfolio.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        list_and_create = ['list', 'create']
        if self.action in list_and_create:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated & UserAuthorizedPortfolio]
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = self.queryset.filter(user=request.user)

        serialized_data = PortfolioSerializer(queryset, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)

    def create(self, request, format='json'):
        try:
            serialized_data = PortfolioSerializer(data=request.data)
            if serialized_data.is_valid():
                serialized_data.save(user=request.user)
                return Response(status=status.HTTP_201_CREATED)

            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, format='json'):
        try:
            instance = self.queryset.get(pk=pk)
            serialized_data = PortfolioSerializer(instance, data=request.data)
            if serialized_data.is_valid():
                serialized_data.save(user=request.user)
                return Response(status=status.HTTP_200_OK)

            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            portfolio = Portfolio.objects.get(pk=pk)
            portfolio.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data=e, status=status.HTTP_400_BAD_REQUEST)
