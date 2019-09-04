from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Clients
from sqlalchemy import desc
from blueprints import app, db, seller_required
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_client = Blueprint('client', __name__)
api = Api(bp_client)

class ClientResource(Resource):

    def __init__(self):
        pass

    ## Options function needed to make interaction between react and api successfull
    def options(self, id):
        return {'Status': 'OK'}, 200
    
    ## Function for get information about client by client id
    @jwt_required
    def get(self, id):
        client = Clients.query.get(id)
        if client is not None:
            return marshal(client, Clients.response_fields), 200, {'Content-Type': 'application/json'}
        return {'status': 'Client Not Found'}, 404, {'Content-Type': 'application/json'}

    ## Function for insert new client data to database
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='json')
        parser.add_argument('client_secret', location='json')
        parser.add_argument('status', type=bool, location='json')
        data = parser.parse_args()

        # check_client_key = Clients.query.filter_by(client_key=data['client_key']).first()
        check_client_key = Clients.is_exists(data['client_key'])
        if check_client_key is True:
            return {'status': 'Username already taken!'}, 500, {'Content-Type': 'application/json'}

        client = Clients(data['client_key'], data['client_secret'], data['status'])
        db.session.add(client)
        db.session.commit()

        app.logger.debug('DEBUG : %s', client)

        return marshal(client, Clients.response_fields), 200, {'Content-Type': 'application/json'}

    ## Function for update client data on database
    @jwt_required
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='json')
        parser.add_argument('client_secret', location='json')
        args = parser.parse_args()

        claims = get_jwt_claims()

        client = Clients.query.get(id)

        if client is None:
            return {'status': 'Client not found!'}, 500, {'Content-Type': 'application/json'}

        client.client_key = args['client_key']
        client.client_secret = args['client_secret']
        client.status = claims['status']
        db.session.commit()

        return marshal(client, Clients.response_fields), 200, {'Content-Type': 'application/json'}

    ## Function for delete client data on database
    @jwt_required
    def delete(self, id):
        client = Clients.query.get(id)
        if client is None:
            return {'status': 'Client Not Found'}, 404, {'Content-Type': 'application/json'}

        db.session.delete(client)
        db.session.commit()

        return {'status': 'Client Deleted'}, 200, {'Content-Type': 'application/json'}

    def patch(self):
        return 'Not yet implemented', 501

class ClientList(Resource):

    def __init__(self):
        pass

    ## Function for get all client on database
    @jwt_required
    @seller_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('client_id', type=int, location='args')
        parser.add_argument('status', type=inputs.boolean, location='args', choices=(True, False))
        parser.add_argument('orderby', location='args', choices=('client_id', 'status'))
        parser.add_argument('sort', location='args', choices=('asc', 'desc'))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        client = Clients.query

        if args['status'] is not None:
            client = client.filter_by(status=args['status'])

        if args['orderby'] is not None:
            if args['orderby'] == 'client_id':
                if args['sort'] == 'desc':
                    client = client.order_by(desc(Clients.client_id)) # bisa gini
                else:
                    client = client.order_by((Clients.client_id))
            elif args['orderby'] == 'status':
                if args['sort'] == 'desc':
                    client = client.order_by((Clients.client_id).desc()) # bisa juga gini   
                else:
                    client = client.order_by((Clients.client_id))

        rows = []
        for row in client.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Clients.response_fields))
        return rows, 200, {'Content-Type': 'application/json'}

api.add_resource(ClientList, '')
api.add_resource(ClientResource, '', '/<id>')

