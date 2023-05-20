from django import forms
from django.contrib import admin
from .models import Depot, DepotRole, Stock, Balance


@admin.register(Depot)
class DepotAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "created_at"]
    search_fields = ["name", "address"]
    ordering = ["-created_at"]


@admin.register(DepotRole)
class DepotRoleAdmin(admin.ModelAdmin):
    list_display = ["depot", "user", "role", "created_at"]
    search_fields = ["depot__name", "user__email"]
    list_filter = ["role"]
    ordering = ["-created_at"]


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ["product", "depot",  "quantity", "stock_updated"]


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ['customer', 'officer', 'depot', 'sales', 'cash_in']
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('customer',  'depot', 'officer', 'sales', 'cash_in'),
        }),
    )
