from rest_framework import viewsets, mixins
from rest_framework.response import Response
from .models import Company, Sector
from .serializers import CompanySerializer, SectorSerializer


class SectorViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    def list(self, request):
        query_set = Sector.objects.all()
        serializer = SectorSerializer(query_set, many=True)
        return Response(serializer.data)


class CompanyViewSet(viewsets.ViewSet):
    def list(self, request):
        query_set = Company.objects.all()
        serializer = CompanySerializer(query_set, many=True)
        return Response(serializer.data)
