from vk_api import VkApi
from random import randint
from vk_api.longpoll import VkLongPoll, VkEventType
import requests

VK_TOKEN = '0c091cd188169ceae08d98b44821f94bcb411e29a5bdc81017ad42b9ba98d165aaaf9eb8353c71be55eb5'
API_KEY = 'e769f0fe046f901526994f29b5bc6f8e'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'

vk_session = VkApi(token=VK_TOKEN)
longpoll = VkLongPoll(vk_session)


def get_current_temperature(town):
    params = {'q': town, 'appid': API_KEY, 'units': 'metric', 'mode': 'json'}
    r = requests.get(WEATHER_URL, params)
    data = r.json()
    return data['main']['temp']


def send_msg(user_id, text):
    vk_session.method('messages.send', {'user_id': user_id, 'message': text,
                                        'random_id': randint(1e16, 1e18)})


def get_user_name(user_id):
    r = vk_session.method('users.get', {'v': '5.71', 'access_token': VK_TOKEN, 'user_ids': user_id})
    return r[0]['first_name']


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:  # Получили новое сообщение
        request = event.text.lower()
        if request == 'привет':
            name = get_user_name(event.user_id)
            send_msg(event.user_id, f'Привет, {name}!')

        elif request == 'пока':
            send_msg(event.user_id, 'Пока!')

        else:
            send_msg(event.user_id, "Пока такой текст не очень понимаю, сори) Или пошел накуй фраер")