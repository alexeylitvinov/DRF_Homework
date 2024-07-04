from rest_framework.serializers import ModelSerializer

from subscriptions.models import Subscription


class SubscriptionSerializer(ModelSerializer):
    """
    Сериализатор подписки.
    """
    class Meta:
        model = Subscription
        fields = '__all__'
