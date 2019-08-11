from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Product
from blueprints.product_category.model import ProductCategory
from sqlalchemy import desc
from blueprints import app, db, internal_required
from flask_jwt_extended import jwt_required

bp_product = Blueprint('product', __name__)
api = Api(bp_product)

class ProductResource(Resource):

    def __init__(self):
        pass
    
    @jwt_required
    @internal_required
    def get(self, id): # get by id
        qry = Product.query.get(id)
        if qry is not None:
            return marshal(qry, Product.response_fields), 200, {'Content-Type': 'application/json'}
        return {'status': 'Product Not Found'}, 404, {'Content-Type': 'application/json'}

    @jwt_required
    @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('product_name', location='json', required=True)
        parser.add_argument('product_category_id', location='json', required=True)
        parser.add_argument('description', location='json', required=True)
        parser.add_argument('price', location='json', required=True)
        parser.add_argument('image', location='json', required=True)
        parser.add_argument('stock', location='json', required=True)
        data = parser.parse_args()

        qry = Product.query.filter_by(product_name=data['product_name']).first()  
        if qry is not None:
            return {'status': 'Product_name already existed! Please choose different product_name!'}, 404, {'Content-Type': 'application/json'}

        # check if product_category is exist
        product_category = ProductCategory.query.filter_by(id=data['product_category_id']).first()  
        if product_category is None:
            return {'status': 'Product Category Not Found!'}, 404, {'Content-Type': 'application/json'}
        
        product = Product(data['product_name'], data['product_category_id'], data['description'], data['price'],data['image'], data['stock'])
        db.session.add(product)
        db.session.commit()

        app.logger.debug('DEBUG : %s', product)

        return marshal(product, Product.response_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    @internal_required
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('product_name', location='json', required=True)
        parser.add_argument('product_category_id', location='json', required=True)
        parser.add_argument('description', location='json', required=True)
        parser.add_argument('price', location='json', required=True)
        parser.add_argument('image', location='json', required=True)
        parser.add_argument('stock', location='json', required=True)
        args = parser.parse_args()

        qry = Product.query.get(id)
        if qry is None:
            return {'status': 'Product Not Found'}, 404, {'Content-Type': 'application/json'}

        check_qry = Product.query.filter_by(product_name=args['product_name']).first()
        if check_qry is not None:
            return {'status': 'product_name already existed! Please choose different product_name!'}, 404, {'Content-Type': 'application/json'}

        qry.product_name = args['product_name']
        qry.product_category_id = args['product_category_id']
        qry.description = args['description']
        qry.price = args['price']
        qry.image = args['image']
        qry.stock = args['stock']
        db.session.commit()

        return marshal(qry, Product.response_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    @internal_required
    def delete(self, id):
        qry = Product.query.get(id)
        if qry is None:
            return {'status': 'Product Not Found'}, 404, {'Content-Type': 'application/json'}

        db.session.delete(qry)
        db.session.commit()

        return {'status': 'Product Deleted'}, 200, {'Content-Type': 'application/json'}

    def patch(self):
        return 'Not yet implemented', 501

class ProductList(Resource):

    def __init__(self):
        pass

    @jwt_required
    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('product_category_id', type=str, location='args')
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=('product_category_id', 'stock'))
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Product.query

        if args['product_category_id'] is not None:
            qry = qry.filter_by(product_category_id=args['product_category_id'])  
        
        if args['orderby'] is not None:
            if args['orderby'] == 'product_category_id':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Product.product_category_id)) # bisa gini
                else:
                    qry = qry.order_by((Product.product_category_id))
            elif args['orderby'] == 'stock':
                if args['sort'] == 'desc':
                    qry = qry.order_by((Product.stock).desc()) # bisa juga gini   
                else:
                    qry = qry.order_by((Product.stock))

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Product.response_fields))
        return rows, 200, {'Content-Type': 'application/json'}

api.add_resource(ProductList, '')
api.add_resource(ProductResource, '', '/<id>')

