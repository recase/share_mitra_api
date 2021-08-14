from ..models import StockPrice


def retrieve_stock_price_list(date):
    return StockPrice.custom_objects.filter(date=date)


def retrieve_stock_price_history(company_id):
    return StockPrice.custom_objects.filter(company_id=company_id).order_by('date')
