from datetime import date
from datetime import datetime
import vk_api
import heapq



class VkApi:

    def __init__(self, login, password):
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

    def get_match_info(self, match):
        match_info = {}
        match_info['url'] = f'https://vk.com/id{match}'
        photo_info = {}
        photo = self.vk.photos.get(owner_id=match, album_id='profile', extended='1')
        for item in photo['items']:
            photo_info[item['sizes'][-1]['url']] = item['likes']['count'] + item['comments']['count']
        three_best_photos = heapq.nlargest(3, photo_info, key=lambda k: photo_info[k])
        match_info['photo1'] = three_best_photos[0]
        match_info['photo2'] = three_best_photos[1]
        match_info['photo3'] = three_best_photos[2]
        return match_info