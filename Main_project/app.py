import os
from flask import *
from flask_cors import CORS, cross_origin
from config import Configuration
import decoder
import db_functions
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='scanner/build')
app.config.from_object(Configuration)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fridge_catalog.db'
db = SQLAlchemy(app)

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@cross_origin()
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/codes', methods=["POST"])
def decode():
    content = request.json
    print(content)
    parsed_data = decoder.HSdecoder(content['codelist'])
    return jsonify(parsed_data)


@app.route('/get_catalog', methods=["GET"])
def send_catalog():
    return jsonify(db_functions.get_catalog())


@app.route('/accept_product', methods=["POST"])
def accept_product():
    content = request.json
    status = db_functions.add_product_card(content)
    return jsonify({"status": status})



if __name__ == "__main__":
    app.run()
