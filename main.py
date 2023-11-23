import telebot
from config import keys, TOKEN
from extensions import Get_Price, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands= ['start', 'help'])
def first_command(message: telebot.types.Message):
    text = ('Чтобы начать работу введите комманду боту в следующем формате: \nНазвание валюты \nВ какую валюту хотите перевести\nКоличество переводимой валюты\n Чтобы увидеть список всех доступных валют, введите команду: /values')
    bot.send_message(message.chat.id,text)
    pass

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text='\n' .join((text,key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        quote, base, amount = values
        if len(values) != 3:
            raise APIException('Слишком много параметров.')

        total_base = Get_Price.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        total_base = float(total_base) * float(amount)
        text = f'Цена {amount} {quote} в {base} - {total_base}'

        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
