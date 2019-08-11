from blueprints import db
from flask_restful import fields

# PRODUCTS CLASS
class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))
    client_name = db.Column(db.String(50), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product_name = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    response_fields = {
        'id': fields.Integer,
        'client_id': fields.Integer,
        'client_name': fields.String,
        'product_id': fields.Integer,
        'product_name': fields.String,
        'price': fields.Integer,
        'qty': fields.Integer
    }

    def __init__(self, client_id, client_name, product_id, product_name, price, qty):
        self.client_id = client_id
        self.client_name = client_name
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.qty = qty

    def __repr__(self):
        return '<Product %r>' % self.id