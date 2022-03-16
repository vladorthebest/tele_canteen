from bd import BD 
import telebot
import config
import TOKEN

#create bot
bot = telebot.TeleBot(TOKEN.TOKEN)
#add keyboard bot
menu_keyboard = config.menu_keyboard


def build_item(item):
    """ Creates a beautiful message from a menu list """
    message_menu = '' #message
    for day, category, dish, price in item:
        message_menu +=  f'📄  {category} \n\n' #add category in message
        message_menu +=  f'🍽  {dish} \n'  #add dish in message
        message_menu +=  f'💵💵💵  {price} \n' #add price in message
    return message_menu


@bot.message_handler(commands="start") #first start bot
def cmd_start(message):
    bot.send_message(message.chat.id, "Что вам показать?", reply_markup=menu_keyboard) #output menu_keyboard



@bot.message_handler(content_types=['text']) #user select category
def menu(message):
    
    all_categorys = {
        'Порции': ("MENU", ),
        'Супы': ("Polievka", ),
        'Остальное': ('SLADKÉ', 'MÚČNE', 'VEGETARIÁNSKE', 'ŠALÁT')
    }
    
    category = message.text #category 

    if category in all_categorys: #the category is in the category pool
        category = all_categorys[category] #new category 
        menu = bd.get_bd(category) #get menu by category from bd
    else:                          
        bot.send_message(message.chat.id, 'Нет такой категории') #the category is not in the category pool


    for item in menu:   #take 1 element in all menu (category)   
        path = item[-1] #path to photo
        photo = open(path, 'rb') #open photo
        bot.send_photo(message.chat.id, photo) #send a photo of the item

        message_menu = build_item([item[:-1]]) #build menu of the item    
        bot.send_message(message.chat.id, message_menu) #send item text
    


if __name__ == '__main__':
    bd = BD()
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            bot = telebot.TeleBot(config.TOKEN)        