from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "group_name", "price", "published", "created_at"]
    search_fields = ["name", "group_name"]
    list_filter = ['published']
    ordering = ['-created_at']
