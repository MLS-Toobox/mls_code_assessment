import os
import subprocess

from .code_assess import CodeAssess

class RadonCCTest(CodeAssess):

    def __init__(self, session_id, local_path, **options):
        super().__init__(session_id, local_path)
        self.options = options
        self.my_id = "Radon - Complexity"

    def rate_app(self):
        files = os.listdir(self.local_path)
        complexity_score = 0.0
        pre_dir = os.getcwd()
        for file in files:
            # check file is folder
            if os.path.isdir(os.path.join(self.local_path, file)):
                current_dir = os.path.join(pre_dir, self.session_id, file)
                os.chdir(current_dir)
                t_ou = subprocess.check_output(
                    ["radon", "cc","--total-average", "-s", '.'])
                blocks, complexity = t_ou.decode("utf-8").split("\n")[-3:-1]
                blocks = int(blocks.split(" ")[0])
                complexity_score = round(10/pow(float(complexity[:-1].split("(")[-1]), .3),2)
                # json_output = t_ou
                # print(json_output.decode("utf-8"))
        self.result = {
            "score": complexity_score,
            "message_count": [],
            "module_count": blocks
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
                ["radon", "cc","--total-average", "-s", '.'])
        self.full_report = readable_output
        os.chdir(pre_dir)
        