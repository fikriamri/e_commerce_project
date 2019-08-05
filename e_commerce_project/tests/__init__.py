Masih perlu diedit

import pytest, json, logging
from flask import Flask, request, json
from blueprints import app
from app import cache

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

def create_token_public():
    token = cache.get('token-public')
    if token is None:
        ## prepare request input
        data = {
            'client_key': 'CLIENT02',
            'client_secret': 'SECRET02'
        }

        ## do request
        req = call_client(request)
        res = req.get('/login',
                        query_string=data) # seperti nembak API luar (contoh weather.io)

        ## store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        ## assert / compare with expected result
        assert res.status_code == 200

        ## save token into cache
        cache.set('token-public', res_json['token'], timeout=60)

        ## return because it useful for other test
        return res_json['token']
    else:
        return token


def create_token_internal():
    token = cache.get('token-internal')
    if token is None:
        ## prepare request input
        data = {
            'client_key': 'internal',
            'client_secret': 'passwordinternal'
        }

        ## do request
        req = call_client(request)
        res = req.get('/login',
                        query_string=data) # seperti nembak API luar (contoh weather.io)

        ## store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        ## assert / compare with expected result
        assert res.status_code == 200

        ## save token into cache
        cache.set('token-internal', res_json['token'], timeout=60)

        ## return because it useful for other test
        return res_json['token']
    else:
        return token
        
            