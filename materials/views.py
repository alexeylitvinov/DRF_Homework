from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.paginations import CustomPagination
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsUser


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
