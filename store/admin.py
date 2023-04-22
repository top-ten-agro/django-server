from django.contrib import admin
from .models import Store, StoreRole, Stock, Balance


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "created_at"]
    search_fields = ["name", "address"]
    ordering = ["-created_at"]


@admin.register(StoreRole)
class StoreRoleAdmin(admin.ModelAdmin):
    list_display = ["store", "employee", "role", "created_at"]
    list_display_links = ["store", "employee"]
    search_fields = ["store__name", "employee__name"]
    list_filter = ["role"]
    ordering = ["-created_at"]


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    pass


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    pass
