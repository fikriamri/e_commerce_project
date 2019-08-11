from blueprints import db
from flask_restful import fields

# PRODUCTS CLASS
class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_key = db.Column(db.Integer, db.ForeignKey('clients.clients_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product_name = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    response_fields = {
        'id': fields.Integer,
        'client_key': fields.Integer,
        'product_id': fields.Integer,
        'product_name': fields.String,
        'price': fields.Integer,
        'qty': fields.Integer
    }

    def __init__(self, client_key, product_id, product_name, price, qty):
        self.client_key = client_key
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.qty = qty

    def __repr__(self):
        return '<Product %r>' % self.id