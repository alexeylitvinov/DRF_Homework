from rest_framework.fields import SerializerMethodField, URLField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson
from materials.validators import ValidateLink
from subscriptions.models import Subscription


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [ValidateLink(field='video_url')]


class CourseSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    is_subscribed = SerializerMethodField()

    def get_lesson_count(self, obj):
        """
        Возвращает количество уроков в заданном объекте курса.
        """
        return obj.lesson_set.count()

    def get_is_subscribed(self, obj):
        """
        Получает статус подписки текущего пользователя на определенный курс.
        Возвращает True, если пользователь подписан на курс, в противном случае False.
        """
        user = self.context['request'].user
        if Subscription.objects.filter(user=user, course=obj).exists():
            return True
        return False

    class Meta:
        model = Course
        fields = '__all__'
