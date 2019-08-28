import json
from . import app, client, cache, create_token_buyer, create_token_seller

class TestProductCategoryCrud():

    product_category_id = 0

######### get list
    def test_product_category_list(self, client):
        token = create_token_seller()
        res = client.get('/admin/category/all',
                        headers={'Authorization': 'Bearer ' + token})
        
        res_json=json.loads(res.data)
        assert res.status_code == 200

    def test_product_category_invalid_list(self, client):
        token = create_token_buyer()
        res = client.get('/admin/category/all', 
                        headers={'Authorization': 'Bearer ' + token})
        res_json=json.loads(res.data)
        assert res.status_code == 403

######### get
    def test_product_category_get(self, client):
        token = create_token_seller()
        res = client.get('/admin/category/2',
                        headers={'Authorization': 'Bearer ' + token})
        
        res_json=json.loads(res.data)
        assert res.status_code == 200

    def test_product_category_invalid_get(self, client):
        token = create_token_seller()
        res = client.get('/admin/category/1000', 
                        headers={'Authorization': 'Bearer ' + token})
        res_json=json.loads(res.data)
        assert res.status_code == 404

######### post

    def test_product_category_input(self, client):
        token = create_token_seller()
        data = {
            "category_name": "peralatan makan",
            "description": "semua peralatan makan anak"
        }
        res=client.post('/admin/category', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)

        TestProductCategoryCrud.product_category_id = res_json['id']
        assert res.status_code == 200

    def test_product_category_invalid_input(self, client):
        token = create_token_seller()
        data = {
            "category_name": "peralatan makan",
            "description": "semua peralatan makan anak"
        }
        res=client.post('/admin/category', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)
        assert res.status_code == 500

######### put

    def test_product_category_update(self, client):
        token = create_token_seller()
        data = {
            "category_name": "peralatan jalan-jalan",
            "description": "semua peralatan jalan-jalan anak"
        }
        res=client.put(f'/admin/category/{TestProductCategoryCrud.product_category_id}', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)
        assert res.status_code == 200
    
    def test_product_category_invalid_update(self, client):
        token = create_token_seller()
        data = {
            "category_name": "peralatan jalan-jalan",
            "description": "semua peralatan jalan-jalan anak"
        }
        res=client.put(f'/admin/category/{TestProductCategoryCrud.product_category_id}', 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')

        res_json=json.loads(res.data)
        assert res.status_code == 500

######### delete
    def test_product_category_delete(self, client):
        token = create_token_seller()
        res=client.delete(f'/admin/category/{TestProductCategoryCrud.product_category_id}', 
                        headers={'Authorization': 'Bearer ' + token})

        assert res.status_code == 200

    def test_product_category_invalid_delete(self, client):
        token = create_token_seller()
        res=client.delete(f'/admin/category/{TestProductCategoryCrud.product_category_id}', 
                        headers={'Authorization': 'Bearer ' + token})

        assert res.status_code == 404

        