from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Cart
from blueprints.product.model import Product
from blueprints.buyer_details.model import BuyerDetails
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
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('product_id', type=int, location='args')
        parser.add_argument('orderby', location='args', choices=('price', 'qty'))
        parser.add_argument('sort', location='args', choices=('asc', 'desc'))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Cart.query

        if args['product_id'] is not None:
            qry = qry.filter_by(product_id=args['product_id'])

        if args['orderby'] is not None:
            if args['orderby'] == 'price':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Cart.price)) # bisa gini
                else:
                    qry = qry.order_by((Cart.price))
            elif args['orderby'] == 'qty':
                if args['sort'] == 'desc':
                    qry = qry.order_by((Cart.qty).desc()) # bisa juga gini   
                else:
                    qry = qry.order_by((Cart.qty))

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Cart.response_fields))
        return rows, 200, {'Content-Type': 'application/json'}

    @jwt_required
    @buyer_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', location='json', required=True)
        parser.add_argument('qty', location='json', required=True)
        data = parser.parse_args()

        claims = get_jwt_claims()

        product = marshal(Product.query.filter_by(id=data['product_id']).first(), Product.response_fields)
        buyer = marshal(BuyerDetails.query.filter_by(client_id=claims['client_id']).first(), BuyerDetails.response_fields)

        check_cart = Cart.query.filter_by(product_id=data['product_id'])
        check_cart = check_cart.filter_by(buyer_id=buyer['id']).first()
        
        if check_cart is None:
            # Mengecek apakah stok barang tersedia sesuai qty yang diinginkan atau tidak
            if int(data['qty']) <= product['stock']:
                add_to_cart = Cart(buyer['id'], buyer['name'], data['product_id'], product['product_name'], product['price'], data['qty'])
                db.session.add(add_to_cart)
                db.session.commit()
                app.logger.debug('DEBUG : %s', add_to_cart)
                return marshal(add_to_cart, Cart.response_fields), 200, {'Content-Type': 'application/json'}
            else:
                return {'status': 'stock available only '+ str(product['stock'])}
        elif check_cart is not None:
            check_cart_contain = marshal(check_cart, Cart.response_fields)
            # Menjumlahkan qty sebelumnya dengan qty yang diinput buyer
            qty = check_cart_contain['qty'] + int(data['qty'])
            # Mengecek apakah stok barang tersedia sesuai qty yang diinginkan atau tidak
            if qty <= product['stock']:
                # Mendapatkan query dengan id sesuai check_cart
                qry = Cart.query.get(check_cart_contain['id'])
                qry.buyer_id = check_cart_contain['buyer_id']
                qry.buyer_name = check_cart_contain['buyer_name']
                qry.product_id = check_cart_contain['product_id']
                qry.price = check_cart_contain['price']
                qry.qty = qty
                db.session.commit()

                return marshal(qry, Cart.response_fields), 200, {'Content-Type': 'application/json'}
            else:
                return {'status': 'stock available only '+ str(product['stock'])}

    @jwt_required
    @buyer_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', location='json', required=True)
        parser.add_argument('qty', location='json', required=True)
        data = parser.parse_args()

        claims = get_jwt_claims()

        product = marshal(Product.query.filter_by(id=data['product_id']).first(), Product.response_fields)
        buyer = marshal(BuyerDetails.query.filter_by(client_id=claims['client_id']).first(), BuyerDetails.response_fields)

        check_cart = Cart.query.filter_by(product_id=data['product_id'])
        check_cart = check_cart.filter_by(buyer_id=buyer['id']).first()
        
        if check_cart is None:
            # Mengecek apakah stok barang tersedia sesuai qty yang diinginkan atau tidak
            if int(data['qty']) <= product['stock']:
                add_to_cart = Cart(buyer['id'], buyer['name'], data['product_id'], product['product_name'], product['price'], data['qty'])
                db.session.add(add_to_cart)
                db.session.commit()
                app.logger.debug('DEBUG : %s', add_to_cart)
                return marshal(add_to_cart, Cart.response_fields), 200, {'Content-Type': 'application/json'}
            else:
                return {'status': 'stock available only '+ str(product['stock'])}
        elif check_cart is not None:
            # Mengecek apakah stok barang tersedia sesuai qty yang diinginkan atau tidak
            if int(data['qty']) <= product['stock']:
                check_cart_contain = marshal(check_cart, Cart.response_fields)
                # Mendapatkan query dengan id sesuai check_cart
                qry = Cart.query.get(check_cart_contain['id'])
                qry.buyer_id = check_cart_contain['buyer_id']
                qry.buyer_name = check_cart_contain['buyer_name']
                qry.product_id = check_cart_contain['product_id']
                qry.price = check_cart_contain['price']
                # Menyesuaikan dengan inputan user
                qry.qty = data['qty']
                db.session.commit()

                return marshal(qry, Cart.response_fields), 200, {'Content-Type': 'application/json'}
            else:
                return {'status': 'stock available only '+ str(product['stock'])}

    @jwt_required
    @buyer_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', location='json', required=True)
        data = parser.parse_args()

        claims = get_jwt_claims()

        buyer = marshal(BuyerDetails.query.filter_by(client_id=claims['client_id']).first(), BuyerDetails.response_fields)

        check_cart = Cart.query.filter_by(product_id=data['product_id'])
        check_cart = check_cart.filter_by(buyer_id=buyer['id']).first()
        
        if check_cart is None:
            return {'status': 'Product Not Found in Cart'}, 404, {'Content-Type': 'application/json'}
        elif check_cart is not None:
            db.session.delete(check_cart)
            db.session.commit()

            return {'status': 'Prodcut Deleted from Cart'}, 200, {'Content-Type': 'application/json'}

    def patch(self):
        return 'Not yet implemented', 501

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

#         qry = Cart.query

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

