## Telegram echo bot

Simple bot which forward messages between you and users. User sends message to bot, bot resends it to administrator's chat, administrator replies and bot send reply to user.

## Installation

Bot uses webhooks, not long pooling. You can run it on local machine, but you need replace webhook setting with long pooling function from pyTelegramBotApi lib.

For correct work you need to create an environment variables such as:

`API_TOKEN` = `'12312342:GDBVNDLFVJDKLKMBE'` - API Token (@BotFather to create new bot);\
`CALLBACK_CHAT` = `'12345678'` - Get your chat ID you can in @userinfobot;\
`APP_URL` = `'https://<app_name>.herokuapp.com/'` - for Heroku (any value on others);

## Usage on Heroku

There is a lot of information about how to deploy your bot to heroku in the Internet. Use Google or something. Actually this project is a fully ready to deploy, only one thing you need for correct work is to set up your local variables.

## Commands

For users:
`/start` - starts bot session with user.\
When user started session he can send any text and it will be send to admin chat.

For admins:
`/reply <chat_id>` - where chat_id will be displayed in message.\
When you typed this command you can type response and send it, bot will send in to user.

## Contributing
Forks, Issues, Pull requests are welcome.
