import pandas as pd

class Logger:

    # Модель данных для отчета
    df = pd.DataFrame(columns=['Name', 'Uptime, %', 'Timestamps', 'Downtime'])

    def __init__(self, banks) -> None:
        # Инициализация массивов с временными промежутками
        self.bankmap = {bank : [] for bank in banks}

    def updateTime(self, name, timestamp):
        # Добавление временного времени потери или восстановления доступа
        self.bankmap[name].append(timestamp)
    
    def makeFile(self):
        # СОздание файла с отчетом в виде csv таблицы
        self.df.to_csv('reviews/my_csv.csv', mode='w', header=True)

    def writeInfo(self, start_time, end_time) -> pd.DataFrame:
        uptimes = {}
        downtimes = {}
        for key, value in self.bankmap.items():
            if len(value) % 2:
                # Добавление четного таймстжмпа, завершающего промежуток времени работы ресурса
                value.append(end_time)

            # Подсчет общего времени доступности ресурса
            total = 0
            for i in range(0, len(value), 2):
                total += (value[i + 1] - value[i]).total_seconds() + (value[0] - start_time).total_seconds()
            time_passed = (end_time - start_time).total_seconds()

            # Время недоступности ресурса в секундах
            downtimes[key] = abs(round(time_passed - total, 1))
            # Время доступности ресурс,а разеленное на время работы программы
            uptimes[key] = round((total/time_passed)*100, 2)
        
        # Добавление строк в модель
        for key, value in self.bankmap.items():
            self.df = self.df.append(
                {
                    'Name': key, 
                    'Uptime, %': uptimes[key], 
                    'Timestamps': " - ".join(map(str, value)), 
                    'Downtime': downtimes[key]
                }, ignore_index=True)
        
        return self.df

    def __str__(self) -> str:
        return self.df