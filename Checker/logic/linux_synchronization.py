from smb.SMBConnection import SMBConnection
from smb.smb_structs import OperationFailure

class LinuxSynchronization():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.server = 'synology_nas.local'
        self.share = 'analytic'
        self.conn = None

    def connect(self):
        try:
            self.conn = SMBConnection(self.username, self.password, "client_name", self.server, use_ntlm_v2=True)
            self.conn.connect(self.server)
            print("Соединение установлено.")
        except OperationFailure as e:
            if e.get_error_code() == 0xC000006D: 
                print("Ошибка: Неправильное имя пользователя или пароль.")
            else:
                print(f"Ошибка при подключении: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def list_folders(self):
        all_folders = []
        if self.conn:
            try:
                folders = self.conn.listPath(self.share, '/')
                for folder in folders:
                    if folder.isDirectory:
                        all_folders.append(folder.filename)
            except Exception as e:
                print(f"Ошибка при получении папок: {e}")
        return all_folders

    def close(self):
        if self.conn:
            try:
                self.conn.close()
                print("Соединение закрыто.")
            except Exception as e:
                print(f"Ошибка при закрытии соединения: {e}")