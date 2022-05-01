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



def check_and_ask_info(user_id, user_info):
    '''получаем у пользователя недостающую информацию'''

    vkbot = VkBot(TOKEN)
    if 'city' not in user_info:
        vkbot.write_msg(user_id, f'Укажите идентификатор вашего города \n'
                                 f'(можно посмотреть в адресной строке при поиске по городу: \n'
                                 f'"...city%##=__... , где __ - id вашего города"')
        for event in vkbot.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text
                    if request.isdigit():
                        user_info['city_id'] = int(request)
                        break
                    else:
                        vkbot.write_msg(user_id, f'Не понимаю :( \n'
                                                 f'Напишите id города числом')
    else:
        user_info['city_id'] = user_info['city']['id']
    if 'age' not in user_info:
        vkbot.write_msg(user_id, f'Укажите ваш возраст \n'
                                 f'(числом до 80 :) ) ')
        for event in vkbot.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text
                    if request.isdigit() and (int(request)<80):
                        user_info['age'] = int(request)
                        break
                    else:
                        vkbot.write_msg(user_id, f'Не понимаю :( \n'
                                                 f'Напишите возраст числом до 80')
    return user_info


def find_matches(user_id, login, password):
    '''Поиск совпадений и запись в базу данных'''

    db = DataBaseWork(URL)
    vkapi = VkApi(login, password)
    user_info = vkapi.get_user_info(user_id)
    convert_user_info = check_and_ask_info(user_id, user_info)
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
                request = event.text.lower()
                if request == "привет":
                    vkbot.write_msg(event.user_id, f"Привет, путник! \n"
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
                                                       f'{match_info["photo1_url"]} \n'
                                                       f'{match_info["photo2_url"]} \n'
                                                       f'{match_info["photo3_url"]} \n'
                                                       f'Нравится? (+\-)')
                        for answer in vkbot.longpoll.listen():
                            if answer.type == VkEventType.MESSAGE_NEW:
                                if answer.to_me:
                                    request = answer.text
                                    if request == '+':
                                        vkbot.write_msg(answer.user_id, "Скорее знакомься ;)")
                                    elif request == '-':
                                        vkbot.write_msg(answer.user_id, "Next")
                                        break
                                    else:
                                        vkbot.write_msg(answer.user_id, f'Напиши: \n'
                                                                        f'"+" - нашел пару \n'
                                                                        f'"-" - не нашел->далее')
                else:
                    vkbot.write_msg(event.user_id, f"'Привет' - поздороваться \n"
                                                   f"'Пока' - попрощаться \n"
                                                   f"'+' - начать поиск пары")



if __name__ == '__main__':
    chat_bot(LOGIN, PASSWORD)







