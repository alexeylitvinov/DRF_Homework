from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course
from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionSerializer


class ManageSubscriptionAPIView(APIView):
    """
    Класс для обработки подписки пользователя на курс.
    """
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает подписку пользователя на основе предоставленного идентификатора курса.
        Удаляет подписку, если она уже существует, в противном случае добавляет новую подписку.
        Возвращает сообщение, указывающее статус операции с подпиской.
        """
        user = self.request.user
        course_id = self.request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            serializer = self.serializer_class(data={'user': user.id, 'course': course_item.id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            message = 'Подписка добавлена'
        return Response({'message': message})
