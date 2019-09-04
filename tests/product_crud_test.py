import json
from . import app, client, cache, create_token_buyer, create_token_seller
import random 

class TestProductCrud():

    product_id = 0



# ######### post

    def test_product_input(self, client):
        token = create_token_seller()
        data = {
            "product_name": "baju tes 2",
            "product_category_id": 1,
            "description": "ini adalah deskripsi tes untuk barang 2",
            "price": 20000,
            "image": "tes image src 2",
            "stock": 32
        }
        res=client.post('/product', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)

        TestProductCrud.product_id = res_json['id']
        assert res.status_code == 200

    def test_product_invalid_input(self, client):
        token = create_token_seller()
        data = {
            "product_name": "baju tes 2",
            "product_category_id": 1,
            "description": "ini adalah deskripsi tes untuk barang 2",
            "price": 20000,
            "image": "tes image src 2",
            "stock": 32
        }
        res=client.post('/product', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)
        assert res.status_code == 500

######### put

    def test_product_update(self, client):
        random_number = random.random() * 1000
        token = create_token_seller()
        data = {
            "product_name": "baju tes " + str(random_number),
            "product_category_id": 1,
            "description": "ini adalah deskripsi tes untuk barang 2",
            "price": 20000,
            "image": "tes image src 2",
            "stock": 32
        }
        res=client.put(f'/product?product_id={TestProductCrud.product_id}', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)
        assert res.status_code == 200
    
    def test_client_invalid_update(self, client):
        token = create_token_seller()
        data = {
            "product_category_id": 1,
            "description": "ini adalah deskripsi tes untuk barang 2",
            "price": 20000,
            "image": "tes image src 2",
        }
        res=client.put(f'/product?product_id={TestProductCrud.product_id}', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)
        assert res.status_code == 400

######### get list (public)
    def test_product_list(self, client):
        res = client.get('/product/all')
        
        res_json=json.loads(res.data)
        assert res.status_code == 200

    def test_product_list_buyer(self, client):
        token = create_token_buyer()
        res = client.get('/product/all',
                        headers={'Authorization': 'Bearer ' + token})
        
        res_json=json.loads(res.data)
        assert res.status_code == 200

######### get list (seller)
    def test_product_list_seller(self, client):
        token = create_token_seller()
        res = client.get('/product/list',
                        headers={'Authorization': 'Bearer ' + token})
        
        res_json=json.loads(res.data)
        assert res.status_code == 200

    def test_product_invalid_list_seller(self, client):
        token = create_token_buyer()
        res = client.get('/product/all',
                        headers={'Authorization': 'Bearer ' + token})
        
        res_json=json.loads(res.data)
        assert res.status_code == 200

# ######### get by id (public)
    def test_product_get(self, client):
        res = client.get('/product?product_id=1')
        
        res_json=json.loads(res.data)
        assert res.status_code == 200

    def test_product_invalid_get(self, client):
        res = client.get('/product?product_id=1000')
        
        res_json=json.loads(res.data)
        assert res.status_code == 404

#########  soft delete
    def test_product_soft_delete(self, client):
        token = create_token_seller()
        res=client.delete(f'/product?product_id={TestProductCrud.product_id}', 
                        headers={'Authorization': 'Bearer ' + token})

        assert res.status_code == 200

    def test_product_invalid_soft_delete(self, client):
        token = create_token_seller()
        res=client.delete('/product?product_id=1000', 
                        headers={'Authorization': 'Bearer ' + token})

        assert res.status_code == 404

#########  hard delete
    def test_product_hard_delete(self, client):
        token = create_token_seller()
        res=client.delete(f'/product/list?product_id={TestProductCrud.product_id}', 
                        headers={'Authorization': 'Bearer ' + token})

        assert res.status_code == 200

    def test_product_category_invalid_hard_delete(self, client):
        token = create_token_seller()
        res=client.delete('/product/list?product_id=1000', 
                        headers={'Authorization': 'Bearer ' + token})

        assert res.status_code == 404 