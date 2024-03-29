import datetime

from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from main.models import Habit
from users.models import User


class MainTests(APITestCase):

    def test_create_habit_is_admin(self):
        """
        Тест на то, что админ может создать привычку
        """
        self.client = APIClient()
        self.user = User.objects.create(email="admin@sky.pro", tg_user_name='@admin_1', is_superuser=True, is_staff=True)
        self.client.force_authenticate(user=self.user)

        data = {
            'user': 1,
            'place': 'Место',
            'time': datetime.datetime.now(),
            'action': 'www',
            'is_pleasant_habit': False,
            'periodicity': 1,
            'remuneration': 'Вознаграждение',
            'time_to_complete': 10,
            'is_published': False
        }

        response = self.client.post(
            '/habit/create/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_create_habit_is_user(self):
        """
        Тест на то, что обычный пользователь может создать привычку
        """
        self.client = APIClient()
        self.user = User.objects.create(email="test@test.test", tg_user_name='@test_1', is_superuser=False, is_staff=False)
        self.client.force_authenticate(user=self.user)

        data = {
            'user': self.user.id,
            'place': 'Место',
            'time': datetime.datetime.now(),
            'action': 'www',
            'is_pleasant_habit': False,
            'periodicity': 1,
            'remuneration': 'Вознаграждение',
            'time_to_complete': 10,
            'is_published': False
        }

        response = self.client.post(
            '/habit/create/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_create_habit_is_moder(self):
        """
        Тест на то, что модератор не может создать привычку
        """
        group, created = Group.objects.get_or_create(name='moderator')
        self.client = APIClient()
        self.user = User.objects.create(email="moder@test.com", tg_user_name='@moder_1', is_superuser=False, is_staff=True)
        self.user.groups.add(group)
        self.client.force_authenticate(user=self.user)

        data = {
            'user': 1,
            'place': 'Место',
            'time': datetime.datetime.now(),
            'action': 'Действие',
            'is_pleasant_habit': False,
            'periodicity': 1,
            'remuneration': 'Вознаграждение',
            'time_to_complete': 10,
            'is_published': False
        }

        response = self.client.post(
            '/habit/create/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertEqual(
            response.json(),
            {'detail': 'У вас недостаточно прав для выполнения данного действия.'}

        )

    def test_list_habit_is_admin(self):
        """
        Тест на то что админ видит все привычки
        """
        self.client = APIClient()
        self.user = User.objects.create(email="admin_1@sky.pro", tg_user_name='@admin_2', is_superuser=True, is_staff=True)
        self.client.force_authenticate(user=self.user)

        test_user = User.objects.create(
            email="test@test.test",
            tg_user_name='@test_2',
            is_superuser=False,
            is_staff=False
        )

        Habit.objects.create(
            user=test_user,
            place='Место',
            time=datetime.datetime.now(),
            action='www',
            is_pleasant_habit=False,
            periodicity=1,
            remuneration='Вознаграждение',
            time_to_complete=10,
            is_published=False,
        )

        response = self.client.get(
            '/habit/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_list_habit_is_user(self):
        """
        Тест на то что обычный пользователь не видит чужие привычки, но видит свои
        """
        self.client = APIClient()
        self.user = User.objects.create(email="test_3@test.test", tg_user_name='@test_3', is_superuser=False, is_staff=False)
        self.client.force_authenticate(user=self.user)

        test_user = User.objects.create(
            email="test_2@test.test",
            tg_user_name='@test_4',
            is_superuser=False,
            is_staff=False
        )

        Habit.objects.create(
            user=test_user,
            place='Место',
            time=datetime.datetime.now(),
            action='Действие',
            is_pleasant_habit=False,
            periodicity=1,
            time_to_complete=10,
            is_published=False,
        )

        Habit.objects.create(
            user=self.user,
            place='Место',
            time=datetime.datetime.now(),
            action='www',
            is_pleasant_habit=False,
            periodicity=1,
            time_to_complete=10,
            is_published=False,
        )

        response = self.client.get(
            '/habit/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_list_habit_is_moder(self):
        """
        Тест на то что модератор видит все привычки
        """
        group, created = Group.objects.get_or_create(name='moderator')
        self.client = APIClient()
        self.user = User.objects.create(email="moder_1@test.com", tg_user_name='@moder_2', is_superuser=False, is_staff=True)
        self.user.groups.add(group)
        self.client.force_authenticate(user=self.user)

        test_user = User.objects.create(
            email="test_4@test.test",
            tg_user_name='@test_5',
            is_superuser=False,
            is_staff=False
        )

        Habit.objects.create(
            user=test_user,
            place='Место',
            time=datetime.datetime.now(),
            action='www',
            is_pleasant_habit=False,
            periodicity=1,
            remuneration='Вознаграждение',
            time_to_complete=10,
            is_published=False,
        )

        response = self.client.get(
            '/habit/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_list_public_habit_is_admin(self):
        """
        Тест на то что админ видит все привычки
        """
        self.client = APIClient()
        self.user = User.objects.create(email="admin_9@sky.pro", tg_user_name='@admin_9', is_superuser=True, is_staff=True)
        self.client.force_authenticate(user=self.user)

        test_user = User.objects.create(
            email="test9@test.test",
            tg_user_name='@test_9',
            is_superuser=False,
            is_staff=False
        )

        Habit.objects.create(
            user=test_user,
            place='Место',
            time=datetime.datetime.now(),
            action='www',
            is_pleasant_habit=False,
            periodicity=1,
            remuneration='Вознаграждение',
            time_to_complete=10,
            is_published=False,
        )

        response = self.client.get(
            '/habit/public/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_list_public_habit_is_user(self):
        """
        Тест на то что обычный пользователь не видит чужие привычки, но видит свои
        """
        self.client = APIClient()
        self.user = User.objects.create(email="test_0@test.test", tg_user_name='@test_0', is_superuser=False, is_staff=False)
        self.client.force_authenticate(user=self.user)

        test_user = User.objects.create(
            email="test_00@test.test",
            tg_user_name='@test_00',
            is_superuser=False,
            is_staff=False
        )

        Habit.objects.create(
            user=test_user,
            place='Место',
            time=datetime.datetime.now(),
            action='Действие',
            is_pleasant_habit=False,
            periodicity=1,
            time_to_complete=10,
            is_published=False,
        )

        Habit.objects.create(
            user=self.user,
            place='Место',
            time=datetime.datetime.now(),
            action='www',
            is_pleasant_habit=False,
            periodicity=1,
            time_to_complete=10,
            is_published=False,
        )

        response = self.client.get(
            '/habit/public/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_list_public_habit_is_moder(self):
        """
        Тест на то что модератор видит все привычки
        """
        group, created = Group.objects.get_or_create(name='moderator')
        self.client = APIClient()
        self.user = User.objects.create(email="moder_0@test.com", tg_user_name='@moder_0', is_superuser=False, is_staff=True)
        self.user.groups.add(group)
        self.client.force_authenticate(user=self.user)

        test_user = User.objects.create(
            email="test_000@test.test",
            tg_user_name='@test_000',
            is_superuser=False,
            is_staff=False
        )

        Habit.objects.create(
            user=test_user,
            place='Место',
            time=datetime.datetime.now(),
            action='www',
            is_pleasant_habit=False,
            periodicity=1,
            remuneration='Вознаграждение',
            time_to_complete=10,
            is_published=False,
        )

        response = self.client.get(
            '/habit/public/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update_habit_is_admin(self):
        """
        Тест на то что админ может обновлять любую привычку
        """
        self.client = APIClient()
        self.user = User.objects.create(email="admin_2@sky.pro", tg_user_name='@admin_3', is_superuser=True, is_staff=True)
        self.client.force_authenticate(user=self.user)

        Habit.objects.create(
            user=self.user,
            place='Место',
            time=datetime.datetime.now(),
            action='Действие',
            is_pleasant_habit=False,
            periodicity=1,
            remuneration='Вознаграждение',
            time_to_complete=10,
            is_published=False,
        )

        response = self.client.patch(
            '/habit/update/14/',
            {"action": "wwwwww"}
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

    def test_update_habit_is_user(self):
        """
        Тест на то что обычный пользователь может обновлять только свою привычку
        """
        self.client = APIClient()
        self.user = User.objects.create(email="test_5@test.test", tg_user_name='@test_6', is_superuser=False, is_staff=False)
        self.client.force_authenticate(user=self.user)

        Habit.objects.create(
            user=self.user,
            place='Место',
            time=datetime.datetime.now(),
            action='Действие',
            is_pleasant_habit=False,
            periodicity=1,
            remuneration='Вознаграждение',
            time_to_complete=10,
            is_published=False,
        )

        response = self.client.patch(
            '/habit/update/16/',
            {"action": "www"}
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

    def test_update_habit_is_moder(self):
        """
        Тест на то что модератор может обновлять любую привычку
        """
        group, created = Group.objects.get_or_create(name='moderator')
        self.client = APIClient()
        self.user = User.objects.create(email="moder@test.com", tg_user_name='@moder_3', is_superuser=False, is_staff=True)
        self.user.groups.add(group)
        self.client.force_authenticate(user=self.user)

        Habit.objects.create(
            user=self.user,
            place='Место',
            time=datetime.datetime.now(),
            action='Действие',
            is_pleasant_habit=False,
            periodicity=1,
            remuneration='Вознаграждение',
            time_to_complete=10,
            is_published=False,

        )

        response = self.client.patch(
            '/habit/update/15/',
            {"action": "wwe"}
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

    def test_delete_habit_is_admin(self):
        """
        Тест на то что админ может удалять любую привычку
        """
        self.client = APIClient()
        self.user = User.objects.create(email="admin@sky.pro", tg_user_name='@admin_4', is_superuser=True, is_staff=True)
        self.client.force_authenticate(user=self.user)

        Habit.objects.create(
            user=self.user,
            place='Место',
            time=datetime.datetime.now(),
            action='Действие',
            is_pleasant_habit=False,
            periodicity=1,
            remuneration='Вознаграждение',
            time_to_complete=10,
            is_published=False,
        )

        response = self.client.delete(
            '/habit/delete/3/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_delete_habit_is_user(self):
        """
        Тест на то что обычный пользователь не может удалять чужую привычку
        """
        self.client = APIClient()
        self.user = User.objects.create(email="test_6@test.test", tg_user_name='@test_7', is_superuser=False, is_staff=False)
        self.client.force_authenticate(user=self.user)

        test_user = User.objects.create(
            email="test_5@test.test",
            tg_user_name='@test_8',
            is_superuser=False,
            is_staff=False
        )

        Habit.objects.create(
            user=test_user,
            place='Место',
            time=datetime.datetime.now(),
            action='Действие',
            is_pleasant_habit=False,
            periodicity=1,
            remuneration='Вознаграждение',
            time_to_complete=10,
            is_published=False,
        )

        response = self.client.delete(
            '/habit/delete/5/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_delete_habit_is_moder(self):
        """
        Тест на то что модератор не может удалять любую привычку
        """
        group, created = Group.objects.get_or_create(name='moderator')
        self.client = APIClient()
        self.user = User.objects.create(email="moder_6@test.com", tg_user_name='@moder_4', is_superuser=False, is_staff=True)
        self.user.groups.add(group)
        self.client.force_authenticate(user=self.user)

        test_user = User.objects.create(
            email="test_7@test.test",
            tg_user_name='@test_9',
            is_superuser=False,
            is_staff=False
        )

        Habit.objects.create(
            user=test_user,
            place='Место',
            time=datetime.datetime.now(),
            action='Действие',
            is_pleasant_habit=False,
            periodicity=1,
            remuneration='Вознаграждение',
            time_to_complete=10,
            is_published=False,
        )

        response = self.client.delete(
            '/habit/delete/1/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
