from flask import *
import json
from controller import Controller

class View():
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'secret_key'
        self.controller = Controller()
        self.main()

    def main(self):
        @self.app.route('/')
        def main():
            self.controller.clear()
            return render_template('main/principle.html')

        @self.app.route('/projectversion', methods=['GET', 'POST'])
        def projectversion():
            if request.method == 'POST':
                project = request.form.get('project')
                version = request.form.get('version')
                self.controller.create_issues_by_projects_versions(project, version)
                return redirect(url_for('tools'))
            return render_template('main/projectversion.html', projects=self.controller.create_projects_list())

        @self.app.route('/range', methods=['GET', 'POST'])
        def range_():
            if request.method == 'POST':
                start = int(request.form.get('start'))
                end = int(request.form.get('end'))
                self.controller.create_issues_by_range(start, end)
                return redirect(url_for('tools'))
            return render_template('main/range.html')

        @self.app.route('/tasklist', methods=['GET', 'POST'])
        def tasklist():
            if request.method == 'POST':
                task_numbers = request.form.get('taskNumbers')
                self.controller.create_issues_by_id_list(task_numbers)
                return redirect(url_for('tools'))
            return render_template('main/tasklist.html')

        @self.app.route('/tools', methods=['GET', 'POST'])
        def tools():
            return render_template('main/tools.html')
        
        @self.app.route('/checker', methods=['GET', 'POST'])
        def checker():
            return render_template('checker/checker.html', tasks=self.controller.checker_data())

        @self.app.route('/timecalculator', methods=['GET', 'POST'])
        def timecalculator():
            return render_template('time_calculator/time_calculator.html', tasks=self.controller.time_calculator_data())

        @self.app.route('/ganttui/resources', methods=['GET', 'POST'])
        def gantt_resources():
            if request.method == 'POST':    
                sa = int(request.form['sa'])
                di = int(request.form['di'])
                alg = int(request.form['alg'])
                sys = int(request.form['sys'])
                web = int(request.form['web'])
                test = int(request.form['test'])
                start_date = request.form['start_date']
                session['create_resources'] = self.controller.gantt.create_resources(start_date, sa, di, alg, sys, web, test)
                return redirect(url_for('gantt_holidays'))
            return render_template('gantt_ui/resources.html')

        @self.app.route('/ganttui/resources/holidays', methods=['GET', 'POST'])
        def gantt_holidays():
            if request.method == 'POST':
                resources = request.form.getlist('resource')
                start_dates_holidays = request.form.getlist('start_date')
                end_dates_holidays = request.form.getlist('end_date')
                self.controller.gantt.create_dict_by_gantt(resources, start_dates_holidays, end_dates_holidays)
                return redirect(url_for('unaccounted'))
            return render_template('gantt_ui/holidays.html', resources=session['create_resources'])

        @self.app.route('/ganttui/unaccounted')
        def unaccounted():
            self.controller.gantt.create_gantt()
            return render_template('gantt_ui/unaccounted.html', tasks=self.controller.gantt.unaccounted_issues())

        @self.app.route('/allissues', methods=['GET', 'POST'])
        def all_issues():
            return render_template('all_issues/all_issues.html')

        @self.app.route('/allissues/ajax', methods=['GET', 'POST'])
        def allissues_ajax():
            return json.dumps({"data": self.controller.all_issues_create()})
        
        @self.app.route("/checker/ajax", methods={'GET', 'POST'})
        def checker_ajax():
            return json.dumps({'data': self.controller.checker_data()})

    def run(self):
        self.app.run(port=self.controller.port)
