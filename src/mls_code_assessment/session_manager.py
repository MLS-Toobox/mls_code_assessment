import os
import shutil
import uuid
from . test_list import TESTS
class SessionManager:
    def __init__(self, app_zip):
        self.app_zip = app_zip
        self.session_id = None
        self.result = None
    
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
    
    def run(self):
        local_path_head = self.__create_session()
        self.result = {}
        for test in TESTS:
            test_object = test(self.session_id, local_path_head)
            test_object.run()
            self.result[test_object.get_id()] = test_object.get_result()
    
    def get_response(self):
        return self.result

    def clean(self):
        local_path_head = self.__get_session_path()
        shutil.rmtree(local_path_head)