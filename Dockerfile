FROM python:3.8.10-alpine

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "python3", "bot.py" ]