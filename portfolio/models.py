from django.db import models
from stock_api.models import Company
from django.contrib.auth import get_user_model

User = get_user_model()


class Portfolio(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="portfolios")
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="portfolios")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['company', 'user'], name='stock user company')
        ]


class Transaction(models.Model):
    IPO = 'IPO'
    FPO = 'FPO'
    Right = 'right'
    Auction = 'auction'
    Bonus = 'bonus'
    Dividend = 'dividend'
    BUY = 'secondary buy'
    SELL = 'sell'
    TRANSACTION_TYPE = ((IPO, 'IPO'), (FPO, 'FPO'), (Right, 'Right'), (Auction, 'Auction'), (
        Bonus, 'Bonus'), (Dividend, 'Dividend'), (BUY, 'Secondary buy'), (SELL, 'Secondary sell'))

    units = models.IntegerField(null=True, blank=True, default=None)
    transaction_type = models.CharField(
        choices=TRANSACTION_TYPE, max_length=20)
    cost_per_unit = models.FloatField(null=True, blank=True, default=None)
    transaction_date = models.DateField()
    sebon_charge = models.FloatField(null=True, blank=True, default=None)
    broker_charge = models.FloatField(null=True, blank=True, default=None)
    dp_charge = models.FloatField(null=True, blank=True, default=None)
    auction_charge = models.FloatField(null=True, blank=True, default=None)
    casba_charge = models.FloatField(null=True, blank=True, default=None)
    capital_gain_tax = models.FloatField(null=True, blank=True, default=None)
    bonus_amount = models.FloatField(null=True, blank=True, default=None)
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, related_name='transactions')

    def __str__(self):
        if self.transaction_type is not self.Bonus:
            return f'{self.units} units {self.transaction_type}'
        else:
            return f'Bonus amount: {self.bonus_amount} at {self.transaction_date}'

    def incoming_transaction(self):
        return self.objects.filter(self.transaction_type is not self.SELL)

    def outgoing_transaction(self):
        return self.objects.filter(self.transaction_type is self.SELL)

    class Meta:
        db_table = 'stock_transaction'

    def save(self, *args, **kwargs):
        on_market = [self.BUY, self.SELL]

        if self.transaction_type in on_market:
            total_cost = self.units * self.cost_per_unit
            self.dp_charge = 25
            self.sebon_charge = round((0.015/100) * total_cost, 2)
            self.broker_charge = round(
                self.broker_rate(total_cost)/100 * total_cost, 2)
        else:
            self.dp_charge = self.sebon_charge = self.broker_charge = None

        super(Transaction, self).save(*args, **kwargs)

    def broker_rate(self, amount):
        if amount <= 50000:
            return 0.4
        elif amount <= 500000:
            return 0.37
        elif amount <= 2000000:
            return 0.34
        elif amount <= 10000000:
            return 0.3
        else:
            return 0.27
