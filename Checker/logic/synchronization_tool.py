import platform
import os
from Checker.logic.windows_synchronization import WindowsSynchronization
from Checker.logic.linux_synchronization import LinuxSynchronization

class SynchronizationTool():
    def __init__(self):
        self.system = platform.system()
        if self.system == 'Windows':
            self.folders = WindowsSynchronization().list_folders()
        else:
            print('Пожалуйста, авторизируйтесь!')
            username = input('Username: ')
            password = input('Password: ')
            self.LS = LinuxSynchronization(username, password)
            self.LS.connect()
            self.folders = self.LS.list_folders()
            self.LS.close()

    def generate_name(self, issue):
        name = f'FA#{issue.id} {issue.caption}'
        return name

    def search_folders(self, issue):
        issue_name = self.generate_name(issue)
        if issue_name in self.folders:
            return ''
        return False