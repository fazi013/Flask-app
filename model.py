from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description =db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity= db.Column(db.Integer)
