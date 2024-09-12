import datetime
from GanttUI.logic.time_logic import TimeLogic
from database_objects.database import Database

'''
Все представленные в данном классе временные списки, которые возвращают методы, имеют формат: [(дата начала, дата конца), (дата начала, дата конца)]
Те списки, что не соответствуют данному формату, помечены #*
'''
    

class IssueProcessing():
    def __init__(self, db_name):
        self.time = TimeLogic()
        self.db = Database(db_name) 
    
    def get_grade(self, issue_id):
        issue = self.db.issue(issue_id)
        grade = {
            'SA': 0,
            'DI': 0,
            'ALG': 0,
            'SYS': 0,
            'WEB': 0,
            'TEST': 0
        }
        for field in issue.fields:
            kind_id = field.field_kind_id
            value = field.value
            try:
                if kind_id == 16: grade['SA'] = int(value)
            except ValueError:
                pass
            try:
                if kind_id == 17: grade['DI'] = int(value)
            except ValueError:
                pass
            try:
                if kind_id == 18: grade['ALG'] = int(value)
            except ValueError:
                pass
            try:
                if kind_id == 31: grade['SYS'] = int(value)
            except ValueError:
                pass
            try:
                if kind_id == 32: grade['WEB'] = int(value)
            except ValueError:
                pass
            try:
                if kind_id == 33: grade['TEST'] = int(value)
            except ValueError:
                pass
        return grade

    def sa_date(self, issue_id, start_date_sa, holidays_interval=[]):
        dates_sa = []
        if self.get_grade(issue_id)['SA'] == 0:
            return [(start_date_sa, start_date_sa)]
        if start_date_sa is None:
            start_date_sa = start_date_sa
        else:
            if isinstance(start_date_sa, datetime.datetime):
                pass
            else:
                start_date_sa = self.time.str_to_datetime(start_date_sa)
        self.end_date_sa = self.time.date_plus_days(start_date_sa, self.get_grade(issue_id)['SA'])
        dates = [[start_date_sa, self.end_date_sa]]
        if holidays_interval == []:
            pass
        else:
            weekends_dates = self.time.interval_for_dates(holidays_interval)
            for week_date in weekends_dates:
                true_false = False
                if self.time.date_in_between(week_date, start_date_sa, self.end_date_sa):
                    true_false = True #проверка, пересекаются ли даты отпуска и даты выполнения задачи
                    break
            if true_false is True:
                self.end_date_sa += datetime.timedelta(days=len(weekends_dates))
                dates = self.time.ranges_holidays(start_date_sa, self.end_date_sa, weekends_dates)
        count_weekends = 0
        for date in dates:
            count_weekends += self.time.count_weeks(date[0], date[1])
        dates[-1][1] += datetime.timedelta(days=count_weekends)
        for date in dates:
            dates_sa += self.time.get_weekday_ranges_between_dates(date[0], date[1])
        return dates_sa

    def di_date(self, issue_id, start_date_di=None, holidays_interval=[]):
        dates_di = []
        if self.get_grade(issue_id)['DI'] == 0:
            return [(start_date_di, start_date_di)]
        if start_date_di is None:
            start_date_di = self.end_date_sa
        else:
            if isinstance(start_date_di, datetime.datetime):
                pass
            else:
                start_date_di = self.time.str_to_datetime(start_date_di)
        self.end_date_di = self.time.date_plus_days(start_date_di, self.get_grade(issue_id)['DI'])
        dates = [[start_date_di, self.end_date_di]]
        if holidays_interval == []:
            pass
        else:
            weekends_dates = self.time.interval_for_dates(holidays_interval)
            for week_date in weekends_dates:
                true_false = False
                if self.time.date_in_between(week_date, start_date_di, self.end_date_di):
                    true_false = True #проверка, пересекаются ли даты отпуска и даты выполнения задачи
                    break
            if true_false is True:
                self.end_date_di += datetime.timedelta(days=len(weekends_dates))
                dates = self.time.ranges_holidays(start_date_di, self.end_date_di, weekends_dates)
        count_weekends = 0
        for date in dates:
            count_weekends += self.time.count_weeks(date[0], date[1])
        dates[-1][1] += datetime.timedelta(days=count_weekends)
        for date in dates:
            dates_di += self.time.get_weekday_ranges_between_dates(date[0], date[1])
        return dates_di
    
    def alg_date(self, issue_id, start_date_alg=None, holidays_interval=[]):
        dates_alg = []
        if self.get_grade(issue_id)['ALG'] == 0:
            return [(start_date_alg, start_date_alg)]
        if start_date_alg is None:
            start_date_alg = self.end_date_web
        else:
            if isinstance(start_date_alg, datetime.datetime):
                pass
            else:
                start_date_alg = self.time.str_to_datetime(start_date_alg)
        self.end_date_alg = self.time.date_plus_days(start_date_alg, self.get_grade(issue_id)['ALG'])
        dates = [[start_date_alg, self.end_date_alg]]
        if holidays_interval == []:
            pass
        else:
            weekends_dates = self.time.interval_for_dates(holidays_interval)
            for week_date in weekends_dates:
                true_false = False
                if self.time.date_in_between(week_date, start_date_alg, self.end_date_alg):
                    true_false = True #проверка, пересекаются ли даты отпуска и даты выполнения задачи
                    break
            if true_false is True:
                self.end_date_alg += datetime.timedelta(days=len(weekends_dates))
                dates = self.time.ranges_holidays(start_date_alg, self.end_date_alg, weekends_dates)
        count_weekends = 0
        for date in dates:
            count_weekends += self.time.count_weeks(date[0], date[1])
        dates[-1][1] += datetime.timedelta(days=count_weekends)
        for date in dates:
            dates_alg += self.time.get_weekday_ranges_between_dates(date[0], date[1])
        return dates_alg

    def sys_date(self, issue_id, start_date_sys=None, holidays_interval=[]):
        dates_sys = []
        if self.get_grade(issue_id)['SYS'] == 0:
            return [(start_date_sys, start_date_sys)]
        if start_date_sys is None:
            start_date_sys = self.end_date_web
        else:
            if isinstance(start_date_sys, datetime.datetime):
                pass
            else:
                start_date_sys = self.time.str_to_datetime(start_date_sys)
        if start_date_sys is None:
            start_date_sys = self.end_date_alg
        self.end_date_sys = self.time.date_plus_days(start_date_sys, self.get_grade(issue_id)['SYS'])
        dates = [[start_date_sys, self.end_date_sys]]
        if holidays_interval == []:
            pass
        else:
            weekends_dates = self.time.interval_for_dates(holidays_interval)
            for week_date in weekends_dates:
                true_false = False
                if self.time.date_in_between(week_date, start_date_sys, self.end_date_sys):
                    true_false = True #проверка, пересекаются ли даты отпуска и даты выполнения задачи
                    break
            if true_false is True:
                self.end_date_sys += datetime.timedelta(days=len(weekends_dates))
                dates = self.time.ranges_holidays(start_date_sys, self.end_date_sys, weekends_dates)
        count_weekends = 0
        for date in dates:
            count_weekends += self.time.count_weeks(date[0], date[1])
        dates[-1][1] += datetime.timedelta(days=count_weekends)
        for date in dates:
            dates_sys += self.time.get_weekday_ranges_between_dates(date[0], date[1])
        return dates_sys

    def web_date(self, issue_id, start_date_web=None, holidays_interval=[]):
        dates_web = []
        if self.get_grade(issue_id)['WEB'] == 0:
            return [(start_date_web, start_date_web)]
        if start_date_web is None:
            start_date_web = self.end_date_web
        else:
            if isinstance(start_date_web, datetime.datetime):
                pass
            else:
                start_date_web = self.time.str_to_datetime(start_date_web)
        if start_date_web is None:
            start_date_web = self.end_date_sys
        self.end_date_web = self.time.date_plus_days(start_date_web, self.get_grade(issue_id)['WEB'])
        dates = [[start_date_web, self.end_date_web]]
        if holidays_interval == []:
            pass
        else:
            weekends_dates = self.time.interval_for_dates(holidays_interval)
            for week_date in weekends_dates:
                true_false = False
                if self.time.date_in_between(week_date, start_date_web, self.end_date_web):
                    true_false = True #проверка, пересекаются ли даты отпуска и даты выполнения задачи
                    break
            if true_false is True:
                self.end_date_web += datetime.timedelta(days=len(weekends_dates))
                dates = self.time.ranges_holidays(start_date_web, self.end_date_web, weekends_dates)
        count_weekends = 0
        for date in dates:
            count_weekends += self.time.count_weeks(date[0], date[1])
        dates[-1][1] += datetime.timedelta(days=count_weekends)
        for date in dates:
            dates_web += self.time.get_weekday_ranges_between_dates(date[0], date[1])
        return dates_web
    
    def test_date(self, issue_id, start_date_test=None, holidays_interval=[]):
        dates_test = []
        if self.get_grade(issue_id)['TEST'] == 0:
            return [(start_date_test, start_date_test)]
        if start_date_test is None:
            start_date_test = self.end_date_web
        else:
            if isinstance(start_date_test, datetime.datetime):
                pass
            else:
                start_date_test = self.time.str_to_datetime(start_date_test)
        self.end_date_test = self.time.date_plus_days(start_date_test, self.get_grade(issue_id)['TEST'])
        dates = [[start_date_test, self.end_date_test]]
        if holidays_interval == []:
            pass
        else:
            weekends_dates = self.time.interval_for_dates(holidays_interval)
            for week_date in weekends_dates:
                true_false = False
                if self.time.date_in_between(week_date, start_date_test, self.end_date_test):
                    true_false = True #проверка, пересекаются ли даты отпуска и даты выполнения задачи
                    break
            if true_false is True:
                self.end_date_test += datetime.timedelta(days=len(weekends_dates))
                dates = self.time.ranges_holidays(start_date_test, self.end_date_test, weekends_dates)
        count_weekends = 0
        for date in dates:
            count_weekends += self.time.count_weeks(date[0], date[1])
        dates[-1][1] += datetime.timedelta(days=count_weekends)
        for date in dates:
            dates_test += self.time.get_weekday_ranges_between_dates(date[0], date[1])
        return dates_test

    def all_dates(self, start_date, issue_id):
        dates = {
            'SA': self.sa_date(start_date, issue_id),
            'DI': self.di_date(issue_id),
            'ALG': self.alg_date(issue_id),
            'SYS': self.sys_date(issue_id),
            'WEB': self.web_date(issue_id),
            'TEST': self.test_date(issue_id)
        }
        return dates
