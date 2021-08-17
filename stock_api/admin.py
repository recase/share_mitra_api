from django.contrib import admin
from .models import Sector, Company, StockPrice, StockUpdateTable, LivePirce

# Register your models here.
admin.site.register(Sector)
admin.site.register(Company)
admin.site.register(StockPrice)
admin.site.register(StockUpdateTable)
admin.site.register(LivePirce)
