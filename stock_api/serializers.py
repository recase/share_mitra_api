from rest_framework import serializers
from .models import Company, Sector, LivePirce, StockPrice


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['id', 'name', 'regulatory_body']


class CompanySerializer(serializers.ModelSerializer):
    sector = serializers.StringRelatedField(
        source='sector.name', read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'symbol', 'sector']


class LivePriceSerializer(serializers.ModelSerializer):
    symbol = serializers.StringRelatedField(
        source='company.symbol', read_only=True)
    last_traded_time = serializers.CharField(source="last_updated_time")
    change = serializers.CharField(source="percentage_change")
    previous_close_price = serializers.CharField(source="previous_close")

    class Meta:
        model = LivePirce
        fields = ['symbol', 'open_price', 'high_price', 'low_price', 'previous_close_price', 'last_traded_price',
                  'total_volume', 'change', "last_traded_time", "last_traded_volume"]


class RoundingDecimalField(serializers.DecimalField):
    def validate_precision(self, value):
        return value


class StockPriceSerializer(serializers.ModelSerializer):
    symbol = serializers.StringRelatedField(
        source='company.symbol', read_only=True)
    percentage_change = RoundingDecimalField(max_digits=4, decimal_places=2)

    class Meta:
        model = StockPrice
        fields = ['id', 'symbol', 'open_price', 'high_price', 'low_price', 'previous_close_price',
                  'close_price', 'percentage_change', 'total_volume', 'date']


class CompanyWithPriceSerializer(serializers.ModelSerializer):
    price_list: StockPriceSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'sector', 'price_list']


# change the fiekds name to different names
# class ParkSerializer(serializers.ModelSerializer):
    # location = serializers.CharField(source='otherModel__other_fields')

    # class Meta:
    #     model = Park
    #     fields = ('other_fields', 'location')
