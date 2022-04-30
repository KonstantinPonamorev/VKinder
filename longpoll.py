import vk_api
from vk_api.longpoll import VkLongPoll
from random import randrange



class VkBot:
    '''Класс для longpoll'''

    def __init__(self, token):
        '''Определение класса, подключение к API и longpoll'''

        self.vk = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(self.vk)

    def write_msg(self, user_id, message):
        '''Отправка сообщения'''

        self.vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})

    def send_photo(self, user_id, url):
        '''Отправка фото'''

        self.vk.method('messages.send', {'user_id': user_id, 'attachment': url, 'random_id': randrange(10 ** 7)})

