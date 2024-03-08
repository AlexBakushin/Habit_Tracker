from django.db import models
from django.conf import settings

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    """
    Модель привычки
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    place = models.CharField(max_length=150, verbose_name='Место')
    time = models.TimeField(verbose_name='Время, когда необходимо выполнить')
    action = models.CharField(max_length=150, verbose_name='Действие')
    is_pleasant_habit = models.BooleanField(default=False, verbose_name='Приятная привычка?')
    related_habit = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Связанная привычка', **NULLABLE)
    periodicity = models.PositiveIntegerField(default=1, verbose_name='Периодичность')
    remuneration = models.CharField(max_length=150, verbose_name='Вознаграждение', **NULLABLE)
    time_to_complete = models.PositiveIntegerField(verbose_name='Время на выполнение')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано?')

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
