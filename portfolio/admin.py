from django.contrib import admin
from .models import Transaction, Portfolio, Alert, WatchList, TargetStopLoss

# Register your models here.

admin.site.register(Portfolio)
admin.site.register(Transaction)
admin.site.register(Alert)
admin.site.register(WatchList)
admin.site.register(TargetStopLoss)
