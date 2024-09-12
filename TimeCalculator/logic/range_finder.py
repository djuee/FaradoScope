from datetime import datetime
from functools import reduce

class RangeFinder():
    def str_to_datetime(self, date_str):
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    def intersect_intervals(self, intervals1, intervals2):
        '''Метод для нахождения пересечения двух интервалов времени'''
        result = []
        for start1, end1 in intervals1:
            for start2, end2 in intervals2:
                start = max(start1, start2)
                end = min(end1, end2)
                if start <= end:
                    result.append((start, end))
        return result

    def find_common_intervals(self, intervals):
        '''Метод для нахождения общего промежутка внутри одной задачи'''
        common_intervals = []
        for i in range(0, len(intervals), 2):
            start = self.str_to_datetime(intervals[i])
            end = self.str_to_datetime(intervals[i+1])
            common_intervals.append((start, end))
        
        common_intervals = reduce(self.intersect_intervals, [common_intervals])
        return common_intervals

    def find_common_time_periods(self, tasks):
        '''Метод для нахождения общих промежутков времени для всех задач'''
        all_common_intervals = []
        
        for task in tasks:
            task_common_intervals = self.find_common_intervals(task)
            all_common_intervals.append(task_common_intervals)
        
        if all_common_intervals:
            final_common_intervals = reduce(self.intersect_intervals, all_common_intervals)
        else:
            final_common_intervals = []
        
        return final_common_intervals