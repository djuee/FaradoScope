from database_objects.information_seeker import InformationSeeker

class FieldsChecker():
    separator = ', ' # разделитель нескольких значений

    def __init__(self, database):
        self.information_seeker = InformationSeeker(database)
        self.field_kinds = self.information_seeker.create_field_kinds_dict()

    def find_fields(self, issue):
        all_fields = {key: '' for key in self.field_kinds.keys()}
        for field in issue.fields:
            if field is None:
                continue
            value_type = self.information_seeker.field_value_type(field)
            for field_kind in self.field_kinds:
                if field.field_kind_id in self.field_kinds[field_kind]:
                    if value_type == 'value':
                        all_fields[field_kind] = field.value
                    if value_type == 'issue_id':
                        all_fields[field_kind] = f'{field.value} {self.information_seeker.issue_caption(field.value)}'
                    if value_type == 'project_id':
                        all_fields[field_kind] = f'{field.value} {self.information_seeker.project_caption(field.value)}'
                    if value_type == 'user_id':
                        user = self.information_seeker.user(field.value)
                        if user is None:
                            break
                        all_fields[field_kind] = f'{field.value} {user.first_name} {user.last_name}'
                    if value_type == 'version_id':
                        all_fields[field_kind] = f'{field.value} {self.information_seeker.version_caption(field.value)}'
                    if value_type == 'issues_id':
                        issues_caption_list = []
                        issues_id = field.value.split(',')
                        if len(issues_id) < 1 or issues_id[0] == 0:
                            break
                        for issue_id in issues_id:
                            issues_caption_list.append(f'{field.value} {self.information_seeker.issue_caption(field.value)}')
                        all_fields[field_kind] = self.separator.join(issues_caption_list)
                    if value_type == 'projects_id':
                        projects_caption_list = []
                        projects_id = field.value.split(',')
                        if len(projects_id) < 1 or projects_id[0] == 0:
                            break
                        for project_id in projects_id:
                            projects_caption_list.append(f'{field.value} {self.information_seeker.project_caption(field.value)}')
                        all_fields[field_kind] = self.separator.join(projects_caption_list)
                    if value_type == 'users_id':
                        users_caption_list = []
                        users_id = field.value.split(',')
                        if len(users_id) < 1 or users_id[0] == 0:
                            break
                        for user_id in users_id:
                            user = self.information_seeker.user(field.value)
                            if user is None:
                                continue
                            users_caption_list.append(f'{field.value} {user.first_name} {user.last_name}')
                        all_fields[field_kind] = self.separator.join(users_caption_list)
                    if value_type == 'versions_id':
                        versions_caption_list = []
                        versions_id = field.value.split(',')
                        if len(versions_id) < 1 or versions_id[0] == 0:
                            break
                        for version_id in versions_id:
                            versions_caption_list.append(f'{field.value} {self.information_seeker.version_caption(field.value)}')
                        all_fields[field_kind] = self.separator.join(versions_caption_list)
                    break
        return all_fields
