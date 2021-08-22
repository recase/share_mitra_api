from django.db.models import fields
from ..models import LivePirce, StockUpdateTable, Sector, Company, StockPrice
import datetime


def update_live_market(data):
    setting, created_flag = StockUpdateTable.objects.get_or_create(
        setting="market_status")
    if data['isOpen'] == 'OPEN':
        setting.value = 'TRUE'
    else:
        setting.value = 'FALSE'
    setting.save()


def update_company_data(data):
    sectors = list(Sector.objects.values('id', 'name'))
    companies = list(Company.objects.values('symbol'))
    companies_symbol = list(company.get('symbol') for company in companies)
    company_list = []
    for company in data:
        if company['status'] == 'A' and company['symbol'] not in companies_symbol:
            sector_list = list(
                filter(lambda com: com['name'] == company['sectorName'], sectors))
            if len(sector_list) > 0:
                sector_id = sector_list[0]['id']
                com = Company(name=company['companyName'],
                              symbol=company['symbol'],
                              instrument_type=company['instrumentType'],
                              sector_id=sector_id
                              )
                company_list.append(com)

    try:
        Company.objects.bulk_create(
            company_list, batch_size=100, ignore_conflicts=True)
    except Exception as e:
        print('error')
        print(e)


def live_market_update(data):
    companies_list = list(Company.objects.values('id', 'symbol'))
    market_data = []
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    for live_market in data:
        companies = list(
            filter(lambda com: com['symbol'] == live_market['symbol'], companies_list))

        if len(companies) > 0:
            company_id = companies[0]['id']
            last_updated_date = datetime.datetime.strptime(
                live_market['lastUpdatedDateTime'], date_format).replace(tzinfo=datetime.timezone.utc)
            market = LivePirce(company_id=company_id,
                               open_price=live_market['openPrice'],
                               high_price=live_market['highPrice'],
                               low_price=live_market['lowPrice'],
                               previous_close=live_market['previousClose'],
                               last_traded_price=live_market['lastTradedPrice'],
                               total_volume=live_market['totalTradeQuantity'],
                               last_traded_volume=live_market['lastTradedVolume'],
                               percentage_change=live_market['percentageChange'],
                               last_updated_time=last_updated_date)
            market_data.append(market)

    try:
        LivePirce.objects.bulk_create(market_data,
                                      batch_size=100,
                                      ignore_conflicts=True)
        LivePirce.objects.bulk_update(market_data,
                                      batch_size=100,
                                      fields=[
                                          'high_price',
                                          'low_price',
                                          'previous_close',
                                          'open_price',
                                          'last_traded_price',
                                          'total_volume',
                                          'percentage_change',
                                          'last_updated_time'
                                      ])

        setting, created_flag = StockUpdateTable.objects.get_or_create(
            setting="live_market_updated_at")
        setting.value = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %z")
        setting.save()
    except Exception as e:
        print('error')
        print(e)


def update_stock_price(stock_price):
    companies_list = list(Company.objects.values('id', 'symbol'))
    stock_price_data = []
    date_format = "%Y-%m-%dT%H:%M:%S.%f"

    for stock in stock_price:
        companies = list(
            filter(lambda com: com['symbol'] == stock['symbol'], companies_list))
        if len(companies) > 0:
            company_id = companies[0]['id']
            date = datetime.datetime.strptime(
                stock['lastUpdatedTime'], date_format).date()
            stock_data = StockPrice(company_id=company_id, open_price=stock['openPrice'],
                                    high_price=stock['highPrice'],
                                    low_price=stock['lowPrice'],
                                    previous_close_price=stock['previousDayClosePrice'],
                                    close_price=stock['closePrice'],
                                    percentage_change=round(calculate_percentage(
                                        stock['previousDayClosePrice'], stock['closePrice'], stock['openPrice']), 4),
                                    total_volume=stock['totalTradedQuantity'],
                                    date=date)
            stock_price_data.append(stock_data)

    try:
        StockPrice.objects.bulk_create(
            stock_price_data, batch_size=100, ignore_conflicts=True)
        # StockPrice.objects.bulk_update(stock_price_data,
        #                                fields=['high_price',
        #                                        'low_price',
        #                                        'previous_close_price',
        #                                        'close_price',
        #                                        'percentage_change',
        #                                        'total_volume'
        #                                        ],
        #                                batch_size=100)
        updated_date = max((stock.date for stock in stock_price_data))
        setting, created_flag = StockUpdateTable.objects.get_or_create(
            setting="stock_table_updated_at")
        setting.value = updated_date
        setting.save()
    except Exception as e:
        print('error')
        print(e)


def calculate_percentage(prevoius_closeing_price, closeing_price, opening_price):
    if prevoius_closeing_price is not None:
        return ((closeing_price - prevoius_closeing_price)/prevoius_closeing_price)*100
    else:
        return ((closeing_price - opening_price)/opening_price)*100
