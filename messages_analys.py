import json
import operator
from analizer import Analizer
self_name = 'Аня'


class Audio_message():

    def __init__(self, message):
        self.date = message["date"]
        self.arriver = message['from']
        try:
            self.len = message['duration_seconds']
        except:
            self.len = 0

    def go_to_user(self, user):
        user.mp3_messages_number += 1
        user.mp3_messages_len += self.len


class Video_message():

    def __init__(self, message):
        self.date = message["date"]
        self.arriver = message['from']
        self.len = message['duration_seconds']

    def go_to_user(self, user):
        user.mp4_messages_number += 1
        user.mp4_messages_len += self.len


class Sticker_message():

    def __init__(self, message):
        self.date = message["date"]
        self.arriver = message['from']
        self.char = message['sticker_emoji'][0]

    def go_to_user(self, user):
        user.top_chars.append(self.char)
        # if self.char not in user.top_chars:
        #     user.top_chars[self.char] = 0
        #     user.top_chars[self.char] += 3


class Phone_call():
    def __init__(self, message):
        self.date = message["date"]
        self.arriver = message['actor']
        self.is_missed = False
        if 'discard_reason' in message:
            self.is_missed = True

        else:
            self.len = message["duration_seconds"]

    def go_to_user(self, user):
        if not self.is_missed:
            user.phone_call += 1
            user.phone_call_len = self.len
        else:
            user.phone_call_missed += 1


class Other_message():
    def __init__(self, message):

        self.arriver = message['from']
        self.text = message["text"]
        self.date = message['date']

    def go_to_user(self, user):
        user.other += 1
        user.other_text.append(self.text)


class Text_message():
    def __init__(self, message):
        self.arriver = message['from']
        self.text = message['text']
        self.len = len(message['text'])
        self.date = message["date"]
        self.caps = [False, 0]
        self.is_big()
        self.to_words()

    def to_words(self):
        """
        Segragates words and chars
        """
        self.words = []
        self.chars = []
        words = self.text.split()
        for word in words:
            new_word = ""
            chars = []
            for let in word:
                if let.isalpha():
                    new_word += let.lower()
                elif let in ".,\'\"-_=" or let.isdigit():
                    pass
                else:
                    chars.append(let)
            self.chars.extend(chars)
            self.words.append(new_word)

    def is_big(self):
        """
        Finds big letters
        """
        for let in self.text:
            if let.isupper():
                if self.caps[0]:
                    self.caps[1] += 1

                else:
                    self.caps[0] = True

            else:
                self.caps[0] = False

    def go_to_user(self, user):
        # user.emotions(self.text)
        user.text_messages += 1
        user.caps += self.caps[1]
        user.text_messages_len += self.len

        user.top_words.extend(self.words)
        user.top_chars.extend(self.chars)
        # for word in self.words:
        #     if word not in user.top_words:
        #         user.top_words[word] = 0
        #     user.top_words[word] += 1
        # for char in self.chars:
        #     if char not in user.top_chars:
        #         user.top_chars[char] = 0
        #     user.top_chars[char] += 1


class Chat:
    def __init__(self, user1, user2):
        self.u1 = user1
        self.u2 = user2
        self.previous_message = None
        self.dialogues = []
        self.total = 0

    def handle_message(self, message):
        """
        Takes messages and creates classes objects with its types
        """
        self.mes = message
        self.total += 1
        self.type = self.mes['type']
        if self.type == "service" and self.mes["action"] == "phone_call":
            self.mes = Phone_call(self.mes)

        elif self.type == "message" and self.mes['text'] and type(self.mes['text']) == str:
            self.mes = Text_message(self.mes)

        elif self.type == "message" and "media_type" in self.mes and self.mes['media_type'] == "voice_message":
            self.mes = Audio_message(self.mes)

        elif self.type == "message" and "media_type" in self.mes and self.mes['media_type'] == "video_message":
            self.mes = Video_message(self.mes)

        elif self.type == "message" and "media_type" in self.mes and self.mes['media_type'] == "sticker":
            self.mes = Sticker_message(self.mes)
        else:
            self.mes = Other_message(self.mes)
        self.detect_arriver()
        self.add_time()

        if self.previous_message:
            self.handle_time()
        else:
            self.new_dialogue = Dialogue(self.mes, self.u1, self.u2)
        self.previous_message = self.mes

    def detect_arriver(self):
        """
        Detects arriver
        """
        if self.mes.arriver == self.u1.name:
            self.mes.go_to_user(self.u1)
        else:
            self.mes.go_to_user(self.u2)

    def add_time(self):
        """
        Calculates the time from D M Y ... to seconds
        """
        t_t = self.mes.date
        self.mes.time = int(t_t[17:19])+int(t_t[14:16])*60+int(
            t_t[11:13]) * 3600+int(t_t[8:10])*3600*24+int(t_t[5:7])*3600*24*30+(int(t_t[:4])-2016)*3600*24*30*365

    def handle_time(self):
        """
        creates the new dialodue object and add info about previous one
        if the dialogue is fifnished (break is more than 8 hours)
        """
        self.new_dialogue.handle_message_time(self.mes)
        if self.new_dialogue.is_finished:
            self.dialogues.append(self.new_dialogue.result())
            self.new_dialogue = Dialogue(self.mes,  self.u1, self.u2)


