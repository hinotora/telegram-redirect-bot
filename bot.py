import logging
from os import getenv
from telegram import Update
from telegram.ext import Updater, CommandHandler,   MessageHandler,  Filters,  CallbackContext

# Env variables
ENV = getenv('ENV', 'local')
TOKEN = getenv('API_TOKEN')
APP_URL = getenv('APP_URL')
ADMIN_CHAT = getenv('CALLBACK_CHAT')

# Enable logging
logging.basicConfig(format='%(asctime)s / %(levelname)s / %(name)s / %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot functions
def start(update: Update, _: CallbackContext) -> None:
    user = update.effective_user
    logger.info(f'{user.name} [{user.id}] typed: {update.message.text}')
    update.message.reply_text(f'Hello, {user.first_name}! Write something to me and I\'ll redirect your message :)')

def help_msg(update: Update, _: CallbackContext) -> None:
    message = f"""
        About bot:
        This is a simple bot which redirect
        messages between users.
        
        Every message (not command) will be
        redirected to bot owner, and later owner
        will maybe answer you.
        
        Available commands:
        /start - Start bot
        /help - Get help
        
        Source: https://github.com/hinotora/telegram-echo-bot
    """

    update.message.reply_text(message)

def unsupported_type(update: Update, _:CallbackContext) -> None:
    update.message.reply_text("Sorry, I can only redirect text messages.")

def redirect_message(update: Update, context: CallbackContext) -> None:
    user = update.effective_user

    logger.info(f'{user.name} [{user.id}] typed: {update.message.text}')

    datetime_string = update.message.date.strftime('%Y-%m-%d %H:%M:%S')

    message_body = f"""
        NEW MESSAGE:
        Date: {datetime_string}
        From: @{user.username} / {user.id}
        Text: {update.message.text}
    """

    context.bot.send_message(ADMIN_CHAT, message_body)

def send_reply(update: Update, context: CallbackContext) -> None:
    user = update.effective_user

    if user.id != int(ADMIN_CHAT):
        logger.info(f'{user.name} [{user.id}] unauthorised: {update.message.text}')
        context.bot.send_message(user.id, "You are not authorized to do that.")
        return

    reply_to = context.args[0]
    message = ' '.join(context.args[1:])

    logger.info(f'Admin started reply to {reply_to}: {message}')

    context.bot.send_message(reply_to, message)


# Script entry point
if __name__ == '__main__':

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    """ User handlers """
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_msg))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, redirect_message))
    dispatcher.add_handler(MessageHandler(Filters.all & ~Filters.text & ~Filters.command, unsupported_type))

    """ Admin handlers """
    dispatcher.add_handler(CommandHandler("reply", send_reply, pass_args=True))


    """ Environment detection """
    if ENV == 'local':
        logger.info('=== LOCAL ENVIRONMENT DETECTED, USING LONG POOLING ===')
        updater.start_polling()
        updater.idle()
    elif ENV == 'production':
        logger.info('=== PRODUCTION ENVIRONMENT DETECTED, SETTING UP WEBHOOKS ===')
        updater.start_webhook(listen="0.0.0.0", port=80, url_path='webhook', webhook_url=APP_URL + 'webhook')
        updater.idle()
    else:
        logger.info('=== UNKNOWN ENVIRONMENT, END OF EXECUTION ===')
        updater.stop()