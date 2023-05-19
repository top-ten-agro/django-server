from django.contrib import admin
from .models import Order, Transaction, Restock


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['balance', 'created_by',
                    'approved', 'total', 'created_at',]
    list_display_links = ['balance']
    search_fields = ['created_by__name']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category',
                    'approved', 'cash_in', 'cash_out', 'created_by', 'created_at',]
    list_display_links = ['id', 'title']


@admin.register(Restock)
class RestockAdmin(admin.ModelAdmin):
    list_display = ['id', 'depot',
                    'created_by', 'approved', 'created_at',]
    list_display_links = ['id', 'depot']
