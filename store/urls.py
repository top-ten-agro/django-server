from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreViewset, StoreRoleViewset

router = DefaultRouter()
router.register(r'',  StoreViewset, basename="")

roleRouter = DefaultRouter()
roleRouter.register(r'/my-roles',  StoreRoleViewset, basename="my-roles")


urlpatterns = [
    path('', include(router.urls)),
]
