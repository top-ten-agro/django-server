from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'designation', 'created_at']
    list_display_links = ['user']
    search_fields = ['name', 'designation', "user__email"]
    ordering = ['-created_at']
