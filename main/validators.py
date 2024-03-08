import re
from rest_framework.serializers import ValidationError


class OrRelatedOrRemunerationValidator:
    """
    Исключает одновременный выбор связанной привычки и указания вознаграждения.
    """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if value.get('related_habit') is not None and value.get('remuneration') is not None:
            raise ValidationError('Одновременный выбор связанной привычки и вознаграждения.')


class TimeToCompleteValidator:
    """
    Время на выполнение должно быть меньше 120 секунд.
    """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if self.field in value and value[self.field] > 120:
            raise ValidationError('Время на выполнение должно быть меньше 120 секунд.')


class RelatedIsPleasantValidator:
    """
    В связанные привычки могут попадать только привычки с признаком приятной привычки.
    """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if value.get('related_habit') is not None and not value.get('related_habit').is_pleasant_habit:
            raise ValidationError('В связанные привычки могут попадать только привычки с признаком приятной.')


class RelatedOrRemunerationValidator:
    """
    У приятной привычки не может быть вознаграждения или связанной привычки.
    """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if value.get('is_pleasant_habit') and (value.get('remuneration') or value.get('related_habit')):
            raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')


class PeriodicityValidator:
    """
    Периодичность должна быть не больше 7.
    """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if self.field in value and value[self.field] > 7:
            raise ValidationError('Периодичность должна быть не больше 7 дней.')
