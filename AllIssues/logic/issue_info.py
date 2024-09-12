from database_objects.information_seeker import InformationSeeker

class IssueInfo():
    def __init__(self, database, issue):
        self.information_seeker = InformationSeeker(database)
        self.issue = issue

    def find_actual_state(self):
        return self.information_seeker.state_caption(self.issue.state_id)
    
    def find_project_caption(self):
        return self.information_seeker.project_caption(self.issue.project_id)

    def find_version_caption(self):
        return self.information_seeker.version_caption(self.issue.version_id)
    
    def create_issue_date(self):
        '''Возвращает не только дату создания, но и имя пользователя, который создал запрос'''
        create_change = self.issue.changes[0]
        date = create_change.date_time
        try:
            user = self.information_seeker.user(create_change.user_id)
            user_name = f'{user.first_name} {user.last_name}'
        except:
            user_name = None
        return date, user_name
    
    def last_change_issue(self):
        '''Возвращает не только дату последнего изменения, но и имя пользователя, который совершил это изменение'''
        last_change = self.issue.changes[-1]
        date = last_change.date_time
        try:
            user = self.information_seeker.user(last_change.user_id)
            user_name = f'{user.first_name} {user.last_name}'
        except:
            user_name = None
        return date, user_name