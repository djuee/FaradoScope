import asyncio
import csv
import math
from datetime import *
from TimeCalculator.logic.issue_processing import IssueProcessing

class TimeCalculatorController():
    def __init__(self, pause_parameter):
        self.issue_list = []
        self.pause_parameter = pause_parameter
        self.issue_processing = IssueProcessing()

    def _sorted_dict(self, tasks_data):
        order = {'Беклог': 1, 'Открыто': 2, 'Исследование': 3, 'Разработка': 4, 'Контроль качества': 5, 'Выполнено': 6, 'Архив': 7, 'Отмена': 8, 'Итого': 9}
        sorted_tasks_data = sorted(tasks_data, key=lambda x: order.get(x['state'], float('inf')), reverse=False)
        return sorted_tasks_data

    def csv_creator(self, data):
        csv_file = f'time_calculator ({datetime.now()}).csv'
        csv_file = csv_file.replace(':', '-')
        with open(f"./download_csv/{csv_file}", mode='w', newline='', encoding='utf-8') as file:
            try:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()            
                writer.writerows(data)
            except:
                pass 

    def create_dict(self, create_csv):
        tasks_data = []
        for issue in self.issue_list:
            if issue is None or issue.issue_kind_id != 1:
                continue
            source, state, grade, pause, realtime = asyncio.run(self.issue_processing.async_run(issue, self.pause_parameter))
            tasks_data.append({
                'id': issue.id,
                'name': issue.caption,
                'source': source,
                'state': state,
                'SA': grade[0]['SA'] if grade[0]['SA'] != 0 else '',
                'DI': grade[0]['DI'] if grade[0]['DI'] != 0 else '',
                'ALG': grade[0]['ALG'] if grade[0]['ALG'] != 0 else '',
                'WEB': grade[0]['WEB'] if grade[0]['WEB'] != 0 else '',
                'SYS': grade[0]['SYS'] if grade[0]['SYS'] != 0 else '',
                'TEST': grade[0]['TEST'] if grade[0]['TEST'] != 0 else '',
                'sum_grade': grade[1],
                'pause': pause[0]//86400,
                'pause_count': pause[1],
                'realtime': math.ceil(realtime/86400)
            })
        total_issues_count = len(tasks_data)
        total_sa = sum(sa['SA'] for sa in tasks_data if sa['SA'] != '')
        total_di = sum(di['DI'] for di in tasks_data if di['DI'] != '')
        total_alg = sum(alg['ALG'] for alg in tasks_data if alg['ALG'] != '')
        total_web = sum(web['WEB'] for web in tasks_data if web['WEB'] != '')
        total_sys = sum(sys['SYS'] for sys in tasks_data if sys['SYS'] != '')
        total_test = sum(test['TEST'] for test in tasks_data if test['TEST'] != '')
        total_sum_grade = sum(grade['sum_grade'] for grade in tasks_data if grade['sum_grade'] != '')
        total_pause = sum(pause['pause'] for pause in tasks_data if pause['pause'] != '')
        total_pause_count = sum(count['pause_count'] for count in tasks_data if count['pause_count'] != '')
        total_realtime = sum(realtime['realtime'] for realtime in tasks_data if realtime['realtime'] != '')
        tasks_data.append({
            'state': total_issues_count,
            'source': 'Итого',
            'SA': total_sa,
            'DI': total_di,
            'ALG': total_alg,
            'WEB': total_web,
            'SYS': total_sys,
            'TEST': total_test,
            'sum_grade': total_sum_grade,
            'pause': total_pause,
            'pause_count': total_pause_count,
            'realtime': total_realtime,
            })
        sorted_dict = self._sorted_dict(tasks_data)
        if create_csv == "y":
            self.csv_creator(sorted_dict)
        return sorted_dict