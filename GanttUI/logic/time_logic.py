from datetime import *

class TimeLogic():
    def __init__(self):
        self.format = '%Y-%m-%d'

    def str_to_datetime(self, date):
        return datetime.strptime(date, self.format)

    def date_plus_days(self, date, days_count):
        return date + timedelta(days=days_count) 

    def date_minus_days(self, date, days_count):
        return date - timedelta(days=days_count)

    def date_in_between(self, date, start_date, end_date):
        return (start_date < date) and (date < end_date) 
    
    def date_in_another_date(self, start_date_1, end_date_1, start_date_2, end_date_2):
        start_date_1 = self.str_to_datetime(start_date_1)
        start_date_2 = self.str_to_datetime(start_date_2)
        end_date_1 = self.str_to_datetime(end_date_1)
        end_date_2 = self.str_to_datetime(end_date_2)

        if (start_date_1 >= start_date_2) and (end_date_2 <= end_date_1):
            return True
        else:
            return False
    
    def interval_for_dates(self, intervals):
        dates = []
        for interval in intervals:
            current_date = interval[0]
            end_date = interval[1]
            while current_date <= end_date:
                dates.append(current_date)
                current_date += timedelta(days=1)
        return dates

    def ranges_holidays(self, start_date, end_date, weekends=[]):
        result = []
        current_date = start_date
        while current_date <= end_date:
            if current_date not in weekends:  # Проверяем, что это не выходной день
                range_start = current_date
                while current_date not in weekends and current_date <= end_date:
                    current_date += timedelta(days=1)
                range_end = current_date 
                result.append([range_start, range_end])
            current_date += timedelta(days=1)
        return result

    def get_weekday_ranges_between_dates(self, start_date, end_date):
        result = []
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() != 5 and current_date.weekday() != 6:  # Проверяем, что это не суббота и не воскресенье
                range_start = current_date
                while current_date.weekday() != 5 and current_date.weekday() != 6 and current_date < end_date:
                    current_date += timedelta(days=1)
                range_end = current_date 
                result.append((range_start.strftime(self.format), range_end.strftime(self.format)))
            current_date += timedelta(days=1)
        return result

    def count_weeks(self, start_date, end_date):
        if not(isinstance(start_date, datetime)):
            start_date = self.str_to_datetime(start_date)
        if not(isinstance(end_date, datetime)):    
            end_date = self.str_to_datetime(end_date)
        weekend_days = 0
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() >= 5:  # Суббота имеет индекс 5, воскресенье - 6
                weekend_days += 1
            current_date += timedelta(days=1)  # Переход к следующему дню
        return weekend_days