class User():
    def __init__(self, name):
        self.caps = 0
        self.wait_time = 0
        self.name = name
        self.other_text = []
        self.other = 0
        self.messages = []
        self.text_messages = 0
        self.text_messages_len = 0
        self.phone_call = 0
        self.phone_call_missed = 0
        self.phone_call_len = 0
        self.top_words = []
        self.mp3_messages_number = 0
        self.mp3_messages_len = 0
        self.mp4_messages_number = 0
        self.mp4_messages_len = 0
        self.top_chars = []
        self.wait_line = []

    def add_message(self, message):
        self.messages.append(message)

    def handle_emotions(self):
        self.emotions = Emotional_Sence(
            self.top_words, self.top_chars, self.caps).analize()

    def __str__(self):
        self.handle_emotions()
        # self.sort_dicts()

        # print("caps letters", self.caps)
        # print("name", self.name)
        # print("messages", self.messages)
        # print("text mes", self.text_messages)
        # print("text_mes_len", self.text_messages_len)
        # print("phone_call", self.phone_call)
        # print('missed_cal', self.phone_call_missed)
        # print('call_len', self.phone_call_len)
        # # print(self.top_words)
        # # print(self.top_chars)
        #
        # # print(self.sorted_top_words[-20:])
        # # print(self.sorted_top_chars)
        #
        # print('mp3_num', self.mp3_messages_number)
        # print('mp3_len', self.mp3_messages_len)
        # print('mp4_num', self.mp4_messages_number)
        # print('mp4_len', self.mp4_messages_len)
        # print(self.emotions)
        return "here is info"

    def sort_dicts(self):
        """
        Sorts dicts with top users words and chars
        """
        self.sorted_top_words = sorted(
            self.top_words.items(), key=lambda x: x[1])
        self.sorted_top_chars = sorted(
            self.top_chars.items(), key=lambda x: x[1])


class Dialogue(Chat):

    def __init__(self, mes, u1, u2):
        super().__init__(u1, u2)
        self.cur_mes_time = mes.time
        self.u1.wait_time = 0
        self.u2.wait_time = 0
        self.break_time = 0
        self.initiator = self.set_initiator(mes)
        self.cur_arriver = self.initiator
        self.finisher = self.cur_arriver
        self.is_finished = False

    def handle_message_time(self, mes):
        """
        detects time between messages and the mes arriver
        if person anvered the message timer stops
        """
        self.wait = mes.time - self.cur_mes_time
        if self.wait > 8*3600:
            self.break_time += self.wait
            self.finisher = self.cur_arriver
            self.is_finished = True
        else:
            if self.cur_arriver == self.set_initiator(mes):
                self.add_time()
            else:
                self.add_time()
                self.change_cur_arriver()
        self.cur_mes_time = mes.time

    def set_initiator(self, mes):
        """
        return the cur messae arriver
        """
        if mes.arriver == self.u1.name:
            return self.u1
        else:
            return self.u2

    def add_time(self):
        """
        Adds time to user
        """
        if self.cur_arriver == self.u1:
            self.u1.wait_time += self.wait
        if self.cur_arriver == self.u2:
            self.u2.wait_time += self.wait

    def change_cur_arriver(self):
        """
        Changes arriver
        """
        if self.cur_arriver == self.u1:
            self.cur_arriver = self.u2
        elif self.cur_arriver == self.u2:
            self.cur_arriver = self.u1

    def result(self):
        """
        Returns thedialogue result (time, arriver, finisher)
        """
        return [self.initiator.name, str(self.u1.wait_time), str(self.u2.wait_time), str(self.break_time), self.finisher.name]


