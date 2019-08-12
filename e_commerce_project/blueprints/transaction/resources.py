from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Transaction
from sqlalchemy import desc
from blueprints import app, db, internal_required, buyer_required
from flask_jwt_extended import jwt_required
from datetime import datetime

bp_transaction = Blueprint('transaction', __name__)
api = Api(bp_transaction)

class TransactionResource(Resource):

    def __init__(self):
        pass
    
    # # @jwt_required
    # # @buyer_required
    # def get(self):
    #     parser = reqparse.RequestParser()
    #     parser.add_argument('p', type=int, location='args', default=1)
    #     parser.add_argument('rp', type=int, location='args', default=25)
    #     parser.add_argument('product_id', type=int, location='args')
    #     parser.add_argument('orderby', location='args', choices=('price', 'qty'))
    #     parser.add_argument('sort', location='args', choices=('asc', 'desc'))
    #     args = parser.parse_args()

    #     offset = (args['p'] * args['rp']) - args['rp']

    #     qry = Cart.query.filter_by(client_id=claims['client_id'])

    #     if args['product_id'] is not None:
    #         qry = qry.filter_by(product_id=args['product_id'])

    #     if args['orderby'] is not None:
    #         if args['orderby'] == 'price':
    #             if args['sort'] == 'desc':
    #                 qry = qry.order_by(desc(Cart.price)) # bisa gini
    #             else:
    #                 qry = qry.order_by((Cart.price))
    #         elif args['orderby'] == 'qty':
    #             if args['sort'] == 'desc':
    #                 qry = qry.order_by((Cart.qty).desc()) # bisa juga gini   
    #             else:
    #                 qry = qry.order_by((Cart.qty))

    #     rows = []
    #     for row in qry.limit(args['rp']).offset(offset).all():
    #         rows.append(marshal(row, Cart.response_fields))
    #     return rows, 200, {'Content-Type': 'application/json'}

    # @jwt_required
    # @buyer_required
    # def post(self):
    #     parser = reqparse.RequestParser()
    #     parser.add_argument('courier', location='json', required=True)
    #     parser.add_argument('payment_method', location='json', required=True)
    #     data = parser.parse_args()

    #     claims = get_jwt_claims()

    #     buyer = marshal(BuyerDetails.query.filter_by(client_id=claims['client_id']).first(), BuyerDetails.response_fields)

    #     check_cart = Cart.query.filter_by(buyer_id=buyer['id'])
        
    #     if check_cart is None:
    #         add_to_cart = Cart(buyer['id'], buyer['name'], data['product_id'], product['product_name'], product['price'], data['qty'])
    #         db.session.add(add_to_cart)
    #         db.session.commit()
    #         app.logger.debug('DEBUG : %s', add_to_cart)
    #         return {'status': 'Cart Empty!'}, 200, {'Content-Type': 'application/json'}
    #     elif check_cart is not None:
    #         now = datetime.now()
    #         date = now.strftime("%d/%m/%Y")
    #         time = now.strftime("%H:%M:%S")
    #         transaction = Transaction(date, time, buyer['id'], buyer['name'], 0, 0, 'JNE', 'bank_transfer')
    #         db.session.add(transaction)
    #         db.session.commit()

    #         total_qty = 0
    #         total_price = 0
    #         for row in check_cart.all():
    #             tran


    #         check_cart_contain = marshal(check_cart, Cart.response_fields)
    #         # Menjumlahkan qty sebelumnya dengan qty yang diinput buyer
    #         qty = check_cart_contain['qty'] + int(data['qty'])
    #         # Mendapatkan query dengan id sesuai check_cart
    #         qry = Cart.query.get(check_cart_contain['id'])
    #         qry.buyer_id = check_cart_contain['buyer_id']
    #         qry.buyer_name = check_cart_contain['buyer_name']
    #         qry.product_id = check_cart_contain['product_id']
    #         qry.price = check_cart_contain['price']
    #         qry.qty = qty
    #         db.session.commit()

    #         return marshal(qry, Cart.response_fields), 200, {'Content-Type': 'application/json'}

api.add_resource(TransactionResource, '/checkout', '/checkout/<id>')

