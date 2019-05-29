import json
import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer(lang='uk')


check_list = ["хтось має", "у когось є", "в когось є",  "хто має", " у кого є", 'є в когось', 'є у когось', "в кого є",
              'має хтось', 'хтось би мав', 'маєте хтось', "має хто", 'є позичити', 'може позичити', 'в когось можна купити', 'хтонебудь має', 'міг би позичити', 'міг позичити', 'у когото есть', "є в кого", "є у кого", 'хто позичить']


def detect_request(mes, check_list):
    for el in check_list:
        if el in mes:
            return "".join(mes.split(el)[1:])[1:]


def mes_edit(mes):
    mes1 = ""
    A = {'а', 'б', 'в', 'г', 'д', 'е',  'є', 'ж', 'з', 'і', 'ї', 'к', 'л', 'м', 'н', 'о', 'п',
         'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ю', 'я', 'и', 'й'}
    mes = mes.replace(",", " ").replace(
        ".", " ").replace("\n", " ").lower()
    for let in mes:
        if let in A or let == " ":
            mes1 += let
    while "  " in mes1:
        mes1 = mes1.replace("  ", " ")
    return mes1.strip()


def reading(file_name):
    chat = dict()
    info = json.load(open(file_name, encoding='utf-8'))
    for chat_index in range(3):
        for message in info['chats']['list'][chat_index]['messages']:
            try:
                if message['text'] != "" and len(message['text']) < 100 and len(message['text']) > 10:
                    mes = mes_edit(message['text'])
                    if mes:
                        if message['from'] not in chat:
                            chat[message['from']] = []
                        chat[message['from']].append((
                            mes, message['date']))
            except Exception as err:
                pass
    return chat


def to_the_normal_form(chat):
    dct = {}
    i = 0
    for act in chat:
        for mes in chat[act]:
            message = detect_request(mes[0], check_list)
            if message:
                i += 1
                normalized = ""
                for el in message.split():
                    cur_word = morph.parse(el)[0]
                    normalized += cur_word.normal_form + " "
                if normalized not in dct:
                    dct[normalized] = 0
                dct[normalized] += 1
    return dct


def delete_unnessesary(dct):
    delete_lst = []
    for el in dct:
        if len(el.split()) == 1:
            for els in dct:
                if el in els and len(els.split()) != 1:
                    delete_lst.append(els)
                    dct[el] += 1
    for el in delete_lst:
        if el in dct:
            del dct[el]
    return dct


def start():
    dcti = delete_unnessesary(
        to_the_normal_form(reading("random.json")))
    s = sorted(dcti.items(), key=lambda x: x[1])
    words_number = int(input("Скікльки топ-запитів хочете бачити? "))
    try:
        if words_number:
            for el in s[-words_number:]:
                print(el[0] + ", запитів "+str(el[1]))
        else:
            for el in s:
                print(el[0] + ", запитів "+str(el[1]))
    except:
        print("Введіть коректні дані!")
