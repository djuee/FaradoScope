from database_objects.database import Database
from Checker.checker_controller import CheckerController
from GanttUI.ganttui_controller import GanttUIController
from TimeCalculator.time_calculator_controller import TimeCalculatorController
from AllIssues.all_issues_controller import AllIssuesController
from initialization import Initialization

class Controller():
    def __init__(self):
        initialization = Initialization()
        self.port, self.database, self.pause_parameter, self.checker_csv, self.calculator_csv = initialization.initialization_config()
        self.checker = CheckerController()
        self.gantt = GanttUIController(self.database)
        self.calculator = TimeCalculatorController(self.pause_parameter)
        self.all_issues = AllIssuesController(self.database)
        self.db = Database(self.database)
        self.issue_list = []
    
    def create_projects_list(self):
        return self.db.all_projects()
    
    def create_issues_by_projects_versions(self, project_id, version_caption):
        target_version = None
        project = self.db.project(project_id)
        for version in project.versions:
            if version.caption == version_caption:
                target_version = version
                break
        for issue in target_version.issues:
            if issue.issue_kind_id != 1 or issue is None:
                continue
            self.issue_list.append(issue)
        self.pass_the_list()
    
    def create_issues_by_range(self, start, end):
        for num in range(start, end+1):
            issue = self.db.issue(int(num))
            if issue is None:
                continue
            elif issue.issue_kind_id != 1:
                continue
            self.issue_list.append(issue)
        self.pass_the_list()
    
    def create_issues_by_id_list(self, id_str):
        for num in id_str.split():
            issue = self.db.issue(int(num))
            if issue is None:
                continue
            elif issue.issue_kind_id != 1:
                continue
            self.issue_list.append(issue)
        self.pass_the_list()

    def pass_the_list(self):
        self.checker.issue_list = self.issue_list
        self.calculator.issue_list = self.issue_list
        self.gantt.issue_list = self.issue_list

    def checker_data(self):
        return self.checker.create_dict_by_table(self.checker_csv)

    def time_calculator_data(self):
        return self.calculator.create_dict(self.calculator_csv)

    def all_issues_create(self):
        self.all_issues.issue_list = self.db.all_issues()
        return self.all_issues.create_dict_by_table()

    def clear(self):
        self.issue_list = []