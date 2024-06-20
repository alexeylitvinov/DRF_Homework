from django.urls import path

from users.apps import UsersConfig
from users.views import UserUpdateAPIView, UserListAPIView, PaymentListAPIView, PaymentCreateAPIView, UserCreateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('users/', UserListAPIView.as_view(), name='users'),
    path('payments/', PaymentListAPIView.as_view(), name='payments'),
    path('users/create/', UserCreateAPIView.as_view(), name='user_create'),
    path('payments/create/', PaymentCreateAPIView.as_view(), name='payment_create'),
    path('users/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
]
