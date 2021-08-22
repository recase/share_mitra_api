from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from .models import Company, LivePirce, Sector, StockPrice, StockUpdateTable
from .serializers import CompanyListingSerializer, CompanySerializer, CompanyWithPriceSerializer, LivePriceSerializer, SectorSerializer, StockPriceSerializer
import datetime
from .helper.stock_price_list import retrieve_stock_price_list, retrieve_stock_price_history
from django.core.exceptions import ObjectDoesNotExist


class SectorViewSet(viewsets.ViewSet):
    queryset = Sector.objects.all()

    def list(self, request):
        serializer = SectorSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        sector = get_object_or_404(self.queryset, pk=pk)
        serializer = SectorSerializer(sector)
        return Response(serializer.data)

# class SectorViewSet(viewsets.ModelViewSet):
#     queryset = Sector.objects.all()
#     serializer_class = SectorSerializer


# class CompanyViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
class CompanyViewSet(viewsets.ViewSet):
    queryset = Company.company_objects.all()

    def list(self, requset):
        company_serializer = CompanySerializer(self.queryset, many=True)
        return Response(company_serializer.data)

    def retrieve(self, request, pk=None):
        company = self.queryset.filter(id=pk)
        company_serializer = CompanySerializer(company)
        return Response(company_serializer.data)

    @action(methods=['get'], detail=False, url_path="listing-data", url_name="listing_data")
    def listing_data(self, request):
        company_serializer = CompanyListingSerializer(self.queryset, many=True)
        return Response(company_serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='price-history', url_name="price_history")
    def price_history(self, request, pk=None):
        company = get_object_or_404(self.queryset, id=pk)
        if company is None:
            return Response('price list not found', status=status.HTTP_404_NOT_FOUND)
        # price_list = StockPrice.objects.filter(company_id=company.id).order_by('date')
        company_price_serilizer = CompanyWithPriceSerializer(company)
        return Response(company_price_serilizer.data)


class LivePirceViewSet(viewsets.ViewSet):
    quuerset = LivePirce.custom_objects.all()

    def list(self, request):
        serializer = LivePriceSerializer(self.quuerset, many=True)
        return Response({'stocks': serializer.data, 'date': datetime.datetime.now()})


class StockPriceViewSet(viewsets.ViewSet):
    # queryset = StockPrice.objects.all()

    def list(self, request):
        last_Stock_table_updated = StockUpdateTable.objects.filter(
            setting='stock_table_updated_at').first()
        if last_Stock_table_updated is not None:
            last_updated_date = datetime.datetime.strptime(
                last_Stock_table_updated.value, '%Y-%m-%d').date()
            stocks = retrieve_stock_price_list(date=last_updated_date)
            serializer = StockPriceSerializer(stocks, many=True)
            return Response({'stocks_price': serializer.data, 'date': last_updated_date})
        else:
            return Response(data="Stock price not found", status=status.HTTP_404_NOT_FOUND)

    @ action(methods=['get'], detail=False, url_path='stock-history/(?P<date>\w+)', url_name='stock_history')
    def stock_history(self, request, date):
        print(date)
        print('hello')
        return Response('allu', status=status.HTTP_200_OK)


# class StockPriceHistory(generics.ListAPIView):
#     serializer_class = StockPriceSerializer

#     def get_queryset(self):
#         try:
#             return retrieve_stock_price_history(company_id=self.kwargs['company_id'])
#         except ObjectDoesNotExist:
#             return Response('data not available', status=status.HTTP_404_NOT_FOUND)
