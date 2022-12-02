## Telegram redirect bot

A simple bot which forward messages between you and users. User sends message to bot, bot resends it to administrator's chat, administrator replies and bot send reply to user.

## Installation

Bot uses webhooks, not long pooling. You can run it on a local machine, but you need replace webhook setting with long pooling function from pyTelegramBotApi lib.

For correct work you need to create an environment variables such as:

`ENV` = `local` or `production` (default is `local`) \
`PORT` = Port for webhook setup (default is `443`)

If env set to local then bot will use long pooling, if env set in production then bot will set webhook into telegram servers.

`API_TOKEN` = `'12312342:GDBVNDLFVJDKLKMBE'` - API Token (@BotFather to create a new bot);\
`CALLBACK_CHAT` = `'12345678'` - Get your chat ID you can in @userinfobot;\
`APP_URL` = `'https://domain.com/'` - for Heroku (any value on others);

## Deploy

Use `docker-compose` for easy deployment on VPS/VDS/Dedicated Server

## Commands

For users:
`/start` - starts bot session with user.\
When user started session he can send any text, and it will be sent to admin chat.

For admins:
`/reply <chat_id> <message>` - chat_id will be displayed in an incoming message.\
When you typed this command you can type response and send it, bot will send in to user.

