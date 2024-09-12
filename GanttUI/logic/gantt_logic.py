from datetime import *
from GanttUI.logic.issue_processing import IssueProcessing
from database_objects.database import Database

#В данном классе представлены 4 метода: test_logic(), dev_logic(), study_logic(), open_logic(). 
#Для получения словаря вида {'Task': sa1, 'Start': '2021-01-01', 'Finish': '2021-01-05', 'Resource': task_name}, который
#отсортирован в зависимости от веса задачи (чем больше вес, тем ближе задача располагается к стартовой дате), методы нужно
#вызывать в том порядке, в котором они указаны выше.

#Методы, называющиеся create_resource_..., создают ресурсы, и возвращают их в виде словаря:
#{'<Ресурс (название + номер)>': <ближайшая свободная дата для этого ресурса>}

class GanttLogic():
    def __init__(self, db_name, issue_list):
        self.issproc = IssueProcessing(db_name)
        self.issue_list = issue_list
        self.diagramm_list = []

    def sorted_issue_lists(self):
        open_states_id = ['5', '9', '15', '29', '35']
        study_states_id = ['16']
        dev_states_id = ['6', '10', '17', '30', '36']
        test_states_id = ['13', '18', '31', '37', '41']
        open_issues = []
        study_issues = []
        dev_issues = []
        test_issues = []
        unaccounted_issues = []
        for issue in self.issue_list:
            if type(issue) == int:
                unaccounted_issues.append({
                    'id': issue,
                    'name': issue,
                    'reason': 'Несуществующая задача'
                    })
                continue
            if issue.parent_id != None:
                continue
            grade = self.issproc.get_grade(issue.id)
            if grade['SA'] == 0 and grade['DI'] == 0 and grade['ALG'] == 0 and grade['SYS'] == 0 and grade['WEB'] == 0 and grade['TEST'] == 0:
                unaccounted_issues.append({
                    'id': issue.id,
                    'name': issue.caption,
                    'reason': 'Нет оценки'
                    })
                continue
            if issue != None:
                changes = issue.changes
                for change in reversed(changes):
                    diff = change.diff
                    if '3' in diff.keys():
                        actual_state_id = list(diff['3'].keys())[-1]
                        if actual_state_id in open_states_id:
                            open_issues.append(issue)
                            break
                        elif actual_state_id in study_states_id:
                            study_issues.append(issue)
                            break
                        elif actual_state_id in dev_states_id:
                            dev_issues.append(issue)
                            break
                        elif actual_state_id in test_states_id:
                            test_issues.append(issue)
                            break
                        else:
                            unaccounted_issues.append({
                                'id': issue.id,
                                'name': issue.caption,
                                'reason': 'Несоответствующий статус'
                                })
                            break
        issues_dict = {
            'open': open_issues,
            'study': study_issues,
            'dev': dev_issues,
            'test': test_issues,
            'unaccounted': unaccounted_issues
        }
        return issues_dict

    def create_resource_sa(self, sa_count, start_date):
        self.resources_sa = {}
        for sa_number in range(1, sa_count+1):
            self.resources_sa[f"sa{sa_number}"] = start_date
            self.diagramm_list.append({'Task': f"sa{sa_number}", 'Start': '', 'Finish': '', 'Resource': '(Пустая задача)'})
        return self.resources_sa

    def create_resource_di(self, di_count, start_date):
        self.resources_di = {}
        for di_number in range(1, di_count+1):
            self.resources_di[f"di{di_number}"] = start_date
            self.diagramm_list.append({'Task': f"di{di_number}", 'Start': '', 'Finish': '', 'Resource': '(Пустая задача)'})
        return self.resources_di

    def create_resource_alg(self, alg_count, start_date):
        self.resources_alg = {}
        for alg_number in range(1, alg_count+1):
            self.resources_alg[f"alg{alg_number}"] = start_date
            self.diagramm_list.append({'Task': f"alg{alg_number}", 'Start': '', 'Finish': '', 'Resource': '(Пустая задача)'})
        return self.resources_alg

    def create_resource_sys(self, sys_count, start_date):
        self.resources_sys = {}
        for sys_number in range(1, sys_count+1):
            self.resources_sys[f"sys{sys_number}"] = start_date
            self.diagramm_list.append({'Task': f"sys{sys_number}", 'Start': '', 'Finish': '', 'Resource': '(Пустая задача)'})
        return self.resources_sys

    def create_resource_web(self, web_count, start_date):
        self.resources_web = {}
        for web_number in range(1, web_count+1):
            self.resources_web[f"web{web_number}"] = start_date
            self.diagramm_list.append({'Task': f"web{web_number}", 'Start': '', 'Finish': '', 'Resource': '(Пустая задача)'})
        return self.resources_web

    def create_resource_test(self, test_count, start_date):
        self.resources_test = {}
        for test_number in range(1, test_count+1):
            self.resources_test[f"test{test_number}"] = start_date
            self.diagramm_list.append({'Task': f"test{test_number}", 'Start': '', 'Finish': '', 'Resource': '(Пустая задача)'})
        return self.resources_test   

    def test_logic(self, holidays):
        issues = self.sorted_issue_lists()['test']
        for issue in issues:
            min_free_resource = min(self.resources_test, key=self.resources_test.get)
            min_free_date = self.resources_test[min_free_resource]
            if min_free_resource not in holidays.keys():
                holidays_interval = []
            else:
                holidays_interval = holidays[min_free_resource]
            dates = self.issproc.test_date(issue.id, min_free_date, holidays_interval)
            for date in dates:
                self.diagramm_list.append({'Task': min_free_resource, 'Start': date[0], 'Finish': date[1], 'Resource': f'#{issue.id} {issue.caption}'})
                self.resources_test[min_free_resource] = date[1]

    def dev_logic(self, holidays):
        issues = self.sorted_issue_lists()['dev']
        for issue in issues:
            #Построение alg
            min_free_resource_alg = min(self.resources_alg, key=self.resources_alg.get)
            min_free_date_alg = self.resources_alg[min_free_resource_alg]
            if min_free_resource_alg not in holidays.keys():
                holidays_interval = []
            else:
                holidays_interval = holidays[min_free_resource_alg]
            dates_alg = self.issproc.alg_date(issue.id, min_free_date_alg, holidays_interval)
            for date in dates_alg:
                self.diagramm_list.append({'Task': min_free_resource_alg, 'Start': date[0], 'Finish': date[1], 'Resource': f'#{issue.id} {issue.caption}'})
                self.resources_alg[min_free_resource_alg] = date[1]

            #Построение sys
            min_free_resource_sys = min(self.resources_sys, key=self.resources_sys.get)
            min_free_date_sys = self.resources_sys[min_free_resource_sys]
            try:
                if min_free_date_sys < dates_alg[-1][1]:
                    min_free_date_sys = dates_alg[-1][1]
            except: 
                pass
            if min_free_resource_sys not in holidays.keys():
                holidays_interval = []
            else:
                holidays_interval = holidays[min_free_resource_sys]
            dates_sys = self.issproc.sys_date(issue.id, min_free_date_sys, holidays_interval)
            for date in dates_sys:
                self.diagramm_list.append({'Task': min_free_resource_sys, 'Start': date[0], 'Finish': date[1], 'Resource': f'#{issue.id} {issue.caption}'})
                self.resources_sys[min_free_resource_sys] = date[1]

            #Построение web
            min_free_resource_web = min(self.resources_web, key=self.resources_web.get)
            min_free_date_web = self.resources_web[min_free_resource_web]
            try:
                if min_free_date_web < dates_sys[-1][1]:
                    min_free_date_web = dates_sys[-1][1]
            except: 
                pass
            try:
                if min_free_date_web < dates_alg[-1][1]:
                    min_free_date_web = dates_alg[-1][1]
            except:
                pass
            if min_free_resource_web not in holidays.keys():
                holidays_interval = []
            else:
                holidays_interval = holidays[min_free_resource_web]
            dates_web = self.issproc.web_date(issue.id, min_free_date_web, holidays_interval)
            for date in dates_web:
                self.diagramm_list.append({'Task': min_free_resource_web, 'Start': date[0], 'Finish': date[1], 'Resource': f'#{issue.id} {issue.caption}'})
                self.resources_web[min_free_resource_web] = date[1]

            #Построение test
            min_free_resource_test = min(self.resources_test, key=self.resources_test.get)
            min_free_date_test = self.resources_test[min_free_resource_test]
            try:
                if min_free_date_test < dates_web[-1][1]:
                    min_free_date_test = dates_web[-1][1]
            except: 
                pass
            try:
                if min_free_date_test < dates_alg[-1][1]:
                    min_free_date_test = dates_alg[-1][1]
            except: 
                pass
            try:
                if min_free_date_test < dates_sys[-1][1]:
                    min_free_date_test = dates_sys[-1][1]
            except: 
                pass
            if min_free_resource_test not in holidays.keys():
                holidays_interval = []
            else:
                holidays_interval = holidays[min_free_resource_test]
            dates_test = self.issproc.test_date(issue.id, min_free_date_test, holidays_interval)
            for date in dates_test:
                self.diagramm_list.append({'Task': min_free_resource_test, 'Start': date[0], 'Finish': date[1], 'Resource': f'#{issue.id} {issue.caption}'})
                self.resources_test[min_free_resource_test] = date[1]

    def study_logic(self, holidays):
        issues = self.sorted_issue_lists()['study']
        for issue in issues:
            #Построение sa
            min_free_resource_sa = min(self.resources_sa, key=self.resources_sa.get)
            min_free_date_sa = self.resources_sa[min_free_resource_sa]
            if min_free_resource_sa not in holidays.keys():
                holidays_interval = []
            else:
                holidays_interval = holidays[min_free_resource_sa]
            dates_sa = self.issproc.sa_date(issue.id, min_free_date_sa, holidays_interval)
            for date in dates_sa:
                self.diagramm_list.append({'Task': min_free_resource_sa, 'Start': date[0], 'Finish': date[1], 'Resource': f'#{issue.id} {issue.caption}'})
                self.resources_sa[min_free_resource_sa] = date[1]

            #Построение di
            min_free_resource_di = min(self.resources_di, key=self.resources_di.get)
            min_free_date_di = self.resources_di[min_free_resource_di]
            try:
                if min_free_date_di < dates_sa[-1][1]:
                    min_free_date_di = dates_sa[-1][1]
            except:
                pass
            if min_free_resource_di not in holidays.keys():
                holidays_interval = []
            else:
                holidays_interval = holidays[min_free_resource_di]
            dates_di = self.issproc.di_date(issue.id, min_free_date_di, holidays_interval)
            for date in dates_di:
                self.diagramm_list.append({'Task': min_free_resource_di, 'Start': date[0], 'Finish': date[1], 'Resource': f'#{issue.id} {issue.caption}'})
                self.resources_di[min_free_resource_di] = date[1]

            #Построение alg
            min_free_resource_alg = min(self.resources_alg, key=self.resources_alg.get)
            min_free_date_alg = self.resources_alg[min_free_resource_alg]
            try:
                if min_free_date_alg < dates_di[-1][1]:
                    min_free_date_alg = dates_di[-1][1]
            except: 
                pass
            try:
                if min_free_date_alg < dates_sa[-1][1]:
                    min_free_date_alg = dates_sa[1][1]
            except:
                pass
            if min_free_resource_alg not in holidays.keys():
                holidays_interval = []
            else:
                holidays_interval = holidays[min_free_resource_alg]
            dates_alg = self.issproc.alg_date(issue.id, min_free_date_alg, holidays_interval)
            for date in dates_alg:
                self.diagramm_list.append({'Task': min_free_resource_alg, 'Start': date[0], 'Finish': date[1], 'Resource': f'#{issue.id} {issue.caption}'})
                self.resources_alg[min_free_resource_alg] = date[1]

            #Построение sys
            min_free_resource_sys = min(self.resources_sys, key=self.resources_sys.get)
            min_free_date_sys = self.resources_sys[min_free_resource_sys]
            try:
                if min_free_date_sys < dates_alg[-1][1]:
                    min_free_date_sys = dates_alg[-1][1]
            except: 
                pass
            try:
                if min_free_date_sys < dates_sa[-1][1]:
                    min_free_date_sys = dates_sa[1][1]
            except: 
                pass
            try:
                if min_free_date_sys < dates_di[-1][1]:
                    min_free_date_sys = dates_di[-1][1]
            except: 
                pass
            if min_free_resource_sys not in holidays.keys():
                holidays_interval = []
            else:
                holidays_interval = holidays[min_free_resource_sys]
            dates_sys = self.issproc.sys_date(issue.id, min_free_date_sys, holidays_interval)
            for date in dates_sys:
                self.diagramm_list.append({'Task': min_free_resource_sys, 'Start': date[0], 'Finish': date[1], 'Resource': f'#{issue.id} {issue.caption}'})
                self.resources_sys[min_free_resource_sys] = date[1]

            #Построение web
            min_free_resource_web = min(self.resources_web, key=self.resources_web.get)
            min_free_date_web = self.resources_web[min_free_resource_web]
            try:
                if min_free_date_web < dates_sys[-1][1]:
                    min_free_date_web = dates_sys[-1][1]
            except: 
                pass
            try:
                if min_free_date_web < dates_sa[-1][1]:
                    min_free_date_web = dates_sa[-1][1]
            except: 
                pass
            try:
                if min_free_date_web < dates_di[-1][1]:
                    min_free_date_web = dates_di[-1][1]
            except: 
                pass
            try:
                if min_free_date_web < dates_alg[-1][1]:
                    min_free_date_web = dates_alg[-1][1]
            except:
                pass
            if min_free_resource_web not in holidays.keys():
                holidays_interval = []
            else:
                holidays_interval = holidays[min_free_resource_web]
            dates_web = self.issproc.web_date(issue.id, min_free_date_web, holidays_interval)
            for date in dates_web:
                self.diagramm_list.append({'Task': min_free_resource_web, 'Start': date[0], 'Finish': date[1], 'Resource': f'#{issue.id} {issue.caption}'})
                self.resources_web[min_free_resource_web] = date[1]

            #Построение test
            min_free_resource_test = min(self.resources_test, key=self.resources_test.get)
            min_free_date_test = self.resources_test[min_free_resource_test]
            try:
                if min_free_date_test < dates_web[-1][1]:
                    min_free_date_test = dates_web[-1][1]
            except: 
                pass
            try:
                if min_free_date_test < dates_sa[-1][1]:
                    min_free_date_test = dates_sa[-1][1]
            except: 
                pass
            try:
                if min_free_date_test < dates_di[-1][1]:
                    min_free_date_test = dates_di[-1][1]
            except: 
                pass
            try:
                if min_free_date_test < dates_alg[-1][1]:
                    min_free_date_test = dates_alg[-1][1]
            except: 
                pass
            try:
                if min_free_date_test < dates_sys[-1][1]:
                    min_free_date_test = dates_sys[-1][1]
            except:
                pass
            if min_free_resource_test not in holidays.keys():
                holidays_interval = []
            else:
                holidays_interval = holidays[min_free_resource_test]
            dates_test = self.issproc.test_date(issue.id, min_free_date_test, holidays_interval)
            for date in dates_test:
                self.diagramm_list.append({'Task': min_free_resource_test, 'Start': date[0], 'Finish': date[1], 'Resource': f'#{issue.id} {issue.caption}'})
                self.resources_test[min_free_resource_test] = date[1]

    def open_logic(self, holidays):
        issues = self.sorted_issue_lists()['open']
        for issue in issues:
            #Построение sa
            min_free_resource_sa = min(self.resources_sa, key=self.resources_sa.get)
            min_free_date_sa = self.resources_sa[min_free_resource_sa]
            if min_free_resource_sa not in holidays.keys():
                holidays_interval = []
            else:
                holidays_interval = holidays[min_free_resource_sa]
            dates_sa = self.issproc.sa_date(issue.id, min_free_date_sa, holidays_interval)
            for date in dates_sa:
                self.diagramm_list.append({'Task': min_free_resource_sa, 'Start': date[0], 'Finish': date[1], 'Resource': f'#{issue.id} {issue.caption}'})
                self.resources_sa[min_free_resource_sa] = date[1]

            #Построение di
            min_free_resource_di = min(self.resources_di, key=self.resources_di.get)
            min_free_date_di = self.resources_di[min_free_resource_di]
            try:
                if min_free_date_di < dates_sa[-1][1]:
                    min_free_date_di = dates_sa[-1][1]
            except:
                pass
            if min_free_resource_di not in holidays.keys():
                holidays_interval = []
            else:
                holidays_interval = holidays[min_free_resource_di]
            dates_di = self.issproc.di_date(issue.id, min_free_date_di, holidays_interval)
            for date in dates_di:
                self.diagramm_list.append({'Task': min_free_resource_di, 'Start': date[0], 'Finish': date[1], 'Resource': f'#{issue.id} {issue.caption}'})
                self.resources_di[min_free_resource_di] = date[1]

            #Построение alg
            min_free_resource_alg = min(self.resources_alg, key=self.resources_alg.get)
            min_free_date_alg = self.resources_alg[min_free_resource_alg]
            try:
                if min_free_date_alg < dates_di[-1][1]:
                    min_free_date_alg = dates_di[-1][1]
            except: 
                pass
            try:
                if min_free_date_alg < dates_sa[-1][1]:
                    min_free_date_alg = dates_sa[1][1]
            except:
                pass
            if min_free_resource_alg not in holidays.keys():
                holidays_interval = []
            else:
                holidays_interval = holidays[min_free_resource_alg]
            dates_alg = self.issproc.alg_date(issue.id, min_free_date_alg, holidays_interval)
            for date in dates_alg:
                self.diagramm_list.append({'Task': min_free_resource_alg, 'Start': date[0], 'Finish': date[1], 'Resource': f'#{issue.id} {issue.caption}'})
                self.resources_alg[min_free_resource_alg] = date[1]

            #Построение sys
            min_free_resource_sys = min(self.resources_sys, key=self.resources_sys.get)
            min_free_date_sys = self.resources_sys[min_free_resource_sys]
            try:
                if min_free_date_sys < dates_alg[-1][1]:
                    min_free_date_sys = dates_alg[-1][1]
            except: 
                pass
            try:
                if min_free_date_sys < dates_sa[-1][1]:
                    min_free_date_sys = dates_sa[1][1]
            except: 
                pass
            try:
                if min_free_date_sys < dates_di[-1][1]:
                    min_free_date_sys = dates_di[-1][1]
            except: 
                pass
            if min_free_resource_sys not in holidays.keys():
                holidays_interval = []
            else:
                holidays_interval = holidays[min_free_resource_sys]
            dates_sys = self.issproc.sys_date(issue.id, min_free_date_sys, holidays_interval)
            for date in dates_sys:
                self.diagramm_list.append({'Task': min_free_resource_sys, 'Start': date[0], 'Finish': date[1], 'Resource': f'#{issue.id} {issue.caption}'})
                self.resources_sys[min_free_resource_sys] = date[1]

            #Построение web
            min_free_resource_web = min(self.resources_web, key=self.resources_web.get)
            min_free_date_web = self.resources_web[min_free_resource_web]
            try:
                if min_free_date_web < dates_sys[-1][1]:
                    min_free_date_web = dates_sys[-1][1]
            except: 
                pass
            try:
                if min_free_date_web < dates_sa[-1][1]:
                    min_free_date_web = dates_sa[-1][1]
            except: 
                pass
            try:
                if min_free_date_web < dates_di[-1][1]:
                    min_free_date_web = dates_di[-1][1]
            except: 
                pass
            try:
                if min_free_date_web < dates_alg[-1][1]:
                    min_free_date_web = dates_alg[-1][1]
            except:
                pass
            if min_free_resource_web not in holidays.keys():
                holidays_interval = []
            else:
                holidays_interval = holidays[min_free_resource_web]
            dates_web = self.issproc.web_date(issue.id, min_free_date_web, holidays_interval)
            for date in dates_web:
                self.diagramm_list.append({'Task': min_free_resource_web, 'Start': date[0], 'Finish': date[1], 'Resource': f'#{issue.id} {issue.caption}'})
                self.resources_web[min_free_resource_web] = date[1]

            #Построение test
            min_free_resource_test = min(self.resources_test, key=self.resources_test.get)
            min_free_date_test = self.resources_test[min_free_resource_test]
            try:
                if min_free_date_test < dates_web[-1][1]:
                    min_free_date_test = dates_web[-1][1]
            except: 
                pass
            try:
                if min_free_date_test < dates_sa[-1][1]:
                    min_free_date_test = dates_sa[-1][1]
            except: 
                pass
            try:
                if min_free_date_test < dates_di[-1][1]:
                    min_free_date_test = dates_di[-1][1]
            except: 
                pass
            try:
                if min_free_date_test < dates_alg[-1][1]:
                    min_free_date_test = dates_alg[-1][1]
            except: 
                pass
            try:
                if min_free_date_test < dates_sys[-1][1]:
                    min_free_date_test = dates_sys[-1][1]
            except:
                pass
            if min_free_resource_test not in holidays.keys():
                holidays_interval = []
            else:
                holidays_interval = holidays[min_free_resource_test]
            dates_test = self.issproc.test_date(issue.id, min_free_date_test, holidays_interval)
            for date in dates_test:
                self.diagramm_list.append({'Task': min_free_resource_test, 'Start': date[0], 'Finish': date[1], 'Resource': f'#{issue.id} {issue.caption}'})
                self.resources_test[min_free_resource_test] = date[1]  
