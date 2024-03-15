import json
from django.db import models
from django.conf import settings
from django_celery_beat.models import IntervalSchedule, PeriodicTask

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    """
    Модель привычки
    """
    habit_id = models.AutoField(primary_key=True, verbose_name='ID привычки')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)
    place = models.CharField(max_length=150, verbose_name='Место')
    time = models.DateTimeField(verbose_name='Время, когда необходимо выполнить')
    action = models.CharField(max_length=150, verbose_name='Действие')
    is_pleasant_habit = models.BooleanField(default=False, verbose_name='Приятная привычка?')
    related_habit = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Связанная привычка', **NULLABLE)
    periodicity = models.PositiveIntegerField(default=1, verbose_name='Периодичность')
    remuneration = models.CharField(max_length=150, verbose_name='Вознаграждение', **NULLABLE)
    time_to_complete = models.PositiveIntegerField(verbose_name='Время на выполнение')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано?')

    def create_periodic_tasks(self):
        """
        Создает периодическую задачу для каждой привычки
        поле time - время начала задачи, а поле periodicity - интервал
        """
        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=self.periodicity,
            period=IntervalSchedule.DAYS
        )

        kwargs = {
            "tg_user_name": self.user.tg_user_name,
            "habit_id": self.habit_id
        }

        task = PeriodicTask.objects.create(
            name=self.action,
            task='main.tasks.send_message',
            interval=schedule,
            start_time=self.time,
            kwargs=json.dumps(kwargs)
        )
        return task

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
