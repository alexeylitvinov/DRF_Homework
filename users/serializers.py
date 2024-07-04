from rest_framework.serializers import ModelSerializer

from users.models import User, Payment


class PaymentSerializer(ModelSerializer):
    """
    Сериализатор для модели Payment
    """
    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(ModelSerializer):
    """
    Сериализатор для модели User
    """
    payments = PaymentSerializer(source='payment_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class UserUpdateSerializer(ModelSerializer):
    """
    Сериализатор для обновления данных пользователя
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'city', 'avatar']
