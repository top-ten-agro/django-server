from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreViewset

router = DefaultRouter()
router.register(r'',  StoreViewset, basename="")


urlpatterns = [
    path('', include(router.urls)),
]
