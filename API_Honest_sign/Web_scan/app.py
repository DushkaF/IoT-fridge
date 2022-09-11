import requests
import json
import os
from flask import *
from config import Configuration, internalServerURL, secretKey
from decoder import HSdecoder

app = Flask(__name__, static_folder='scanner/build')
app.config.from_object(Configuration)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = secretKey


# @app.route('/')
# def hello():
#     return render_template('index.html')

# @app.route('/static/<dir>/<file
# def statics(dir, file):
#     path = "static/" + dir + "/" + file
#     return send_file(path)


# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/codes', methods=["POST"])
def decode():
    content = request.json
    print(content)
    parsed_data = HSdecoder(content['codelist'])
    return jsonify(parsed_data)
