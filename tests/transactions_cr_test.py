import json
from . import app, client, cache, create_token_buyer, create_token_seller
import random 

class TestTransactionCr():

######### options
    def test_transactions_option1(self, client):
        res = client.options('/checkout?p=1&orderby=total_qty')
        assert res.status_code == 200

######### get list
    def test_transaction_list1(self, client):
        token = create_token_buyer()
        res = client.get('/checkout?p=1&orderby=total_qty',
                        headers={'Authorization': 'Bearer ' + token})
        
        res_json=json.loads(res.data)
        assert res.status_code == 200

    def test_transaction_list2(self, client):
        token = create_token_buyer()
        res = client.get('/checkout?p=1&orderby=total_qty&sort=desc',
                        headers={'Authorization': 'Bearer ' + token})
        
        res_json=json.loads(res.data)
        assert res.status_code == 200

    def test_transaction_list3(self, client):
        token = create_token_buyer()
        res = client.get('/checkout?p=1&orderby=total_price&sort=desc',
                        headers={'Authorization': 'Bearer ' + token})
        
        res_json=json.loads(res.data)
        assert res.status_code == 200

    def test_transaction_list4(self, client):
        token = create_token_buyer()
        res = client.get('/checkout?p=1&orderby=total_price',
                        headers={'Authorization': 'Bearer ' + token})
        
        res_json=json.loads(res.data)
        assert res.status_code == 200

    def test_transaction_invalid_list(self, client):
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

