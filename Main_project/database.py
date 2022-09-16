from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

class ProductCard(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    check_date = db.Column(db.Integer, nullable=False)
    expiration_date = db.Column(db.Integer)
    expiration_days = db.Column(db.String(100))
    expiration_warning = db.Column(db.Boolean, nullable=False)
    good_img = db.Column(db.String(1024))
    good_quantity = db.Column(db.String(10))
    good_unit = db.Column(db.String(10))
    product_name = db.Column(db.String(200), nullable=False)

    # def __init__(self, text, tags):
    #     self.text = text.strip()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fridge_catalog.db'
    db.init_app(app)
    return app


if __name__ == "__main__":

    db.create_all(app=create_app())




