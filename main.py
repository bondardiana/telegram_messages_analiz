import messages_analys
import analizer
import collegium_needs
import choosing_the_dialogue


def funct_first():
    collegium_needs.start()


def func_second():
    print("Choose the chat")
    all_chats = choosing_the_dialogue.start()[1]
    for chat in all_chats:
        print(chat)
    name = input()
    if name in all_chats:
        pass
        messages_analys.reading(name)
    else:
        print("Такого чату не існує, виберийте з того, що є.")


def main():
    print("Витаємо!")
    print("Якщо хочете отримати аналіз потреб мешканців Колегіуму ім. Йосипа Сліпого, натисніть 0")
    print("Якщо хочете отримати аназіз людини на основі вашій переписки, натисніть 1")
    action = int(input())
    if action == 0:
        funct_first()
    elif action == 1:
        func_second()
    else:
        print("Ви ввели неправильну цифру")
    print("До побачення")


if __name__ == "__main__":
    main()
