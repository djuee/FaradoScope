import json
import socket
import os
import glob
import sys
from database_objects.database import Database

class Initialization():
    def initialization_config(self):
        with open("config.json", "r") as cfg:
            config = json.load(cfg)
        try:
            port = int(config["global"]['port'])
        except:
            pass
        if self.check_port('localhost', port):
            port = self.find_free_port()
            print('В config.json был задан некорректный/занятый порт! Автоматически найден свободный порт: ', port)
        database = config["global"]['database']
        if database == "":
            database = self.find_database()
            if database == None:
                sys.exit()
        pause_parameter = int(config["time_calculator"]["pause_parameter"])
        checker_csv = config["checker"]["csv_create"] # будет ли создаваться csv-файл Cherker'a (y/n)
        calculator_csv = config["time_calculator"]["csv_create"] # будет ли создаваться csv-файл TimeCalculator'a (y/n)
        return port, database, pause_parameter, checker_csv, calculator_csv

    def check_port(self, host, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2) 
            result = sock.connect_ex((host, port))
            if result == 0:
                return True
            else:
                return False
        except Exception as e:
            return False
        finally:
            sock.close()

    def find_free_port(self):
        port = 5000
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('localhost', port)) != 0:  
                    return port
                port += 1  

    def find_database(self):
        database_folder = 'database'
        path = os.path.join(os.getcwd(), database_folder, "*.sqlite")
        sqlite_files = glob.glob(path)
        if not sqlite_files:
            print("База данных не найдена автоматически. Пожалуйста, укажите её вручную в config.json и запустите утилиту заново.")
            return None
        latest_file = max(sqlite_files, key=os.path.getmtime)
        return latest_file