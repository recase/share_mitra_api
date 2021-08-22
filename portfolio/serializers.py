from stock_api.serializers import CompanySerializer
from rest_framework import serializers
from .models import Transaction, Portfolio
from stock_api.models import Company, LivePirce, StockPrice
from django.db.models import Sum, F
from django.db.models.functions import Coalesce
import datetime


class TransactionSerializer(serializers.ModelSerializer):
    investment = serializers.SerializerMethodField()
    total_investment = serializers.SerializerMethodField()
    sold_amount = serializers.SerializerMethodField()
    receivable_amount = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['id', 'units', 'portfolio', 'cost_per_unit', 'bonus_amount', 'transaction_type', 'transaction_date', 'capital_gain_tax', 'casba_charge',
                  'auction_charge', 'dp_charge', 'broker_charge', 'sebon_charge', 'investment', 'total_investment', 'sold_amount', 'receivable_amount']
        read_only_fields = ['capital_gain_tax', 'dp_charge',
                            'broker_charge', 'sebon_charge']
        extra_kwargs = {'id': {'read_only': False,
                               'required': False}}

    def get_investment(self, transaction):
        if transaction.transaction_type != Transaction.SELL and transaction.units is not None and transaction.cost_per_unit is not None:
            return transaction.units * transaction.cost_per_unit

    def get_total_investment(self, transaction):
        total_investment = self.get_investment(transaction)
        if total_investment is None:
            return None
        if transaction.sebon_charge is not None:
            total_investment = total_investment + transaction.sebon_charge
        if transaction.broker_charge is not None:
            total_investment = total_investment + transaction.broker_charge
        if transaction.dp_charge is not None:
            total_investment = total_investment + transaction.dp_charge
        if transaction.auction_charge is not None:
            total_investment = total_investment + transaction.auction_charge
        if transaction.casba_charge is not None:
            total_investment = total_investment + transaction.casba_charge
        return round(total_investment, 2)

    def get_sold_amount(self, transaction):
        if transaction.transaction_type == Transaction.SELL and transaction.units is not None and transaction.cost_per_unit is not None:
            return transaction.units * transaction.cost_per_unit

    def get_receivable_amount(self, transaction):
        receivable_amount = self.get_sold_amount(transaction)
        if receivable_amount is None:
            return None
        if transaction.dp_charge is not None:
            receivable_amount = receivable_amount - transaction.dp_charge
        if transaction.sebon_charge is not None:
            receivable_amount = receivable_amount - transaction.sebon_charge
        if transaction.broker_charge is not None:
            receivable_amount = receivable_amount - transaction.broker_charge
        return round(receivable_amount, 2)

    def validate(self, attrs):
        self._custom_validation(attrs)
        return super().validate(attrs)

    def _custom_validation(self, data):
        transaction_type = data.get('transaction_type')
        transaction_date = data.get('transaction_date')

        if transaction_type is None or transaction_date is None:
            raise serializers.ValidationError(
                {'error': 'data error'})

        date = datetime.datetime.strptime(
            str(transaction_date), '%Y-%m-%d').date()

        if date > datetime.datetime.now().date():
            raise serializers.ValidationError(
                {'error': 'welcome to future!!'})

        units = data.get('units')
        cost_per_unit = data.get('cost_per_unit')
        bonus_amount = data.get('bonus_amount')

        buy_transactions = [Transaction.IPO, Transaction.FPO, Transaction.Right,
                            Transaction.Auction, Transaction.BUY, Transaction.SELL]

        if transaction_type in buy_transactions:
            required_fields = {'units': units, 'cost_per_unit': cost_per_unit}
            self._buy_validation(**required_fields)
        elif transaction_type is Transaction.Bonus:
            required_fields = {'units': units}
            self._bonus_validation(**required_fields)
        elif transaction_type is Transaction.Dividend:
            required_fields = {'bonus_amount': bonus_amount}
            self._dividend_validation(**required_fields)
        else:
            raise serializers.ValidationError(
                {'error': "transaction type error"})

    def _buy_validation(self, **kwargs):
        units = kwargs['units']
        cost_per_unit = kwargs['cost_per_unit']
        if units is None or cost_per_unit is None:
            raise serializers.ValidationError(
                {'error': "units and cost price are required"})

    def _bonus_validation(self, **kwargs):
        units = kwargs['units']
        if units is None or units < 1:
            raise serializers.ValidationError({'error': 'units is required'})

    def _dividend_validation(self, **kwargs):
        bonus_amount = kwargs['bonus_amount']
        if bonus_amount is None or bonus_amount < 1:
            raise serializers.ValidationError(
                {'error': 'bonus amount is required'})


class PortfolioSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        source='company', queryset=Company.objects.all(), write_only=True)
    transactions = TransactionSerializer(many=True)

    class Meta:
        model = Portfolio
        fields = ['id', 'company', 'company_id', 'transactions']
        read_only_fields = ['id']

    def to_representation(self, portfolio):
        data = super().to_representation(portfolio)
        ltp, previous_close_price, change = self.get_close_prices(portfolio)
        data['ltp'] = ltp
        data['previous_close_price'] = previous_close_price
        data['change'] = change
        return self.append_summary_to_portfolio(portfolio, data)

    def append_summary_to_portfolio(self, portfolio, data):
        incomming, selling, dividend = self.get_portfolio_summary(portfolio)
        data['total_units'] = incomming['total_units'] - selling['total_units']
        data['investment'] = incomming['total_cost']
        data['total_investment'] = incomming['total_cost'] + incomming['total_casba_charge'] + incomming['total_auction_charge'] + \
            incomming['total_dp_charge'] + incomming['total_broker_charge'] + \
            incomming['total_sebon_charge']
        data['total_sold_amount'] = selling['total_sell_amount']
        data['total_received_amount'] = selling['total_sell_amount'] - \
            (selling['total_dp_charge'] + selling['total_broker_charge'] +
             selling['total_sebon_charge'] + selling['total_tax'])
        data['total_dividend_amount'] = dividend['total_dividend']
        return self.append_profit_loss_to_portfolio(data)

    def append_profit_loss_to_portfolio(self, data):
        data['current_value'] = data['total_units'] * data['ltp']
        data['over_all_profit_loss'] = (data['current_value']) + (
            data['total_received_amount'] + data['total_dividend_amount']) - (data['total_investment'])
        previous_balance = (data['total_units'] * data['previous_close_price']) + (
            data['total_received_amount'] + data['total_dividend_amount']) - (data['total_investment'])
        data['todays_profit_loss'] = data['over_all_profit_loss'] - \
            previous_balance
        data['over_all_profit_loss_percentage'] = round((
            data['over_all_profit_loss']/(data['total_investment']))*100, 2)
        return data

    def get_close_prices(self, portfolio):
        try:
            data = LivePirce.objects.get(company=portfolio.company)
            change = 0.0
            if data is not None:
                if datetime.datetime.today().date() == data.last_updated_time.date():
                    ltp = data.last_traded_price
                    previous_close_price = data.previous_close
                    change = data.percentage_change
                else:
                    ltp, previous_close_price = self.retrieve_stock_price(
                        portfolio.company)
        except LivePirce.DoesNotExist:
            ltp, previous_close_price = self.retrieve_stock_price(
                portfolio.company)
        return ltp, previous_close_price, change

    def retrieve_stock_price(self, company):
        stock_datas = StockPrice.objects.filter(
            company=company).order_by('date')
        if len(stock_datas):
            stock_data = stock_datas[0]
            ltp = previous_close_price = stock_data.close_price
            return ltp, previous_close_price
        return None, None

    def get_portfolio_summary(self, portfolio):
        incomming_unit_transaction = [Transaction.IPO, Transaction.FPO,
                                      Transaction.Right, Transaction.Auction, Transaction.BUY, Transaction.Bonus]
        outgoing_unit_transaction = [Transaction.SELL]
        dividend_transaction = [Transaction.Dividend]

        incomming_data = portfolio.transactions.filter(transaction_type__in=incomming_unit_transaction).aggregate(total_units=Coalesce(Sum('units'), 0), total_cost=Coalesce(Sum(F('units') * F('cost_per_unit')), 0.0), total_casba_charge=Coalesce(Sum(
            'casba_charge'), 0.0), total_auction_charge=Coalesce(Sum('auction_charge'), 0.0), total_dp_charge=Coalesce(Sum('dp_charge'), 0.0), total_broker_charge=Coalesce(Sum('broker_charge'), 0.0), total_sebon_charge=Coalesce(Sum('sebon_charge'), 0.0))
        selling_data = portfolio.transactions.filter(transaction_type__in=outgoing_unit_transaction).aggregate(total_units=Coalesce(Sum('units'), 0), total_sell_amount=Coalesce(Sum(
            F('units') * F('cost_per_unit')), 0.0), total_dp_charge=Coalesce(Sum('dp_charge'), 0.0), total_broker_charge=Coalesce(Sum('broker_charge'), 0.0), total_sebon_charge=Coalesce(Sum('sebon_charge'), 0.0), total_tax=Coalesce(Sum('capital_gain_tax'), 0.0))
        dividend_data = portfolio.transactions.filter(transaction_type__in=dividend_transaction).aggregate(
            total_dividend=Coalesce(Sum('bonus_amount'), 0.0))
        return incomming_data, selling_data, dividend_data

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        transactions = validated_data.pop('transactions')
        portfolio = Portfolio.objects.create(**validated_data)
        for transaction in transactions:
            Transaction.objects.create(portfolio=portfolio, **transaction)
        return portfolio

    def update(self, instance, validated_data):
        instance.company = validated_data.get('company', instance.company)
        instance.save()

        transactions = validated_data.get('transactions')
        transaction_items_dict = dict((i.id, i)
                                      for i in instance.transactions.all())

        for transaction in transactions:
            transaction_id = transaction.get('id', None)

            if transaction_id:
                transaction_obj = transaction_items_dict.pop(transaction['id'])
                transaction_obj.units = transaction.get('units')
                transaction_obj.transaction_type = transaction.get(
                    'transaction_type', transaction_obj.transaction_type)
                transaction_obj.transaction_date = transaction.get(
                    'transaction_date', transaction_obj.transaction_date)
                transaction_obj.cost_per_unit = transaction.get(
                    'cost_per_unit')
                transaction_obj.bonus_amount = transaction.get('bonus_amount')
                transaction_obj.auction_charge = transaction.get(
                    'auction_charge')
                transaction_obj.casba_charge = transaction.get('casba_charge')
                transaction_obj.save()

            else:
                Transaction.objects.create(portfolio=instance, **transaction)

        if len(transaction_items_dict) > 0:
            for transaction in transaction_items_dict.values():
                transaction.delete()

        return instance
