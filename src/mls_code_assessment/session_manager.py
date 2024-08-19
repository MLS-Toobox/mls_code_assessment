import os
import shutil
import uuid
from . test_list import TESTS
class SessionManager:
    def __init__(self, app_zip):
        self.app_zip = app_zip
        self.session_id = None
        self.result = None
        self.full_report = None
    
    def __get_session_id(self):
        return str(uuid.uuid4())

    def __get_session_path(self):
        local_path_head = './'+ self.session_id
        return local_path_head

    def __create_session(self):
        session_id = self.__get_session_id()
        self.session_id = session_id
        local_path_head = self.__get_session_path()
        os.mkdir(local_path_head)
        file = open(local_path_head+'/tmp.zip', 'wb')
        file.write(self.app_zip)
        file.close()

        shutil.unpack_archive(local_path_head + '/tmp.zip', local_path_head)

        return local_path_head
    
    def run_score(self):
        local_path_head = self.__create_session()
        self.result = {}
        for test in TESTS:
            test_object = test(self.session_id, local_path_head)
            test_object.rate_app()
            self.result[test_object.get_id()] = test_object.get_score()
        
    def run_report(self, test_id):
        local_path_head = self.__create_session()
        self.result = {}
        for test in TESTS:
            test_object = test(self.session_id, local_path_head)
            if test_object.get_id() == test_id:
                test_object = test(self.session_id, local_path_head)
                test_object.run_report()
                self.full_report = test_object.get_report()
    
    def get_response(self):
        return self.result

    def get_report(self):
        return self.full_report

    def clean(self):
        local_path_head = self.__get_session_path()
        shutil.rmtree(local_path_head)