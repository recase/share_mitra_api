from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import LogoutView, UserInfoView, UserRegistrationView

app_name = "user"
urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('user-info/', UserInfoView.as_view(), name="user_info"),
]
