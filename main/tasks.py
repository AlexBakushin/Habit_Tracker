import requests
from celery import shared_task
from main.models import Habit


@shared_task
def send_message(tg_user_name, habit_id):
    bot_token = "6886757391:AAEMY5Lt2_JlIEhNkAFs8b2P1ujWPDg5oh8"
    chats_info = requests.get(
            url=f'https://api.telegram.org/bot{bot_token}/getUpdates',
        )
    for item in chats_info['result']:
        username = item['message']['chat']['username']
        if username == tg_user_name[1:]:
            chat_id = item['message']['chat']['id']
            habit = Habit.objects.get(habit_id=habit_id)
            response = requests.get(
                url=f'https://api.telegram.org/bot{bot_token}/sendMessage',
                params={
                    'chat_id': chat_id,
                    'text': f'''Привет!
                                {habit.time} в {habit.place} необходимо выполнять {habit.action}
                                в течение {habit.duration} !'''
                }
            )
            print(response.json())


# celery -A main worker -l info -P eventlet
# celery -A main beat -l info -S django
