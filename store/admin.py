from django.contrib import admin
from .models import Store, StoreRole, Stock, Balance


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    pass


@admin.register(StoreRole)
class StoreRoleAdmin(admin.ModelAdmin):
    pass


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    pass


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    pass
