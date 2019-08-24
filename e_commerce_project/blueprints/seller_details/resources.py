from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import SellerDetails
from blueprints.clients.model import Clients
from sqlalchemy import desc
from blueprints import app, db, internal_required, buyer_required
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_seller_details = Blueprint('seller_details', __name__)
api = Api(bp_seller_details)

class SellerSignUp(Resource):
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
        parser.add_argument('store_name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('phone_number', location='json', required=True)
        parser.add_argument('address', location='json', required=True)
        parser.add_argument('postal_code', location='json', required=True)

        data = parser.parse_args()

        # cek dulu apakah client_name sudah ada yang menggunakan
        check_client = Clients.query.filter_by(client_key=data['client_key']).first()
        if check_client is not None:
            return {'status': 'client_name already taken'}
        

        # Membuat data client, status pasti True
        client = Clients(data['client_key'], data['client_secret'], True)
        db.session.add(client)
        db.session.commit()

        client_id = client.client_id

        seller_details = SellerDetails(data['name'], data['store_name'], data['email'], data['phone_number'], data['address'], data['postal_code'], client_id)
        db.session.add(seller_details)
        db.session.commit()

        app.logger.debug('DEBUG : %s', seller_details)

        client_output = marshal(client, Clients.response_fields)

        seller_details_output = marshal(seller_details, SellerDetails.response_fields)

        return {'username': client_output['client_key'], 'seller_details': seller_details_output}, 200, {'Content-Type': 'application/json'}


    def patch(self):
        return 'Not yet implemented', 501

class SellerProfile(Resource):

    def __init__(self):
        pass

    def options(self):
        return {'Status': 'OK'}, 200

    @jwt_required
    @internal_required
    def get(self):
        claims = get_jwt_claims()
        seller_details = SellerDetails.query.filter_by(client_id=claims['client_id']).first()
        client_key = claims['client_key']
        seller_details_output = marshal(seller_details, SellerDetails.response_fields)
        return {'username': client_key, 'seller_details': seller_details_output}, 200, {'Content-Type': 'application/json'}

    @jwt_required
    @internal_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('store_name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('phone_number', location='json', required=True)
        parser.add_argument('address', location='json', required=True)
        parser.add_argument('postal_code', location='json', required=True)
        args = parser.parse_args()

        claims = get_jwt_claims()
        qry = SellerDetails.query.filter_by(client_id=claims['client_id']).first()
        qry.name = args['name']
        qry.store_name = args['store_name']
        qry.email = args['email']
        qry.phone_number = args['phone_number']
        qry.address = args['address']
        qry.postal_code = args['postal_code']
        qry.client_id = claims['client_id']
        db.session.commit()

        seller_details_output = marshal(qry, SellerDetails.response_fields)

        return {'username': claims['client_key'], 'seller_details': seller_details_output}, 200, {'Content-Type': 'application/json'}

    @jwt_required
    @internal_required
    def delete(self):
        claims = get_jwt_claims()
        seller_details = SellerDetails.query.filter_by(client_id=claims['client_id']).first()
        db.session.delete(seller_details)
        db.session.commit()
        
        client = Clients.query.filter_by(client_id=claims['client_id']).first()
        db.session.delete(client)
        db.session.commit()



        return {'status': 'Profile has been deleted'}, 200, {'Content-Type': 'application/json'}

api.add_resource(SellerSignUp, '/seller/signup')
api.add_resource(SellerProfile, '/seller/profile')

