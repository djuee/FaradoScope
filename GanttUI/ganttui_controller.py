import plotly.figure_factory as ff
import random
import re
from GanttUI.logic.gantt_logic import GanttLogic
from database_objects.database import Database
from GanttUI.logic.time_logic import TimeLogic

class GanttUIController():
    def __init__(self, database):
        self.issue_list = []
        self.database = database

    def create_holidays(self, resources, start_dates, end_dates):
        '''Выходные для каждого ресурса сохраняются парами: (дата начала, дата конца, дата начала, дата конца)'''
        time = TimeLogic()
        holidays = {}
        for number in range(len(resources)):
            if resources[number] not in holidays.keys():
                holidays[resources[number]] = [(time.str_to_datetime(start_dates[number]), time.str_to_datetime(end_dates[number]))]
            else:
                holidays[resources[number]].append((time.str_to_datetime(start_dates[number]), time.str_to_datetime(end_dates[number])))
            self.gantt.diagramm_list.append({'Task': resources[number], 'Start': start_dates[number], 'Finish': end_dates[number], 'Resource': 'Нерабочие дни'})
        return holidays

    def create_resources(self, start_date, sa_count=1, di_count=1, alg_count=1, sys_count=1, web_count=1, test_count=1):
        resources = {}
        self.gantt = GanttLogic(self.database, self.issue_list)
        self.gantt.create_resource_sa(sa_count, start_date)
        self.gantt.create_resource_di(di_count, start_date)
        self.gantt.create_resource_alg(alg_count, start_date)
        self.gantt.create_resource_sys(sys_count, start_date)
        self.gantt.create_resource_web(web_count, start_date)
        self.gantt.create_resource_test(test_count, start_date)
        for sa in self.gantt.resources_sa.keys():
            resources[sa] = sa
        for di in self.gantt.resources_di.keys():
            resources[di] = di
        for alg in self.gantt.resources_alg.keys():
            resources[alg] = alg 
        for sys in self.gantt.resources_sys.keys():
            resources[sys] = sys
        for web in self.gantt.resources_web.keys():
            resources[web] = web
        for test in self.gantt.resources_test.keys():
            resources[test] = test
        return resources

    def create_dict_by_gantt(self, resources, start_dates_holidays, end_dates_holidays):
        holidays = self.create_holidays(resources, start_dates_holidays, end_dates_holidays)
        self.gantt.test_logic(holidays)
        self.gantt.dev_logic(holidays)
        self.gantt.study_logic(holidays)
        self.gantt.open_logic(holidays)

    def unaccounted_issues(self):
        return self.gantt.sorted_issue_lists()['unaccounted']

    def create_gantt(self):
        tasks = self.gantt.diagramm_list
        colors = {}
        colors['Нерабочие дни'] = 'rgb(255, 255, 255)'
        colors['(Пустая задача)'] = 'rgb(222, 255, 255)'
        for issue in tasks:
            if issue['Resource'] != '(Пустая задача)' and issue['Resource'] != 'Нерабочие дни':
                r = random.randint(1, 255)
                g = random.randint(1, 255)
                b = random.randint(1, 255)
                colors[issue['Resource']] = f"rgb({r}, {g}, {b})"
        fig = ff.create_gantt(tasks, colors=colors, index_col='Resource', show_colorbar=True, group_tasks=True, showgrid_x=True, showgrid_y=True)
        fig.show()