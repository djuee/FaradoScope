from datetime import *

class WeeksFinder():
    def to_datetime_format(self, date):
        format = "%Y-%m-%d %H:%M:%S"
        if not(isinstance(date, datetime)):
            date = datetime.strptime(date, format)
        return date

    def count_weekends(self, start_date, end_date):
        '''Метод возвращает количество выходных дней между двумя отрезками времени'''
        start_date = self.to_datetime_format(start_date)
        end_date = self.to_datetime_format(end_date)
        weekends = 0
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() in [5, 6]:  # 5 - суббота, 6 - воскресенье
                weekends += 1
            current_date += timedelta(days=1)
        return weekends