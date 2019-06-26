import json

info = json.load(open('all.json', encoding='utf-8'))

try:
    me = info['personal_information']["first_name"] + \
        info['personal_information']["last_name"]
except:
    me = 'Аня'


def detect_user(chats):
    for mes in chats['messages']:
        try:
            if mes['from'] != me:
                own_chats[chats['name']] = [(mes['from'])]
                break
        except:
            pass


phone_number_dct = {}
group_chats = []
own_chats = {}


def start():
    for chats in info['chats']['list']:
        try:
            if len(chats['messages']) > 10:
                if chats['type'] == 'private_group':
                    group_chats.append(chats['name'])
                if chats['type'] == 'personal_chat':
                    detect_user(chats)

        except Exception as err:
            print(err)

            if chats['type'] == 'saved_messages':
                pass
            else:
                print("Error #001")
    for contacts in info['contacts']['list']:
        name = contacts['first_name']+contacts['last_name']
        for el in own_chats:
            if el == name or own_chats[el] == name:
                own_chats[el].append(contacts['phone_number'])
    return group_chats, own_chats
