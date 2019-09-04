from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Cart
from blueprints.product.model import Product
from blueprints.buyer_details.model import BuyerDetails
from sqlalchemy import desc
from blueprints import app, db, seller_required, buyer_required
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_cart = Blueprint('cart', __name__)
api = Api(bp_cart)

class CartResource(Resource):

    def __init__(self):
        pass

    ## Options function needed to make interaction between react and api successfull
    def options(self):
        return {'Status': 'OK'}, 200

    ## Function to get cart data by product id
    @jwt_required
    @buyer_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', location='args', required=True)
        data = parser.parse_args()

        claims = get_jwt_claims()

        buyer = marshal(BuyerDetails.query.filter_by(client_id=claims['client_id']).first(), BuyerDetails.response_fields)

        check_cart = Cart.query.filter_by(product_id=data['product_id'])
        check_cart = check_cart.filter_by(buyer_id=buyer['id']).first()
        
        if check_cart is None:
            return {'status': 'Product Not Found in Cart'}, 404, {'Content-Type': 'application/json'}
        elif check_cart is not None:
            return marshal(check_cart, Cart.response_fields), 200, {'Content-Type': 'application/json'}

    ## Function for add product to cart
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
        
        ## Check whether product already in cart for signed in buyer
        if check_cart is None:
            ## Check whether product stock available or not
            if int(data['qty']) <= product['stock']:
                add_to_cart = Cart(buyer['id'], buyer['name'], data['product_id'], product['product_name'], product['price'], data['qty'])
                db.session.add(add_to_cart)
                db.session.commit()
                app.logger.debug('DEBUG : %s', add_to_cart)
                return marshal(add_to_cart, Cart.response_fields), 200, {'Content-Type': 'application/json'}
            else:
                return {'status': 'stock available only '+ str(product['stock'])}, 400, {'Content-Type': 'application/json'}
        elif check_cart is not None:
            check_cart_contain = marshal(check_cart, Cart.response_fields)
            # Sum previous qty with new qty inputted
            qty = check_cart_contain['qty'] + int(data['qty'])
            ## Check whether product stock available or not
            if qty <= product['stock']:
                cart = Cart.query.get(check_cart_contain['id'])
                cart.buyer_id = check_cart_contain['buyer_id']
                cart.buyer_name = check_cart_contain['buyer_name']
                cart.product_id = check_cart_contain['product_id']
                cart.price = check_cart_contain['price']
                cart.qty = qty
                db.session.commit()
                return marshal(cart, Cart.response_fields), 200, {'Content-Type': 'application/json'}
            else:
                return {'status': 'stock available only '+ str(product['stock'])}, 400, {'Content-Type': 'application/json'}

    ## Function for updating qty product in cart
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
            ## Check whether product stock available or not
            if int(data['qty']) <= product['stock']:
                add_to_cart = Cart(buyer['id'], buyer['name'], data['product_id'], product['product_name'], product['price'], data['qty'])
                db.session.add(add_to_cart)
                db.session.commit()
                app.logger.debug('DEBUG : %s', add_to_cart)
                return marshal(add_to_cart, Cart.response_fields), 200, {'Content-Type': 'application/json'}
            else:
                return {'status': 'stock available only '+ str(product['stock'])}, 400, {'Content-Type': 'application/json'}
        elif check_cart is not None:
            # Mengecek apakah stok barang tersedia sesuai qty yang diinginkan atau tidak
            if int(data['qty']) <= product['stock']:
                check_cart_contain = marshal(check_cart, Cart.response_fields)
                cart = Cart.query.get(check_cart_contain['id'])
                cart.buyer_id = check_cart_contain['buyer_id']
                cart.buyer_name = check_cart_contain['buyer_name']
                cart.product_id = check_cart_contain['product_id']
                cart.price = check_cart_contain['price']
                cart.qty = data['qty']
                db.session.commit()

                return marshal(cart, Cart.response_fields), 200, {'Content-Type': 'application/json'}
            else:
                return {'status': 'stock available only '+ str(product['stock'])}, 400, {'Content-Type': 'application/json'}

    ## Function for delete product in cart
    @jwt_required
    @buyer_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', location='args', required=True)
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

            return {'status': 'Product Deleted from Cart'}, 200, {'Content-Type': 'application/json'}

    def patch(self):
        return 'Not yet implemented', 501

class CartList(Resource):

    def __init__(self):
        pass

    ## Options function needed to make interaction between react and api successfull
    def options(self):
        return {'Status': 'OK'}, 200

    ## Function for get all product in cart
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

        claims = get_jwt_claims()

        buyer = marshal(BuyerDetails.query.filter_by(client_id=claims['client_id']).first(), BuyerDetails.response_fields)

        cart = Cart.query.filter_by(buyer_id=buyer['id'])

        if args['product_id'] is not None:
            cart = cart.filter_by(product_id=args['product_id'])

        if args['orderby'] is not None:
            if args['orderby'] == 'price':
                if args['sort'] == 'desc':
                    cart = cart.order_by(desc(Cart.price)) # bisa gini
                else:
                    cart = cart.order_by((Cart.price))
            elif args['orderby'] == 'qty':
                if args['sort'] == 'desc':
                    cart = cart.order_by((Cart.qty).desc()) # bisa juga gini   
                else:
                    cart = cart.order_by((Cart.qty))

        rows = []
        for row in cart.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Cart.response_fields))
        return rows, 200, {'Content-Type': 'application/json'}

api.add_resource(CartList, '/all')
api.add_resource(CartResource, '')

