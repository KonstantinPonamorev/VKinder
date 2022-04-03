import vk_api
from vk_api.longpoll import VkLongPoll
from random import randrange



class VkBot:

    def __init__(self, token):
        self.vk = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(self.vk)

    def write_msg(self, user_id, message):
        self.vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})


