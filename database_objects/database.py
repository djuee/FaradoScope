import sqlite3 as sq
import json
import asyncio
import re
from threading import Lock

from database_objects.project import Project
from database_objects.version import Version
from database_objects.issue import Issue
from database_objects.change import Change
from database_objects.field import Field
from database_objects.comment import Comment

class Database():
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:  
                if not cls._instance: 
                    cls._instance = super(Database, cls).__new__(cls)
                    cls._instance._initialize(*args, **kwargs)
        return cls._instance
    
    def _initialize(self, db_name):
        self.conn = sq.connect(db_name, check_same_thread=False)

    def initialization(self):
        conn = sq.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM issues, projects, fields, versions, issue_changes, comments''')

    def project(self, project_id):
        '''Метод возвращает объект класса Project'''
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM projects WHERE projects.id=?''', (project_id, ))
        try:
            project_info = cursor.fetchone()
            project = Project()
            project.id = project_id
            project.caption = project_info[1]
            project.content = project_info[2]
            project.issues_view_settings = project_info[3]
            project.versions = self.versions_by_project(project_id)
            return project
        except:
            return None

    def version(self, version_id):
        '''Метод возвращает объект класса Version'''
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM versions WHERE versions.id=?''', (version_id, ))
        try:
            version_info = cursor.fetchone()
            version = Version()
            version.id = version_id
            version.caption = version_info[1]
            version.content = version_info[2]
            version.project_id = version_info[3]
            version.start_date = version_info[4]
            version.release_date = version_info[5]
            version.issues = self.issues_by_versions(version.id)
            return version
        except:
            return None

    def issue(self, issue_id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM issues WHERE issues.id=?''', (issue_id, ))
        try:
            issue_info = cursor.fetchone()
            issue = Issue()
            issue.id = issue_id
            issue.issue_kind_id = issue_info[1]
            issue.parent_id = issue_info[2]
            issue.project_id = issue_info[3]
            issue.state_id = issue_info[4]
            issue.caption = issue_info[5]
            issue.content = issue_info[6]
            issue.version_id = issue_info[7]
            issue.fields, issue.comments, issue.changes = asyncio.run(self.asyncio_fields_find(issue_id))
            issue.kids = self.find_kids_by_issue(issue_id)
            return issue
        except:
            return None

    def field(self, field_id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM fields WHERE fields.id=?''', (field_id, ))
        try:
            field_info = cursor.fetchone()
            field = Field()
            field.id = field_id
            field.issue_id = field_info[1]
            field.field_kind_id = field_info[2]
            field.value = field_info[3]
            return field
        except:
            return None
    
    def change(self, change_id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM issue_changes WHERE issue_changes.id=?''', (change_id, ))
        try:
            change_info = cursor.fetchone()
            change = Change()
            change.id = change_id
            change.issue_id = change_info[1]
            change.diff = json.loads(change_info[2])
            change.user_id = change_info[3]
            change.date_time = change_info[4][:-7]
            return change
        except:
            return None

    def comment(self, comment_id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM comments WHERE comments.id=?''', (comment_id, ))
        try:
            comment_info = cursor.fetchone()
            comment = Comment()
            comment.id = comment_id
            comment.issue_id = comment_info[1]
            comment.user_id = comment_info[2]
            comment.creation_datetime = comment_info[3]
            comment.content = comment_info[4]
            return comment
        except:
            return None

    def versions_by_project(self, project_id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT versions.id FROM versions WHERE versions.project_id=?''', (project_id, ))
        versions_container = []
        for version_id in cursor.fetchall():
            version = self.version(version_id[0])
            versions_container.append(version)
        return versions_container

    def issues_by_versions(self, version_id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT issues.id FROM issues WHERE issues.version_id=?''', (version_id, ))
        issues_container = []
        for issue_id in cursor.fetchall():
            issue = self.issue(issue_id[0])
            issues_container.append(issue)
        return issues_container

    async def fields_by_issue(self, issue_id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT fields.id FROM fields WHERE fields.issue_id=?''', (issue_id, ))
        fields_container = []
        for field_id in cursor.fetchall():
            field = self.field(field_id[0])
            fields_container.append(field)
            await asyncio.sleep(0)
        return fields_container

    async def changes_by_issue(self, issue_id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT issue_changes.id FROM issue_changes WHERE issue_changes.issue_id=?''', (issue_id, ))
        changes_container = []
        for change_id in cursor.fetchall():
            change = self.change(change_id[0])
            changes_container.append(change)
            await asyncio.sleep(0)
        return changes_container

    def find_kids_by_issue(self, issue_id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT issues.id FROM issues WHERE issues.parent_id=?''', (issue_id, ))
        kids_container = []
        for kid_id in cursor.fetchall():
            kid = self.issue(kid_id[0])
            kids_container.append(kid)
        return kids_container

    async def comments_by_issue(self, issue_id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT comments.id FROM comments WHERE comments.issue_id=?''', (issue_id, ))
        comments_container = []
        for comment_id in cursor.fetchall():
            comment = self.comment(comment_id[0])
            comments_container.append(comment)
            await asyncio.sleep(0)
        return comments_container

    async def asyncio_fields_find(self, issue_id):
        fields = asyncio.create_task(self.fields_by_issue(issue_id))
        comments = asyncio.create_task(self.comments_by_issue(issue_id))
        changes = asyncio.create_task(self.changes_by_issue(issue_id))
        return await fields, await comments, await changes

    def all_projects(self):
        '''Функция возвращает не объекты класса Projects, а словари с id проекта, caption и списком версий. Это сделано для оптимизации'''
        cursor = self.conn.cursor()
        cursor2 = self.conn.cursor()
        cursor.execute('''SELECT projects.id, projects.caption FROM projects''')
        projects = []
        for project in cursor.fetchall():
            versions = []
            cursor2.execute('''SELECT versions.caption FROM versions WHERE versions.project_id=?''', (project[0], ))
            for version in cursor2.fetchall():
                versions.append(version[0])
            projects.append({
                'id': project[0],
                'caption': project[1] if '"' not in project[1] else project[1].replace('"', ' '),
                'versions': sorted(versions, key=version_key)
            })
        return projects

    def all_issues(self):
        issues_list = []
        cursor = self.conn.cursor()
        cursor.execute('''SELECT issues.id FROM issues''')
        for issue_id in cursor.fetchall():
            issues_list.append(self.issue(int(issue_id[0])))
        return issues_list

def version_key(version):
    parts = re.split(r'\.', version)
    return [int(part) if part.isdigit() else float('inf') for part in parts]  # Используем float('inf') для нечисловых частей