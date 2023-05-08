from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product.views import ProductViewset
from sales.views import OrderViewset, TransactionViewset, RestockViewset
from store.views import StoreViewset, StoreRoleViewset

router = DefaultRouter()
router.register(r"products", ProductViewset, basename='products')
router.register(r"stores", StoreViewset, basename='stores')
router.register(r"roles", StoreRoleViewset, basename='roles')
router.register(r'orders',  OrderViewset, basename="orders")
router.register(r'transactions',  TransactionViewset, basename="transactions")
router.register(r'restocks',  RestockViewset, basename="restocks")

urlpatterns = [
    path('', include(router.urls)),
]
