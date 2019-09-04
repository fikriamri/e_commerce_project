import json
from . import app, client, cache, create_token_buyer, create_token_seller, create_token_invalid
import random
from tests import reset_database

class TestBuyerDetailsCrud():

    reset_database()

######### options
    def test_buyer_option1(self, client):
        res = client.options('profile')
        assert res.status_code == 200

    def test_buyer_option2(self, client):
        res = client.options('signup')
        assert res.status_code == 200

######### get profile
    def test_buyer_details_profile(self, client):
        token = create_token_buyer()
        res = client.get('profile',
                        headers={'Authorization': 'Bearer ' + token})
        
        res_json=json.loads(res.data)
        assert res.status_code == 200

    def test_buyer_details_invalid_profile(self, client):
        token = create_token_invalid()
        res = client.get('profile', 
                        headers={'Authorization': 'Bearer ' + token})
        res_json=json.loads(res.data)
        assert res.status_code == 403

######### post

    def test_buyer_sign_up(self, client):
        random_number = int(random.random() * 1000)
        data = {
            "client_key": "Buyer Tes " + str(random_number),
            "client_secret": "passwordbuyer" + str(random_number),
            "name": "Buyer "+ str(random_number),
            "email": "buyer"+ str(random_number) +"@yahoo.com",
            "phone_number": "082buyer"+ str(random_number),
            "address": "Alamat "+ str(random_number),
            "postal_code": "4061"+ str(random_number)
        }
        res=client.post('signup', 
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)

        assert res.status_code == 200

    def test_buyer_invalid_sign_up(self, client):
        data = {
            "client_key": "buyer_1",
            "client_secret": "buyer1",
            "name": "Buyer 1",
            "email": "buyer1@yahoo.com",
            "phone_number": "082buyer1",
            "address": "Alamat 1",
            "postal_code": "40611"
        }
        res=client.post('signup', 
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)

        res_json=json.loads(res.data)
        assert res.status_code == 500

######### put

    def test_buyer_update(self, client):
        token = create_token_buyer()
        data = {
            "client_key": "buyer_2",
            "client_secret": "buyer1",
            "name": "Buyer 1",
            "email": "buyer1@yahoo.com",
            "phone_number": "082buyer1",
            "address": "Alamat 1",
            "postal_code": "40611"
        }
        res=client.put('profile', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)
        assert res.status_code == 200
    
    def test_buyer_invalid_update(self, client):
        token = create_token_seller()
        data = {
            "client_key": "buyer_1",
            "client_secret": "buyer1",
            "name": "Buyer 1",
            "email": "buyer1@yahoo.com",
            "phone_number": "082buyer1",
            "address": "Alamat 1",
            "postal_code": "40611"
        }
        res=client.put('profile', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)
        assert res.status_code == 403


# test untuk delete belum dibuat karena perlu merombak init test agar tidak menghapus buyer1 
######### delete
#     def test_product_category_delete(self, client):
#         token = create_token_seller()
#         res=client.delete(f'/admin/category/{TestProductCategoryCrud.product_category_id}', 
#                         headers={'Authorization': 'Bearer ' + token})

#         assert res.status_code == 200

#     def test_product_category_invalid_delete(self, client):
#         token = create_token_seller()
#         res=client.delete(f'/admin/category/{TestProductCategoryCrud.product_category_id}', 
#                         headers={'Authorization': 'Bearer ' + token})

#         assert res.status_code == 404

        