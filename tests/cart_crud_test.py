import json
from . import app, client, cache, create_token_buyer, create_token_seller

class TestCartCrud():

######### get list
    def test_cart_list(self, client):
        token = create_token_buyer()
        res = client.get('/cart/all',
                        headers={'Authorization': 'Bearer ' + token})
        
        res_json=json.loads(res.data)
        assert res.status_code == 200

    def test_invalid_cart_list(self, client):
        token = create_token_seller()
        res = client.get('/cart/all',
                        headers={'Authorization': 'Bearer ' + token})
        
        res_json=json.loads(res.data)
        assert res.status_code == 403

######### post

    def test_cart_input(self, client):
        token = create_token_buyer()
        data = {
            "product_id": 1,
            "qty": 1
        }
        res=client.post('/cart', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)

        assert res.status_code == 200

    def test_cart_input2(self, client):
        token = create_token_buyer()
        data = {
            "product_id": 2,
            "qty": 1
        }
        res=client.post('/cart', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)

        assert res.status_code == 200

    def test_cart_input3(self, client):
        token = create_token_buyer()
        data = {
            "product_id": 2,
            "qty": 1
        }
        res=client.post('/cart', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)

        assert res.status_code == 200

    def test_cart_invalid_input1(self, client):
        token = create_token_buyer()
        data = {
            "product_id": 1,
            "qty": 100
        }
        res=client.post('/cart', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)

        assert res.status_code == 400

    def test_cart_invalid_input2(self, client):
        token = create_token_buyer()
        data = {
            "product_id": 2,
            "qty": 500
        }
        res=client.post('/cart', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)

        assert res.status_code == 400

# ######### get by id
    def test_cart_get(self, client):
        token = create_token_buyer()
        res = client.get('/cart?product_id=2',
                        headers={'Authorization': 'Bearer ' + token})
        
        res_json=json.loads(res.data)
        assert res.status_code == 200

    def test_cart_invalid_get(self, client):
        token = create_token_buyer()
        res = client.get('/cart?product_id=1000',
                        headers={'Authorization': 'Bearer ' + token})
        
        res_json=json.loads(res.data)
        assert res.status_code == 404


######### put

    def test_cart_update(self, client):
        token = create_token_buyer()
        data = {
            "product_id": 2,
            "qty": 1
        }
        res=client.put('/cart', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)
        assert res.status_code == 200
    
    def test_client_invalid_update(self, client):
        token = create_token_seller()
        data = {
            "product_id": 1,
            "qty": 1
        }
        res=client.put('/cart', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)
        assert res.status_code == 403

#########  delete
    def test_cart_delete(self, client):
        token = create_token_buyer()
        res=client.delete('/cart?product_id=1', 
                        headers={'Authorization': 'Bearer ' + token})

        assert res.status_code == 200

    def test_cart_invalid_delete(self, client):
        token = create_token_buyer()
        res=client.delete('/cart?product_id=1000', 
                        headers={'Authorization': 'Bearer ' + token})

        assert res.status_code == 404 