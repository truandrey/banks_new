import time as t
import datetime as dt
from auto.bot import *
from models.websites import *
from models.banks import *
from models.logger import *
from presentation.present import *
from presentation.plot import *

def jobs(webs, log, bot, start):
    # 24 часовой цикл
    while (dt.datetime.now() - start).total_seconds() < 86400:
        # Проход по названиям организаций
        for key in bankmap.keys():
            try:
                # Получение статус кода сервиса
                response = webs[key].getStatus()
            except:
                # Если ответ не получен, проверяем пинг
                print(webs[key].checkPing())

                # Обнуление переменной ответа
                response = 0
            
            if response != 1:
                if webs[key].logger:
                    # Добавление таймстэмпа
                    log.updateTime(key, dt.datetime.now())
                if response == 0:
                    arg = 0
                else:
                    arg = response.status_code
                
                # Отправка поста с уведомлением в телеграм канал
                bot.post(key, bankmap[key], dt.datetime.now(), arg)

        # Добавление дилея для избежания блокировки за спам
        t.sleep(5)

def main():
    # Инициализация бота
    main_bot = Bot()
    while True:
        # Инициализация модели отчета с дефолтными параметрами
        main_logger = Logger(bankmap.keys())

        # Инициализация словаря с названиями организаций и моделями для обработки запросов
        webs = {key: Website(key, value) for key, value in bankmap.items()} 
        
        # Запись начала работы
        start_time = dt.datetime.now()

        # Функция запуска всех процессов
        jobs(webs, main_logger, main_bot, start_time)

        # Запись конца работы
        end_time = dt.datetime.now()

        # Создание графика
        makeBar(main_logger.writeInfo(start_time, end_time))

        # Создание слайда в формате pptx
        createPresentation()

        # Создание отчета в формате csv
        main_logger.makeFile()

if __name__ == '__main__':
    main()