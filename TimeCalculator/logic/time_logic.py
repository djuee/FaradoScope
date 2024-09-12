from datetime import *

class TimeLogic():
    def time_difference(self, date1, date2):
        format = '%Y-%m-%d %H:%M:%S'
        if not(isinstance(date1, datetime)) and not(isinstance(date2, datetime)):
            date1 = datetime.strptime(date1, format)
            date2 = datetime.strptime(date2, format)
        difference = date2 - date1
        return difference.days * 86400 + difference.seconds

    def minimal_date(self, time_intervals):
        return datetime.strftime(min(datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S") 
                for intervals in time_intervals 
                for date_str in intervals), "%Y-%m-%d %H:%M:%S")
