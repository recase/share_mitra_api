from django.db import models


class Sector(models.Model):
    name = models.CharField(max_length=200, unique=True)
    regulatory_body = models.CharField(max_length=200)

    def __Str__(self):
        return self.name


class Company(models.Model):
    name: models.CharField(max_length=200)
    symbol: models.CharField(max_length=20, unique=True)
    instrument_type: models.CharField(max_length=20)
    sector = models.ForeignKey(
        Sector, related_name='companies', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def full_name(self):
        return f'{self.name}({self.symbol})'


class LivePirce(models.Model):
    # live market data
    company_id: models.OneToOneField(
        Company, primary_key=True, on_delete=models.CASCADE)
    open_price: models.FloatField()
    high_price: models.FloatField()
    low_price: models.FloatField()
    previous_close: models.FloatField()
    last_traded_price: models.FloatField()
    total_volume: models.IntegerField()
    percentage_change: models.FloatField()
    last_updated_time: models.DateTimeField()

    def save(self, *args, **kwargs):
        self.percentage_change = round(self.percentage_change, 3)
        super(LivePirce, self).save(*args, **kwargs)


class StockPrice(models.Model):
    # historical stock data
    company_id: models.ForeignKey(Company, on_delete=models.CASCADE)
    open_price: models.FloatField()
    high_price: models.FloatField()
    low_price: models.FloatField()
    previous_price: models.FloatField()
    close_price: models.FloatField()
    percentage_change: models.FloatField()
    total_volume: models.IntegerField()
    date: models.DateField()

    def save(self, *args, **kwargs):
        self.percentage_change = round(self.percentage_change, 3)
        super(StockPrice, self).save(*args, **kwargs)


class StockUpdateTable(models.Model):
    # fields to check the stoock status
    # last_updated_live_data: models.DateTimeField()
    # market_status: models.BooleanField()
    # last_updated_stock_price: models.DateField()
    setting = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
