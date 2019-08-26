from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import ProductCategory
from sqlalchemy import desc
from blueprints import app, db, seller_required
from flask_jwt_extended import jwt_required

bp_product_category = Blueprint('product_category', __name__)
api = Api(bp_product_category)

class ProductCategoryResource(Resource):

    def __init__(self):
        pass

    ## Options function needed to make interaction between react and api successfull
    def options(self):
        return {'Status': 'OK'}, 200
    
    ## Seller function for get product category by id
    @jwt_required
    @seller_required
    def get(self, id):
        product_category = ProductCategory.query.get(id)
        if product_category is not None:
            return marshal(product_category, ProductCategory.response_fields), 200, {'Content-Type': 'application/json'}
        return {'status': 'Category Not Found'}, 404, {'Content-Type': 'application/json'}

    ## Seller function for add product category
    @jwt_required
    @seller_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('category_name', location='json', required=True)
        parser.add_argument('description', location='json', required=True)
        data = parser.parse_args()

        ## Check whether category name already existed in database
        product_category = ProductCategory.query.filter_by(category_name=data['category_name']).first()  
        if product_category is not None:
            return {'status': 'Category_name already existed! Please choose different category_name!'}, 500, {'Content-Type': 'application/json'}
        
        product_category = ProductCategory(data['category_name'], data['description'])
        db.session.add(product_category)
        db.session.commit()

        app.logger.debug('DEBUG : %s', product_category)

        return marshal(product_category, ProductCategory.response_fields), 200, {'Content-Type': 'application/json'}

    ## Seller function for edit product category by id
    @jwt_required
    @seller_required
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('category_name', location='json', required=True)
        parser.add_argument('description', location='json', required=True)
        args = parser.parse_args()

        ## Check whether category existed
        product_category = ProductCategory.query.get(id)
        if product_category is None:
            return {'status': 'Category Not Found'}, 404, {'Content-Type': 'application/json'}

        ## Check whether category name already existed
        check_product_category = ProductCategory.query.filter_by(category_name=args['category_name']).first()
        if check_product_category is not None:
            return {'status': 'Category_name already existed! Please choose different category_name!'}, 500, {'Content-Type': 'application/json'}

        product_category.category_name = args['category_name']
        product_category.description = args['description']
        db.session.commit()

        return marshal(product_category, ProductCategory.response_fields), 200, {'Content-Type': 'application/json'}

    ## Seller function for delete product category by id
    @jwt_required
    @seller_required
    def delete(self, id):
        product_category = ProductCategory.query.get(id)
        if product_category is None:
            return {'status': 'Category Not Found'}, 404, {'Content-Type': 'application/json'}

        db.session.delete(product_category)
        db.session.commit()

        return {'status': 'Category Deleted'}, 200, {'Content-Type': 'application/json'}

    def patch(self):
        return 'Not yet implemented', 501

class ProductCategoryList(Resource):

    def __init__(self):
        pass

    ## Options function needed to make interaction between react and api successfull
    def options(self):
        return {'Status': 'OK'}, 200

    ## Seller function for get all product category listed in database
    @jwt_required
    @seller_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('category_name', type=str, location='args')
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        product_category = ProductCategory.query

        if args['category_name'] is not None:
            product_category = product_category.filter_by(category_name=args['category_name'])  

        rows = []
        for row in product_category.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, ProductCategory.response_fields))
        return rows, 200, {'Content-Type': 'application/json'}

api.add_resource(ProductCategoryList, '/all')
api.add_resource(ProductCategoryResource, '', '/<id>')

