from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Product
from blueprints.seller_details.model import SellerDetails
from blueprints.product_category.model import ProductCategory
from sqlalchemy import desc
from blueprints import app, db, seller_required
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_product = Blueprint('product', __name__)
api = Api(bp_product)

class ProductResource(Resource):

    def __init__(self):
        pass

    ## Options function needed to make interaction between react and api successfull
    def options(self):
        return {'Status': 'OK'}, 200
    
    ## Public function for get product by id
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', location='args', required=True)
        data = parser.parse_args()
        product = Product.query.filter_by(id=data['product_id']).first()
        if product is not None:
            return marshal(product, Product.response_fields), 200, {'Content-Type': 'application/json'}
        return {'status': 'Product Not Found'}, 404, {'Content-Type': 'application/json'}

    ## Seller function for add new product 
    @jwt_required
    @seller_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('product_name', location='json', required=True)
        parser.add_argument('product_category_id', location='json', required=True)
        parser.add_argument('description', location='json', required=True)
        parser.add_argument('price', location='json', required=True)
        parser.add_argument('image', location='json', required=True)
        parser.add_argument('stock', location='json', required=True)
        data = parser.parse_args()

        ## get information about signed in user
        claims = get_jwt_claims()

        seller = marshal(SellerDetails.query.filter_by(client_id=claims['client_id']).first(), SellerDetails.response_fields)

        ## check whether product_name is already listed in database for signed in seller
        product = Product.query.filter_by(product_name=data['product_name'])
        product = product.filter_by(seller_id=seller['id']).first()
        if product is not None:
            return {'status': 'Product_name already existed! Please choose different product_name!'}, 500, {'Content-Type': 'application/json'}

        # check if product_category is exist
        product_category = ProductCategory.query.filter_by(id=data['product_category_id']).first()  
        if product_category is None:
            return {'status': 'Product Category Not Found!'}, 404, {'Content-Type': 'application/json'}
        
        product = Product(seller['id'], seller['store_name'], data['product_name'], data['product_category_id'], data['description'], data['price'],data['image'], data['stock'], 0)
        db.session.add(product)
        db.session.commit()

        app.logger.debug('DEBUG : %s', product)

        return marshal(product, Product.response_fields), 200, {'Content-Type': 'application/json'}

    ## Seller function for edit product data 
    @jwt_required
    @seller_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', location='args', required=True)
        parser.add_argument('product_name', location='json')
        parser.add_argument('product_category_id', location='json', required=True)
        parser.add_argument('description', location='json', required=True)
        parser.add_argument('price', location='json', required=True)
        parser.add_argument('image', location='json', required=True)
        parser.add_argument('stock', location='json', required=True)
        args = parser.parse_args()

        ## get information about signed in user
        claims = get_jwt_claims()
        seller = marshal(SellerDetails.query.filter_by(client_id=claims['client_id']).first(), SellerDetails.response_fields)

        ## Check whether product is listed in database
        product = Product.query.filter_by(id=args['product_id']).first()
        if product is None:
            return {'status': 'Product Not Found'}, 404, {'Content-Type': 'application/json'}

        product.seller_id = seller['id']
        product.store_name = seller['store_name']
        product.product_name = args['product_name']
        product.product_category_id = args['product_category_id']
        product.description = args['description']
        product.price = args['price']
        product.image = args['image']
        product.stock = args['stock']
        db.session.commit()
        return marshal(product, Product.response_fields), 200, {'Content-Type': 'application/json'}

    # Seller function for soft delete product
    @jwt_required
    @seller_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', location='args', required=True)
        args = parser.parse_args()

        ## get information about signed in user
        claims = get_jwt_claims()
        seller = marshal(SellerDetails.query.filter_by(client_id=claims['client_id']).first(), SellerDetails.response_fields)

        ## Check whether product is listed in database
        product = Product.query.filter_by(id=args['product_id']).first()
        if product is None:
            return {'status': 'Product Not Found'}, 404, {'Content-Type': 'application/json'}

        product.description = 'deleted'
        db.session.commit()

        return {'status': 'Product Deleted'}, 200, {'Content-Type': 'application/json'}

    def patch(self):
        return 'Not yet implemented', 501

class ProductList(Resource):

    def __init__(self):
        pass

    ## Options function needed to make interaction between react and api successfull
    def options(self):
        return {'Status': 'OK'}, 200

    ## Seller function for get all product for signed in seller
    @jwt_required
    @seller_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('product_category_id', type=str, location='args')
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=('product_category_id', 'stock'))
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        ## get information about signed in user
        claims = get_jwt_claims()
        seller = marshal(SellerDetails.query.filter_by(client_id=claims['client_id']).first(), SellerDetails.response_fields)

        product = Product.query.filter_by(seller_id=seller['id'])

        if args['product_category_id'] is not None:
            product = product.filter_by(product_category_id=args['product_category_id'])  
        
        if args['orderby'] is not None:
            if args['orderby'] == 'product_category_id':
                if args['sort'] == 'desc':
                    product = product.order_by(desc(Product.product_category_id)) # bisa gini
                else:
                    product = product.order_by((Product.product_category_id))
            elif args['orderby'] == 'stock':
                if args['sort'] == 'desc':
                    product = product.order_by((Product.stock).desc()) # bisa juga gini   
                else:
                    product = product.order_by((Product.stock))

        rows = []
        for row in product.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Product.response_fields))
        return rows, 200, {'Content-Type': 'application/json'}

    # Seller function for hard delete product
    @jwt_required
    @seller_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', location='args', required=True)
        args = parser.parse_args()
        product = Product.query.get(args['product_id'])
        if product is None:
            return {'status': 'Product Not Found'}, 404, {'Content-Type': 'application/json'}

        db.session.delete(product)
        db.session.commit()

        return {'status': 'Product Deleted'}, 200, {'Content-Type': 'application/json'}

class AllProductList(Resource):

    def __init__(self):
        pass

    def options(self):
        return {'Status': 'OK'}, 200
    
    ## Public function to get all product listed in database
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('product_category_id', type=str, location='args')
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=('product_category_id', 'stock'))
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        product = Product.query

        if args['product_category_id'] is not None:
            product = product.filter_by(product_category_id=args['product_category_id'])  
        
        if args['orderby'] is not None:
            if args['orderby'] == 'product_category_id':
                if args['sort'] == 'desc':
                    product = product.order_by(desc(Product.product_category_id)) # bisa gini
                else:
                    product = product.order_by((Product.product_category_id))
            elif args['orderby'] == 'stock':
                if args['sort'] == 'desc':
                    product = product.order_by((Product.stock).desc()) # bisa juga gini   
                else:
                    product = product.order_by((Product.stock))

        rows = []
        for row in product.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Product.response_fields))
        return rows, 200, {'Content-Type': 'application/json'}


api.add_resource(ProductList, '/list')
api.add_resource(AllProductList, '/all')
api.add_resource(ProductResource, '', '/<id>')

