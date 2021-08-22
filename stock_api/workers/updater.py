from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import retrive_live_data, update_market_data, retrieve_live_market_status, retrieve_company_data, retrieve_todays_price

job_defaults = {
    'coalesce': False,
    'max_instances': 1
}
# scheduler = BackgroundScheduler(
#     job_defaults=job_defaults, timezone="Asia/Kathmandu")
scheduler = BackgroundScheduler()


def start():
    print('Now running...........')
    # scheduler.add_job(update_market_data, "cron", day_of_week="0-4",
    #                   hour=10, minute=55, id="sector_jod", replace_existing=True)
    # scheduler.add_job(retrieve_live_market_status, 'cron', day_of_week="0-4", hour='11-15',
    #                   second="*/30", timezone="Asia/Kathmandu", id="market_status_id", replace_existing=True)
    # scheduler.remove_job('market_status_id')
    # scheduler.remove_job('company_status_id')
    # scheduler.add_job(retrieve_live_market_status, 'interval',
    #                   seconds=20, id="market_status_id", replace_existing=True)
    # scheduler.add_job(retrive_live_data, 'cron', day_of_week='sun', hour='11-15',
    #                   second="*/30", id="live_market_data_id", replace_existing=True)
    # scheduler.add_job(retrieve_stock_price, 'interval',
    #                   seconds=25, id="stock_price_id", replace_existing=True)
    scheduler.add_job(retrieve_todays_price, 'interval',
                      seconds=25, id="today_price_id", replace_existing=True)

    # scheduler.remove_job('market_status_id')
    scheduler.start()
