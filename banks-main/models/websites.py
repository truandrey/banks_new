import subprocess
import requests
import re
from wrapt_timeout_decorator import *

class Website:
    # Переменнные для проверки необходимости поста в телеграм канале
    first_time = True # Первый пост
    up = False # Состояние сайта

    # Переменная для проверки необходимости осуществления записи в отчет
    logger = True

    def __init__(self, name, url) -> None:
        self.url = url
        self.name = name

    # Функция проверки пинга для дебаггинга
    def checkPing(self) -> tuple:

        # Получение пинга
        ping = subprocess.Popen(
            ["ping", "-c", "4", self.url.replace("http://", "")],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )
        out, error_1 = ping.communicate()
        print(f"================\n\n\n{out}\n\n\n================")
        try:
            # Парсинг пинга
            matcher = re.compile("round-trip min/avg/max/stddev = (\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)")
            result = matcher.search(str(out)).groups()
            return 0, result
        except Exception as error_2:
            return 1, (error_1.decode("UTF-8"), error_2)

    # Функция получения ответа на запрос, работающая не дольше 10ти секунд
    @timeout(10)
    def getStatus(self) -> requests.Response:
        resp = requests.get(self.url)
        if resp.status_code == 200 and not self.up:
            self.up = True
            self.logger = True
            return resp
        elif resp.status_code != 200:
            if self.up:
                self.up = False
                self.logger = True
                return resp
            if self.first_time:
                self.first_time = False
                self.logger = False
                return resp
            return 1
        # При отсутствии изменений в работе сервиса, ответ не требуется
        return 1