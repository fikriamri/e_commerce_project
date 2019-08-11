from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import BuyerDetails
from blueprints.clients.model import Clients
from sqlalchemy import desc
from blueprints import app, db, internal_required, buyer_required
from flask_jwt_extended import jwt_required

bp_buyer_details = Blueprint('buyer_details', __name__)
api = Api(bp_buyer_details)

class BuyerSignUp(Resource):

    def __init__(self):
        pass
    
    # @jwt_required
    # @buyer_required
    # def get(self, id): # get by id
    #     qry = Users.query.get(id)
    #     if qry is not None:
    #         return marshal(qry, Users.response_fields), 200, {'Content-Type': 'application/json'}
    #     return {'status': 'Client Not Found'}, 404, {'Content-Type': 'application/json'}

    def post(self):
        parser = reqparse.RequestParser()
        # Untuk membuat client
        parser.add_argument('client_key', location='json', required=True)
        parser.add_argument('client_secret', location='json', required=True)
        # Untuk membuat buyer details
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('dob', location='json', required=True)
        parser.add_argument('sex', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('province', location='json', required=True)
        parser.add_argument('city', location='json', required=True)
        parser.add_argument('sub_district', location='json', required=True)
        parser.add_argument('address', location='json', required=True)
        parser.add_argument('postal_code', location='json', required=True)
        data = parser.parse_args()

        # Membuat data client, status pasti False
        client = Clients(data['client_key'], data['client_secret'], False)
        db.session.add(client)
        db.session.commit()

        client_id = client.client_id

        buyer_details = BuyerDetails(data['name'], data['dob'], data['sex'], data['email'], data['province'], data['city'], data['sub_district'], data['address'], data['postal_code'], client_id)
        db.session.add(buyer_details)
        db.session.commit()

        app.logger.debug('DEBUG : %s', buyer_details)

        client_output = marshal(client, Clients.response_fields)

        buyer_details_output = marshal(buyer_details, BuyerDetails.response_fields)

        return {'username': client_output['client_key'], 'buyer_details': buyer_details_output}, 200, {'Content-Type': 'application/json'}

#     @jwt_required
#     @internal_required
#     def put(self, id):
#         parser = reqparse.RequestParser()
#         parser.add_argument('name', location='json', required=True)
#         parser.add_argument('age', location='json')
#         parser.add_argument('sex', location='json', required=True)
#         parser.add_argument('client_id', location='json', required=True)
#         args = parser.parse_args()

#         qry = Users.query.get(id)
#         if qry is None:
#             return {'status': 'User Not Found'}, 404, {'Content-Type': 'application/json'}

#         qry.name = args['name']
#         qry.age = args['age']
#         qry.sex = args['sex']
#         qry.client_id = args['client_id']
#         db.session.commit()

#         return marshal(qry, Users.response_fields), 200, {'Content-Type': 'application/json'}

#     @jwt_required
#     @internal_required
#     def delete(self, id):
#         qry = Users.query.get(id)
#         if qry is None:
#             return {'status': 'Client Not Found'}, 404, {'Content-Type': 'application/json'}

#         db.session.delete(qry)
#         db.session.commit()

#         return {'status': 'Client Deleted'}, 200, {'Content-Type': 'application/json'}

#     def patch(self):
#         return 'Not yet implemented', 501

# class UserList(Resource):

#     def __init__(self):
#         pass

#     @jwt_required
#     @internal_required
#     def get(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('p', type=int, location='args', default=1)
#         parser.add_argument('rp', type=int, location='args', default=25)
#         parser.add_argument('sex', location='args', choices=('male', 'female'))
#         parser.add_argument('orderby', location='args', choices=('client_id', 'sex'))
#         parser.add_argument('sort', location='args', choices=('asc', 'desc'))
#         args = parser.parse_args()

#         offset = (args['p'] * args['rp']) - args['rp']

#         qry = Users.query

#         if args['sex'] is not None:
#             qry = qry.filter_by(sex=args['sex'])

#         if args['orderby'] is not None:
#             if args['orderby'] == 'client_id':
#                 if args['sort'] == 'desc':
#                     qry = qry.order_by(desc(Users.id)) # bisa gini
#                 else:
#                     qry = qry.order_by((Users.id))
#             elif args['orderby'] == 'sex':
#                 if args['sort'] == 'desc':
#                     qry = qry.order_by((Users.id).desc()) # bisa juga gini   
#                 else:
#                     qry = qry.order_by((Users.id))

#         rows = []
#         for row in qry.limit(args['rp']).offset(offset).all():
#             rows.append(marshal(row, Users.response_fields))
#         return rows, 200, {'Content-Type': 'application/json'}

# api.add_resource(UserList, '')
api.add_resource(BuyerSignUp, '/signup')

