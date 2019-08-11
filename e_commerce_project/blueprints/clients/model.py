from blueprints import db
from flask_restful import fields

# CLIENT CLASS
class Clients(db.Model):
    __tablename__ = "client"
    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_key = db.Column(db.String(30), unique=True, nullable=False)
    client_secret = db.Column(db.String(30), nullable=False)
    status = db.Column(db.Boolean, nullable=False)

    response_fields = {
        'client_id': fields.Integer,
        'client_key': fields.String,
        'client_secret': fields.String,
        'status': fields.Boolean
    }

    def __init__(self, client_key, client_secret, status):
        self.client_key = client_key
        self.client_secret = client_secret
        self.status = status

    def __repr__(self):
        return '<Client %r>' % self.id