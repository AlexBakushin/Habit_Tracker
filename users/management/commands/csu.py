from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """
    Команда для создания администратора
    """

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='admin@sky.pro',
            first_name='Admin',
            last_name='SkyPro',
            is_staff=True,
            is_superuser=True
        )
        user.set_password('2202')
        user.save()
