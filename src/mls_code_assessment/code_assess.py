
class CodeAssess:
    def __init__(self, session_id, local_path):
        self.session_id = session_id
        self.local_path = local_path
        self.result = {}
        self.full_report = None

    def rate_app(self):
        pass

    def run_report(self):
        pass

    def get_score(self):
        return self.result
    
    def get_report(self):
        return self.full_report

    def get_id(self):
        return "Code Assess"