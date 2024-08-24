import os
import subprocess
import json
from .code_assess import CodeAssess

class RadonMITest(CodeAssess):

    def __init__(self, session_id, local_path, **options):
        super().__init__(session_id, local_path)
        self.options = options
        self.my_id = "Radon - Maintainability"

    def rate_app(self):
        files = os.listdir(self.local_path)
        json_result = {
            "score": 0.0,
            "message_count":
                {
                    "Very High": 0,
                    "Medium": 0,
                    "Extremely low": 0
                }
            ,
            "module_count": 0
        }
        pre_dir = os.getcwd()
        for file in files:
            # check file is folder
            if os.path.isdir(os.path.join(self.local_path, file)):
                current_dir = os.path.join(pre_dir, self.session_id, file)
                os.chdir(current_dir)
                t_ou = subprocess.check_output(
                    ["radon", "mi","-j", '.'])
                json_data = dict(json.loads(t_ou))
                print(json_data)
                json_result["module_count"] = len(json_data)
                score = 0.0
                added_to_score = 0
                for key, value in json_data.items():
                    if 'mi' not in value:
                        continue
                    score += float(value['mi']) / 10.0
                    added_to_score += 1
                    if value['rank'] == 'A':
                        json_result["message_count"]["Very High"] += 1
                    elif value['rank'] == 'B':
                        json_result["message_count"]["Medium"] += 1
                    elif value['rank'] == 'C':
                        json_result["message_count"]["Extremely low"] += 1
                json_result["score"] = round(score/added_to_score, 2)
                # json_output = t_ou
                # print(json_output.decode("utf-8"))
        self.result = {
            "score": json_result["score"],
            "message_count": json_result["message_count"],
            "module_count": json_result["module_count"]
        }
        os.chdir(pre_dir)

    def run_report(self):
        files = os.listdir(self.local_path)
        readable_output = None

        pre_dir = os.getcwd()
        for file in files:
            # check file is folder
            if os.path.isdir(os.path.join(self.local_path, file)):
                current_dir = os.path.join(pre_dir, self.session_id, file)
                os.chdir(current_dir)
                readable_output = subprocess.check_output(
                ["radon", "mi", "-s", '.'])
        self.full_report = readable_output
        os.chdir(pre_dir)
        