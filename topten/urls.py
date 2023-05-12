
from django.contrib import admin
from django.urls import path, include


admin.site.site_header = 'Top Ten Agro Ltd. administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/auth/', include('user.urls')),
]
