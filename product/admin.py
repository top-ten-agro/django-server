from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "pack_size", "price", "published", "created_at"]
    search_fields = ["name", "pack_size"]
    list_filter = ['published']
    ordering = ['-created_at']
