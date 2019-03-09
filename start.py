import json
import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer(lang='uk')


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


chat1 = dict()
chat2 = dict()
chat3 = dict()
info1 = json.load(open('result.json', encoding='utf-8'))
info2 = json.load(open('random.json', encoding='utf-8'))
for message in info2['chats']['list'][0]['messages']:
    try:
        if message['text'] != "" and len(message['text']) < 100 and len(message['text']) > 10:
            mes = mes_edit(message['text'])
            if mes:
                if message['from'] not in chat1:
                    chat1[message['from']] = []
                chat1[message['from']].append((
                    mes, message['date']))
    except Exception as err:
        print("not only text mes")
        print(err)

dcti = {}
check_list = ["хтось має", "у когось є", "в когось є",  "хто має", " у кого є", 'є в когось', 'є у когось', "в кого є",
              'має хтось', 'хтось би мав', 'маєте хтось', "має хто", 'є позичити', 'може позичити', 'в когось можна купити', 'хтонебудь має', 'міг би позичити', 'міг позичити', 'у когото есть', "є в кого", "є у кого", 'хто позичить']
i = 0
for act in chat1:
    #     #     print(act+'\n')
    for mes in chat1[act]:
        message = detect_request(mes[0], check_list)
        if message:
            i += 1
            m = ""
            momomo = ""
            for el in message.split():
                momo = morph.parse(el)[0]
                if str(momo.tag).startswith("NOUN"):
                    momomo += momo.normal_form + " "
                # print(momo.normal_form)
                m += momo.normal_form + " "
            print(m, "  ***  ", momomo)
            # print(m, "   *******   ", mes[0])
            if m not in dcti:
                dcti[m] = 0
            dcti[m] += 1
            # if i > 10:
            #     break


# print(i)
s = sorted(dcti.items(), key=lambda x: x[1])
print(s)
