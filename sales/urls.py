from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewset, TransactionViewset, RestockViewset

router = DefaultRouter()
router.register(r'orders',  OrderViewset, basename="orders")
router.register(r'transactions',  TransactionViewset, basename="transactions")
router.register(r'restocks',  RestockViewset, basename="restocks")


urlpatterns = [
    path('', include(router.urls)),
]
