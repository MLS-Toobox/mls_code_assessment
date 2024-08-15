""" Server. """

import os
import shutil
import uuid
import subprocess
import json

from flask import Flask, request
from flask_cors import cross_origin, CORS
from waitress import serve

app = Flask(__name__)

@app.route('/api/rate_app', methods=['GET','POST'])
@cross_origin()
def rate_app():
    """ Rates code quality. """

    ## Receive binary .zip file
    content = request.data ## binary data

    ## Unzip

    path_head = str(uuid.uuid4())
    local_path_head = './'+ path_head
    os.mkdir(local_path_head)
    file = open(local_path_head+'/tmp.zip', 'wb')
    file.write(content)
    file.close()

    shutil.unpack_archive(local_path_head + '/tmp.zip', local_path_head)

    files = os.listdir(local_path_head)
    output = ""
    for file in files:
        # check file is folder
        if os.path.isdir(local_path_head + '/' + file):
            current_dir = os.getcwd() + '/' + path_head + '/' + file
            try:
                output = subprocess.check_output(
                    ["pylint", "--recursive", "y", "--output-format", "json2", current_dir])
            except subprocess.CalledProcessError as e:
                output = e.output
    shutil.rmtree(local_path_head)
    return json.loads(output)

@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def home():
    """ Used to test the connectivity in the server. """
    return 'hello from mls_code_assessment. Method : ' + request.method

if __name__ == '__main__':
    CORS(app, supports_credentials=True, origins=['*'])
    app.config["CORS_HEADERS"] = ["Content-Type", "X-Requested-With", "X-CSRFToken"]
    
    execution_mode = os.getenv("EXECUTION_MODE", "debug")
    
    HOST = "0.0.0.0"
    PORT = 5060

    if execution_mode == "prod":
        serve(app, host = HOST, port = PORT)
    else:
        app.run(host = HOST, port = PORT, debug=False)
