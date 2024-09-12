import os

class WindowsSynchronization():
    def __init__(self):
        self.path = r'\\Synology_NAS\ANALYTIC'

    def list_folders(self):
        folders = []
        if os.path.exists(self.path):
            for item in os.listdir(self.path):
                full_path = os.path.join(self.path, item)
                if os.path.isdir(full_path):
                    folders.append(item)
        else:
            print('Директория для синхронизации не найдена!')
        return folders