class Emotional_Sence:
    SAD = "(😳😡😠😤😝😱😨😰👿😈🙀😿"
    STRESSED = "!😳😡😠😤😝😱😨😰👿😈🙀"
    LAUGHT = ")😂🤣😛😝😜😋😏😹😺😀😃😄😁☺"
    LOVE = "😻❤️😍😘😚😗😙😽💑👩‍❤️‍👩👨‍❤️‍💋‍👨👩‍❤️‍💋‍👩💏👨‍❤️‍👨❤️💛💚💙💕❣️💟🖤💜💞💝💓💗💖💘❤"
    BAGS = ["коротше", "сенсі", "це", "насправді", "просто",
            "типу", "значить", "слухай", "блін", "чорт", 'чуєш', 'знаєш']
    PUNCTUATION = ".,-?:;*^%&#@"

    def __init__(self, words, chars, caps):
        self.words = words
        self.chars = chars
        self.result = {"sad": 0, "stressed": int(caps),
                       "laught": 0, "love": 0, "bags": 0, "punctuation": 0, 'other': 0}

    def analize(self):
        """
        finds each tpe of emotions in the dialogue and calculates
        """
        self.result['other'] += self.result['stressed']
        self.result["sad"] = self.find(self.SAD)
        self.result["stressed"] += self.find(self.STRESSED)
        self.result["laught"] = self.find(self.LAUGHT)
        self.result["love"] = self.find(self.LOVE)
        self.result["punctuation"] = self.find(self.PUNCTUATION)
        self.result["bags"] = self.find(self.BAGS, words=True)
        self.result['other'] += len(self.chars)-(self.result["sad"] +
                                                 self.result["stressed"] +
                                                 self.result["laught"]+self.result["love"])

        if self.result['other'] < 0:
            self.result['other'] = 0

        return self.result

    def find(self, emotion, words=False):
        """
        "xaxaxaxxaxa'-LAUGHT
        "Aaaaaaaaaaa'- as usually panica
        """
        result = 0
        if not words:
            for ch in self.chars:
                if ch in emotion:
                    result += 1
        else:
            for ch in self.words:
                if "аха" in ch:
                    self.result['laught'] += int(len(ch)//4)
                if "ааа" in ch:
                    self.result["stressed"] += int(len(ch)//10)+1
                if ch in emotion:
                    result += 1
        return result


def dialogue_analiz(dialogues):
    u1_init = 0
    u2_init = 0
    u1_wait_time = 0
    u2_wait_time = 0
    for d in dialogues:
        if d[0] == self_name:
            u1_init += 1
        else:
            u2_init += 1
        u1_wait_time += int(d[1])
        u2_wait_time += int(d[2])
    return (u1_init, u2_init, u1_wait_time, u2_wait_time)


def reading(name):
    """
    Reading all.json and return all the info
    """
    info = json.load(open('all.json', encoding='utf-8'))

    for chat in info['chats']['list']:
        try:

            if chat["name"] == name:
                break
        except:
            if chat["type"] == "saved_messages":
                pass
            else:
                print("Error003")

    with open("cur_dialog.json", "w") as fp:
        json.dump(chat, fp)

    chat = json.load(open('cur_dialog.json', encoding='utf-8'))
    # user1 = User(info['personal_information']["first_name"] +
    #              info['personal_information']["last_name"])

    user1 = User(self_name)
    user2 = User(name)
    cur_chat = Chat(user1, user2)
    for mes in chat['messages']:
        cur_chat.handle_message(mes)
    d_a = dialogue_analiz(cur_chat.dialogues)
    user2.total = cur_chat.total
    print(str(user1))
    print(str(user2))
    analiz = Analizer(user2, d_a)
    print(str(analiz))
