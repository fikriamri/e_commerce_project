from blueprints import db
from flask_restful import fields

# PRODUCTS CLASS
class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(50), unique=True, nullable=False)
    product_category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'))
    description = db.Column(db.String(255), nullable=False) 
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    response_fields = {
        'id': fields.Integer,
        'product_name': fields.String,
        'product_category_id': fields.Integer,
        'description': fields.String,
        'price': fields.Integer,
        'image': fields.String,
        'stock': fields.Integer
    }

    def __init__(self, product_name, product_category_id, description, price, image, stock):
        self.product_name = product_name
        self.product_category_id = product_category_id
        self.description = description
        self.price = price
        self.image = image
        self.stock = stock

    def __repr__(self):
        return '<Product %r>' % self.id