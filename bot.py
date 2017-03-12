#!/usr/bin/env python
import os

from telebot import TeleBot

from db_utils import save_user, get_user
from markup_utils import two_option_markup

bot = TeleBot(os.environ['TELEGRAM_TOKEN'])


@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id
    admin_or_student = two_option_markup('/admin', '/student')
    reply = "Hiyaa {}! What's your role?".format(message.from_user.first_name)
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
    if (secret_word == os.environ['SECRET_WORD']):
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
    if (user['admin'] == 'True'):
        reply = """
{}, you're an admin. What would you like to do?""".format(user['first_name'])
        view_update_monitors = \
            two_option_markup('/view_monitors', '/update_monitors')
        bot.send_message(chat_id, reply, reply_markup=view_update_monitors)
    else:
        reply = """
{}, you're a student. What would you like to do?""".format(user['first_name'])
        view_monitors_get_me = \
            two_option_markup('/view_monitors', '/me')
        bot.send_message(chat_id, reply, reply_markup=view_monitors_get_me)


bot.polling()
