class Issue():
    def __init__(self):
        self.id = int()
        self.issue_kind_id = int()
        self.parent_id = int()
        self.project_id = int()
        self.state_id = int()
        self.caption = str()
        self.content = str()
        self.version_id = int()
        self.changes = []
        self.fields = []
        self.comments = []
        self.kids = []