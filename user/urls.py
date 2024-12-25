from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserViewSet

app_name = "user"

urlpatterns = [
    path("auth-token/", obtain_auth_token, name="auth-token"),
    path("register/", UserViewSet.as_view({"post": "create"}), name="user-register"),
    path("users/", UserViewSet.as_view({"get": "list"}), name="user-list"),
    path("users/<int:pk>/", UserViewSet.as_view({"get": "retrieve"}), name="user-detail"),
]