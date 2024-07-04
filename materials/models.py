from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    """
    Модель курса
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Пользователь')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='courses/preview', **NULLABLE, verbose_name='Превью')
    price = models.PositiveIntegerField(default=1000, verbose_name='Цена')

    class Meta:
        db_table = 'courses'
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return f'{self.title}'


class Lesson(models.Model):
    """
    Модель урока
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Пользователь')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='lessons/preview', **NULLABLE, verbose_name='Превью')
    video_url = models.URLField(max_length=200, **NULLABLE, verbose_name='Ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')

    class Meta:
        db_table = 'lessons'
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return f'{self.title} {self.course}'
