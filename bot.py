import logging
import datetime
from os import getenv
from telegram import Update, Bot
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext
)

ENV = getenv('ENV', 'local')
TOKEN = getenv('API_TOKEN')
APP_URL = getenv('APP_URL')
ADMIN_CHAT = getenv('CALLBACK_CHAT')

# Enable logging
logging.basicConfig(
    format='%(asctime)s / %(levelname)s / %(name)s / %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, _: CallbackContext) -> None:
    user = update.effective_user
    logger.info(f'{user.name} [{user.id}] typed: {update.message.text}')
    update.message.reply_text(f'Hello, {user.first_name}! Write something to me and I\'ll redirect your message :)')

def redirect_message(update: Update, context: CallbackContext) -> None:

    datetime_string = update.message.date.strftime('%Y-%m-%d %H:%M:%S')
    user = update.effective_user

    message_body = f"""
        New message / {datetime_string}
        From: {user.username} / {user.id}
        Text: {update.message.text}
    """

    logger.info(f'{user.name} [{user.id}] typed: {update.message.text}')

    context.bot.send_message(ADMIN_CHAT, message_body)

def unsupported_type(update: Update, _:CallbackContext) -> None:
    update.message.reply_text("Sorry, I can only redirect text messages.")

def main() -> None:

    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    """ User handlers """
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, redirect_message))
    dispatcher.add_handler(MessageHandler(Filters.all & ~Filters.text & ~Filters.command, unsupported_type))

    if ENV == 'local':
        logger.info('=== LOCAL ENVIRONMENT DETECTED, USING LONG POOLING ===')

        updater.start_polling()
        updater.idle()
    elif ENV == 'production':
        logger.info('=== PRODUCTION ENVIRONMENT DETECTED, SETTING UP WEBHOOKS ===')

        updater.start_webhook(listen="0.0.0.0",
                              port=80,
                              url_path='webhook',
                              webhook_url=APP_URL + 'webhook')
        updater.idle()
    else:
        logger.info('=== UNKNOWN ENVIRONMENT, END OF EXECUTION ===')


if __name__ == '__main__':
    main()