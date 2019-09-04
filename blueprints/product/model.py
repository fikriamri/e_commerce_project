from blueprints import db
from flask_restful import fields

# PRODUCTS CLASS
class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller_details.id'))
    store_name = db.Column(db.String(50), nullable=False)
    product_name = db.Column(db.String(50), nullable=False)
    product_category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'))
    description = db.Column(db.String(255), nullable=False) 
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    sold = db.Column(db.Integer, nullable=False)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    response_fields = {
        'id': fields.Integer,
        'seller_id': fields.Integer,
        'store_name': fields.String,
        'product_name': fields.String,
        'product_category_id': fields.Integer,
        'description': fields.String,
        'price': fields.Integer,
        'image': fields.String,
        'stock': fields.Integer,
        'sold': fields.Integer
    }

    def __init__(self, seller_id, store_name, product_name, product_category_id, description, price, image, stock, sold):
        self.seller_id = seller_id
        self.store_name = store_name
        self.product_name = product_name
        self.product_category_id = product_category_id
        self.description = description
        self.price = price
        self.image = image
        self.stock = stock
        self.sold = sold

    # def __repr__(self):
    #     return '<Product %r>' % self.id