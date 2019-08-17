from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Transaction
from blueprints.transaction_details.model import TransactionDetails
from blueprints.buyer_details.model import BuyerDetails
from blueprints.cart.model import Cart
from sqlalchemy import desc
from blueprints import app, db, internal_required, buyer_required
from flask_jwt_extended import jwt_required, get_jwt_claims
from datetime import datetime

bp_transaction = Blueprint('transaction', __name__)
api = Api(bp_transaction)

class TransactionResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    @buyer_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('courier', location='json', required=True)
        parser.add_argument('payment_method', location='json', required=True)
        data = parser.parse_args()

        claims = get_jwt_claims()

        buyer = marshal(BuyerDetails.query.filter_by(client_id=claims['client_id']).first(), BuyerDetails.response_fields)

        check_cart = Cart.query.filter_by(buyer_id=buyer['id'])
        
        if check_cart is None:
            add_to_cart = Cart(buyer['id'], buyer['name'], data['product_id'], product['product_name'], product['price'], data['qty'])
            db.session.add(add_to_cart)
            db.session.commit()
            app.logger.debug('DEBUG : %s', add_to_cart)
            return {'status': 'Cart Empty!'}, 200, {'Content-Type': 'application/json'}
        elif check_cart is not None:
            now = datetime.now()
            date = now.strftime("%d/%m/%Y")
            time = now.strftime("%H:%M:%S")
            transaction = Transaction(date, time, buyer['id'], buyer['name'], 0, 0, data['courier'], data['payment_method'])
            db.session.add(transaction)
            db.session.commit()
            # untuk mendapatkan id dari transaksi yang baru dibuat
            transaction_contain = marshal(transaction, Transaction.response_fields)

            total_qty = 0
            total_price = 0
            for row in check_cart.all():
                row_contain = marshal(row, Cart.response_fields)
                transaction_details = TransactionDetails(transaction_contain['id'], row_contain['product_id'], row_contain['product_name'], row_contain['price'], row_contain['qty'])
                db.session.add(transaction_details)
                db.session.commit()
                # Untuk mendapatkan total qty
                total_qty += int(row_contain['qty'])
                # Untuk mendapatkan total price
                total_price += int(row_contain['qty']) * int(row_contain['price'])

            transaction.id = transaction_contain['id']
            transaction.date = transaction_contain['date']
            transaction.time = transaction_contain['time']
            transaction.buyer_id = transaction_contain['buyer_id']
            transaction.buyer_name = transaction_contain['buyer_name']
            transaction.total_qty = total_qty
            transaction.total_price = total_price
            transaction.courier = transaction_contain['courier']
            transaction.payment_method = transaction_contain['payment_method']
            db.session.commit()

            return marshal(transaction, Transaction.response_fields), 200, {'Content-Type': 'application/json'}

api.add_resource(TransactionResource, '/checkout', '/checkout/<id>')

