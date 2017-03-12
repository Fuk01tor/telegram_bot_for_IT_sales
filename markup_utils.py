from telebot import types


def two_option_markup(first_option, second_option):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton(first_option)
    itembtn2 = types.KeyboardButton(second_option)
    markup.add(itembtn1, itembtn2)
    return markup


def three_option_markup(first_option, second_option, third_option):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton(first_option)
    itembtn2 = types.KeyboardButton(second_option)
    itembtn3 = types.KeyboardButton(third_option)
    markup.add(itembtn1, itembtn2, itembtn3)
    return markup


def four_option_markup(first_option, second_option,
                       third_option, fourth_option):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton(first_option)
    itembtn2 = types.KeyboardButton(second_option)
    itembtn3 = types.KeyboardButton(third_option)
    itembtn4 = types.KeyboardButton(fourth_option)
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    return markup
