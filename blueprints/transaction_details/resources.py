from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import TransactionDetails
from blueprints.seller_details.model import SellerDetails
from blueprints.product.model import Product
from blueprints.transaction.model import Transaction
from blueprints.buyer_details.model import BuyerDetails
from sqlalchemy import desc
from blueprints import app, db, seller_required, buyer_required
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_transaction_details = Blueprint('transaction_details', __name__)
api = Api(bp_transaction_details)

class TransactionDetailsResource(Resource):

    def __init__(self):
        pass

    ## Options function needed to make interaction between react and api successfull
    def options(self):
        return {'Status': 'OK'}, 200

    ## Buyer function for get transaction details data by transaction id
    @jwt_required
    @buyer_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('transaction_id', location='args', required=True)
        args = parser.parse_args()

        transaction_details = TransactionDetails.query.filter_by(transaction_id=args['transaction_id'])

        rows = []
        for row in transaction_details:
            rows.append(marshal(row, TransactionDetails.response_fields))
        return rows, 200, {'Content-Type': 'application/json'}

class OrderDetailsResource(Resource):

    def __init__(self):
        pass

    ## Options function needed to make interaction between react and api successfull
    def options(self):
        return {'Status': 'OK'}, 200

    ## Seller function for get order details data by seller client id
    @jwt_required
    @seller_required
    def get(self):
        # Get information about signed in seller
        claims = get_jwt_claims()
        seller = marshal(SellerDetails.query.filter_by(client_id=claims['client_id']).first(), SellerDetails.response_fields)

        order_details = TransactionDetails.query

        rows = []
        for row in order_details:
            check_transaction_details = marshal(row, TransactionDetails.response_fields)
            check_product = marshal(Product.query.filter_by(id=check_transaction_details['product_id']).first(), Product.response_fields)
            if check_product['seller_id'] == seller['id']:
                check_transaction = marshal(Transaction.query.filter_by(id=check_transaction_details['transaction_id']).first(), Transaction.response_fields)
                check_buyer = marshal(BuyerDetails.query.filter_by(id=check_transaction['buyer_id']).first(), BuyerDetails.response_fields)

                response = {
                    'transaction': check_transaction,
                    'transaction_details': check_transaction_details,
                    'buyer_details': check_buyer
                }

                rows.append(response)
        return rows, 200, {'Content-Type': 'application/json'}
    
api.add_resource(TransactionDetailsResource, '/transaction_details')
api.add_resource(OrderDetailsResource, '/order_details')

