from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    UserUpdateAPIView,
    UserListAPIView,
    PaymentListAPIView,
    PaymentCreateAPIView,
    UserCreateAPIView,
    UserRetrieveAPIView,
    UserDestroyAPIView
)

app_name = UsersConfig.name

urlpatterns = [
    path('users/', UserListAPIView.as_view(), name='users'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('payments/', PaymentListAPIView.as_view(), name='payments'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('payments/<int:pk>/', PaymentCreateAPIView.as_view(), name='payment_create'),
    path('users/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('users/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', UserDestroyAPIView.as_view(), name='user_delete'),
]
