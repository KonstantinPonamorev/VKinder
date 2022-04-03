from pprint import pprint
from datetime import date
from datetime import datetime
import vk_api






class VkApi:

    def __init__(self, login, password, version='5.131'):
        self.vk_session = vk_api.VkApi(login, password)
        self.vk_session.auth()
        self.vk = self.vk_session.get_api()

    def calculate_age(self, bdate):
        born = datetime.strptime(bdate, '%d.%m.%Y')
        age = date.today().year - born.year - (
                    (date.today().month, date.today().day) < (date.today().month, date.today().day))
        return age

    def get_user_info(self, user_id):
        res = self.vk.users.get(user_ids=user_id, fields='bdate, sex, city')[0]
        return res

    def convert_user_info(self, info):
        user_info = {}
        user_info['sex'] = info['sex']
        user_info['city'] = info['city']['id']
        user_info['age'] = self.calculate_age(info['bdate'])
        return user_info

    def get_search_params(self, user_info):
        params = {}
        params['sort'] = '0'
        params['count'] = 20
        params['city'] = user_info['city']
        if user_info['sex'] == 1:
            params['sex'] = 2
        else:
            params['sex'] = 1
        params['age_from'] = user_info['age'] - 3
        params['age_to'] = user_info['age'] + 3
        params['status'] = 6
        return params

    def search_people(self, params):
        matches = []
        res = self.vk.users.search(age_from=params['age_from'], age_to=params['age_to'], city=params['city'],
                                   count=params['count'], sex=params['sex'], sort=params['sort'],
                                   status=params['status'])
        for item in res['items']:
            matches.append(item['id'])
        return matches




vkapi = VkApi(LOGIN, PASSWORD)
user_info = vkapi.get_user_info(USER_ID)
convert_user_info = vkapi.convert_user_info(user_info)
params = vkapi.get_search_params(convert_user_info)
peoples = vkapi.search_people(params)
pprint(peoples)






