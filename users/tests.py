from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from users.models import User


class UserTestCase(APITestCase):
    def test_create_user(self):
        """
        Тест на создание пользователя
        """
        self.client = APIClient()

        data = {
            'email': 'test665443@test.test',
            'password': '12345',
            'tg_user_name': '@test23988'
        }

        response = self.client.post('/users/user/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_user(self):
        """
        Тест на получение списка пользователей
        """
        self.client = APIClient()
        self.user = User.objects.create(email="test_783@test.test", tg_user_name='@test_1440', is_superuser=False, is_staff=False)
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/users/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user(self):
        """
        Тест на получение пользователя
        """
        self.client = APIClient()
        self.user = User.objects.create(email="test_311@test.test", tg_user_name='@test_03010', is_superuser=False, is_staff=False)
        self.client.force_authenticate(user=self.user)

        User.objects.create(
            email="test_2343@test.test",
            is_superuser=False,
            is_staff=False,
            tg_user_name='@test656'
        )

        response = self.client.get('/users/user/26/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        """
        Тест на обновление пользователя
        """
        self.client = APIClient()
        self.user = User.objects.create(email="test_333@test.test", tg_user_name='@test_0333010', is_superuser=False, is_staff=False)
        self.client.force_authenticate(user=self.user)

        data = {
            'email': 'test12313@test.test',
            'password': '12345',
            'tg_user_name': '@test_0010'
        }

        response = self.client.put('/users/user/29/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        """
        Тест на удаление пользователя
        """
        self.client = APIClient()
        self.user = User.objects.create(email="test_54645632@test.test", tg_user_name='@tes4443010', is_superuser=False, is_staff=False)
        self.client.force_authenticate(user=self.user)

        response = self.client.delete('/users/user/25/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
