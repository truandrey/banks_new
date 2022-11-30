import telegram
import os
from http.client import responses

class Bot:
    def __init__(self) -> None:
        self.bot = telegram.Bot(token=os.getenv('TELEGRAM_TOKEN'))

    def post(self, name, url, timestamp, resp):
        if resp == 200:
            msg = f"Сервис работает:\n{name} - 'Веб-сайт' - {url} - {timestamp}"
        elif resp == 0:
            msg = f"Запрос не прошел:\n{name} - 'Веб-сайт' - {url} - {timestamp}"
        else:
            # При отсутствии доступа к ресурсу записывается соответсвующая статус коду ошибка
            msg = f"Сервис не работает:\n{name} - 'Веб-сайт' - {url} - {timestamp} - {responses[resp]}"

        # Отправка поста в телеграм канал с помощью бота
        self.bot.send_message(chat_id="@bank_uptime", text=msg)
