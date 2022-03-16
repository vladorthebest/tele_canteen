import telebot


#menu_keyboard for bot
menu_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
menu_keyboard.row('Супы')
menu_keyboard.row('Порции')
menu_keyboard.row('Остальное')
