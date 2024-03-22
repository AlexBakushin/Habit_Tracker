import requests
from celery import shared_task
from main.models import Habit
from django.conf import settings
import asyncio
from main.services import main


@shared_task
def send_message(tg_user_name, habit_id):
    """
    Задача для отправки уведомления о выполнении привычки в телеграм
    """
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = asyncio.run(main(tg_user_name))
    habit = Habit.objects.get(habit_id=habit_id)
    response = requests.get(
        url=f'https://api.telegram.org/bot{bot_token}/sendMessage',
        params={
            'chat_id': chat_id,
            'text': f'Привет!\n'
                    f'Пора выполнить свою привычку- {habit.action} {habit.place} в течение {habit.time_to_complete} секунд!'
        }
    )

# celery -A main worker -l info -P eventlet
# celery -A main beat -l info -S django
