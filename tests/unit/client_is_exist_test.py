from tests import reset_database
from blueprints.clients.model import Clients

class TestClient():

    reset_database()

    def test_is_client_key_already_exist(self):

        client_key = "seller_2"

        assert Clients.is_exists(client_key) == True

    def test_is_client_key_doesnt_exist(self):

        client_key = "seller_9"

        assert Clients.is_exists(client_key) == False