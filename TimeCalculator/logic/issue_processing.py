import asyncio
import math
from datetime import *
from database_objects.database import Database
from TimeCalculator.logic.range_finder import RangeFinder
from TimeCalculator.logic.weeks_finder import WeeksFinder
from TimeCalculator.logic.time_logic import TimeLogic

def list_in_range(list_):
    result = []
    if len(list_) < 2:
        return []
    for elem in range(0, len(list_), 2):
        result.append([list_[elem], list_[elem+1]])
    return result

class IssueProcessing():
    def __init__(self):
        self.range_finder = RangeFinder()
        self.weeks_finder = WeeksFinder()
        self.time_logic = TimeLogic()
        self.id_work_states = ['16', '6', '10', '17', '30', '36', '13', '18', '31', '37', '41']
        self.id_dont_work_states = ['5', '9', '14', '15', '21', '28', '29', '34', '35', '40', '42', '7', '8', '11', '12', '19', '20', '32', '33', '38', '39']

    def find_work_ranges(self, issue):
        '''Метод возвращает промежутки, когда задача находилась в работе'''
        work_ranges = []
        for change in issue.changes:
            diff = change.diff
            if '3' not in diff.keys():
                continue
            if (list(diff['3'].keys())[1] in self.id_work_states and list(diff['3'].keys())[0] in self.id_dont_work_states) or (list(diff['3'].keys())[0] in self.id_work_states and list(diff['3'].keys())[1] in self.id_dont_work_states):
                work_ranges.append(change.date_time)
        if len(work_ranges) % 2 != 0:
            work_ranges.append(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
        return work_ranges
    
    def find_dont_work_ranges(self, issue):
        dont_work_ranges = []
        start_date = issue.changes[0].date_time
        for change in issue.changes:
            diff = change.diff
            if '3' not in diff.keys():
                continue
            if (list(diff['3'].keys())[0] in self.id_dont_work_states and list(diff['3'].keys())[1] in self.id_work_states) or (list(diff['3'].keys())[1] in self.id_dont_work_states and list(diff['3'].keys())[0] in self.id_work_states):
                dont_work_ranges.append(change.date_time)
        if len(dont_work_ranges)>=2:
            dont_work_ranges.insert(0, start_date)
            if len(dont_work_ranges)%2!=0:
                dont_work_ranges.append('2100-01-01 00:00:00')
        return dont_work_ranges

    async def get_source(self, issue):
        for field in issue.fields:
            if field.field_kind_id == 68:
                return field.value
        await asyncio.sleep(0)

    async def get_state(self, issue):
        states = {
            "14": "Беклог",
            "15": "Открыто",
            "16": "Исследование",
            "17": "Разработка",
            "18": "Контроль качества",
            "19": "Выполнено",
            "20": "Архив",
            "21": "Отмена"
        }
        return states[str(issue.state_id)]
        await asyncio.sleep(0)

    async def get_grade(self, issue):
        grades = {
            "SA": 0,
            "DI": 0,
            "ALG": 0,
            "WEB": 0,
            "SYS": 0,
            "TEST": 0
        }
        for field in issue.fields:
            if field.field_kind_id == 16 and field.value != '':
                grades['SA'] = int(field.value)
            if field.field_kind_id == 17 and field.value != '':
                grades['DI'] = int(field.value)
            if field.field_kind_id == 18 and field.value != '':
                grades['ALG'] = int(field.value)
            if field.field_kind_id == 31 and field.value != '':
                grades['WEB'] = int(field.value)
            if field.field_kind_id == 32 and field.value != '':
                grades['SYS'] = int(field.value)
            if field.field_kind_id == 33 and field.value != '':
                grades['TEST'] = int(field.value)
        sum_grade = sum(grade for grade in grades.values())
        return grades, sum_grade
        await asyncio.sleep(0)

    async def calculation_realtime(self, issue):
        '''Возвращает реальное время выполнения задачи в секундах'''
        weeks_count = 0
        general_time = 0
        for kid in issue.kids:
            if len(kid.kids) == 0:
                work_ranges = self.find_work_ranges(kid)
                for i in range(0, len(work_ranges), 2):
                    general_time += self.time_logic.time_difference(work_ranges[i], work_ranges[i+1])
                    weeks_count += self.weeks_finder.count_weekends(work_ranges[i], work_ranges[i+1])
            else:
                general_time += await self.calculation_realtime(kid)
        return general_time - weeks_count * 86400
        await asyncio.sleep(0)
    
    async def calculation_pause(self, issue, pause_parameter):
        pause_time = 0
        count_weeks = 0
        count_pause = 0
        ranges_list = []
        ranges = [] # список для хранения промежутков, во время которых задача была в работе, а её дочерние были не в работе
        for kid in issue.kids:
            dont_work_kid = self.find_dont_work_ranges(kid)
            if len(dont_work_kid) % 2 != 0 or len(dont_work_kid) == 0:
                continue
            ranges.append(dont_work_kid)
        if len(ranges) != 0:
            min_date = self.time_logic.minimal_date(ranges)
            for i in range(len(ranges)):
                ranges[i][0] = min_date
        ranges.append(self.find_work_ranges(issue))
        for date in self.range_finder.find_common_time_periods(ranges):
            diff_time = self.time_logic.time_difference(date[0], date[1])
            if (diff_time // 86400 > 0) and (diff_time % 86400 > pause_parameter):
                pause_time += diff_time + 86400
                count_weeks += self.weeks_finder.count_weekends(date[0], date[1])
                count_pause += 1
            elif (diff_time // 86400 > 0) and (diff_time % 86400 < pause_parameter):
                pause_time += diff_time
                count_weeks += self.weeks_finder.count_weekends(date[0], date[1])
                count_pause += 1
            elif (diff_time // 86400 < 0) and (diff_time % 86400 > pause_parameter):
                pause_time += 86400
                count_weeks += self.weeks_finder.count_weekends(date[0], date[1])
                count_pause += 1
        return pause_time - count_weeks * 86400, count_pause
        await asyncio.sleep(0)

    async def async_run(self, issue, pause_parameter):
        return await asyncio.gather(
            self.get_source(issue),
            self.get_state(issue),
            self.get_grade(issue),
            self.calculation_pause(issue, pause_parameter),
            self.calculation_realtime(issue),
        )