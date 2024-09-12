from AllIssues.logic.fields_checker import FieldsChecker
from AllIssues.logic.issue_info import IssueInfo

class AllIssuesController():
    def __init__(self, database):
        self.database = database
        self.fields_checker = FieldsChecker(self.database)
        self.issue_list = []

    def create_dict_by_table(self):
        dicts_by_table = []
        for issue in self.issue_list:
            issue_info = IssueInfo(self.database, issue)
            create_change = issue_info.create_issue_date()
            last_change = issue_info.last_change_issue()
            info_dict = {
                'Номер': issue.id,
                'Название': issue.caption,
                'Статус': issue_info.find_actual_state(),
                'Проект': issue_info.find_project_caption(),
                'Версия': issue_info.find_version_caption(),
                'Дата создания': create_change[0],
                'Создатель': create_change[1],
                'Последнее изменение': last_change[0],
                'Последний изменивший': last_change[1],
            }
            issue_fields = self.fields_checker.find_fields(issue)
            dicts_by_table.append({**info_dict, **issue_fields})
        return dicts_by_table