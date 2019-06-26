class Analizer():

    def __init__(self, User, d_a):
        self.User = User
        self.d_a = d_a
        self.handle()

    def handle(self):
        """
        Calculetes users Emotional_Sence
        Emotional_Sence.txt
        """
        if self.User.total <= 100:
            self.frequency = "мало"
        elif self.User.total < 1000:
            self.frequency = "достатньо"
        else:
            self.frequency = "дуже багато"

        self.average_mes_len = int(
            self.User.text_messages_len/self.User.text_messages)
        self.bags = self.cut(int(
            (self.User.emotions["bags"] + self.User.emotions["other"])/self.User.text_messages * 100))
        self.positive = self.cut(int(
            (self.User.emotions["laught"])/self.User.text_messages * 100))
        self.negative = self.cut(int(
            (self.User.emotions["sad"])/self.User.text_messages * 100))
        self.stress = self.cut(int(
            (self.User.emotions["stressed"])/self.User.text_messages * 100))
        self.selfish = self.cut(int((self.User.mp4_messages_len*2 +
                                     self.User.mp4_messages_len)/self.User.text_messages_len * 1000))
        # print(self.d_a)
        try:
            self.willeness_to_chat = self.cut(int(((self.d_a[1]/self.d_a[0])+(
                self.d_a[3]/self.d_a[2]))*50+self.User.phone_call+self.User.phone_call_missed))
        except ZeroDivisionError:
            self.willeness_to_chat = "- 'недостатньо інформації'"

    def cut(self, value):
        if value > 100:
            value = 100
        return value

    def __str__(self):
        info = "Інформація про {}\n".format(self.User.name)
        info += "В вас {} повідомлень ({}).\n".format(
            self.frequency, self.User.total)
        info += "Середня довжина повідомлень {} знака\n".format(
            str(self.average_mes_len))
        info += "Заспамленість тексту {} %\n".format(
            str(self.bags))
        info += "Позитість {}%\n".format(str(self.positive))
        info += "Негативність {}%\n".format(str(self.negative))
        info += "Самовпевненість {}%\n".format(str(self.selfish))
        info += "Нервозність {}%\n".format(str(self.stress))
        info += "Бажання спілкуватись {}%".format(
            str(self.willeness_to_chat))

        return info
