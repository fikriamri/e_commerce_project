from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Cart
from blueprints.product.model import Product
from sqlalchemy import desc
from blueprints import app, db, internal_required, buyer_required
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_cart = Blueprint('cart', __name__)
api = Api(bp_cart)

class CartResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    @buyer_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', location='json', required=True)
        parser.add_argument('qty', location='json', required=True)
        data = parser.parse_args()

        claims = get_jwt_claims()

        product = marshal(Product.query.filter_by(id=data['product_id']).first(), Product.response_fields)

        add_to_cart = Cart(claims['client_id'], claims['client_key'], data['product_id'], product['product_name'], product['price'], data['qty'])
        db.session.add(add_to_cart)
        db.session.commit()

        app.logger.debug('DEBUG : %s', add_to_cart)

        return marshal(add_to_cart, Cart.response_fields), 200, {'Content-Type': 'application/json'}

#     @jwt_required
#     @internal_required
#     def put(self, id):
#         parser = reqparse.RequestParser()
#         parser.add_argument('client_key', location='json')
#         parser.add_argument('client_secret', location='json')
#         parser.add_argument('status', type=bool, location='json', required=True)
#         args = parser.parse_args()

#         qry = Clients.query.get(id)
#         if qry is None:
#             return {'status': 'Client Not Found'}, 404, {'Content-Type': 'application/json'}

#         qry.client_key = args['client_key']
#         qry.client_secret = args['client_secret']
#         qry.status = args['status']
#         db.session.commit()

#         return marshal(qry, Clients.response_fields), 200, {'Content-Type': 'application/json'}

#     @jwt_required
#     @internal_required
#     def delete(self, id):
#         qry = Clients.query.get(id)
#         if qry is None:
#             return {'status': 'Client Not Found'}, 404, {'Content-Type': 'application/json'}

#         db.session.delete(qry)
#         db.session.commit()

#         return {'status': 'Client Deleted'}, 200, {'Content-Type': 'application/json'}

#     def patch(self):
#         return 'Not yet implemented', 501

# class ClientList(Resource):

#     def __init__(self):
#         pass

#     @jwt_required
#     @internal_required
#     def get(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('p', type=int, location='args', default=1)
#         parser.add_argument('rp', type=int, location='args', default=25)
#         parser.add_argument('client_id', type=int, location='args')
#         parser.add_argument('status', type=inputs.boolean, location='args', choices=(True, False))
#         parser.add_argument('orderby', location='args', choices=('client_id', 'status'))
#         parser.add_argument('sort', location='args', choices=('asc', 'desc'))
#         args = parser.parse_args()

#         offset = (args['p'] * args['rp']) - args['rp']

#         qry = Clients.query

#         if args['status'] is not None:
#             qry = qry.filter_by(status=args['status'])

#         if args['orderby'] is not None:
#             if args['orderby'] == 'client_id':
#                 if args['sort'] == 'desc':
#                     qry = qry.order_by(desc(Clients.client_id)) # bisa gini
#                 else:
#                     qry = qry.order_by((Clients.client_id))
#             elif args['orderby'] == 'status':
#                 if args['sort'] == 'desc':
#                     qry = qry.order_by((Clients.client_id).desc()) # bisa juga gini   
#                 else:
#                     qry = qry.order_by((Clients.client_id))

#         rows = []
#         for row in qry.limit(args['rp']).offset(offset).all():
#             rows.append(marshal(row, Clients.response_fields))
#         return rows, 200, {'Content-Type': 'application/json'}

# api.add_resource(ClientList, '')
api.add_resource(CartResource, '')

