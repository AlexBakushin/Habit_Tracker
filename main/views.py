from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Habit
from main.serliazers import HabitSerializer
from main.permissions import IsOwnerOrModerator, IsOwner, IsModer
from main.paginator import MainPaginator
from main.tasks import send_message
from users.models import User


class HabitCreateAPIView(generics.CreateAPIView):
    """
    Создание модели привычки
    """
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        """
        При создании, user - пользователь
        """
        new_habit = serializer.save()
        new_habit.user = self.request.user
        new_habit.save()


class HabitListAPIView(generics.ListAPIView):
    """
    Список привычек
    """
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    pagination_class = MainPaginator

    def get_queryset(self):
        """
        Передает queryset привычек, где user - пользователь и все публичные, кроме админа и модератора
        """
        if self.request.user.is_staff:
            return Habit.objects.all()

        published_habits = Habit.objects.filter(is_published=True)
        user_habits = Habit.objects.filter(user=self.request.user)
        combined_habits = published_habits.union(user_habits)
        return combined_habits


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """
    Выводит модель выбранной привычки, где user - пользователь и все публичные, кроме админа и модератора
    """
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Habit.objects.all()

        published_habits = Habit.objects.filter(is_published=True)
        user_habits = Habit.objects.filter(user=self.request.user)
        combined_habits = published_habits | user_habits
        return combined_habits


class HabitUpdateAPIView(generics.UpdateAPIView):
    """
    Обновление выбранной привычки, только те, где user - пользователь, кроме админа и модератора
    """
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """
    Удаление выбранной привычки, только те, где user - пользователь, модератор не может
    """
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, ~IsModer & IsOwner]


class MessageSendAPIView(APIView):
    """
    Отправка сообщения в чат
    """

    def post(self, request):
        user = get_object_or_404(User, pk=request.data.get('user'))
        send_message.delay(user.email)
        return Response({'success': 'Сообщение отправлено'}, status=200)
