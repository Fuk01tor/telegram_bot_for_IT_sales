from telebot import types


def two_option_markup(first_option, second_option):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton(first_option)
    itembtn2 = types.KeyboardButton(second_option)
    markup.add(itembtn1, itembtn2)
    return markup
