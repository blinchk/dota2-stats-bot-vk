import vk_api
import random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotMessageEvent
from vk_api.bot_longpoll import VkBotEventType
from vk_api.utils import get_random_id
import opendota2py

class Server:

    def __init__(self, api_token, group_id):
        self.vk = vk_api.VkApi(token=api_token)
        self.longpoll = VkBotLongPoll(self.vk, group_id, wait=25)
        self.vk_api = self.vk.get_api()

    def send_msg(self, send_id, msg):
        self.vk.method('messages.send', {'user_id': send_id, 'random_id': get_random_id(), 'message': msg})

    def test(self):
        self.send_msg(328862061, "Привет-привет!")

    def start(self):
        for event in self.longpoll.listen():
            print(event)
