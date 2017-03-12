#!/usr/bin/env python
import os

from telebot import TeleBot

from db_utils import (
    save_user,
    get_user,
    save_monitor,
    get_monitors,
    remove_monitor,
    reserve_monitor,
)
from markup_utils import (
    two_option_markup,
    three_option_markup,
    four_option_markup,
)

bot = TeleBot(os.environ['TELEGRAM_TOKEN'])
monitor_dict = dict()


@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id
    admin_or_student = two_option_markup('/admin', '/student')
    reply = "Hiyaa {}! for help, type /help\nWhat's your role?".format(
        message.from_user.first_name)
    bot.send_message(chat_id, reply, reply_markup=admin_or_student)


@bot.message_handler(commands=['student'])
def student_handler(message):
    chat_id = message.chat.id
    save_user(message)
    bot.send_message(chat_id, 'Nice to meet you!')
    help_me(message)


@bot.message_handler(commands=['admin'])
def admin_handler(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Enter the secret word')
    bot.register_next_step_handler(msg, admin_confirm_handler)


def admin_confirm_handler(message):
    chat_id = message.chat.id
    secret_word = message.text
    if (secret_word.lower() == os.environ['SECRET_WORD']):
        save_user(message, admin=True)
        bot.send_message(chat_id, "You've been promoted to an admin.")
        help_me(message)
    else:
        bot.send_message(chat_id, "Wrong secret code.")
        help_me(message)


@bot.message_handler(commands=['me'])
def about_me(message):
    chat_id = message.chat.id
    user = get_user(message)
    reply = 'first_name: {}\nlast_name: {}\nusername: {}\nadmin: {}'.format(
        user['first_name'], user['last_name'], user['username'], user['admin'])
    bot.send_message(chat_id, reply)
    help_me(message)


@bot.message_handler(commands=['help'])
def help_me(message):
    chat_id = message.chat.id
    user = get_user(message)
    if (user['admin']):
        reply = """
{}, you're an admin. What would you like to do?""".format(user['first_name'])
        view_update_monitors = \
            two_option_markup('/view_monitors', '/update_monitors')
        bot.send_message(chat_id, reply, reply_markup=view_update_monitors)
    else:
        reply = """
{}, you're a student. What would you like to do?""".format(user['first_name'])
        view_monitors_get_me = \
            two_option_markup('/update_monitors', '/me')
        bot.send_message(chat_id, reply, reply_markup=view_monitors_get_me)


@bot.message_handler(commands=['update_monitors'])
def update_monitors_handler(message):
    chat_id = message.chat.id
    user = get_user(message)
    reply = 'What would you like to do?'
    if (not user['admin']):
        view_reserve = two_option_markup('/view_monitors', '/reserve_monitor')
        bot.send_message(chat_id, reply, reply_markup=view_reserve)
        return

    add_remove_monitor = three_option_markup(
        '/add_monitor', '/remove_monitor', '/view_monitors')
    bot.send_message(chat_id, reply, reply_markup=add_remove_monitor)


@bot.message_handler(commands=['add_monitor'])
def add_monitor_handler(message):
    chat_id = message.chat.id
    user = get_user(message)
    if (not user['admin']):
        bot.send_message(chat_id, 'Forbiddon operation!')
        help_me(message)
        return

    monitor_brands = four_option_markup('LG', 'Samsung', 'Dell', 'Apple')
    msg = bot.send_message(chat_id, 'Choose brand',
                           reply_markup=monitor_brands)
    bot.register_next_step_handler(msg, add_monitor_brand_handler)


def add_monitor_brand_handler(message):
    chat_id = message.chat.id
    monitor_brand = message.text
    monitor_dict[chat_id] = {
        'brand': monitor_brand,
    }
    monitor_manufacture_years = four_option_markup(
        '2000', '2005', '2010', '2015')
    msg = bot.send_message(chat_id, 'Choose manufacture year',
                           reply_markup=monitor_manufacture_years)
    bot.register_next_step_handler(msg, add_monitor_manufacture_year_handler)


def add_monitor_manufacture_year_handler(message):
    chat_id = message.chat.id
    manufacture_year = message.text
    monitor = monitor_dict[chat_id]
    monitor['manufacture_year'] = manufacture_year
    monitor_prices = four_option_markup('20€', '40€', '60€', '80€')
    msg = bot.send_message(chat_id, 'Choose price',
                           reply_markup=monitor_prices)
    bot.register_next_step_handler(msg, add_monitor_price_handler)


def add_monitor_price_handler(message):
    chat_id = message.chat.id
    monitor_price = message.text
    monitor = monitor_dict[chat_id]
    monitor['price'] = monitor_price
    save_monitor(**monitor)
    reply = """
{} monitor manufactured in {} which costs {} was added to the stock.
""".format(monitor['brand'], monitor['manufacture_year'], monitor['price'])
    bot.send_message(chat_id, reply)
    update_monitors_handler(message)


@bot.message_handler(commands=['view_monitors'])
def view_monitors_handler(message):
    chat_id = message.chat.id
    user = get_user(message)
    monitors = get_monitors()
    if (monitors):
        bot.send_message(chat_id, monitors)
    else:
        bot.send_message(chat_id, 'No monitor in the stock.')
    update_monitors_handler(message)


@bot.message_handler(commands=['remove_monitor'])
def remove_monitor_handler(message):
    chat_id = message.chat.id
    user = get_user(message)
    if (not user['admin']):
        bot.send_message(chat_id, 'Forbiddon operation!')
        help_me(message)
        return
    msg = bot.send_message(chat_id, "Enter id of monitor you'd like to remove")
    bot.register_next_step_handler(msg, remove_monitor_confirm_handler)


def remove_monitor_confirm_handler(message):
    chat_id = message.chat.id
    monitor_id = message.text
    try:
        remove_monitor(monitor_id)
        bot.send_message(
            chat_id,
            'Monitor {} was removed from the stock'.format(monitor_id))
    except Exception as e:
        bot.send_message(chat_id, str(e))
    update_monitors_handler(message)


@bot.message_handler(commands=['reserve_monitor'])
def reserve_monitor_handler(message):
    chat_id = message.chat.id
    user = get_user(message)
    if (user['admin']):
        bot.send_message(chat_id, 'Forbiddon operation!')
        help_me(message)
        return
    msg = bot.send_message(chat_id,
                           "Enter id of monitor you'd like to reserve")
    bot.register_next_step_handler(msg, reserve_monitor_confirm_handler)


def reserve_monitor_confirm_handler(message):
    chat_id = message.chat.id
    monitor_id = message.text
    try:
        reserve_monitor(monitor_id, message)
        bot.send_message(
            chat_id,
            'Monitor {} was reserved for you, {}'.format(
                monitor_id, message.from_user.first_name))
    except Exception as e:
        bot.send_message(chat_id, str(e))
    update_monitors_handler(message)


bot.polling()
