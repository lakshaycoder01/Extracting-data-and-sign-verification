from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
from gevent.pywsgi import WSGIServer
from werkzeug.serving import run_with_reloader
from werkzeug.debug import DebuggedApplication
import logging
from process import mainfile
import os
import json

log_folder = os.path.basename('log')
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
print(APP_ROOT)
app = Flask(__name__)
CORS(app)

app.config['log_folder'] = log_folder


@app.route('/upload/<path:path>', methods=['GET', 'POST'])
def get_images(path):
    print(path)
    return send_from_directory('', path)


@app.route('/upload', methods=['GET', 'POST'])
def predict():
    try:
        image_files = request.files
        form_data = request.form
        person_name = form_data['name']
        img_to_ext_sign = image_files['file']
        print(img_to_ext_sign)
        image_processing_class = mainfile.image_process_verify(
            img_to_ext_sign, person_name)
        data = image_processing_class.processing_image()
        return data
    except:
        return "Please send a Proper server Request"


def run_server():
    if(app.debug):
        application = DebuggedApplication(app)
    else:
        application = app
    logger = logging.getLogger()
    fh = logging.FileHandler(os.path.join(app.config['log_folder'], 'log.txt'))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    server = WSGIServer(('0.0.0.0', 8551), application, log=logger)
    print("Server Start")
    server.serve_forever()


if (__name__ == '__main__'):

    run_with_reloader(run_server)
    # serve(application,listen='localhost:8545')
    # application.run(debug=True,port=8545,threaded=True)
