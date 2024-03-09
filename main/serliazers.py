from django.core.exceptions import ValidationError
from rest_framework import serializers
from main.models import Habit
from main.validators import TimeToCompleteValidator, PeriodicityValidator, RelatedOrRemunerationValidator, \
    RelatedIsPleasantValidator, OrRelatedOrRemunerationValidator


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор привычек
    """

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            OrRelatedOrRemunerationValidator(field='__all__'),
            TimeToCompleteValidator(field='time_to_complete'),
            RelatedIsPleasantValidator(field='__all__'),
            PeriodicityValidator(field='periodicity'),
            RelatedOrRemunerationValidator(field='__all__')
        ]

    def create(self, validated_data):
        """
        Создает привычку
        :param validated_data:
        :return:
        """
        user = self.context['request'].user  # получаем авторизированного пользователя
        habit = Habit(**validated_data)
        habit.user = user  # устанавливаем пользователя
        habit.save()  # сохраняем объект
        habit.create_periodic_tasks()  # создаем периодическую задачу
        return habit
