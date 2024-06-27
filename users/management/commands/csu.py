from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        admin_user = User.objects.create(
            email='admin@admin.com',
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        admin_user.set_password('admin')
        admin_user.save()
