from blueprints.weather.resources import PublicGetCurrentWeather
from mock import patch
from . import app, client, cache, create_token_buyer, create_token_seller
from tests import reset_database
import json

class TestWeather():

    reset_database()

    @patch.object(PublicGetCurrentWeather, 'get')
    def test_get_weather_info_mock(self, mock_get):

        token = create_token_buyer()

        response = {
                        "city": "Bandung",
                        "organization": "AS9657 Melsa-i-net AS",
                        "timezone": "Asia/Jakarta",
                        "current_weather": {
                            "date": "2019-09-04:07",
                            "temp": 27.6
                        }
                    }
        
        mock_get.return_value = response

        assert PublicGetCurrentWeather.get('/weather?ip=202.138.233.162',
                        headers={'Authorization': 'Bearer ' + token}) == response

    def test_get_weather_info(self, client):
        token = create_token_buyer()
        res=client.get('/weather?ip=202.138.233.162', 
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json=json.loads(res.data)
        assert res.status_code == 200
