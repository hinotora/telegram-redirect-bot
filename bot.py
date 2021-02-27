import os
import telebot
import datetime
from flask import Flask, request

# Fetching an environment variables
TOKEN = str(os.environ['API_TOKEN'])
CALLBACK_CHAT = str(os.environ['CALLBACK_CHAT'])
APP_URL = str(os.environ['APP_URL'])

# Using telebot
bot = telebot.TeleBot(TOKEN)

# Helper function for an argument extracting
def extract_arg(arg):
    return arg.split()[1:][0]

# Command /start
@bot.message_handler(commands=['start'])
def start(message):
    text = 'Hello! Write me something and I\'ll reply to you later.'
    bot.send_message(message.chat.id, text)

# 1st step. Command /reply <chat>
@bot.message_handler(commands=['reply'])
def reply_start(message):

    if str(message.chat.id) != CALLBACK_CHAT:
        bot.send_message(message.chat.id, "You are not allowed to do that.")
        bot.send_message(CALLBACK_CHAT, f"{message.chat.id} tried to {message.text}.")
        return

    try:
        reply_chat = str(extract_arg(message.text))
    except:
        bot.send_message(CALLBACK_CHAT, "Argument error. Usage: /reply <chat>")
    else:
        msg = bot.send_message(CALLBACK_CHAT, f"Reply to: {reply_chat}.\nEnter message and send:")
        bot.register_next_step_handler(msg, reply_send, reply_chat)

# 2nd step. Sending reply
def reply_send(message, reply_chat):
    try:
        bot.send_message(reply_chat, message.text)
    except:
        bot.send_message(message.chat.id, "Error while replying error. Try later.")
    else:
        bot.send_message(CALLBACK_CHAT, "Successfully replied.")

# When user sends text. Function for a message forwarding.
@bot.message_handler(content_types=["text"])
def resend(message):
    try:
        from_chat = message.from_user.id
        message_text = str(message.text)
        message_date = datetime.datetime.fromtimestamp(int(message.date)).strftime('%Y-%m-%d %H:%M:%S')

        text = f"From: {from_chat}\nDate: {message_date}\nText: {message_text}"

        bot.send_message(CALLBACK_CHAT, text)
    except:
        bot.send_message(message.chat.id, "Error while message sending. Try later.")
    else:
        bot.send_message(message.chat.id, "Message has been sent.")

# Setting up webhooks
server = Flask(__name__)

@server.route('/webhook', methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL + 'webhook')
    return "!", 200

# Initialization stuff
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))

