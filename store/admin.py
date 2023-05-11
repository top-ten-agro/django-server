from django.contrib import admin
from .models import Store, StoreRole, Stock, Balance


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "created_at"]
    search_fields = ["name", "address"]
    ordering = ["-created_at"]


@admin.register(StoreRole)
class StoreRoleAdmin(admin.ModelAdmin):
    list_display = ["store", "user", "role", "created_at"]
    search_fields = ["store__name", "user__email"]
    list_filter = ["role"]
    ordering = ["-created_at"]


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ["product", "store",  "quantity", "stock_updated"]


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ['customer', 'store', 'revenue', 'cash_in']
