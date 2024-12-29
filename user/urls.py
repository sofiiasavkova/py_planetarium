from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import UserViewSet

app_name = "user"

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("register/", UserViewSet.as_view({"post": "create"}), name="user-register"),
    path("users/", UserViewSet.as_view({"get": "list"}), name="user-list"),
    path("users/<int:pk>/", UserViewSet.as_view({"get": "retrieve"}), name="user-detail"),
]