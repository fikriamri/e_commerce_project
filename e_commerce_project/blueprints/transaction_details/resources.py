from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import TransactionDetails
from sqlalchemy import desc
from blueprints import app, db, internal_required
from flask_jwt_extended import jwt_required

bp_transaction_details = Blueprint('transaction_details', __name__)
api = Api(bp_transaction_details)

class TransactionDetailsResource(Resource):

    def __init__(self):
        pass
    
    

api.add_resource(TransactionDetailsResource, '/transaction_details', '/transaction_details/<id>')

