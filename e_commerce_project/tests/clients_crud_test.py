import json
from . import app, client, cache, create_token_buyer, create_token_seller

class TestClientCrud():

    client_id = 0

######### get list
    def test_client_list(self, client):
        token = create_token_seller()
        res = client.get('/client',
                        headers={'Authorization': 'Bearer ' + token})
        
        res_json=json.loads(res.data)
        assert res.status_code == 200

    def test_client_invalid_list(self, client):
        token = create_token_buyer()
        res = client.get('/client', 
                        headers={'Authorization': 'Bearer ' + token})
        res_json=json.loads(res.data)
        assert res.status_code == 403

######### get
    def test_client_get(self, client):
        token = create_token_seller()
        res = client.get('/client/2',
                        headers={'Authorization': 'Bearer ' + token})
        
        res_json=json.loads(res.data)
        assert res.status_code == 200

    def test_client_invalid_get(self, client):
        token = create_token_seller()
        res = client.get('/client/1000', 
                        headers={'Authorization': 'Bearer ' + token})
        res_json=json.loads(res.data)
        assert res.status_code == 404

######### post

    def test_client_input(self, client):
        token = create_token_seller()
        data = {
            "client_key": "CLIENT103",
            "client_secret": "SECRET103",
            "status": False
        }
        res=client.post('/client', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)

        TestClientCrud.client_id = res_json['client_id']
        assert res.status_code == 200


    def test_client_invalid_input(self, client):
        token = create_token_seller()
        data = {
            "client_key": "seller_2",
            "client_secret": "seller2",
            "status": False
        }
        res=client.post('/client', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)
        assert res.status_code == 500

######### put

    def test_client_update(self, client):
        token = create_token_seller()
        data = {
            "client_key": "seller_1",
            "client_secret": "seller1",
        }
        res=client.put('/client/1', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)
        assert res.status_code == 200
    
    def test_client_invalid_update(self, client):
        token = create_token_seller()
        data = {
            "client_key": "seller_1",
            "client_secret": "seller1",
            "status": True
        }
        res=client.put('/client/1000', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)
        assert res.status_code == 500

######### delete
    def test_client_delete(self, client):
        token = create_token_seller()
        res=client.delete(f'/client/{TestClientCrud.client_id}', 
                        headers={'Authorization': 'Bearer ' + token})

        assert res.status_code == 200

    def test_client_invalid_delete(self, client):
        token = create_token_seller()
        res=client.delete(f'/client/{TestClientCrud.client_id}', 
                        headers={'Authorization': 'Bearer ' + token})

        assert res.status_code == 404

        