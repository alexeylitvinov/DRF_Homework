from django.urls import path

from subscriptions.apps import SubscriptionsConfig
from subscriptions.views import ManageSubscriptionAPIView

app_name = SubscriptionsConfig.name

urlpatterns = [
    path('subscriptions/', ManageSubscriptionAPIView.as_view(), name='manage_subscription'),
]
