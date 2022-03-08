from bd import BD 
import telebot
import config

bot = telebot.TeleBot(config.TOKEN)


main_kayboard = telebot.types.ReplyKeyboardMarkup(True, False)
main_kayboard.row('Супы')
main_kayboard.row('Порции')
main_kayboard.row('Остальное')



def build_item(item):
    message_menu = ''
    for day, title, name, price in item:
        message_menu +=  f'📄  {title} \n\n'
        message_menu +=  f'🍽  {name} \n'
        message_menu +=  f'💵💵💵  {price} \n'
    return message_menu


@bot.message_handler(commands="start")
def cmd_start(message):
    bot.send_message(message.chat.id, "Что вам показать?", reply_markup=main_kayboard)


@bot.message_handler(content_types=['text'])
def menu(message):
    if message.text == 'Порции': 
        menu = bd.get_bd(("MENU", ))

    elif message.text == 'Супы': 
        menu = bd.get_bd(("Polievka", ))

    elif message.text == 'Остальное': 
        menu = bd.get_bd(('SLADKÉ', 'MÚČNE', 'VEGETARIÁNSKE', 'ŠALÁT'))
    
    else:
        bot.send_message(message.chat.id,'Нет такой категории')

    for item in menu:     
        path = item[-1]
        photo = open(path, 'rb')
        bot.send_photo(message.chat.id, photo)

        message_menu = build_item([item[:-1]])      
        bot.send_message(message.chat.id, message_menu)
    


if __name__ == '__main__':
    bd = BD()
    bot.polling(none_stop=True)