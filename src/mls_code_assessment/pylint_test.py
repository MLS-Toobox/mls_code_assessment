from .code_assess import CodeAssess

import os
import subprocess
import json

class PyLintTest(CodeAssess):

    def __init__(self, session_id, local_path, **options):
        super().__init__(session_id, local_path)
        self.options = options

    def run(self):
        files = os.listdir(self.local_path)
        readable_output = ""
        json_output = {}

        for file in files:
            # check file is folder
            if os.path.isdir(self.local_path + '/' + file):
                current_dir = os.getcwd() + '/' + self.session_id + '/' + file
                try:
                    subprocess.check_output(
                        ["pylint", "--recursive", "y", current_dir])
                except subprocess.CalledProcessError as e:
                    readable_output = str(e.output, "utf-8")
                try:
                    subprocess.check_output(
                        ["pylint", "--recursive", "y", "--output-format", "json2", current_dir])
                except subprocess.CalledProcessError as e:
                    json_output = json.loads(str(e.output, "utf-8"))

        self.result = {
            "full_report": readable_output,
            "score": json_output["statistics"]["score"],
            "message_count": json_output["statistics"]["messageTypeCount"],
            "modules_count": json_output["statistics"]["modulesLinted"]
        }
    
    def get_id(self):
        return "PyLint"