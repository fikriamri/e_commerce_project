from blueprints import db
from flask_restful import fields

# PRODUCTCATEGORY CLASS
class ProductCategory(db.Model):
    __tablename__ = "product_category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    response_fields = {
        'id': fields.Integer,
        'category_name': fields.String,
        'description': fields.String,
    }

    def __init__(self, category_name, description):
        self.category_name = category_name
        self.description = description

    # def __repr__(self):
    #     return '<Product_Category %r>' % self.id