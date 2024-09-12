import fnmatch
import asyncio
from Checker.logic.issue_checker import IssueChecker
from Checker.logic.synchronization_tool import SynchronizationTool

class Creator():
    def __init__(self):
        y_n = input('Произвести синхронизацию? (y/n)')
        if fnmatch.fnmatch(y_n, '*y*') and ('n' not in y_n):
            self.synchronization = SynchronizationTool()
        else:
            self.synchronization = False

    def input_issue(self, issue_list):
        self.issue_list = issue_list
    
    def tasks_data(self):
        tasks_data = []
        for issue in self.issue_list:
            if issue == None or issue.issue_kind_id != 1:
                continue
            checker = IssueChecker(issue)
            requirements, grade, layout, performer_at_kids, develop_departments, state, performer, versions, test, playback, documentation, correction, basic_request_in_issue = asyncio.run(checker.async_run())
            tasks_data.append({
                'id': issue.id,
                'name': issue.caption,
                'check_synchronization': self.synchronization.search_folders(issue) if self.synchronization != False else False,
                'check_requirements': requirements if requirements is False else '',
                'check_grade': grade if grade is False else '',
                'check_layout': layout if layout is False else '',
                'check_performer_at_kids': performer_at_kids if performer_at_kids is False else '',
                'check_develop_department': develop_departments if develop_departments is False else '',
                'check_state': state if state is False else '',
                'check_performer': performer if performer is False else '',
                'check_versions': versions if versions is False else '',
                'check_test': test if test is False else '',
                'check_playback': playback if playback is False else '',
                'check_documentation': documentation if documentation is False else '',
                'check_correction': correction if correction != 0 else False,
                'check_basic_request': basic_request_in_issue if basic_request_in_issue is False else '',
                'count_kids': len(issue.kids) if len(issue.kids) != 0 else False
            })
        return tasks_data

