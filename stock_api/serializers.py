from rest_framework import serializers
from .models import Company, Sector, LivePirce, StockPrice


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['id', 'name', 'regulatory_body']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'symbol', 'sector']


class LivePriceSerializer(serializers.ModelSerializer):
    symbol = serializers.StringRelatedField(source='symbol', read_only=True)

    class Meta:
        model = LivePirce
        fields = ['id', 'symbol', 'open_price', 'high_price', 'low_price', 'previous_close', 'last_traded_price',
                  'total_volume', 'percentage_change', "last_updated_time"]


class StockPriceSerializer(serializers.ModelSerializer):
    symbol = serializers.StringRelatedField(source='symbol', read_only=True)

    class Meta:
        model = StockPrice
        fields = ['id', 'symbol', 'open_price', 'high_price', 'low_price', 'previous_price',
                  'close_price', 'percentage_change', 'total_volume', 'date']


class CompanyWithPriceSerializer(serializers.ModelSerializer):
    price_list: StockPriceSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'sector', 'price_list']
