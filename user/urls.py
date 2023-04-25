from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserRegistrationView, UserUpdateView, CustomTokenObtainPairView


urlpatterns = [
    path('', include('rest_framework.urls')),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('profile/', UserUpdateView.as_view(), name='user-profile'),
]
