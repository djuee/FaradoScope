import csv
from datetime import datetime
from database_objects.database import Database
from Checker.logic.creator import Creator

class CheckerController():
    def __init__(self):
        self.issue_list = []
        self.creator = Creator()

    def csv_creator(self, data):
        csv_file = f'checker ({datetime.now()}).csv'
        csv_file = csv_file.replace(':', '-')
        with open(f"./download_csv/{csv_file}", mode='w', newline='', encoding='utf-8') as file:
            try:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()            
                writer.writerows(data)
            except:
                pass

    def create_dict_by_table(self, create_csv):
        self.creator.input_issue(self.issue_list)
        data = self.creator.tasks_data()
        if create_csv == "y":
            self.csv_creator(data)
        return data



