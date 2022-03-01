import telebot
import config
import parse

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['menu'])
def menu(message):

    

    count = parse.parse()
    for item in count:
        message_menu = ''

        
        for key, countent in item.items():
            if key != 'path':
                message_menu += countent + '\n'
            else:
                photo = open(countent, 'rb')
                bot.send_photo(message.chat.id, photo)

        bot.send_message(message.chat.id, message_menu)
   


bot.polling(none_stop=True)