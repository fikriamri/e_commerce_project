from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import ProductCategory
from sqlalchemy import desc
from blueprints import app, db, internal_required
from flask_jwt_extended import jwt_required

bp_product_category = Blueprint('product_category', __name__)
api = Api(bp_product_category)

class ProductCategoryResource(Resource):

    def __init__(self):
        pass
    
    # @jwt_required
    # @internal_required
    # def get(self, id): # get by id
    #     qry = Books.query.get(id)
    #     if qry is not None:
    #         return marshal(qry, Books.response_fields), 200, {'Content-Type': 'application/json'}
    #     return {'status': 'Book Not Found'}, 404, {'Content-Type': 'application/json'}

    # @jwt_required
    # @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('category_name', location='json', required=True)
        parser.add_argument('description', location='json', required=True)
        data = parser.parse_args()

        product_category = Books(data['category_name'], data['description'])
        db.session.add(product_category)
        db.session.commit()

        app.logger.debug('DEBUG : %s', product_category)

        return marshal(product_category, ProductCategory.response_fields), 200, {'Content-Type': 'application/json'}


    # @jwt_required
    # @internal_required
    # def put(self, id):
    #     parser = reqparse.RequestParser()
    #     parser.add_argument('title', location='json')
    #     parser.add_argument('isbn', location='json')
    #     parser.add_argument('writer', location='json')
    #     args = parser.parse_args()

    #     qry = Books.query.get(id)
    #     if qry is None:
    #         return {'status': 'Book Not Found'}, 404, {'Content-Type': 'application/json'}

    #     qry.title = args['title']
    #     qry.isbn = args['isbn']
    #     qry.writer = args['writer']
    #     db.session.commit()

    #     return marshal(qry, Books.response_fields), 200, {'Content-Type': 'application/json'}

    # @jwt_required
    # @internal_required
    # def delete(self, id):
    #     qry = Books.query.get(id)
    #     if qry is None:
    #         return {'status': 'Book Not Found'}, 404, {'Content-Type': 'application/json'}

    #     db.session.delete(qry)
    #     db.session.commit()

    #     return {'status': 'Book Deleted'}, 200, {'Content-Type': 'application/json'}

    # def patch(self):
    #     return 'Not yet implemented', 501

# class BookList(Resource):

#     def __init__(self):
#         pass

#     @jwt_required
#     @internal_required
#     def get(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('p', type=int, location='args', default=1)
#         parser.add_argument('rp', type=int, location='args', default=25)
#         parser.add_argument('title', type=str, location='args')
#         parser.add_argument('isbn', type=str, location='args')
#         args = parser.parse_args()

#         offset = (args['p'] * args['rp']) - args['rp']

#         qry = Books.query

#         if args['title'] is not None:
#             qry = qry.filter_by(title=args['title'])
#         if args['isbn'] is not None:
#             qry = qry.filter_by(isbn=args['isbn'])    

#         rows = []
#         for row in qry.limit(args['rp']).offset(offset).all():
#             rows.append(marshal(row, Books.response_fields))
#         return rows, 200, {'Content-Type': 'application/json'}

# api.add_resource(BookList, '')
api.add_resource(ProductCategoryResource, '', '/<id>')

