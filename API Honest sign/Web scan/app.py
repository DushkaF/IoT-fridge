import requests
import json
from flask import *
from config import Configuration, internalServerURL, secretKey
from decoder import HSdecoder

app = Flask(__name__, template_folder = "static/html")
app.config.from_object(Configuration)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = secretKey


# @app.route('/')
# def hello():
#     return render_template('index.html')

# @app.route('/static/<dir>/<file>')
# def statics(dir, file):
#     path = "static/" + dir + "/" + file
#     return send_file(path)

@app.route('/codes', methods=["POST"])
def decode():
    content = request.json
    print(content)
    parsed_data = HSdecoder(content['codelist'])
    return jsonify(parsed_data)
