from decouple import config
import requests
from pprint import pprint
from datetime import date
from datetime import datetime

TOKEN = config('token', default='')
MY_TOKEN = config('my_token', default='')
USER_ID = 'gromovaleila'

class VkApi:

    url = 'https://api.vk.com/method/'

    def __init__(self, version='5.131'):
        self.params = {
            'access_token': TOKEN,
            'v': version
        }

    def calculate_age(self, bdate):
        born = datetime.strptime(bdate, '%d.%m.%Y')
        age = date.today().year - born.year - (
                    (date.today().month, date.today().day) < (date.today().month, date.today().day))
        return age

    def get_user_info(self, user_id):
        user_info = {}
        user_info_url = self.url + 'users.get'
        params = {
            'access_token': TOKEN,
            'user_ids': user_id,
            'fields': ['bdate', 'sex', 'city'],
            'name_case': 'nom',
            'v': '5.131'
        }
        res = requests.get(user_info_url, params).json()                 #надо разобрать почему не выдает все fields
        user_info['sex'] = res['response'][0]['sex']
        user_info['city'] = res['response'][0]['city']['id']
        user_info['age'] = calculate_age(res['response'][0]['bdate'])
        return user_info

    def get_search_params(self, user_info):
        params = {}
        params['sort'] = '0'
        params['count'] = 1000
        params['city'] = user_info['city']
        if user_info['sex'] == 1:
            params['sex'] = 2
        else:
            params['sex'] = 1
        params['age_from'] = user_info['age'] - 3
        params['age_to'] = user_info['age'] + 3
        params['status'] = [1, 6]
        return params

    def search_people(self, params):
        search_people_url = self.url + 'users.search'
        params = params
        res = requests.get(search_people_url, params)
        return res.json()

params = {
    'age_from': 22,
     'age_to': 28,
     'city': 175,
     'count': 1000,
     'sex': 2,
     'sort': '0',
     'status': [1, 6]
}

vkapi = VkApi()
# user_info = vkuser.get_user_info(USER_ID)
# params = vkapi.get_search_params(USER_INFO)
peoples = vkapi.search_people(params)
pprint(peoples)












