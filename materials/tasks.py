from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from users.models import User


@shared_task
def email_sender(subject, message, user):
    """Функция отправки писем клиентам"""
    send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[user],
        fail_silently=False
    )
    print(f'{user} - письмо отправлено')


@shared_task
def block_users():
    """Функция блокировки пользователей"""
    one_month_ago = timezone.now() - timezone.timedelta(days=30)
    # Выбираем пользователей, у которых last_login был больше месяца назад
    users_to_update = User.objects.filter(last_login__lt=one_month_ago)
    print(users_to_update)
    # Обновляем значение is_active для выбранных пользователей
    users_to_update.update(is_active=False)
    print('Пользователи были заблокированы')
