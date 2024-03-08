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
