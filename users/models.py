from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    """
    Модель пользователя
    """
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    first_name = models.CharField(max_length=50, **NULLABLE, verbose_name='Имя')
    last_name = models.CharField(max_length=50, **NULLABLE, verbose_name='Фамилия')
    phone = models.CharField(max_length=50, **NULLABLE, verbose_name='Телефон')
    city = models.CharField(max_length=100, **NULLABLE, verbose_name='Город')
    avatar = models.ImageField(upload_to='users/avatars', **NULLABLE, verbose_name='Аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email}'


from materials.models import Course


class Payment(models.Model):
    """
    Модель оплаты
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name='Пользователь')
    date = models.DateField(auto_now_add=True, verbose_name='Дата')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name='Оплаченный курс')
    payment_amount = models.PositiveIntegerField(default=1000, verbose_name='Сумма платежа')
    link = models.URLField(max_length=400, **NULLABLE, verbose_name='Ссылка на оплату')
    session_id = models.CharField(max_length=400, **NULLABLE, verbose_name='Сессия')

    def save(self, *args, **kwargs):
        if self.paid_course is not None:
            self.payment_amount = self.paid_course.price
        super(Payment, self).save(*args, **kwargs)

    class Meta:
        db_table = 'payments'
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'

    def __str__(self):
        return f'{self.user} {self.date} {self.paid_course} {self.payment_amount}'
