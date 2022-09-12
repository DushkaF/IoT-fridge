import requests
import json
import os
from flask import *
from config import Configuration
from decoder import HSdecoder

app = Flask(__name__, static_folder='scanner/build')
app.config.from_object(Configuration)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", use_reloader=False)