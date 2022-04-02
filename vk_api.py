from decouple import config
import requests

token = config('token', default='')

class VkApi:

    url = 'https://api.vk.com/method/'

    def __init__(self, token, version='5.131'):
        self.params = {
            'access_token': token,
            'v': version
        }




