import requests
from ..utils import sector_service, live_market_services
import json
import os

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
           "Accept-Encoding": "*", "Connection": "keep-alive"}


def update_market_data():
    retrieve_sector_data()
    retrieve_company_data()


def retrieve_sector_data():
    sectors_url = os.environ['SECTOR_URL']

    try:
        response = requests.get(sectors_url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        sector_service.updateSectors(data['sectors'])

    except Exception as e:
        return None


def retrieve_company_data():
    company_list_url = os.environ['COMPANY_LIST_URL']

    try:
        response = requests.get(company_list_url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        live_market_services.update_company_data(data)
    except Exception as e:
        print('error')
        print(e)


def retrive_live_data():
    live_market_url = os.environ['LIVE_MARKET_URL']

    try:
        print('here it go!!!')
        response = requests.get(live_market_url, headers=HEADERS)
        print(response)
        response.raise_for_status()
        data = response.json()
        live_market_services.live_market_update(data)
    except Exception as e:
        print('error!!!')
        print(e)


def retrieve_live_market_status():
    market_status_url = os.environ['MARKET_STATUS_URL']

    try:
        response = requests.get(market_status_url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        print(data)
        live_market_services.update_live_market(data)
    except Exception as e:
        print('error!!!')
        print(e)


# def retrieve_stock_price():
#     stock_price_url = 'https://newweb.nepalstock.com/api/nots/securityDailyTradeStat/58'

#     try:
#         print('im going')
#         response = requests.get(stock_price_url, headers=HEADERS)
#         response.raise_for_status()
#         data = response.json()
#         live_market_services.update_stock_price(data)
#     except Exception as e:
#         print('error')
#         print(e)


def retrieve_todays_price():
    todays_price_url = os.environ['TODAYS_PRICE_URL']
    data = json.dumps({'id': os.environ['API_ID']})
    header = {"content-type": "application/json",
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding": "*", "Connection": "keep-alive"}

    try:
        print('lets go')
        response = requests.post(todays_price_url, data=data, headers=header)
        response.raise_for_status()
        data = response.json()
        live_market_services.update_stock_price(data['content'])

    except Exception as e:
        print('errer')
        print(e)
