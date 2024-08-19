import os
import subprocess
import json

from .code_assess import CodeAssess

class PyLintTest(CodeAssess):

    def __init__(self, session_id, local_path, **options):
        super().__init__(session_id, local_path)
        self.options = options

    def rate_app(self):
        files = os.listdir(self.local_path)
        json_output = {}

        for file in files:
            # check file is folder
            if os.path.isdir(self.local_path + '/' + file):
                current_dir = os.getcwd() + '/' + self.session_id + '/' + file
                try:
                    subprocess.check_output(
                        ["pylint", "--recursive", "y", "--output-format", "json2",
                         "--disable", "E0401", "--clear-cache-post-run", "y", current_dir])
                except subprocess.CalledProcessError as e:
                    json_output = json.loads(str(e.output, "utf-8"))

        self.result = {
            "score": json_output["statistics"]["score"],
            "message_count": json_output["statistics"]["messageTypeCount"],
            "module_count": json_output["statistics"]["modulesLinted"]
        }

    def run_report(self):
        files = os.listdir(self.local_path)
        readable_output = None

        for file in files:
            # check file is folder
            if os.path.isdir(self.local_path + '/' + file):
                current_dir = os.getcwd() + '/' + self.session_id + '/' + file
                try:
                    subprocess.check_output(
                        ["pylint", "--recursive", "y", "--score","n", "--reports", "y",
                         "--disable", "E0401", "--clear-cache-post-run", "y", current_dir])
                except subprocess.CalledProcessError as e:
                    readable_output = e.output, "utf-8"
        self.full_report = readable_output
    
    def get_id(self):
        return "PyLint"