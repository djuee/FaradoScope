import asyncio
from database_objects.database import Database

class IssueChecker:
    def __init__(self, issue):
        self.issue = issue

    async def check_grade(self):
        '''Метод возвращает те ресурсы, по которым нет оценки'''    
        grades = {
            'SA': '',
            'DI': '',
            'ALG': '',
            'SYS': '',
            'WEB': '',
            'TEST': '',
        }
        for field in self.issue.fields:
            if field.field_kind_id == 16:
                grades['SA'] = field.value
            if field.field_kind_id == 17:
                grades['DI'] = field.value
            if field.field_kind_id == 18:
                grades['ALG'] = field.value
            if field.field_kind_id == 31:
                grades['WEB'] = field.value
            if field.field_kind_id == 32:
                grades['SYS'] = field.value
            if field.field_kind_id == 33:
                grades['TEST'] = field.value
        return any(value != '' for value in grades.values())
        await asyncio.sleep(0)

    async def check_develop_departments(self):
        '''Метод возвращает True, если отделы разработки указаны, в ином случае - False'''
        bool_list = []
        field_kinds_id = [69, 70, 71, 72]
        for field in self.issue.fields:
            if field.field_kind_id in field_kinds_id:
                bool_list.append(field.value == '')
        return not all(bool_list)
        await asyncio.sleep(0)

    async def check_requirements(self):
        states_id = [7, 8, 11, 12, 19, 20, 32, 33, 38, 39]
        needed_kid = False
        for kid in self.issue.kids:
            if kid.issue_kind_id == 5:
                needed_kid = kid
                break
        if not needed_kid:
            return False
        return needed_kid.state_id in states_id
        await asyncio.sleep(0)

    async def check_test(self):
        return any(kid.issue_kind_id == 10 for kid in self.issue.kids)
        await asyncio.sleep(0)

    async def check_performer_at_kids(self):
        field_kinds_id = [4, 6, 10, 13, 20, 22, 24, 26, 28, 30]
        for kid in self.issue.kids:
            for field in kid.fields:
                if (field.field_kind_id in field_kinds_id) and (field.value == '0'):
                    return False
        return True
        await asyncio.sleep(0)

    async def check_state(self):
        work_states = [16, 6, 10, 17, 30, 36, 13, 18, 31, 37, 41]
        dont_work_states = [5, 9, 14, 15, 21, 28, 29, 34, 35, 40, 42, 7, 8, 11, 12, 19, 20, 32, 33, 38, 39]
        if self.issue.state_id in work_states:
            return all(kid.state_id in work_states for kid in self.issue.kids)
        elif self.issue.state_id in dont_work_states:
            return all(kid.state_id in dont_work_states for kid in self.issue.kids)
        await asyncio.sleep(0)

    async def check_basic_request_in_issue(self):
        return all(kid.issue_kind_id != 1 for kid in self.issue.kids)
        await asyncio.sleep(0)

    async def check_correction(self):
        return sum(1 for kid in self.issue.kids if kid.issue_kind_id == 8)
        await asyncio.sleep(0)

    async def check_versions(self):
        return all(self.issue.version_id == kid.version_id for kid in self.issue.kids)
        await asyncio.sleep(0)

    async def check_performer(self):
        field_kinds_id = [68, 73, 74]
        return all(field.value != '' and field.value != 'None' for field in self.issue.fields if field.field_kind_id in field_kinds_id)
        await asyncio.sleep(0)

    async def check_layout(self):
        return any(kid.issue_kind_id == 4 for kid in self.issue.kids)
        await asyncio.sleep(0)

    async def check_playback(self):
        for kid in self.issue.kids:
            if kid.issue_kind_id == 11:
                return True
        return False
        await asyncio.sleep(0)
    
    async def check_documentation(self):
        for kid in self.issue.kids:
            if kid.issue_kind_id == 12:
                return True
        return False
        await asyncio.sleep(0)

    async def async_run(self):
        return await asyncio.gather(
            self.check_requirements(), 
            self.check_grade(), 
            self.check_layout(), 
            self.check_performer_at_kids(), 
            self.check_develop_departments(),
            self.check_state(),
            self.check_performer(),
            self.check_versions(),
            self.check_test(),
            self.check_playback(),
            self.check_documentation(),
            self.check_correction(),
            self.check_basic_request_in_issue(),
            )
        