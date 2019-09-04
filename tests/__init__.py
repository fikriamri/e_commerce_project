import pytest, json, logging
from flask import Flask, request, json
from blueprints import app
from app import cache
import json
from blueprints import db
from blueprints.clients.model import Clients
from blueprints.buyer_details.model import BuyerDetails
from blueprints.seller_details.model import SellerDetails
from blueprints.product_category.model import ProductCategory
from blueprints.product.model import Product

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

def reset_database():

    db.drop_all()
    db.create_all()

    buyer_client = Clients('buyer_1', 'buyer1', 0)
    seller_client = Clients('seller_2', 'seller2', 1)
    buyer = BuyerDetails('Buyer 1', 'buyer1@gmail.com', '081buyer1', 'alamat 1', '40611', 1)
    seller = SellerDetails('Seller 1', 'Store 1', 'seller1@gmail.com', '081seller1', 'alamat 2', '40612', 2)
    product_category1 = ProductCategory('mainan anak', 'semua mainan anak')
    product_category2 = ProductCategory('perlengkapan anak', 'semua perlengkapan anak')
    product_category3 = ProductCategory('baju anak', 'semua baju anak')
    product1= Product(1, 'Store 1', 'mainan 1', 1, 'description', 1000, 'image', 50, 0)
    product2= Product(1, 'Store 1', 'perlengkapan 1', 1, 'description', 1000, 'image', 50, 0)
    product3= Product(1, 'Store 1', 'baju 1', 1, 'description', 1000, 'image', 50, 0)

    # admin = UserModel("admin-tria", bcrypt.generate_password_hash("triapass"), "0986463", "Balikpapan", "admin")

    # create test non-admin user

    # save users to database
    db.session.add(buyer_client)
    db.session.add(seller_client)
    db.session.commit()

    db.session.add(buyer)
    db.session.add(seller)
    db.session.commit()

    db.session.add(product_category1)
    db.session.add(product_category2)
    db.session.add(product_category3)
    db.session.commit()

    db.session.add(product1)
    db.session.add(product2)
    db.session.add(product3)
    db.session.commit()


def create_token_buyer():
    token = cache.get('token-buyer')
    if token is None:
        ## prepare request input
        data = {
            'client_key': 'buyer_1',
            'client_secret': 'buyer1'
        }

        ## do request
        req = call_client(request)
        res = req.post('/signin',
                        data=json.dumps(data),
                        content_type='application/json') # seperti nembak API luar (contoh weather.io)

        ## store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        ## assert / compare with expected result
        assert res.status_code == 200

        ## save token into cache
        cache.set('token-buyer', res_json['token'], timeout=60)

        ## return because it useful for other test
        return res_json['token']
    else:
        return token


def create_token_seller():
    token = cache.get('token-seller')
    if token is None:
        ## prepare request input
        data = {
            'client_key': 'seller_2',
            'client_secret': 'seller2'
        }

        ## do request
        req = call_client(request)
        res = req.post('/signin',
                        data=json.dumps(data),
                        content_type='application/json') # seperti nembak API luar (contoh weather.io)

        ## store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        ## assert / compare with expected result
        assert res.status_code == 200

        ## save token into cache
        cache.set('token-seller', res_json['token'], timeout=60)

        ## return because it useful for other test
        return res_json['token']
    else:
        return token

def create_token_invalid():
    token = cache.get('token-seller')
    if token is None:
        ## prepare request input
        data = {
            'client_key': 'seller_2',
            'client_secret': 'seller2'
        }

        ## do request
        req = call_client(request)
        res = req.post('/signin',
                        data=json.dumps(data),
                        content_type='application/json') # seperti nembak API luar (contoh weather.io)

        ## store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        ## assert / compare with expected result
        assert res.status_code == 200

        ## save token into cache
        cache.set('token-seller', res_json['token'], timeout=60)

        ## return because it useful for other test
        return res_json['token']
    else:
        return token
        
            