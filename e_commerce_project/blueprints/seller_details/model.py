from blueprints import db
from flask_restful import fields

# CLIENT CLASS
class SellerDetails(db.Model):
    __tablename__ = "seller_details"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    store_name = db.Column(db.String(50), nullable=False)
    # email harus unique 
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    province = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    # sub_district ~ kecamatan
    sub_district = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    
    response_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'store_name': fields.String,
        'email': fields.String,
        'phone_number': fields.String,
        'province': fields.String,
        'city': fields.String,
        'sub_district': fields.String,
        'address': fields.String,
        'postal_code': fields.String,
        'client_id': fields.Integer
    }

    def __init__(self, name, store_name, email, phone_number, province, city, sub_district, address, postal_code, client_id):
        self.name = name
        self.store_name = store_name
        self.email = email
        self.phone_number = phone_number
        self.province = province
        self.city = city
        self.sub_district = sub_district
        self.address = address
        self.postal_code = postal_code
        self.client_id = client_id

    def __repr__(self):
        return '<User %r>' % self.id