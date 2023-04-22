from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "group_name", "price",
                    "published", "archived", "created_at"]
    search_fields = ["name", "group_name"]
    ordering = ['-created_at']
