from vkapi import VkApi
from longpoll import VkBot
from vk_api.longpoll import VkEventType
from decouple import config
from database import NewDataBase, DataBaseWork



LOGIN = config('LOGIN', default='')
PASSWORD = config('PASSWORD', default='')
TOKEN = config('TOKEN', default='')
URL = config('URL', default='')
DBDIALECT = config('DBDIALECT', default='')
DBUSERBANE = config('DBUSERBANE', default='')
DBPASSWORD = config('DBPASSWORD', default='')
DBHOST = config('DBHOST', default='')
DBPORT = config('DBPORT', default='')
DBDB = config('DBDB', default='')
URL = f'{DBDIALECT}://{DBUSERBANE}:{DBPASSWORD}@{DBHOST}:{DBPORT}/{DBDB}'



def find_matches(user_id, login, password):
    '''Поиск совпадений и запись в базу данных'''

    db = DataBaseWork(URL)
    vkapi = VkApi(login, password)
    user_info = vkapi.get_user_info(user_id)
    convert_user_info = vkapi.convert_user_info(user_info)
    if db.check_user(convert_user_info['id']):
        db.delete_user_match(convert_user_info['id'])
        db.delete_user(convert_user_info['id'])
    else:
        ...
    db.insert_user(convert_user_info)
    params = vkapi.get_search_params(convert_user_info)
    matches = vkapi.search_people(params)
    return matches

def chat_bot(login, password):
    '''Основная логика чат-бота'''

    vkapi = VkApi(login, password)
    vkbot = VkBot(TOKEN)
    newdb = NewDataBase(URL)
    db = DataBaseWork(URL)
    for event in vkbot.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                if request == "привет":
                    vkbot.write_msg(event.user_id, f"Хай, {event.user_id} \n"
                                                   f"Если хочешь найти пару - напиши '+'")
                elif request == "пока":
                    vkbot.write_msg(event.user_id, "Пока((")
                elif request == '+':
                    matches = find_matches(event.user_id, login, password)
                    for match in matches:
                        match_info = vkapi.get_match_info(int(match))
                        if db.check_match(match_info['id']):
                            db.delete_match_user(match_info['id'])
                            db.delete_match(match_info['id'])
                        else:
                            ...
                        db.insert_match(match_info, event.user_id)
                        vkbot.write_msg(event.user_id, f'{match_info["url"]} \n'
                                                       f'{match_info["photo1"]} \n'
                                                       f'{match_info["photo2"]} \n'
                                                       f'{match_info["photo3"]} \n'
                                                       f'Нравится? (+\-)')
                        for event in vkbot.longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW:
                                if event.to_me:
                                    request = event.text
                                    if request == '+':
                                        vkbot.write_msg(event.user_id, "Скорее знакомься ;)")
                                    if request == '-':
                                        pass
                else:
                    vkbot.write_msg(event.user_id, "Не поняла вашего ответа...")



if __name__ == '__main__':
    chat_bot(LOGIN, PASSWORD)







