from django.contrib import admin
from .models import Order, Transaction, Restock


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'balance',
                    'created_by', 'approved', 'total', 'created_at',]
    list_display_links = ['__str__', 'balance']
    search_fields = ['balance__customer', 'created_by__name']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category',
                    'balance__customer', 'approved', 'cash_in', 'cash_out', 'created_by', 'created_at',]
    list_display_links = ['id', 'title']


@admin.register(Restock)
class RestockAdmin(admin.ModelAdmin):
    list_display = ['id', 'depot',
                    'created_by', 'approved', 'created_at',]
    list_display_links = ['id', 'depot']
