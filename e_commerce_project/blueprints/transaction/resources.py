from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Transaction
from blueprints.transaction_details.model import TransactionDetails
from blueprints.buyer_details.model import BuyerDetails
from blueprints.cart.model import Cart
from blueprints.product.model import Product
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

        # untuk mendapatkan data buyer
        buyer = marshal(BuyerDetails.query.filter_by(client_id=claims['client_id']).first(), BuyerDetails.response_fields)

        # untuk mengecek apakah cart kosong atau tidak
        check_cart = Cart.query.filter_by(buyer_id=buyer['id'])
        
        if check_cart.first() is None:
            return {'status': 'Cart Empty!'}, 200, {'Content-Type': 'application/json'}
        elif check_cart is not None:
            # variable untuk menyimpan data product yang kurang
            stock_less = []
            # untuk mengecek apakah stock product yang akan dicheckout mencukupi atau tidak
            for row in check_cart.all():
                row_contain = marshal(row, Cart.response_fields)
                product = marshal(Product.query.filter_by(id=row_contain['product_id']).first(), Product.response_fields)
                if row_contain['qty'] > product['stock']:
                    stock_less.append({'product_id': product['id'], 'product_name': product['product_name'], 'stock': product['stock']})

            # Conditional apabila stock less tidak kosong
            if stock_less != []:
                return {'status': 'checkout failed because stock not available', 'stock_available': stock_less}
            else:
                now = datetime.now()
                date = now.strftime("%d/%m/%Y")
                time = now.strftime("%H:%M:%S")
                transaction = Transaction(date, time, buyer['id'], buyer['name'], 0, 0, data['courier'], data['payment_method'])
                db.session.add(transaction)
                db.session.commit()
                # untuk mendapatkan id dari transaksi yang baru dibuat
                transaction_contain = marshal(transaction, Transaction.response_fields)

                # Untuk menghitung total qty dan total price yang nantinya akan ditambahkan ke table transaction
                total_qty = 0
                total_price = 0
                for row in check_cart.all():
                    # Untuk memasukan barang dari cart ke transaction details
                    row_contain = marshal(row, Cart.response_fields)
                    transaction_details = TransactionDetails(transaction_contain['id'], row_contain['product_id'], row_contain['product_name'], row_contain['price'], row_contain['qty'])
                    db.session.add(transaction_details)
                    db.session.commit()
                    # Untuk mendapatkan total qty
                    total_qty += int(row_contain['qty'])
                    # Untuk mendapatkan total price
                    total_price += int(row_contain['qty']) * int(row_contain['price'])

                    # Untuk mengurangi product stock dengan product yang dicheckout
                    product_contain = marshal(Product.query.filter_by(id=row_contain['product_id']).first(), Product.response_fields)
                    product = Product.query.get(row_contain['product_id'])
                    product.id = product_contain['id']
                    product.product_name = product_contain['product_name']
                    product.product_category_id = product_contain['product_category_id']
                    product.description = product_contain['description']
                    product.price = product_contain['price']
                    product.image = product_contain['image']
                    product.stock = int(product_contain['stock']) - int(row_contain['qty'])
                    db.session.commit()

                    # Untuk menghapus barang dari cart
                    product_in_cart = Cart.query.filter_by(product_id=row_contain['product_id'])
                    product_in_cart = product_in_cart.filter_by(buyer_id=buyer['id']).first()
                    db.session.delete(product_in_cart)
                    db.session.commit()

                # Menginput ulang di transaction untuk memasukan total qty dan total price
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

