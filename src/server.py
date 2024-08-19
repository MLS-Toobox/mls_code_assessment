""" Server. """

import os

from flask import Flask, make_response, request
from flask_cors import cross_origin, CORS
from waitress import serve

from mls_code_assessment import SessionManager


app = Flask(__name__)

@app.route('/api/rate_app', methods=['GET','POST'])
@cross_origin()
def rate_app():
    """ Rates code quality. """

    ## Receive binary .zip file
    content = request.data ## binary data

    s = SessionManager(content)
    
    s.run_score()
    response = s.get_response()
    s.clean()

    return response

@app.route('/api/get_report', methods=['GET','POST'])
@cross_origin()
def get_report():
    """ Gets the report for code quality """

    ## Receive binary .zip file
    content = request.data ## binary data

    s = SessionManager(content)

    test_id = request.args.get('test_id', default = "NONE", type = str)

    if test_id == "NONE":
        return "Please provide test_id"

    s.run_report(test_id)
    data = s.get_report()
    s.clean()

    if data is None:
        return "No report found for test_id : " + test_id
    response = make_response(data)
    response.headers.set('Content-Type', 'application/x-binary')
    response.headers.set('Content-Disposition', 'attachment', filename='report.txt')
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
    ## set status code
    response.status_code = 200
    return response

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
        app.run(host = HOST, port = PORT, debug = False)
