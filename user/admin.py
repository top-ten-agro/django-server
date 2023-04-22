from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Employee
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.models import Group


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ['-date_joined']
    filter_horizontal = ('groups', 'user_permissions',)
    


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'designation', 'created_at']
    list_display_links = ['name']
    search_fields = ['name', 'designation', "user__email"]
    ordering = ['-created_at']