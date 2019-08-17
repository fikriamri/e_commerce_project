from flask import Flask, request
import json
## Import yang dibutuhkan untuk database
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from datetime import timedelta
from functools import wraps

app = Flask(__name__)

###################################
# JWT
###################################

app.config['JWT_SECRET_KEY'] = 'zENpazwq97E5BqkFUcAdc9ssMqnRMuufe7aQDHYc'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

# Perlu diedit
# Buat Decorator untuk internal only
def internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims['status']: # If berjalan jika statement True, jadi 'not False' = True
            return {'status': 'FORBIDDEN', 'message': 'Seller Only'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

# Perlu diedit
# Buat Decorator untuk client-public
def buyer_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['status']: # If berjalan jika statement True, jadi 'not False' = True
            return {'status': 'FORBIDDEN', 'message': 'Buyer Only'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


## Setting Database
app.config['APP_DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://fikriamri:threecheers@127.0.0.1:3306/e_commerce_project' # localhost aka 127.0.0.1
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# log error (middlewares)
@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()

    app.logger.warning("REQUEST_LOG\t%s", 
        json.dumps({
            'method': request.method,
            'code': response.status,
            'uri':request.full_path, 
            'request': requestData, 
            'response': json.loads(response.data.decode('utf-8'))
            }))
    
    return response


# import blueprints

# perlu diedit sesuai kebutuhan
from blueprints.clients.resources import bp_client
from blueprints.auth import bp_auth
from blueprints.product_category.resources import bp_product_category
from blueprints.product.resources import bp_product
from blueprints.buyer_details.resources import bp_buyer_details
from blueprints.seller_details.resources import bp_seller_details
from blueprints.cart.resources import bp_cart
from blueprints.transaction.resources import bp_transaction
from blueprints.transaction_details.resources import bp_transaction_details


app.register_blueprint(bp_client, url_prefix='/client')
app.register_blueprint(bp_auth, url_prefix='/login')
app.register_blueprint(bp_product_category, url_prefix='/admin/category')
app.register_blueprint(bp_product, url_prefix='/admin/product')
app.register_blueprint(bp_buyer_details, url_prefix='')
app.register_blueprint(bp_seller_details, url_prefix='')
app.register_blueprint(bp_cart, url_prefix='/cart')
app.register_blueprint(bp_transaction, url_prefix='')
app.register_blueprint(bp_transaction_details, url_prefix='')


db.create_all()

