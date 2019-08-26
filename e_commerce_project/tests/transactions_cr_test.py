import json
from . import app, client, cache, create_token_buyer, create_token_seller
import random 

class TestTransactionCr():

######### get list
    def test_transaction_list(self, client):
        token = create_token_buyer()
        res = client.get('/checkout',
                        headers={'Authorization': 'Bearer ' + token})
        
        res_json=json.loads(res.data)
        assert res.status_code == 200

    def test_transaction_list(self, client):
        token = create_token_seller()
        res = client.get('/checkout',
                        headers={'Authorization': 'Bearer ' + token})
        
        res_json=json.loads(res.data)
        assert res.status_code == 403

######### post

    def test_transaction_input(self, client):
        token = create_token_buyer()
        data = {
                "courier": "JNE",
                "payment_method": "bank_transfer"
            }
        res=client.post('/checkout', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)

        assert res.status_code == 200

    def test_transaction_invalid_input(self, client):
        token = create_token_buyer()
        data = {
                "courier": "JNE",
                "payment_method": "bank_transfer"
            }
        res=client.post('/checkout', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)
        assert res.status_code == 404

