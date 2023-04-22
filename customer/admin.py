from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'address', 'created_at']
    ordering = ['-created_at']
    fields = ["name", "phone", "address"]
