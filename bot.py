import parse
import telebot
import config


bot = telebot.TeleBot(config.TOKEN)


def build_item(item):
    message_menu = ''
    title = item['title']
    menu = item['menu']
    price = item['price']
    
    message_menu +=  f'📄  {title} \n\n'
    message_menu +=  f'🍽  {menu} \n'
    message_menu +=  f'💵💵💵  {price} \n'
    return message_menu


@bot.message_handler(commands=['menu'])
def menu(message):

    parse.parse()

    for item in count:
        
        photo = open(item['path'], 'rb')
        bot.send_photo(message.chat.id, photo)

        message_menu = build_item(item)      
        bot.send_message(message.chat.id, message_menu)
   

if __name__ == '__main__':
    bot.polling(none_stop=True)