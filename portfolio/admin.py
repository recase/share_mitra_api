from django.contrib import admin
from .models import Transaction, Portfolio

# Register your models here.

admin.site.register(Portfolio)
admin.site.register(Transaction)
