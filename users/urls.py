from django.urls import path

from users.apps import UsersConfig
from users.views import UserUpdateAPIView, UserListAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('', UserListAPIView.as_view(), name='users'),
    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
]
