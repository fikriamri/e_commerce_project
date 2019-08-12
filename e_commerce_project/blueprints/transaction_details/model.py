from blueprints import db
from flask_restful import fields

# PRODUCTS CLASS
class TransactionDetails(db.Model):
    __tablename__ = "transaction_details"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transcation_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product_name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    response_fields = {
        'id': fields.Integer,
        'transaction_id': fields.Integer,
        'product_id': fields.Integer,
        'product_name': fields.String, 
        'price': fields.Integer,
        'qty': fields.Integer
    }

    def __init__(self, transaction_id, product_id, product_name, price, qty):
        self.transaction_id = transaction_id
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.qty = qty

    def __repr__(self):
        return '<transactionDetails %r>' % self.id