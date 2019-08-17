from blueprints import db
from flask_restful import fields

# PRODUCTS CLASS
class Transaction(db.Model):
    __tablename__ = "transaction"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer_details.id'))
    buyer_name = db.Column(db.String(50), nullable=False)
    total_qty = db.Column(db.Integer)
    total_price = db.Column(db.Integer)
    # Sementara string dulu, sebelum dibuat tablenya
    courier = db.Column(db.String(255), nullable=False)
    payment_method = db.Column(db.String(255), nullable=False)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    response_fields = {
        'id': fields.Integer,
        'buyer_id': fields.Integer,
        'buyer_name': fields.String,
        'total_qty': fields.Integer,
        'total_price': fields.Integer,
        'courier': fields.String,
        'payment_method': fields.String
    }

    def __init__(self, buyer_id, buyer_name, total_qty, total_price, courier, payment_method):
        self.buyer_id = buyer_id
        self.buyer_name = buyer_name
        self.total_qty = total_qty
        self.total_price = total_price
        self.courier = courier
        self.payment_method = payment_method

    def __repr__(self):
        return '<Transaction %r>' % self.id