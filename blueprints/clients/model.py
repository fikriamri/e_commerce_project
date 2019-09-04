from blueprints import db
from flask_restful import fields

# CLIENT CLASS
class Clients(db.Model):
    __tablename__ = "client"
    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_key = db.Column(db.String(30), unique=True, nullable=False)
    client_secret = db.Column(db.String(30), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

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

    @classmethod
    def is_exists(cls, data):

        all_data = cls.query.all()

        existing_username = [item.client_key for item in all_data]

        if data in existing_username:
            return True

        return False