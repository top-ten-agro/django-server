from django.urls import path, include
from .views import UserRegistrationView, UserUpdateView

urlpatterns = [
    path('', include('rest_framework.urls')),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('profile/', UserUpdateView.as_view(), name='user-profile'),
]
