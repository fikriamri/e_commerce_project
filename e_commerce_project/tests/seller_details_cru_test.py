import json
from . import app, client, cache, create_token_buyer, create_token_seller
import random

class TestSellerDetailsCrud():

######### get profile
    def test_seller_details_profile(self, client):
        token = create_token_seller()
        res = client.get('seller/profile',
                        headers={'Authorization': 'Bearer ' + token})
        
        res_json=json.loads(res.data)
        assert res.status_code == 200

    def test_seller_details_invalid_profile(self, client):
        token = create_token_buyer()
        res = client.get('seller/profile', 
                        headers={'Authorization': 'Bearer ' + token})
        res_json=json.loads(res.data)
        assert res.status_code == 403

######### post

    def test_seller_sign_up(self, client):
        random_number = random.random() * 100
        data = {
            "client_key": "Seller Tes " + str(random_number),
            "client_secret": "passwordseller" + str(random_number),
            "name": "Seller "+ str(random_number),
            "store_name": "Store ",
            "email": "seller"+ str(random_number) +"@yahoo.com",
            "phone_number": "082seller"+ str(random_number),
            "address": "Alamat "+ str(random_number),
            "postal_code": "4061"+ str(random_number)
        }
        res=client.post('seller/signup', 
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)

        assert res.status_code == 200

    def test_seller_invalid_sign_up(self, client):
        data = {
            "client_key": "Seller 1",
            "client_secret": "passwordseller2",
            "name": "Seller 3",
            "store_name": "Store 2",
            "email": "seller2@yahoo.co1",
            "phone_number": "082seller",
            "address": "Alamat 2",
            "postal_code": "40612"
        }
        res=client.post('seller/signup', 
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)

        res_json=json.loads(res.data)
        assert res.status_code == 500

######### put

    def test_seller_update(self, client):
        token = create_token_seller()
        data = {
            "name": "Seller 1 tes",
            "store_name": "Store 1",
            "email": "seller2@yahoo.co1",
            "phone_number": "082seller1",
            "address": "Kera Ngalam",
            "postal_code": "40611"
        }
        res=client.put('seller/profile', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)
        assert res.status_code == 200
    
    def test_seller_invalid_update(self, client):
        token = create_token_buyer()
        data = {
            "name": "Seller 1 tes",
            "store_name": "Store 1",
            "email": "seller2@yahoo.co1",
            "phone_number": "082seller1",
            "address": "Kera Ngalam",
            "postal_code": "40611"
        }
        res=client.put('seller/profile', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)
        assert res.status_code == 403


# test untuk delete belum dibuat karena perlu merombak init test agar tidak menghapus seller1 
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

        