
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/stores/', include('store.urls')),
    path('api/products/', include('product.urls')),
    path('api/auth/', include('user.urls')),
]
