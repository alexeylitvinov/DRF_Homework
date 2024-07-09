from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.paginations import CustomPagination
from materials.serializers import CourseSerializer, LessonSerializer
from subscriptions.models import Subscription
from users.permissions import IsModer, IsUser
from .tasks import email_sender


class CourseViewSet(ModelViewSet):
    """
    Работа с курсами.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        """
        Устанавливает права для действий.
        """
        if self.action in 'create':
            self.permission_classes = (~IsModer,)
        elif self.action in ['update']:
            self.permission_classes = (IsModer | IsUser,)
        elif self.action in 'destroy':
            self.permission_classes = (~IsModer | IsUser,)
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Устанавливает пользователя курсу.
        """
        course = serializer.save()
        course.user = self.request.user
        course.save()
        # add.delay()

    def perform_update(self, serializer):
        """
        Отправляет письмо всем подписчикам курса при обновлении курса
        """
        course = serializer.instance
        updated_subscriptions = Subscription.objects.filter(course=course)
        users_subscribed_to_course = [subscription.user for subscription in updated_subscriptions]
        subject = 'Тема письма'
        message = 'Текст письма'
        for user in users_subscribed_to_course:
            email_sender.delay(subject, message, user.email)
        return super().perform_update(serializer)


class LessonCreateAPIView(CreateAPIView):
    """
    Обрабатывает создание урока пользователя.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        """
        Устанавливает пользователя уроку.
        """
        lesson = serializer.save()
        lesson.user = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    """
    Возвращает список уроков пользователя.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    """
    Возвращает конкретный урок пользователя.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsUser,)


class LessonUpdateAPIView(UpdateAPIView):
    """
    Обрабатывает обновление урока пользователя.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsUser,)


class LessonDestroyAPIView(DestroyAPIView):
    """
    Обрабатывает удаление урока пользователя.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModer | IsUser,)
