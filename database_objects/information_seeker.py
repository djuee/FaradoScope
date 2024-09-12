from database_objects.user import User
from database_objects.database import Database

'''Практически все методы, представленные здесь, нужны для оптимизации утилиты "AllIssues". Они позволяют не создавать большие объекты, а вытаскивать инф-цию из базы'''

class InformationSeeker():
    def __init__(self, database):
        self.db = Database(database)

    def user(self, user_id):
        cursor = self.db.conn.cursor()
        cursor.execute('''SELECT * from users WHERE users.id=?''', (user_id, ))
        try:
            user_info = cursor.fetchone()
            user = User()
            user.id = user_id
            user.login = user_info[1]
            user.first_name = user_info[2]
            user.middle_name = user_info[3]
            user.last_name = user_info[4]
            user.email = user_info[5]
            return user
        except:
            return None

    def create_field_kinds_dict(self):
        field_kinds = {}
        cursor = self.db.conn.cursor()
        cursor.execute('''SELECT field_kinds.id, field_kinds.caption FROM field_kinds''')
        for field_kind in cursor.fetchall():
            field_kind_id = field_kind[0]
            field_kind_caption = field_kind[1]
            if field_kind_caption in field_kinds.keys():
                field_kinds[field_kind_caption].append(field_kind_id)
                continue
            field_kinds[field_kind_caption] = [field_kind_id]
        return field_kinds

    def field_value_type(self, field) -> str:
        one_value = [0, 1, 2, 3, 4, 5, 6, 50, 51] # содержит те value_type, когда в поле хранится не id, а готовое значение
        cursor = self.db.conn.cursor()
        try:
            cursor.execute('''SELECT field_kinds.value_type FROM field_kinds WHERE field_kinds.id=?''', (field.field_kind_id, ))
            value_type = cursor.fetchone()[0]
        except:
            return None
        if value_type in one_value: 
            return 'value'
        if value_type == 100:
            return 'issue_id'
        if value_type == 101:
            return 'user_id'
        if value_type == 102:
            return 'project_id'
        if value_type == 103:
            return 'version_id'
        if value_type == 200:
            return 'issues_id'
        if value_type == 201:
            return 'users_id'
        if value_type == 202:
            return 'projects_id'
        if value_type == 203:
            return 'versions_id'
        return None
    
    def issue_caption(self, issue_id):
        cursor = self.db.conn.cursor()
        try:
            cursor.execute('''SELECT issues.caption FROM issues WHERE issues.id=?''', (issue_id, ))
            return cursor.fetchone()[0]
        except:
            return None

    def project_caption(self, project_id):
        cursor = self.db.conn.cursor()
        try:
            cursor.execute('''SELECT projects.caption FROM projects WHERE projects.id=?''', (project_id, ))
            return cursor.fetchone()[0]
        except:
            return None
    
    def version_caption(self, version_id):
        cursor = self.db.conn.cursor()
        try:
            cursor.execute('''SELECT versions.caption FROM versions WHERE versions.id=?''', (version_id, ))
            return cursor.fetchone()[0]
        except:
            return None

    def state_caption(self, state_id):
        cursor = self.db.conn.cursor()
        try:
            cursor.execute('''SELECT states.caption FROM states WHERE states.id=?''', (state_id, ))
            return cursor.fetchone()[0]
        except:
            return None

