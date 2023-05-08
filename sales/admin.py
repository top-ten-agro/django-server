from django.contrib import admin
from .models import Order, Transaction, Restock


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'customer',
                    'created_by', 'approved', 'created_at',]
    list_display_links = ['__str__', 'customer']
    search_fields = ['customer__name', 'created_by__name']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass


@admin.register(Restock)
class RestockAdmin(admin.ModelAdmin):
    pass
