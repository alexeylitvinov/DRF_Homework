# Generated by Django 4.2.9 on 2024-07-09 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_payment_session_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'get_latest_by': 'last_login', 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]