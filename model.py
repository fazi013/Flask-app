from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class user(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

 






'''
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description =db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity= db.Column(db.Integer)
'''