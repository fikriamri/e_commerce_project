from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import BuyerDetails
from blueprints.clients.model import Clients
from sqlalchemy import desc
from blueprints import app, db, internal_required, buyer_required
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_buyer_details = Blueprint('buyer_details', __name__)
api = Api(bp_buyer_details)

class BuyerSignUp(Resource):

    def __init__(self):
        pass

    def options(self):
        return {'Status': 'OK'}, 200
    
    def post(self):
        parser = reqparse.RequestParser()
        # Untuk membuat client
        parser.add_argument('client_key', location='json', required=True)
        parser.add_argument('client_secret', location='json', required=True)
        # Untuk membuat buyer details
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('phone_number', location='json', required=True)
        parser.add_argument('address', location='json', required=True)
        parser.add_argument('postal_code', location='json', required=True)
        data = parser.parse_args()

        # Membuat data client, status pasti False
        client = Clients(data['client_key'], data['client_secret'], False)
        db.session.add(client)
        db.session.commit()

        client_id = client.client_id

        buyer_details = BuyerDetails(data['name'], data['email'], data['phone_number'], data['address'], data['postal_code'], client_id)
        db.session.add(buyer_details)
        db.session.commit()

        app.logger.debug('DEBUG : %s', buyer_details)

        client_output = marshal(client, Clients.response_fields)

        buyer_details_output = marshal(buyer_details, BuyerDetails.response_fields)

        return {'username': client_output['client_key'], 'buyer_details': buyer_details_output}, 200, {'Content-Type': 'application/json'}



    def patch(self):
        return 'Not yet implemented', 501

class BuyerProfile(Resource):

    def __init__(self):
        pass

    def options(self):
        return {'Status': 'OK'}, 200

    @jwt_required
    @buyer_required
    def get(self):
        claims = get_jwt_claims()
        buyer_details = BuyerDetails.query.filter_by(client_id=claims['client_id']).first()
        client_key = claims['client_key']
        buyer_details_output = marshal(buyer_details, BuyerDetails.response_fields)
        return {'username': client_key, 'buyer_details': buyer_details_output}, 200, {'Content-Type': 'application/json'}

    @jwt_required
    @buyer_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('phone_number', location='json', required=True)
        parser.add_argument('address', location='json', required=True)
        parser.add_argument('postal_code', location='json', required=True)
        args = parser.parse_args()

        claims = get_jwt_claims()
        qry = BuyerDetails.query.filter_by(client_id=claims['client_id']).first()
        qry.name = args['name']
        qry.email = args['email']
        qry.phone_number = args['phone_number']
        qry.address = args['address']
        qry.postal_code = args['postal_code']
        qry.client_id = claims['client_id']
        db.session.commit()

        buyer_details_output = marshal(qry, BuyerDetails.response_fields)

        return {'username': claims['client_key'], 'buyer_details': buyer_details_output}, 200, {'Content-Type': 'application/json'}

    @jwt_required
    @buyer_required
    def delete(self):
        claims = get_jwt_claims()
        buyer_details = BuyerDetails.query.filter_by(client_id=claims['client_id']).first()
        db.session.delete(buyer_details)
        db.session.commit()
        
        client = Clients.query.filter_by(client_id=claims['client_id']).first()
        db.session.delete(client)
        db.session.commit()



        return {'status': 'Profile has been deleted'}, 200, {'Content-Type': 'application/json'}

api.add_resource(BuyerSignUp, '/signup')
api.add_resource(BuyerProfile, '/profile')

