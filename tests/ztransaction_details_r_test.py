import json
from . import app, client, cache, create_token_buyer, create_token_seller
import random 

class TestTransactionDetailsR():

######### options
    def test_transactions_details_option1(self, client):
        res = client.options('/transaction_details?transaction_id=2')
        assert res.status_code == 200

    def test_transactions_details_option2(self, client):
        res = client.options('/order_details')
        assert res.status_code == 200

######### get transaction details (buyer)
    def test_transaction_details_list(self, client):
        token = create_token_buyer()
        res=client.get('/transaction_details?transaction_id=2', 
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json=json.loads(res.data)
        assert res.status_code == 200

    def test_transaction_details_invalid_list(self, client):
        token = create_token_seller()
        res = client.get('/transaction_details?transaction_id=100',
                        headers={'Authorization': 'Bearer ' + token})
        
        res_json=json.loads(res.data)
        assert res.status_code == 403

######### get order details (seller)
    def test_order_details_list(self, client):
        token = create_token_seller()
        res=client.get('/order_details', 
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json=json.loads(res.data)
        assert res.status_code == 200

    def test_order_details_invalid_list(self, client):
        token = create_token_buyer()
        res = client.get('/order_details',
                        headers={'Authorization': 'Bearer ' + token})
        
        res_json=json.loads(res.data)
        assert res.status_code == 403

