from flask_sqlalchemy import SQLAlchemy

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
    




