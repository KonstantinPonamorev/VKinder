from vkapi import VkApi
from longpoll import VkBot
from vk_api.longpoll import VkEventType



LOGIN =
PASSWORD =
TOKEN =



def find_matches(user_id, login, password):
    vkapi = VkApi(login, password)
    user_info = vkapi.get_user_info(user_id)
    convert_user_info = vkapi.convert_user_info(user_info)
    params = vkapi.get_search_params(convert_user_info)
    matches = vkapi.search_people(params)
    return matches

def chat_bot(login, password):
    vkapi = VkApi(login, password)
    vkbot = VkBot(TOKEN)
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
                                        break
                                    if request == '-':
                                        pass
                else:
                    vkbot.write_msg(event.user_id, "Не поняла вашего ответа...")



if __name__ == '__main__':
    chat_bot(LOGIN, PASSWORD)







