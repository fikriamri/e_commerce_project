from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Transaction
from blueprints.transaction_details.model import TransactionDetails
from blueprints.buyer_details.model import BuyerDetails
from blueprints.cart.model import Cart
from blueprints.product.model import Product
from sqlalchemy import desc
from blueprints import app, db, seller_required, buyer_required
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_transaction = Blueprint('transaction', __name__)
api = Api(bp_transaction)

class TransactionResource(Resource):

    def __init__(self):
        pass

    ## Options function needed to make interaction between react and api successfull
    def options(self):
        return {'Status': 'OK'}, 200

    ## Buyer function to get transaction
    @jwt_required
    @buyer_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=('total_qty', 'total_price'))
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        claims = get_jwt_claims()
        buyer = marshal(BuyerDetails.query.filter_by(client_id=claims['client_id']).first(), BuyerDetails.response_fields)

        transaction = Transaction.query.filter_by(buyer_id=buyer['id'])
        
        if args['orderby'] is not None:
            if args['orderby'] == 'total_qty':
                if args['sort'] == 'desc':
                    transaction = transaction.order_by(desc(Transaction.total_qty)) # bisa gini
                else:
                    transaction = transaction.order_by((Transaction.total_qty))
            elif args['orderby'] == 'total_price':
                if args['sort'] == 'desc':
                    transaction = transaction.order_by((Transaction.total_price).desc()) # bisa juga gini   
                else:
                    transaction = transaction.order_by((Transaction.total_price))

        rows = []
        for row in transaction.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Transaction.response_fields))
        return rows, 200, {'Content-Type': 'application/json'}

    ## Buyer function for checkout
    @jwt_required
    @buyer_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('courier', location='json', required=True)
        parser.add_argument('payment_method', location='json', required=True)
        argument = parser.parse_args()

        claims = get_jwt_claims()

        # get buyer information
        buyer = marshal(BuyerDetails.query.filter_by(client_id=claims['client_id']).first(), BuyerDetails.response_fields)

        # Check whether cart empty or not
        check_cart = Cart.query.filter_by(buyer_id=buyer['id'])
        if check_cart.first() is None:
            return {'status': 'Cart Empty!'}, 404, {'Content-Type': 'application/json'}
        elif check_cart is not None:
            # Variable for storing information about product that its stock is less than qty wanted by buyer
            stock_less = []
            # Check whether product stock enough or not for qty wanted by buyer
            for row in check_cart.all():
                row_contain = marshal(row, Cart.response_fields)
                product = marshal(Product.query.filter_by(id=row_contain['product_id']).first(), Product.response_fields)
                if row_contain['qty'] > product['stock']:
                    stock_less.append({'product_id': product['id'], 'product_name': product['product_name'], 'stock': product['stock']})

            # Conditional covering one or more product stock is less than qty wanted
            if stock_less != []:
                return {'status': 'checkout failed because stock not available', 'stock_available': stock_less}, 400
            else:
                transaction = Transaction(buyer['id'], buyer['name'], 0, 0, argument['courier'], argument['payment_method'])
                db.session.add(transaction)
                db.session.commit()
                # get transaction id 
                transaction_contain = marshal(transaction, Transaction.response_fields)

                # variable for storing total qty and total price that will be submitted to transaction table
                total_qty = 0
                total_price = 0

                for row in check_cart.all():
                    # moving product from cart to transaction details
                    row_contain = marshal(row, Cart.response_fields)
                    transaction_details = TransactionDetails(transaction_contain['id'], row_contain['product_id'], row_contain['product_name'], row_contain['price'], row_contain['qty'])
                    db.session.add(transaction_details)
                    db.session.commit()
                    total_qty += int(row_contain['qty'])
                    total_price += int(row_contain['qty']) * int(row_contain['price'])

                    # substract product stock by qty checked out product
                    product_contain = marshal(Product.query.filter_by(id=row_contain['product_id']).first(), Product.response_fields)
                    product = Product.query.get(row_contain['product_id'])
                    product.id = product_contain['id']
                    product.seller_id = product_contain['seller_id']
                    product.store_name = product_contain['store_name']
                    product.product_name = product_contain['product_name']
                    product.product_category_id = product_contain['product_category_id']
                    product.description = product_contain['description']
                    product.price = product_contain['price']
                    product.image = product_contain['image']
                    product.stock = int(product_contain['stock']) - int(row_contain['qty'])
                    product.sold = int(product_contain['sold']) + int(row_contain['qty'])
                    db.session.commit()

                    # erase product from cart
                    product_in_cart = Cart.query.filter_by(product_id=row_contain['product_id'])
                    product_in_cart = product_in_cart.filter_by(buyer_id=buyer['id']).first()
                    db.session.delete(product_in_cart)
                    db.session.commit()

                # reinput transaction with new total qty and total prince
                transaction.id = transaction_contain['id']
                transaction.buyer_id = transaction_contain['buyer_id']
                transaction.buyer_name = transaction_contain['buyer_name']
                transaction.total_qty = total_qty
                transaction.total_price = total_price
                transaction.courier = transaction_contain['courier']
                transaction.payment_method = transaction_contain['payment_method']
                db.session.commit()

                return marshal(transaction, Transaction.response_fields), 200, {'Content-Type': 'application/json'}

api.add_resource(TransactionResource, '/checkout')

