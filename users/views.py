from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import UpdateAPIView, ListAPIView, CreateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from materials.models import Course
from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer, UserUpdateSerializer
from users.services import create_price, create_stripe_session


class UserCreateAPIView(CreateAPIView):
    """
    Регистрация пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """
        Устанавливает пользователя активным
        """
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    """
    Список пользователей
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    """
    Обновление пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    """
    Просмотр пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDestroyAPIView(DestroyAPIView):
    """
    Удаление пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentCreateAPIView(CreateAPIView):
    """
    Создание оплаты
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        """
        Сохраняет оплату пользователя для конкретного курса формируя ссылку на оплату
        """
        course_id = self.kwargs.get('pk')
        course = get_object_or_404(Course, id=course_id)
        price = course.price
        amount = create_price(price)
        payment_link, session_id = create_stripe_session(amount)
        serializer.save(
            user=self.request.user,
            paid_course_id=course_id,
            link=payment_link,
            session_id=session_id
        )


class PaymentListAPIView(ListAPIView):
    """
    Список оплат
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_amount')
    ordering_fields = ('date',)
