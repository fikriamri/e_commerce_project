from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints.clients.resources import Clients, ClientList

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

### Resources
class CreateTokenResources(Resource):

    ## Options function needed to make interaction between react and api successfull
    def options(self):
        return {'Status': 'OK'}, 200

    ## Function for get token for signin purpose
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', type=str, location='json', required=True)
        parser.add_argument('client_secret', type=str, location='json', required= True)
        args = parser.parse_args()

        clients = Clients.query

        clients = clients.filter_by(client_key=args['client_key'])
        clients = clients.filter_by(client_secret=args['client_secret']).first()
        
        ## Check whether client_key that user input is listed in database
        if clients is not None:
            client_data= marshal(clients, Clients.response_fields)
            client_data.pop("client_secret")
            token = create_access_token(identity=args['client_key'], user_claims=client_data)
        else:
            return {'status': 'UNATHORIZED', 'message': 'invalid key or secret'}, 401
        return {'status': 'oke',  'token': token}, 200

    ## Function for get user information based on token
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        return {'claims': claims}, 200

class RefreshTokenResources(Resource):

    ## Options function needed to make interaction between react and api successfull
    def options(self):
        return {'Status': 'OK'}, 200
    
    ## Function for get newer token before previous token expired
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        current_claim = get_jwt_claims()
        token = create_access_token(identity=current_user, user_claims=current_claim)
        return {'token': token}, 200
        

api.add_resource(CreateTokenResources, '')
api.add_resource(RefreshTokenResources, '/refresh')
