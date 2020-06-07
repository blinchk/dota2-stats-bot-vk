import vk_api.vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
import opendota2py

class Server:

    def __init(self, api_token, group_id):
        self.vk = vk_api.VkApi(token = api_token)
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()

    def send_msg(self, send_id, msg):
        self.vk_api.messages.send(peer_id=send_id, message=msg)

    def test(self):
        self.send_msg(328862061, "Салам алейкум!")